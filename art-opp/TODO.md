# TODO - ART-OPP-2026Q2

## Near-term

- [ ] Wire CLI triage actions to persistent storage (JSONL or SQLite).
- [ ] Add schema validation step on import (current parser is example-only).
- [ ] Add deadline parsing robustness for multiple date formats/timezones.
- [ ] Add scoring weight configuration via YAML/JSON.
- [ ] Add explainability output (`score_breakdown`) to CLI commands.

## Quality

- [ ] Add tests for CSV parser edge cases (empty rows, malformed dates, bad URLs).
- [ ] Add tests for CLI argument validation and exit codes.
- [ ] Add CI workflow for lint + tests.

## Product

- [ ] Define canonical source-of-truth for `status` transitions.
- [ ] Confirm final scoring ranges and threshold tuning with validation plan.
- [ ] Align output fields with downstream reporting requirements.
