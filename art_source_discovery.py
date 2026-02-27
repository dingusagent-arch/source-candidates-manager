#!/usr/bin/env python3
import argparse
import datetime as dt
import json
import os
from urllib.parse import urlparse

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE, "data")
CANDIDATES_PATH = os.path.join(DATA_DIR, "art_sources_candidates.json")


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def ensure_store() -> dict:
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(CANDIDATES_PATH):
        payload = {
            "notes": "Brave-discovered source queue. status: proposed|approved|rejected|paused",
            "candidates": [],
        }
        with open(CANDIDATES_PATH, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
        return payload

    with open(CANDIDATES_PATH, "r", encoding="utf-8") as f:
        try:
            payload = json.load(f)
        except Exception:
            payload = {"notes": "auto-recovered", "candidates": []}

    if not isinstance(payload, dict):
        payload = {"notes": "auto-recovered", "candidates": []}
    payload.setdefault("notes", "Brave-discovered source queue. status: proposed|approved|rejected|paused")
    payload.setdefault("candidates", [])
    return payload


def save_store(payload: dict) -> None:
    with open(CANDIDATES_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)


def normalize_url(url: str) -> str:
    u = (url or "").strip()
    if not u.startswith(("http://", "https://")):
        raise ValueError("url must start with http:// or https://")
    return u


def infer_name_from_url(url: str) -> str:
    host = urlparse(url).netloc.replace("www.", "")
    return host or "Unnamed Source"


def cmd_add(args):
    payload = ensure_store()
    url = normalize_url(args.url)
    candidates = payload["candidates"]
    for c in candidates:
        if c.get("url") == url:
            print(f"EXISTS: {url} (status={c.get('status','')})")
            return

    item = {
        "name": (args.name or infer_name_from_url(url)).strip(),
        "url": url,
        "type": (args.type or "unknown").strip(),
        "coverage": (args.coverage or "unknown").strip(),
        "status": "proposed",
        "source": (args.source or "manual").strip(),
        "notes": (args.notes or "").strip(),
        "created_at": now_iso(),
        "updated_at": now_iso(),
    }
    candidates.append(item)
    save_store(payload)
    print(f"ADDED: {url}")


def cmd_set_status(args):
    payload = ensure_store()
    url = normalize_url(args.url)
    status = args.status.strip().lower()
    allowed = {"proposed", "approved", "rejected", "paused"}
    if status not in allowed:
        raise ValueError(f"status must be one of: {', '.join(sorted(allowed))}")

    for c in payload["candidates"]:
        if c.get("url") == url:
            c["status"] = status
            c["updated_at"] = now_iso()
            if args.notes is not None:
                c["notes"] = args.notes
            save_store(payload)
            print(f"UPDATED: {url} -> {status}")
            return

    raise ValueError("url not found in candidates")


def cmd_list(args):
    payload = ensure_store()
    items = payload["candidates"]
    if args.status:
        items = [i for i in items if i.get("status") == args.status]

    print(json.dumps({"count": len(items), "items": items}, indent=2))


def main():
    ap = argparse.ArgumentParser(description="Manage discovered art source candidates")
    sub = ap.add_subparsers(dest="cmd", required=True)

    add = sub.add_parser("add", help="Add discovered source candidate")
    add.add_argument("--url", required=True)
    add.add_argument("--name")
    add.add_argument("--type", default="unknown")
    add.add_argument("--coverage", default="unknown")
    add.add_argument("--source", default="manual")
    add.add_argument("--notes", default="")
    add.set_defaults(func=cmd_add)

    st = sub.add_parser("set-status", help="Set candidate status")
    st.add_argument("--url", required=True)
    st.add_argument("--status", required=True, help="proposed|approved|rejected|paused")
    st.add_argument("--notes")
    st.set_defaults(func=cmd_set_status)

    ls = sub.add_parser("list", help="List candidates")
    ls.add_argument("--status", choices=["proposed", "approved", "rejected", "paused"])
    ls.set_defaults(func=cmd_list)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
