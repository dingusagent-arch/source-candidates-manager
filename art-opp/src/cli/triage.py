"""CLI stub for triage actions: approve/reject/skip.

This is a non-persistent stub that prints intended action payloads.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone


def _base_payload(action: str, opportunity_id: str, note: str | None = None) -> dict:
    payload = {
        "action": action,
        "opportunity_id": opportunity_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    if note:
        payload["note"] = note
    return payload


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Triage opportunities")
    sub = parser.add_subparsers(dest="command", required=True)

    approve = sub.add_parser("approve", help="approve an opportunity")
    approve.add_argument("opportunity_id")
    approve.add_argument("--note", default=None)

    reject = sub.add_parser("reject", help="reject an opportunity")
    reject.add_argument("opportunity_id")
    reject.add_argument("--reason", default=None)

    skip = sub.add_parser("skip", help="skip an opportunity")
    skip.add_argument("opportunity_id")
    skip.add_argument("--note", default=None)

    return parser


def main(argv: list[str]) -> int:
    parser = build_parser()
    args = parser.parse_args(argv[1:])

    if args.command == "approve":
        payload = _base_payload("approved", args.opportunity_id, args.note)
    elif args.command == "reject":
        payload = _base_payload("rejected", args.opportunity_id, args.reason)
    else:
        payload = _base_payload("skipped", args.opportunity_id, args.note)

    print(json.dumps(payload, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
