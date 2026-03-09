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


def parse_rows(csv_path: Path) -> Iterator[Dict[str, object]]:
    with csv_path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        missing = REQUIRED_COLUMNS - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Missing required CSV columns: {sorted(missing)}")

        now = datetime.now(timezone.utc).isoformat()
        for row in reader:
            yield {
                "id": row["id"].strip(),
                "title": row["title"].strip(),
                "source": row["source"].strip(),
                "deadline": row["deadline"].strip(),
                "city": row["city"].strip(),
                "discipline": row["discipline"].strip(),
                "fee_usd": float(row["fee_usd"]),
                "status": "new",
                "url": row["url"].strip(),
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
