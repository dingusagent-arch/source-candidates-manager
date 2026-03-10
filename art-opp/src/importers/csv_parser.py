"""Example CSV parser for opportunity rows.

This parser maps CSV columns into v2 storage records.
No schema validation is done here yet (see TODO.md).
"""

from __future__ import annotations

import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterator


REQUIRED_COLUMNS = {
    "id",
    "title",
    "source",
    "deadline",
    "city",
    "discipline",
    "fee_usd",
    "url",
}


# Header map: common variants -> canonical name
HEADER_ALIASES = {
    "id": "id",
    "identifier": "id",
    "title": "title",
    "name": "title",
    "url": "url",
    "link": "url",
    "source": "source",
    "origin": "source",
    "deadline": "deadline",
    "due": "deadline",
    "discipline": "discipline",
    "category": "discipline",
    "fee": "fee_usd",
    "fee_usd": "fee_usd",
    "city": "city",
    "location": "city",
}


def _normalize_fieldnames(fieldnames: list[str]) -> dict:
    """Return a mapping from canonical field -> actual CSV column name."""
    mapping: dict[str, str] = {}
    for col in (fieldnames or []):
        key = col.strip().lower()
        if key in HEADER_ALIASES:
            canonical = HEADER_ALIASES[key]
            mapping[canonical] = col
    return mapping


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
            try:
                fee_val = row.get(normalized.get("fee_usd", "fee_usd"), "0")
                fee = float(fee_val) if fee_val not in (None, "") else 0.0
            except Exception:
                fee = 0.0

            yield {
                "id": row[normalized["id"]].strip(),
                "title": row[normalized["title"]].strip(),
                "source": row[normalized["source"]].strip(),
                "deadline": row[normalized["deadline"]].strip(),
                "city": row[normalized["city"]].strip(),
                "discipline": row[normalized["discipline"]].strip(),
                "fee_usd": fee,
                "status": "new",
                "url": row[normalized["url"]].strip(),
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
