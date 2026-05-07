# HIERARCHICAL REFACTORED STRUCTURE

This document is the canonical reference for the target directory and file layout
of the refactored Family Support Scheduler / Remittance Platform.
It is the single source of truth for WHERE every file lives and WHAT it is responsible for.
No file listed here serves more than one responsibility.

---

## Legend

    [NEW]      File or directory does not exist yet and will be created.
    [KEEP]     File exists and its content is retained as-is (possibly minor cleanup).
    [REFACTOR] File exists but its content will be significantly changed.
    [SPLIT]    File exists and its content will be split into multiple files.
    [DELETE]   File exists but will be removed as part of cleanup.
    [RENAME]   File is moved or renamed, content may or may not change.

---

## Root

    InternshipProject/
    ├── .env                           [REFACTOR]  Add new env vars: receiver/sender panel ports,
    │                                              JWT secret, panel base URLs.
    ├── .gitignore                     [KEEP]      No changes required.
    ├── Makefile                       [REFACTOR]  Add targets: start-receiver, start-sender,
    │                                              start-all, run-tests. Fix venv path to be relative.
    ├── requirements.txt               [REFACTOR]  Add: passlib[bcrypt], python-jose[cryptography].
    ├── README.md                      [REFACTOR]  Update to describe dual-panel architecture and
    │                                              new startup commands.
    ├── PROMPT.md                      [KEEP]      Source specification, never modified.
    ├── HIERARCHICAL_REFACTORED_STRUCTURE.md  [NEW]
    ├── DESIGN_ALL.md                  [NEW]
    └── TASKS_ALL.md                   [NEW]

---

## backend/

    backend/
    └── app/
        ├── __init__.py                [KEEP]      Package marker, no logic.
        │
        ├── main.py                    [REFACTOR]  Register all routers (bills, auth, remittance).
        │                                          CORS origins expanded to cover both panel ports.
        │
        ├── constants.py               [NEW]       Central store for all magic strings and enums:
        │                                          STATUS_PAID, STATUS_UNPAID, ROLE_SENDER,
        │                                          ROLE_BENEFICIARY, INTERVAL_NONE, INTERVAL_WEEKLY,
        │                                          INTERVAL_MONTHLY, SOFT_DELETE_YES, SOFT_DELETE_NO,
        │                                          EXPIRED_YES, EXPIRED_NO, CURRENCY_USDT, etc.
        │
        ├── core/                      [NEW DIR]   Cross-cutting concerns, no business logic.
        │   ├── __init__.py            [NEW]
        │   ├── config.py              [NEW]       Reads .env, exposes a single Settings object.
        │                                          All other modules import from here, not os.getenv.
        │   └── exceptions.py          [NEW]       Custom exception classes: BillNotFoundError,
        │                                          BillAlreadyPaidError, RemittanceValidationError,
        │                                          AuthenticationError, UnauthorizedRoleError.
        │
        ├── db/                        [REFACTOR DIR]
        │   ├── __init__.py            [REFACTOR]  Export only get_db_connection context manager.
        │   ├── connection.py          [REFACTOR]  Convert to a context manager using @contextmanager.
        │                                          Handles open, cursor, commit, rollback, close in
        │                                          one place. All query files use this exclusively.
        │   └── queries/               [NEW DIR]   Replaces the monolithic queries.py.
        │       ├── __init__.py        [NEW]       Re-exports all query functions as a flat namespace.
        │       ├── bill_insert.py     [NEW]       insert_bill() only.
        │       ├── bill_select.py     [NEW]       select_all_bills(), select_bill_by_id(),
        │                                          select_bills_by_name(), select_upcoming_bills(),
        │                                          select_expired_bills().
        │       ├── bill_update.py     [NEW]       update_bill_status().
        │       ├── bill_delete.py     [NEW]       soft_delete_bill_by_id().
        │       ├── user_insert.py     [NEW]       insert_user().
        │       ├── user_select.py     [NEW]       select_user_by_username(), select_user_by_id().
        │       ├── remittance_insert.py [NEW]     insert_remittance_transaction().
        │       └── remittance_select.py [NEW]     select_remittance_by_bill_id(),
        │                                          select_remittance_by_sender_id().
        │
        ├── schemas/                   [NEW DIR]   Replaces the monolithic schemas.py.
        │   ├── __init__.py            [NEW]       Re-exports all schema classes.
        │   ├── bill_schemas.py        [NEW]       BillCreateRequest, BillUpdateRequest,
        │                                          BillResponse, BillListResponse.
        │   ├── auth_schemas.py        [NEW]       RegisterRequest, LoginRequest, TokenResponse,
        │                                          UserResponse.
        │   └── remittance_schemas.py  [NEW]       RemittanceCreateRequest, RemittanceResponse.
        │
        ├── services/                  [REFACTOR DIR]
        │   ├── __init__.py            [REFACTOR]  Updated exports to match renamed service files.
        │   ├── bill_service.py        [NEW]       Consolidates bill_creation, bill_listing,
        │   │                                      bill_status, bill_deletion, bill_search into one
        │   │                                      cohesive module. Each function remains separate
        │   │                                      and named clearly.
        │   │                                      Functions: create_bill(), list_bills(),
        │   │                                      get_upcoming_bills(), get_expired_bills(),
        │   │                                      mark_bill_status(), delete_bill(), search_bills().
        │   ├── auth_service.py        [NEW]       register_user(), login_user(), verify_token(),
        │   │                                      get_current_user(), hash_password(),
        │   │                                      verify_password(). Uses passlib + python-jose.
        │   └── remittance_service.py  [NEW]       pay_bill_via_remittance(),
        │                                          get_remittance_history_for_sender(),
        │                                          get_remittance_history_for_bill().
        │
        │   [DELETE] bill_creation.py  -- merged into bill_service.py
        │   [DELETE] bill_listing.py   -- merged into bill_service.py
        │   [DELETE] bill_status.py    -- merged into bill_service.py
        │   [DELETE] bill_deletion.py  -- merged into bill_service.py
        │   [DELETE] bill_search.py    -- merged into bill_service.py
        │
        └── routes/                    [REFACTOR DIR]
            ├── __init__.py            [REFACTOR]  Updated router imports.
            ├── bill_routes.py         [RENAME]    Renamed from api_endpoints.py. Routes are
            │                                      logically identical but use the new unified
            │                                      bill_service and new schema imports.
            │                                      Adds: filter/sort query params (month, sort).
            │                                      Enforces role-based access: only beneficiaries
            │                                      can create/delete bills.
            ├── auth_routes.py         [NEW]       POST /auth/register, POST /auth/login.
            │                                      Returns JWT token on success.
            └── remittance_routes.py   [NEW]       POST /remittance/pay, GET /remittance/history.
                                                   Sender role required.

        [DELETE] schemas.py            -- replaced by schemas/ directory

---

## database/

    database/
    ├── README.md                      [KEEP]
    ├── schema.sql                     [REFACTOR]  Add users table and remittance_transactions table.
    │                                              Retain existing bills table unchanged except
    │                                              adding user_id foreign key (beneficiary owner).
    └── sample-data.sql                [REFACTOR]  Add sample users (one sender, two beneficiaries)
                                                   and sample remittance transactions aligned with
                                                   existing sample bills.

Schema additions to schema.sql:

    users:
        id INT AUTO_INCREMENT PRIMARY KEY
        username VARCHAR(100) UNIQUE NOT NULL
        password_hash VARCHAR(255) NOT NULL
        role VARCHAR(20) NOT NULL           -- 'sender' or 'beneficiary'
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP

    remittance_transactions:
        transaction_id INT AUTO_INCREMENT PRIMARY KEY
        bill_id INT NOT NULL               (FK -> bills.id)
        sender_user_id INT NOT NULL        (FK -> users.id)
        beneficiary_user_id INT NOT NULL   (FK -> users.id)
        amount DECIMAL(10,2) NOT NULL
        currency VARCHAR(20) DEFAULT 'USDT'
        transaction_status VARCHAR(20) NOT NULL   -- 'PENDING', 'COMPLETED', 'FAILED'
        payment_method VARCHAR(50) DEFAULT 'stablecoin'
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP

    bills table modification:
        Add column: user_id INT (FK -> users.id, nullable for backward compatibility)

---

## frontend/

The existing flat frontend/ directory is reorganized into two independent panels.
Current frontend/css/ and frontend/js/ content is migrated into receiver_panel/
with targeted modifications. sender_panel/ is a new parallel structure.

    frontend/
    ├── [DELETE] dashboard.html        -- migrated to receiver_panel/pages/dashboard.html
    ├── [DELETE] index.html            -- migrated to receiver_panel/pages/login.html
    ├── [DELETE] styles.css            -- replaced by receiver_panel/css/ directory
    ├── [DELETE] js/                   -- migrated and restructured under panels
    │
    ├── receiver_panel/                [NEW DIR]   Serves on port 3000.
    │   ├── pages/                     [NEW DIR]   One HTML file per logical screen. No hidden divs.
    │   │   ├── index.html             [NEW]       Redirect to login.html (landing).
    │   │   ├── login.html             [NEW]       Backend-connected login form. No hardcoded creds.
    │   │   │                                      Loads: js/auth.js only.
    │   │   ├── register.html          [NEW]       Registration form for new beneficiary accounts.
    │   │   │                                      Loads: js/auth.js only.
    │   │   ├── dashboard.html         [REFACTOR]  Calendar + due bills + paid bills.
    │   │   │                                      No create modal here (moved to create.html).
    │   │   │                                      Loads: js/dashboard.js only.
    │   │   ├── bills.html             [NEW]       Full bill list with filtering and search.
    │   │   │                                      Loads: js/bills.js only.
    │   │   ├── create.html            [NEW]       Bill creation form, dedicated page.
    │   │   │                                      Loads: js/create.js only.
    │   │   └── history.html           [NEW]       Payment history / remittance status.
    │   │                                          Loads: js/history.js only.
    │   │
    │   ├── css/                       [NEW DIR]   Migrated from frontend/css/, no visual changes.
    │   │   ├── base.css               [KEEP]      Reset, variables, typography, global defaults.
    │   │   ├── layout.css             [KEEP]      Grid system, dashboard-grid, panel layouts.
    │   │   ├── components.css         [KEEP]      Buttons, tables, bill rows, badges, form inputs.
    │   │   ├── calendar.css           [KEEP]      Calendar grid, day glows, legend.
    │   │   └── modals.css             [KEEP]      Modal overlay, modal-content, modal-actions.
    │   │
    │   └── js/                        [NEW DIR]   One entry-point JS per page.
    │       ├── config.js              [NEW]       API_BASE_URL, RECEIVER_PORT.
    │       ├── core/                  [NEW DIR]
    │       │   ├── api.js             [REFACTOR]  Adds Authorization header from localStorage token.
    │       │   │                                  Adds: fetchBillsByMonth(), fetchBillsSorted(),
    │       │   │                                  payBill(), fetchRemittanceHistory().
    │       │   │                                  Reads API_BASE_URL from config.js.
    │       │   ├── auth_guard.js      [NEW]       Reads token from localStorage. Redirects to
    │       │   │                                  login.html if absent or expired.
    │       │   ├── state.js           [REFACTOR]  Adds: currentUser field from decoded token payload.
    │       │   └── utils.js           [KEEP]      Unchanged. Date helpers and projection engine.
    │       │
    │       ├── components/            [NEW DIR]
    │       │   ├── ui.js              [REFACTOR]  Removes create modal element refs.
    │       │   │                                  Adds: renderRemittanceStatusBadge().
    │       │   ├── calendar.js        [KEEP]      Unchanged. Pure calendar renderer.
    │       │   └── modal.js           [KEEP]      Only delete confirmation modal remains here.
    │       │
    │       ├── dashboard.js           [REFACTOR]  Auth guard check at top. No create modal wiring.
    │       ├── bills.js               [NEW]       Full bill management: search, list, status, delete.
    │       ├── create.js              [NEW]       Bill creation form submission only.
    │       ├── history.js             [NEW]       Remittance history display for beneficiary.
    │       └── auth.js                [NEW]       Login + register form handling. Token storage.
    │
    └── sender_panel/                  [NEW DIR]   Serves on port 3001.
        ├── pages/                     [NEW DIR]
        │   ├── index.html             [NEW]       Redirect to login.html.
        │   ├── login.html             [NEW]       Sender login. Enforces role check post-login.
        │   ├── register.html          [NEW]       Optional sender registration.
        │   ├── dashboard.html         [NEW]       Shows all beneficiary bills. Pay button per bill.
        │   │                                      Loads: js/dashboard.js only.
        │   ├── bills.html             [NEW]       Read-only bill list with pay action.
        │   │                                      Loads: js/bills.js only.
        │   └── history.html           [NEW]       Sender's outgoing remittance transaction history.
        │                                          Loads: js/history.js only.
        │
        ├── css/                       [NEW DIR]   Shared CSS, identical to receiver_panel/css/.
        │   ├── base.css               [NEW]       Copied from receiver panel.
        │   ├── layout.css             [NEW]       Copied from receiver panel.
        │   ├── components.css         [NEW]       Copied from receiver panel.
        │   ├── calendar.css           [NEW]       Copied from receiver panel.
        │   └── modals.css             [NEW]       Copied from receiver panel.
        │
        └── js/                        [NEW DIR]
            ├── config.js              [NEW]       API_BASE_URL, SENDER_PORT.
            ├── core/                  [NEW DIR]
            │   ├── api.js             [NEW]       Sender API calls: fetchAllBills(), payBill(),
            │   │                                  fetchRemittanceHistory(). No createBill().
            │   ├── auth_guard.js      [NEW]       Same as receiver but enforces role === 'sender'.
            │   ├── state.js           [NEW]       Same structure as receiver state.js.
            │   └── utils.js           [NEW]       Same file as receiver utils.js (copied).
            │
            ├── components/            [NEW DIR]
            │   ├── ui.js              [NEW]       Sender UI: renderPayButton(), read-only bill table.
            │   ├── calendar.js        [NEW]       Copied from receiver calendar.js.
            │   └── modal.js           [NEW]       Pay confirmation modal.
            │
            ├── dashboard.js           [NEW]       Sender dashboard entry point.
            ├── bills.js               [NEW]       Sender bill list entry point.
            ├── history.js             [NEW]       Sender remittance history entry point.
            └── auth.js                [NEW]       Sender auth: login, register, role enforcement.

---

## tests/

    tests/
    ├── __init__.py                    [NEW]       Package marker.
    │
    ├── test_db/                       [NEW DIR]
    │   ├── __init__.py                [NEW]
    │   └── test_connection.py         [NEW]       Tests the connection context manager:
    │                                              commit on success, rollback on exception,
    │                                              connection always closed.
    │
    ├── test_services/                 [NEW DIR]
    │   ├── __init__.py                [NEW]
    │   ├── test_bill_service.py       [NEW]       All bill service tests consolidated from
    │   │                                          test_services_no_api.py. Uses unittest.mock.
    │   ├── test_auth_service.py       [NEW]       Tests register_user, login_user, verify_token.
    │   └── test_remittance_service.py [NEW]       Tests pay_bill_via_remittance.
    │
    └── test_api/                      [NEW DIR]
        ├── __init__.py                [NEW]
        ├── test_bill_routes.py        [NEW]       Migrated from test_api_server.py. TestClient
        │                                          + mocked services for bill route coverage.
        ├── test_auth_routes.py        [NEW]       Tests /auth/register and /auth/login.
        └── test_remittance_routes.py  [NEW]       Tests /remittance/pay and /remittance/history.

    [DELETE] tests/test_api_server.py       -- migrated to test_api/test_bill_routes.py
    [DELETE] tests/test_services_no_api.py  -- migrated to test_services/test_bill_service.py
    [DELETE] tests/test_raw_sql_queries.py  -- migrated to test_db/test_connection.py

---

## scripts/ (unchanged)

    scripts/
    ├── main.sh                        [KEEP]
    ├── cron_simulator.sh              [KEEP]
    ├── cron_.log                      [KEEP]
    └── commands/
        ├── add_bill.sh                [KEEP]
        ├── change_status.sh           [KEEP]
        ├── delete_bill.sh             [KEEP]
        ├── health.sh                  [KEEP]
        ├── list_all.sh                [KEEP]
        └── upcoming.sh                [KEEP]

---

## docs/ (updated for new structure)

    docs/
    ├── OTHER.md                       [KEEP]
    ├── backend/
    │   ├── BACKEND.md                 [REFACTOR]  Describes core/, constants.py, queries/, auth,
    │   │                                          and remittance service additions.
    │   ├── API_AND_SCHEMAS.md         [REFACTOR]  Adds auth and remittance API documentation.
    │   ├── FILES_INVOLVED.md          [REFACTOR]  All file paths synced to new structure.
    │   └── SERVICE_LOGIC.md           [REFACTOR]  Adds auth_service and remittance_service logic.
    └── frontend/
        ├── FRONTEND.md                [REFACTOR]  Describes dual-panel MPA structure.
        ├── FILES_INVOLVED.md          [REFACTOR]  Synced to receiver_panel / sender_panel layout.
        ├── RENDERING_LOGIC.md         [REFACTOR]  Updated for per-page JS entry points.
        └── UI_AND_COMPONENTS.md       [KEEP]      CSS component descriptions still valid.

---

## File Count Summary

    New files to be created:     approximately 65
    Files to be refactored:      approximately 25
    Files kept unchanged:        approximately 20
    Files to be deleted:         approximately 10

---
