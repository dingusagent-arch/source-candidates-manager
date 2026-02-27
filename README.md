# source-candidates-manager

Standalone local web app + CLI for managing Brave-discovered art-source candidates.

## Why
Keeps candidate/source workflow outside `art-catalog-2025` while still feeding approved sources into OpenClaw scouting jobs.

## Components
- `source_candidates_server.py` — local web UI (default: http://127.0.0.1:8011)
- `art_source_discovery.py` — CLI helper for add/list/status operations

## Data store
Both tools use:

`~/.openclaw/workspace/data/art_sources_candidates.json`

Approved entries from this file are consumed by `art_events_scout.py`.

## Run web UI
```bash
python3 source_candidates_server.py
```

## CLI examples
```bash
python3 art_source_discovery.py list --status proposed
python3 art_source_discovery.py add --url "https://example.org/events" --name "Example Arts" --type gallery --coverage Cincinnati --source brave
python3 art_source_discovery.py set-status --url "https://example.org/events" --status approved
```

## Theme
Web UI defaults to dark mode with a light/dark toggle.
