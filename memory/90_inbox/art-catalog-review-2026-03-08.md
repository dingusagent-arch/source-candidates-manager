# Art Catalog Project Review

Date: 2026-03-08 13:25 EDT
Project: `/home/dingus/Projects/art-catalog-2025`
Reviewer: main agent (direct review)

## Scope requested
- Current code/project state
- Suggested improvements
- Suggested backlog of features

## What I checked
- Git branch/status and recent commits
- Project structure and key files
- Backend API implementation (`admin_backend/main.py`)
- Admin frontend (`admin_app/app.js`)
- Data pipelines (`scripts/build-catalog-data.py`, `scripts/sync-sheet-metadata.py`)
- CI config (`.github/workflows/python-ci.yml`)
- Test files (`admin_backend/tests/test_admin_save_flow.py`)

## Current state (snapshot)

### Repository
- Active branch: `fix/admin-save-qa-ci` (tracking `origin/fix/admin-save-qa-ci`)
- Recent focus: admin save QA automation + Python CI + admin auth/paging hardening.

### Architecture
- Public gallery is static (`index.html`, `app.js`, `styles.css`) served by http server.
- Admin is split:
  - frontend: `admin_app/`
  - backend: FastAPI (`admin_backend/main.py`)
- Metadata lives in JSON files (`metadata-map.json`, `catalog-data.json`) with a lock + temp-write replacement in backend.
- Auth/session/audit are persisted in SQLite (`admin_backend/admin.db`).

### Security posture (code-level)
Good:
- Startup hard-fails if `ADMIN_PASSWORD` is missing/default (`change-me`).
- Password hashing uses PBKDF2-HMAC-SHA256 with salt.
- Session cookie set `HttpOnly` + `SameSite=lax`.
- Basic response hardening headers for API responses.
- Filename normalization/validation helps prevent path traversal.

Needs improvement:
- `openclaw.json` currently contains plaintext secrets (Discord token, gateway auth token) outside this repo; this is a host config risk.
- CORS defaults are permissive-ish in env-driven mode; local default is okay, but should be explicit per environment.
- No CSRF token mechanism for cookie-authenticated mutating API calls.

### Test/CI state
- CI workflow is present and sensible (ruff + pytest; optional smoke workflow_dispatch).
- Local test execution in this runtime could not be completed because toolchain packages are absent in available Python env (`pytest`/`ruff` modules missing).
- Test suite currently covers core save/revert path and one validation boundary (overlong description).

## Suggested improvements (prioritized)

## High
1. **Add CSRF protection for mutating admin endpoints**
   - Why: cookie auth + mutating endpoints (`PATCH/POST/DELETE`) is vulnerable to cross-site request scenarios.
   - Effort: 4-8h

2. **Replace or encrypt secrets in host config / move to env source of truth**
   - Why: plaintext secrets in config files increase compromise blast radius.
   - Effort: 2-4h

3. **Expand backend tests for auth/session/edge cases**
   - Add tests for expired session, invalid cookie, delete/rebuild failure path, bulk partial failure semantics, and audit correctness.
   - Effort: 6-10h

4. **Add transactional/atomic strategy for delete + rebuild workflow**
   - Why: current delete then rebuild may leave partial system state if rebuild fails.
   - Effort: 6-12h

## Medium
5. **Centralize validation schema for metadata fields**
   - Move repeated field logic to a shared Pydantic model or utility with stricter typing.
   - Effort: 3-5h

6. **Add structured logging and request correlation IDs**
   - Why: improves troubleshooting and traceability for admin changes.
   - Effort: 3-6h

7. **Pagination/filter UX + backend query parity**
   - Backend supports `offset/limit/q`; frontend currently loads all entries and filters client-side. Add paged fetching for scale.
   - Effort: 6-12h

8. **CI: add security/static checks and dependency audit**
   - Add `pip-audit` or equivalent; include basic SAST checks.
   - Effort: 2-4h

## Low
9. **Refactor large `main.py` into modules**
   - Split auth/session, metadata service, audit service, and API router modules.
   - Effort: 8-16h

10. **Frontend state management cleanup**
   - `admin_app/app.js` is monolithic; modularize for maintainability.
   - Effort: 8-14h

11. **Developer onboarding updates**
   - Cross-platform env bootstrap script and one-command local checks.
   - Effort: 2-3h

## Suggested feature backlog (product-facing)

## High-value near-term
1. **Bulk review workflow improvements**
   - Multi-select, batch tag/period/title templates, keyboard-first review queue.
   - Effort: 10-18h

2. **Versioned metadata history + one-click rollback per record**
   - Build on audit table to restore prior snapshots quickly.
   - Effort: 8-14h

3. **Duplicate detection / near-duplicate assistant**
   - Detect filename/content duplicates and flag before publish.
   - Effort: 12-24h

4. **Publish pipeline status dashboard**
   - Last sync time, rebuild status, failures, and stale-data warnings.
   - Effort: 6-10h

## Medium-term
5. **Role-based admin access (read-only vs editor)**
   - Current model is single admin identity.
   - Effort: 10-20h

6. **Metadata quality rules + scorecard**
   - Completeness scoring and missing critical fields by period/tag.
   - Effort: 8-12h

7. **Image lifecycle ops**
   - Replace image, rotate/crop metadata, and safe delete/archive pipeline.
   - Effort: 12-24h

## Long-term
8. **Headless API for external integrations**
   - Cleaner integration with social/content pipelines.
   - Effort: 16-30h

## Recommended next sprint (practical)
1. CSRF protection + auth/session tests
2. Delete/rebuild transaction safety
3. Frontend paged loading + backend query parity
4. Metadata history rollback MVP

## Notes / constraints from this run
- I did not run internet installs from this runtime (no external package install executed).
- Local lint/tests were not executable in the current runtime due missing modules in available env.
- CI workflow appears ready to validate lint/test once run in GitHub Actions.
