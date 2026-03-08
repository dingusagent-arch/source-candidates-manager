# Art Catalog Implementation Progress

Date: 2026-03-08 14:19 EDT

## Work started from suggested improvements

Implemented first hardening slice: **CSRF protection** for admin mutating APIs.

### Changes made

#### Backend (`admin_backend/main.py`)
- Added CSRF cookie constant: `admin_csrf`.
- Added `csrf_token` to `sessions` table schema and lightweight migration (`PRAGMA table_info` + `ALTER TABLE` if missing).
- Login now generates and stores CSRF token per session.
- Login response now includes `csrfToken`.
- Added CSRF dependency (`require_csrf`) validating `X-CSRF-Token` against session token (constant-time compare).
- Enforced CSRF on mutating endpoints:
  - `PATCH /api/entries/{filename}`
  - `POST /api/entries/bulk`
  - `POST /api/rebuild`
  - `DELETE /api/entries/{filename}`
- `/api/auth/me` now returns `csrfToken` and re-sets CSRF cookie.
- Logout clears both session and CSRF cookies.

#### Frontend (`admin_app/app.js`)
- Added `state.csrfToken`.
- `api.login()` and `api.me()` now capture and store `csrfToken`.
- `api.request()` now automatically sends `X-CSRF-Token` on mutating methods (`POST/PATCH/PUT/DELETE`) when token exists.

#### Tests / QA script
- Updated `admin_backend/tests/test_admin_save_flow.py`:
  - login helper now returns CSRF token
  - patch calls include CSRF header
- Updated `admin_backend/scripts/qa_admin_save_smoke.py`:
  - captures `csrfToken` on login
  - sends `X-CSRF-Token` on update + revert

### Validation performed
- Python syntax compile checks passed for edited files via `python3 -m py_compile`.

## Verification pass (post Code Agent run)
- Confirmed changed files in repo:
  - `admin_backend/main.py`
  - `admin_backend/tests/test_admin_save_flow.py`
  - `admin_backend/scripts/qa_admin_save_smoke.py`
  - `admin_app/app.js`
  - `README.md`
  - `CHANGELOG.md` (new)
- Ran tests/lint in Linux venv:
  - `admin_backend/.venv-linux/bin/python -m pytest -q` → **5 passed**
  - `admin_backend/.venv-linux/bin/python -m ruff check admin_backend/main.py admin_backend/tests/test_admin_save_flow.py` → **passed**
- Observed warnings:
  - FastAPI `@app.on_event("startup")` deprecation (non-blocking; future cleanup item).

## Remaining queue
1. Frontend/backend pagination parity for large catalogs.
2. Backup/staging retention policy in `process-report/` to avoid growth.
3. Optional modernization: migrate startup hook to FastAPI lifespan API.
