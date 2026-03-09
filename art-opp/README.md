# ART-OPP-2026Q2 (ticket-ready starter)

Minimal, non-sensitive repository skeleton for ART-OPP-2026Q2.

## Included

- **Flask web UI scaffold**
  - `run_server.py`
  - `app/__init__.py`, `app/routes.py`, `app/backend.py`
  - `app/templates/index.html`, `app/static/main.js`
  - API endpoints for listing/detail/triage/import

- **Storage schema v2**
  - `src/storage/schema_v2.md` (human-readable contract)
  - `src/storage/schema_v2.json` (JSON Schema draft 2020-12)
- **Scoring engine (rule-based)**
  - `src/scoring/engine.py`
  - `src/scoring/pseudocode.md`
  - `tests/test_scoring_engine.py`
- **CSV import example parser**
  - `src/importers/csv_parser.py`
  - `src/importers/examples/opportunities.csv`
- **CLI triage stub**
  - `src/cli/triage.py` (`approve`, `reject`, `skip`)
- **Project TODOs**
  - `TODO.md`

## Notes

- Code is intentionally small and documented to support quick iteration.
- No external packages required.
- Builds/dependency installs were intentionally not run per task constraints.

## Quick usage (optional)

```bash
python3 src/cli/triage.py approve opp_001 --note "Looks like a fit"
python3 src/cli/triage.py reject opp_002 --reason "Deadline passed"
python3 src/cli/triage.py skip opp_003

python3 src/importers/csv_parser.py src/importers/examples/opportunities.csv
```

## Web UI

Install minimal deps:

```bash
python3 -m pip install Flask pytest
```

Run app:

```bash
python3 run_server.py
# or
FLASK_APP=run_server.py python3 -m flask run
```

Open `http://localhost:5000`.

### API endpoints

- `GET /api/opportunities?status=&min_score=&search=`
- `GET /api/opportunities/<id>`
- `POST /api/opportunities/<id>/triage` with JSON `{ "action": "approve|reject|skip", "note": "..." }`
- `POST /api/import-csv` with multipart file field `file`

### Tests

```bash
python3 -m pytest -q
```

## Layout

```
src/
  cli/
    triage.py
  importers/
    csv_parser.py
    examples/opportunities.csv
  scoring/
    engine.py
    pseudocode.md
  storage/
    schema_v2.md
    schema_v2.json
tests/
  test_scoring_engine.py
TODO.md
README.md
```
