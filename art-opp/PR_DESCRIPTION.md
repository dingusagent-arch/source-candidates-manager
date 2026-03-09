# PR: ART-OPP-2026Q2 ticket-ready starter artifacts

## Summary

Adds a minimal, documented repository skeleton for ART-OPP-2026Q2 under `art-opp/src/` including:

1. Storage schema v2
   - `src/storage/schema_v2.md`
   - `src/storage/schema_v2.json`
2. Rule-based scoring engine
   - `src/scoring/engine.py`
   - `src/scoring/pseudocode.md`
   - `tests/test_scoring_engine.py`
3. CSV import example parser
   - `src/importers/csv_parser.py`
   - `src/importers/examples/opportunities.csv`
4. CLI triage stub (`approve/reject/skip`)
   - `src/cli/triage.py`
5. Project documentation and next steps
   - `README.md`
   - `TODO.md`

## Why

Provides non-sensitive, ticket-ready scaffolding aligned to MVP artifacts without introducing external dependencies or build/install requirements.

## Notes

- No builds/install steps were run.
- Parser currently demonstrates mapping only; schema validation is listed in TODO.
- CLI is intentionally non-persistent and prints action payloads.

## Commit

- `df62fdf` feat(art-opp): add q2 starter skeleton with schema, scoring, parser, and triage cli

## Manual PR open steps (when remote is configured)

```bash
git checkout -b feat/art-opp-2026q2-starter
git push -u origin feat/art-opp-2026q2-starter
gh pr create --title "ART-OPP-2026Q2: starter schema/scoring/import/triage skeleton" --body-file art-opp/PR_DESCRIPTION.md
```
