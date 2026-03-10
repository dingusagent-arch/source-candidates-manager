"""Example CSV parser for opportunity rows.

This parser maps CSV columns into v2 storage records.
No schema validation is done here yet (see TODO.md).
"""

from __future__ import annotations

import csv
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterator


REQUIRED_COLUMNS = {"id", "title", "deadline"}


# Header map: common variants -> canonical name
HEADER_ALIASES = {
    "id": "id",
    "identifier": "id",
    "opportunity_id": "id",
    "title": "title",
    "name": "title",
    "url": "url",
    "link": "url",
    "source": "source",
    "origin": "source",
    "organization": "source",
    "org": "source",
    "deadline": "deadline",
    "due": "deadline",
    "due_date": "deadline",
    "discipline": "discipline",
    "category": "discipline",
    "type": "discipline",
    "fee": "fee_usd",
    "fee_usd": "fee_usd",
    "entry_fee": "fee_usd",
    "city": "city",
    "location": "city",
}


def _normalized_key(name: str) -> str:
    return re.sub(r"[\s\-]+", "_", name.strip().lower())


def _normalize_fieldnames(fieldnames: list[str]) -> dict[str, list[str]]:
    """Return mapping from canonical field -> matching CSV column names (in order)."""
    mapping: dict[str, list[str]] = {}
    for col in (fieldnames or []):
        key = _normalized_key(col)
        if key in HEADER_ALIASES:
            canonical = HEADER_ALIASES[key]
            mapping.setdefault(canonical, [])
            if col not in mapping[canonical]:
                mapping[canonical].append(col)
    return mapping


def _first_value(row: dict[str, str], candidates: list[str], default: str = "") -> str:
    for column in candidates:
        value = row.get(column)
        if value is not None and str(value).strip() != "":
            return str(value).strip()
    return default


def parse_rows(csv_path: Path) -> Iterator[Dict[str, object]]:
    with csv_path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []
        normalized = _normalize_fieldnames(fieldnames)
        missing = REQUIRED_COLUMNS - set(normalized.keys())
        if missing:
            raise ValueError(f"Missing required CSV columns: {sorted(missing)}")

        now = datetime.now(timezone.utc).isoformat()
        for row in reader:
            fee_text = _first_value(row, normalized.get("fee_usd", []), default="0")
            try:
                fee = float(fee_text) if fee_text else 0.0
            except Exception:
                fee = 0.0

            yield {
                "id": _first_value(row, normalized["id"]),
                "title": _first_value(row, normalized["title"]),
                "source": _first_value(row, normalized.get("source", []), default=""),
                "deadline": _first_value(row, normalized["deadline"]),
                "city": _first_value(row, normalized.get("city", []), default=""),
                "discipline": _first_value(row, normalized.get("discipline", []), default=""),
                "fee_usd": fee,
                "status": "new",
                "url": _first_value(row, normalized.get("url", []), default=""),
                "created_at": now,
                "updated_at": now,
            }


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("Usage: python3 src/importers/csv_parser.py <path/to/file.csv>")
        return 2

    csv_path = Path(argv[1])
    for record in parse_rows(csv_path):
        print(json.dumps(record, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
