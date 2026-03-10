from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any

from src.importers.csv_parser import parse_rows
from src.scoring.engine import ScoringConfig, score_opportunity

DEFAULT_CONFIG = ScoringConfig(
    preferred_disciplines=("Painting", "Mixed Media", "Sculpture"),
    preferred_cities=("Boston", "Providence", "New York"),
    trusted_sources=("TrustedFoundation", "ArtDeadline", "LocalArtsOrg"),
)


class OpportunityStore:
    def __init__(self, data_file: str | Path, scoring_config: ScoringConfig | None = None):
        self.path = Path(data_file)
        self.scoring_config = scoring_config or DEFAULT_CONFIG

    def _now(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def _ensure_parent(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def _read(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        return json.loads(self.path.read_text(encoding="utf-8"))

    def _write(self, items: list[dict[str, Any]]) -> None:
        self._ensure_parent()
        with NamedTemporaryFile("w", delete=False, dir=str(self.path.parent), encoding="utf-8") as tf:
            json.dump(items, tf, ensure_ascii=False, indent=2)
            tmp_name = tf.name
        Path(tmp_name).replace(self.path)

    def list_items(
        self,
        *,
        status: str | None = None,
        min_score: float | None = None,
        search: str | None = None,
    ) -> list[dict[str, Any]]:
        items = self._read()
        if status:
            items = [i for i in items if i.get("status") == status]
        if min_score is not None:
            items = [i for i in items if float(i.get("score_total") or 0) >= min_score]
        if search:
            q = search.lower()
            items = [
                i
                for i in items
                if q in str(i.get("title", "")).lower()
                or q in str(i.get("city", "")).lower()
                or q in str(i.get("discipline", "")).lower()
            ]
        return sorted(items, key=lambda i: float(i.get("score_total") or 0), reverse=True)

    def get_item(self, item_id: str) -> dict[str, Any] | None:
        for item in self._read():
            if item.get("id") == item_id:
                return item
        return None

    def import_csv(self, csv_path: str | Path) -> dict[str, Any]:
        existing = self._read()
        by_id = {i["id"]: i for i in existing if "id" in i}
        imported = 0
        updated = 0

        for row in parse_rows(Path(csv_path)):
            score = score_opportunity(row, self.scoring_config)
            row.update(score)
            if row["id"] in by_id:
                prev = by_id[row["id"]]
                row["status"] = prev.get("status", row.get("status", "new"))
                row["notes"] = prev.get("notes", row.get("notes", ""))
                updated += 1
            else:
                imported += 1
            by_id[row["id"]] = row

        merged = list(by_id.values())
        self._write(merged)
        return {"imported": imported, "updated": updated, "total": len(merged)}

    def triage(self, item_id: str, action: str, note: str = "") -> dict[str, Any] | None:
        if action not in {"approve", "reject", "skip"}:
            raise ValueError("action must be approve|reject|skip")

        status_map = {"approve": "approved", "reject": "rejected", "skip": "skipped"}

        items = self._read()
        for item in items:
            if item.get("id") == item_id:
                item["status"] = status_map[action]
                if note:
                    item["notes"] = note
                item["updated_at"] = self._now()
                self._write(items)
                return item
        return None
