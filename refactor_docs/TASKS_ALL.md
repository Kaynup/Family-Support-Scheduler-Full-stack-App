# TASKS_ALL

Ordered execution plan. Each task has a clear scope, files affected, and done condition.
Tasks are grouped by phase. No phase begins before the previous phase is complete.
Do not code anything outside the listed scope of the active task.

---

## PHASE 1 — Backend Structural Refactoring

---

### TASK 1.1 — Create constants.py

File: backend/app/constants.py
Action: Create new file.

Write all magic strings as module-level named constants:
STATUS_PAID, STATUS_UNPAID, ROLE_SENDER, ROLE_BENEFICIARY,
INTERVAL_NONE, INTERVAL_WEEKLY, INTERVAL_MONTHLY,
SOFT_DELETE_YES, SOFT_DELETE_NO, EXPIRED_YES, EXPIRED_NO,
CURRENCY_USDT, TRANSACTION_PENDING, TRANSACTION_COMPLETED, TRANSACTION_FAILED.

Done when: file exists, no logic, only string assignments.

---

### TASK 1.2 — Create core/config.py

Files: backend/app/core/__init__.py, backend/app/core/config.py
Action: Create new directory and files.

config.py reads all .env variables once and exposes a single `settings` object.
Fields: db_host, db_user, db_password, db_name, db_table, db_conn_pooling,
fe_url, fe_local_url, receiver_panel_url, sender_panel_url,
jwt_secret_key, jwt_algorithm, jwt_expire_minutes.

Done when: `from app.core.config import settings` works and settings.db_host returns a value.

---

### TASK 1.3 — Create core/exceptions.py

File: backend/app/core/exceptions.py
Action: Create new file.

Define custom exception classes:
BillNotFoundError(Exception)
BillAlreadyPaidError(Exception)
RemittanceValidationError(Exception)
AuthenticationError(Exception)
UnauthorizedRoleError(Exception)

Done when: all five classes exist and can be imported.

---

### TASK 1.4 — Refactor db/connection.py to context manager

File: backend/app/db/connection.py
Action: Refactor existing file.

Replace get_connection() function with get_db_connection() context manager using
@contextmanager. It must: get connection from pool, yield (conn, cursor), commit on
success, rollback on exception, always close cursor and connection in finally block.

Done when: existing queries.py still imports from connection.py without error
and context manager handles commit/rollback/close automatically.

---

### TASK 1.5 — Split queries.py into queries/ directory

Files to create:
  backend/app/db/queries/__init__.py
  backend/app/db/queries/bill_insert.py
  backend/app/db/queries/bill_select.py
  backend/app/db/queries/bill_update.py
  backend/app/db/queries/bill_delete.py

Action: Split existing backend/app/db/queries.py into above files.
Each query function is rewritten to use the get_db_connection() context manager.
queries/__init__.py re-exports all functions so `from app.db import queries as dbq`
still works in all service files without any import changes.

File: backend/app/db/__init__.py
Action: Update to export only get_db_connection.

Delete: backend/app/db/queries.py after split is confirmed working.

Done when: all existing services import dbq successfully, all existing tests pass.

---

### TASK 1.6 — Split schemas.py into schemas/ directory

Files to create:
  backend/app/schemas/__init__.py
  backend/app/schemas/bill_schemas.py
  backend/app/schemas/auth_schemas.py
  backend/app/schemas/remittance_schemas.py

bill_schemas.py: move BillStatus, BillCreateRequest, BillUpdateRequest from schemas.py.
Add BillResponse and BillListResponse dataclasses.
auth_schemas.py: create RegisterRequest, LoginRequest, TokenResponse, UserResponse.
remittance_schemas.py: create RemittanceCreateRequest, RemittanceResponse.
__init__.py: re-export all schema classes.

Delete: backend/app/schemas.py after split is confirmed working.

Done when: routes import from app.schemas without error, existing tests still pass.

---

### TASK 1.7 — Consolidate services into bill_service.py

File to create: backend/app/services/bill_service.py
Action: Merge bill_creation.py, bill_listing.py, bill_status.py,
bill_deletion.py, bill_search.py into one file.

Functions to define (names updated for clarity):
  create_bill(...)
  list_bills(upcoming_only, expired_only, days)
  get_bill_by_id(bill_id)
  mark_bill_status(bill_id, new_status)
  delete_bill(bill_id)
  search_bills_by_name(name)

Private helper _format_bill_row(row) defined once here.
Replaces the duplicate in bill_listing.py and bill_search.py.

Use custom exceptions (BillNotFoundError) instead of ValueError where applicable.
Use constants from constants.py instead of raw strings.

File: backend/app/services/__init__.py
Action: Update exports to reference bill_service.py functions.

Delete: bill_creation.py, bill_listing.py, bill_status.py,
bill_deletion.py, bill_search.py after consolidation confirmed.

Done when: routes import from services without error, all existing tests pass.

---

### TASK 1.8 — Rename and refactor bill routes

File: backend/app/routes/bill_routes.py (renamed from api_endpoints.py)
Action: Rename file. Update imports to use new schema paths and new service names.
Update exception handling to catch typed exceptions instead of string-matching ValueError.
Add query parameters: month (str, optional), sort (str, optional, default "due_date_asc").

File: backend/app/routes/__init__.py
Action: Update import to reference bill_routes instead of api_endpoints.

File: backend/app/main.py
Action: Update router import. Import settings from core.config instead of os.getenv.
Update CORS allow_origins to read receiver and sender panel URLs from settings.

Done when: backend starts with uvicorn, /health returns 200, all bill routes work.

---

### TASK 1.9 — Add users table to database schema

File: database/schema.sql
Action: Add CREATE TABLE users and CREATE TABLE remittance_transactions.
Add user_id column (nullable FK) to bills table.

File: database/sample-data.sql
Action: Add INSERT statements for two beneficiary users and one sender user
with bcrypt-hashed passwords. Add two sample remittance_transactions.

Done when: schema.sql executes cleanly on a fresh MySQL database.

---

### TASK 1.10 — Implement user query files

Files to create:
  backend/app/db/queries/user_insert.py   -- insert_user(username, password_hash, role)
  backend/app/db/queries/user_select.py   -- select_user_by_username(username),
                                             select_user_by_id(user_id)

All functions use get_db_connection() context manager.
Export from queries/__init__.py.

Done when: functions importable and callable with mocked connection in tests.

---

### TASK 1.11 — Implement auth_service.py

File: backend/app/services/auth_service.py
Action: Create new file.

Functions:
  hash_password(plain_password) -> str
  verify_password(plain_password, hashed_password) -> bool
  create_access_token(user_id, username, role) -> str
  decode_access_token(token) -> dict
  register_user(username, password, role) -> dict
  login_user(username, password) -> dict
  get_current_user(token: str) -> dict  (used as FastAPI Dependency)

Uses passlib[bcrypt] for hashing, python-jose for JWT.
Raises AuthenticationError for bad credentials.
Raises UnauthorizedRoleError for wrong role.

Done when: register and login callable with mocked DB in tests.

---

### TASK 1.12 — Implement auth_routes.py

File: backend/app/routes/auth_routes.py
Action: Create new file.

Routes:
  POST /auth/register  -- calls register_user(), returns 201
  POST /auth/login     -- calls login_user(), returns TokenResponse

File: backend/app/main.py
Action: Include auth_routes router.

Done when: POST /auth/register and POST /auth/login return correct responses.

---

### TASK 1.13 — Implement remittance query files

Files to create:
  backend/app/db/queries/remittance_insert.py  -- insert_remittance_transaction(...)
  backend/app/db/queries/remittance_select.py  -- select_remittance_by_bill_id(bill_id),
                                                  select_remittance_by_sender_id(sender_id)

Done when: functions importable and use context manager correctly.

---

### TASK 1.14 — Implement remittance_service.py

File: backend/app/services/remittance_service.py
Action: Create new file.

Functions:
  pay_bill_via_remittance(bill_id, sender_user_id, amount, currency) -> dict
    Steps: fetch bill, assert UNPAID, assert amount sufficient,
           insert transaction, mark bill PAID, return transaction record.
  get_remittance_history_for_sender(sender_user_id) -> dict
  get_remittance_history_for_bill(bill_id) -> dict

Raises RemittanceValidationError on business rule violations.

Done when: pay_bill_via_remittance callable with mocked DB in tests.

---

### TASK 1.15 — Implement remittance_routes.py

File: backend/app/routes/remittance_routes.py
Action: Create new file.

Routes:
  POST /remittance/pay      -- requires sender role. Calls pay_bill_via_remittance.
  GET  /remittance/history  -- requires sender role. Returns sender's transaction history.

File: backend/app/main.py
Action: Include remittance_routes router.

Done when: both routes return correct responses with a valid sender JWT.

---

### TASK 1.16 — Refactor requirements.txt and .env

File: requirements.txt
Action: Add passlib[bcrypt] and python-jose[cryptography].

File: .env
Action: Add RECEIVER_PANEL_PORT, SENDER_PANEL_PORT, JWT_SECRET_KEY,
JWT_ALGORITHM, JWT_EXPIRE_MINUTES.

File: Makefile
Action: Add start-receiver, start-sender, start-all, run-tests targets.
Fix venv path from external hardcoded path to .venv/bin/activate.

Done when: `make run-tests` executes all tests without ImportError.

---

## PHASE 2 — Test Restructuring

---

### TASK 2.1 — Restructure test directories

Create directory structure:
  tests/__init__.py
  tests/test_db/__init__.py
  tests/test_services/__init__.py
  tests/test_api/__init__.py

Done when: directories and __init__.py files exist.

---

### TASK 2.2 — Migrate bill service tests

File: tests/test_services/test_bill_service.py
Action: Migrate all tests from test_services_no_api.py.
Update mock paths to match new bill_service.py location.
Update function call names to match renamed service functions.
Add test cases for BillNotFoundError being raised correctly.

Delete: tests/test_services_no_api.py after migration confirmed.

Done when: pytest tests/test_services/test_bill_service.py passes all cases.

---

### TASK 2.3 — Migrate bill route tests

File: tests/test_api/test_bill_routes.py
Action: Migrate all tests from test_api_server.py.
Update mock paths to reference new bill_routes.py and bill_service.py.

Delete: tests/test_api_server.py after migration confirmed.

Done when: pytest tests/test_api/test_bill_routes.py passes all cases.

---

### TASK 2.4 — Migrate DB tests

File: tests/test_db/test_connection.py
Action: Migrate tests from test_raw_sql_queries.py.
Add tests for the context manager: verify commit called on success,
rollback called on exception, connection always closed via finally.

Delete: tests/test_raw_sql_queries.py after migration confirmed.

Done when: pytest tests/test_db/ passes all cases.

---

### TASK 2.5 — Write auth service tests

File: tests/test_services/test_auth_service.py
Action: Create new file.

Test cases:
  test_register_user_success
  test_register_user_duplicate_username
  test_login_user_success
  test_login_user_wrong_password
  test_login_user_not_found
  test_decode_valid_token
  test_decode_expired_token

All DB calls mocked.

Done when: pytest tests/test_services/test_auth_service.py passes all cases.

---

### TASK 2.6 — Write auth route tests

File: tests/test_api/test_auth_routes.py
Action: Create new file.

Test cases:
  test_register_endpoint_success
  test_login_endpoint_success
  test_login_endpoint_invalid_credentials

All service calls mocked via unittest.mock.patch.

Done when: pytest tests/test_api/test_auth_routes.py passes all cases.

---

### TASK 2.7 — Write remittance service tests

File: tests/test_services/test_remittance_service.py
Action: Create new file.

Test cases:
  test_pay_bill_success
  test_pay_bill_already_paid
  test_pay_bill_insufficient_amount
  test_get_history_for_sender

Done when: pytest tests/test_services/test_remittance_service.py passes.

---

### TASK 2.8 — Write remittance route tests

File: tests/test_api/test_remittance_routes.py
Action: Create new file.

Test cases:
  test_pay_endpoint_sender_role_success
  test_pay_endpoint_beneficiary_role_rejected
  test_history_endpoint_success

Done when: pytest tests/test_api/test_remittance_routes.py passes.

---

## PHASE 3 — Frontend MPA Migration

---

### TASK 3.1 — Create receiver_panel directory structure

Action: Create all directories.
  frontend/receiver_panel/pages/
  frontend/receiver_panel/css/
  frontend/receiver_panel/js/core/
  frontend/receiver_panel/js/components/

Copy frontend/css/*.css into receiver_panel/css/ unchanged.

Done when: all directories exist and CSS files are in place.

---

### TASK 3.2 — Create receiver_panel config.js

File: frontend/receiver_panel/js/config.js
Action: Create new file.

  export const API_BASE_URL = "http://127.0.0.1:8000";
  export const PANEL_NAME = "receiver";

Done when: file exists and exports are correct.

---

### TASK 3.3 — Migrate core JS files to receiver_panel

Files:
  frontend/receiver_panel/js/core/state.js     -- migrate from frontend/js/core/state.js,
                                                  add currentUser: null field.
  frontend/receiver_panel/js/core/utils.js     -- copy unchanged from frontend/js/core/utils.js.
  frontend/receiver_panel/js/core/api.js       -- migrate from frontend/js/core/api.js,
                                                  read API_BASE_URL from config.js,
                                                  inject Authorization header from localStorage.
  frontend/receiver_panel/js/core/auth_guard.js -- create new.
                                                  guardRoute() reads token from localStorage,
                                                  redirects to login.html if absent.

Done when: all four files exist and auth_guard.js redirects correctly when no token.

---

### TASK 3.4 — Migrate component JS files to receiver_panel

Files:
  frontend/receiver_panel/js/components/ui.js      -- migrate from frontend/js/components/ui.js.
                                                      Remove create modal element refs.
                                                      Add renderRemittanceStatusBadge(status).
  frontend/receiver_panel/js/components/calendar.js -- copy unchanged.
  frontend/receiver_panel/js/components/modal.js    -- copy unchanged (delete modal only).

Done when: all three files exist without reference to removed elements.

---

### TASK 3.5 — Create receiver_panel login.html and auth.js

Files:
  frontend/receiver_panel/pages/login.html   -- form with username, password inputs.
                                               Action calls auth.js handleLoginSubmit.
                                               Link to register.html.
                                               No hardcoded credentials.
  frontend/receiver_panel/pages/register.html -- form with username, password, role=beneficiary.
                                                Action calls auth.js handleRegisterSubmit.
  frontend/receiver_panel/js/auth.js          -- handleLoginSubmit: POST /auth/login,
                                                store token in localStorage,
                                                redirect to dashboard.html.
                                                handleRegisterSubmit: POST /auth/register,
                                                redirect to login.html on success.

Done when: login form submits to API, valid credentials store token and redirect.

---

### TASK 3.6 — Migrate dashboard.html and dashboard.js to receiver_panel

Files:
  frontend/receiver_panel/pages/dashboard.html -- migrate from frontend/dashboard.html.
                                                  Remove create-modal HTML block.
                                                  Add nav links to bills.html and create.html.
  frontend/receiver_panel/js/dashboard.js      -- migrate from frontend/js/dashboard.js.
                                                  Add guardRoute() call at top.
                                                  Remove all create modal event wiring.
                                                  Retain: calendar, bill listing, delete modal,
                                                  upcoming popup, search, month nav.

Done when: dashboard loads bills from API with valid token, calendar renders correctly.

---

### TASK 3.7 — Create bills.html and bills.js for receiver_panel

Files:
  frontend/receiver_panel/pages/bills.html -- table layout for all bills.
                                              Search bar, filter controls.
                                              Mark Paid and Delete buttons.
  frontend/receiver_panel/js/bills.js      -- guardRoute() at top.
                                              Load: BillSearch, BillListing, BillStatus,
                                              BillDeletion features.
                                              Wire all event listeners for this page only.

Done when: bills.html shows all bills, search works, mark paid works, delete works.

---

### TASK 3.8 — Create create.html and create.js for receiver_panel

Files:
  frontend/receiver_panel/pages/create.html -- standalone bill creation form.
                                               Same fields as the old modal form.
                                               Cancel button navigates back to bills.html.
  frontend/receiver_panel/js/create.js      -- guardRoute() at top.
                                              handleCreateBillSubmit: validate, POST to API,
                                              redirect to bills.html on success.

Done when: creating a bill from create.html persists to DB and redirects correctly.

---

### TASK 3.9 — Create history.html and history.js for receiver_panel

Files:
  frontend/receiver_panel/pages/history.html -- table of remittance transactions for
                                                bills owned by this beneficiary.
  frontend/receiver_panel/js/history.js      -- guardRoute() at top.
                                               Fetch GET /remittance/history,
                                               render transaction rows with status badges.

Done when: history page shows remittance records for the logged-in beneficiary.

---

### TASK 3.10 — Create sender_panel directory structure and config

Action: Create all directories mirroring receiver_panel structure.
  frontend/sender_panel/pages/
  frontend/sender_panel/css/
  frontend/sender_panel/js/core/
  frontend/sender_panel/js/components/

Copy receiver_panel/css/*.css into sender_panel/css/ unchanged.

File: frontend/sender_panel/js/config.js
  export const API_BASE_URL = "http://127.0.0.1:8000";
  export const PANEL_NAME = "sender";

Done when: all directories and config.js exist.

---

### TASK 3.11 — Create sender_panel core JS files

Files:
  frontend/sender_panel/js/core/state.js      -- same structure as receiver state.js.
  frontend/sender_panel/js/core/utils.js      -- copy of receiver utils.js.
  frontend/sender_panel/js/core/api.js        -- same as receiver api.js.
                                                 No createBill(). Has payBill().
  frontend/sender_panel/js/core/auth_guard.js -- same as receiver auth_guard.js
                                                 but also checks role === 'sender'.
                                                 Redirects to login.html if role mismatch.

Done when: all four files exist. auth_guard blocks non-sender role tokens.

---

### TASK 3.12 — Create sender_panel component JS files

Files:
  frontend/sender_panel/js/components/ui.js      -- renderPayButton(bill),
                                                     read-only renderBillTable() (no delete btn).
  frontend/sender_panel/js/components/calendar.js -- copy of receiver calendar.js.
  frontend/sender_panel/js/components/modal.js    -- pay confirmation modal only.

Done when: all three files exist.

---

### TASK 3.13 — Create sender_panel auth pages

Files:
  frontend/sender_panel/pages/login.html   -- same structure as receiver login.html.
  frontend/sender_panel/pages/register.html -- optional sender registration.
  frontend/sender_panel/js/auth.js         -- same as receiver auth.js.
                                              After login, check token role === 'sender'.
                                              If not sender, clear token and show error.

Done when: sender login enforces role check, non-sender credentials are rejected at UI.

---

### TASK 3.14 — Create sender_panel dashboard

Files:
  frontend/sender_panel/pages/dashboard.html -- calendar + all beneficiary bills.
                                                Pay button per bill row. No create/delete.
  frontend/sender_panel/js/dashboard.js      -- guardRoute() (sender role check).
                                               Fetch all bills, render calendar.
                                               Wire Pay button to remittance flow.

Done when: sender dashboard loads all bills, Pay button triggers remittance API call.

---

### TASK 3.15 — Create sender_panel bills and history pages

Files:
  frontend/sender_panel/pages/bills.html   -- read-only bill list with Pay action.
  frontend/sender_panel/js/bills.js        -- guardRoute(). Renders bills with pay flow.
  frontend/sender_panel/pages/history.html -- sender's outgoing remittance history.
  frontend/sender_panel/js/history.js      -- guardRoute(). Fetch GET /remittance/history
                                              for sender, render transaction table.

Done when: both pages render correctly with valid sender token.

---

## PHASE 4 — Documentation Sync

---

### TASK 4.1 — Update backend docs

Files:
  docs/backend/BACKEND.md       -- add sections for core/, constants.py, queries/ split,
                                   auth_service, remittance_service.
  docs/backend/API_AND_SCHEMAS.md -- add /auth and /remittance route documentation.
  docs/backend/FILES_INVOLVED.md  -- sync all file paths to new structure.
  docs/backend/SERVICE_LOGIC.md   -- add auth and remittance service logic descriptions.

Done when: docs accurately reflect the refactored backend, no stale file paths.

---

### TASK 4.2 — Update frontend docs

Files:
  docs/frontend/FRONTEND.md        -- describe dual-panel MPA structure, port assignments.
  docs/frontend/FILES_INVOLVED.md  -- sync all paths to receiver_panel / sender_panel.
  docs/frontend/RENDERING_LOGIC.md -- update for per-page entry JS pattern.
  docs/frontend/UI_AND_COMPONENTS.md -- verify still accurate, minor updates if needed.

Done when: docs accurately reflect the MPA frontend with no references to old flat structure.

---

### TASK 4.3 — Update root docs

Files:
  README.md -- rewrite to describe: project purpose, dual-panel architecture,
               startup instructions (make start-backend, start-receiver, start-sender),
               test instructions (make run-tests), role descriptions.

Done when: a new developer can read README.md and understand how to start and use the app.

---

## Execution Order Summary

  Phase 1: Tasks 1.1 through 1.16   (backend refactoring and new features)
  Phase 2: Tasks 2.1 through 2.8    (test restructuring and new test coverage)
  Phase 3: Tasks 3.1 through 3.15   (frontend MPA migration and dual panel)
  Phase 4: Tasks 4.1 through 4.3    (documentation sync)

Total tasks: 36

---
