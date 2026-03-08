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

## Remaining queue
1. Expand tests for auth/session/delete-rebuild failure paths.
2. Improve delete/rebuild failure safety (transaction/rollback semantics).
3. Add pagination parity improvements for frontend to consume backend paging.
4. Re-run full lint/tests in proper env (current runtime lacked local pytest/ruff installation in active path).
