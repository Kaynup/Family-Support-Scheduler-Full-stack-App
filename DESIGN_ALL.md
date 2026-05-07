# DESIGN_ALL

This document describes every architectural and design decision for the refactored
Family Support Scheduler / Remittance Platform. It explains WHY things are structured
the way they are, what patterns are used, and what is intentionally avoided.

---

## 1. Overall Philosophy

The primary goal is NOT feature addition. It is structural correctness.
Every decision made here prioritizes:

- High cohesion: each file has one clear reason to exist.
- Low coupling: changing one module does not cascade into unrelated modules.
- Simplicity: no enterprise overengineering. Patterns must be readable by a junior developer.
- Backend authority: all filtering, sorting, validation, and business logic live in Python.
- Frontend thinness: JavaScript is responsible only for rendering, navigation, and UX states.

---

## 2. Backend Architecture

### 2.1 Application Entry Point: main.py

main.py registers three routers only: bill_routes, auth_routes, remittance_routes.
It reads CORS origins from the Settings object (not raw os.getenv).
It has no business logic. It is the wiring layer, nothing more.

### 2.2 core/ Module

Purpose: cross-cutting infrastructure that does not belong to any single feature.

config.py:
- Reads all environment variables once using pydantic-settings or python-dotenv.
- Exposes a single module-level `settings` object.
- All other modules import `from app.core.config import settings`.
- No other module calls os.getenv() directly. This eliminates scattered env reads.

exceptions.py:
- Defines application-specific exception classes that carry semantic meaning.
- BillNotFoundError replaces generic ValueError("No bill found").
- AuthenticationError, UnauthorizedRoleError, RemittanceValidationError prevent
  exception message string matching in route handlers (the existing anti-pattern).
- Route handlers catch typed exceptions and map them to HTTP status codes cleanly.

### 2.3 constants.py

A flat module at app/ level.
Contains every magic string used across the backend as named constants.

    STATUS_PAID = "PAID"
    STATUS_UNPAID = "UNPAID"
    ROLE_SENDER = "sender"
    ROLE_BENEFICIARY = "beneficiary"
    INTERVAL_NONE = "NONE"
    INTERVAL_WEEKLY = "WEEKLY"
    INTERVAL_MONTHLY = "MONTHLY"
    SOFT_DELETE_YES = "Y"
    SOFT_DELETE_NO = "N"
    EXPIRED_YES = "Y"
    EXPIRED_NO = "N"
    CURRENCY_USDT = "USDT"
    TRANSACTION_STATUS_PENDING = "PENDING"
    TRANSACTION_STATUS_COMPLETED = "COMPLETED"
    TRANSACTION_STATUS_FAILED = "FAILED"

Rationale: changing "UNPAID" to "unpaid" system-wide requires editing one line,
not hunting across five files.

### 2.4 db/connection.py — Context Manager Pattern

Current problem: every query function manually opens a connection, gets a cursor,
commits or rolls back, then closes both. This pattern is duplicated 10+ times.
Any deviation (forgetting conn.close()) causes a connection leak.

Solution: convert connection.py to expose a context manager.

    @contextmanager
    def get_db_connection():
        conn = conn_pool.get_connection()
        cursor = conn.cursor()
        try:
            yield conn, cursor
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()

Every query function becomes:

    def insert_bill(name, due_date, ...):
        with get_db_connection() as (conn, cursor):
            cursor.execute(query, values)
            return cursor.lastrowid

This guarantees commit/rollback/close behavior is never omitted by accident.

### 2.5 db/queries/ — Split by SQL Operation Type

Current problem: queries.py is 161 lines mixing INSERT, SELECT, UPDATE, DELETE
for different domain objects (bills only for now, but users and remittance are coming).

Solution: split into a queries/ directory, one file per operation type per domain.

    bill_insert.py    -- INSERT into bills
    bill_select.py    -- all SELECT variants for bills
    bill_update.py    -- UPDATE bills
    bill_delete.py    -- soft DELETE bills
    user_insert.py    -- INSERT into users
    user_select.py    -- SELECT from users
    remittance_insert.py  -- INSERT into remittance_transactions
    remittance_select.py  -- SELECT from remittance_transactions

The queries/__init__.py re-exports all functions flat so callers write:
    from app.db import queries as dbq
    dbq.insert_bill(...)

This preserves the existing import style in services/ with no refactoring cascade.

### 2.6 schemas/ — Split by Domain

Current problem: schemas.py mixes BillStatus enum, BillCreateRequest, BillUpdateRequest.
As auth and remittance schemas are added, this file becomes a dumping ground.

Solution: one schema file per domain.

    bill_schemas.py       -- BillCreateRequest, BillUpdateRequest, BillResponse, BillListResponse
    auth_schemas.py       -- RegisterRequest, LoginRequest, TokenResponse, UserResponse
    remittance_schemas.py -- RemittanceCreateRequest, RemittanceResponse

Validation logic stays inside the Pydantic models where it belongs.
The existing field validators in BillCreateRequest are preserved exactly.

### 2.7 services/ — Consolidation into Domain Services

Current problem: five separate files (bill_creation.py, bill_listing.py, bill_status.py,
bill_deletion.py, bill_search.py) each have 15-35 lines. The directory has high file count
for very little code. This creates unnecessary navigation overhead.

Solution: consolidate all bill operations into one file: bill_service.py.
Each function retains its own name and clear single responsibility.
The file groups all bill-domain logic together — high cohesion.

Functions in bill_service.py:
    create_bill(name, due_date, total_amount, creation_date, category, recurring_interval, status)
    list_bills(upcoming_only, expired_only, days)
    get_bill_by_id(bill_id)
    mark_bill_status(bill_id, new_status)
    delete_bill(bill_id)
    search_bills_by_name(name)

The private _format_bill_row(row) helper is defined once here (currently duplicated
across bill_listing.py and bill_search.py — this is the most visible redundancy bug).

New files:
    auth_service.py        -- user registration, login, JWT handling
    remittance_service.py  -- remittance payment and history

### 2.8 routes/ — One Router File Per Domain

Current problem: api_endpoints.py is named generically and will grow chaotically
as auth and remittance routes are added to it.

Solution: one router file per domain.

    bill_routes.py        -- /bills prefix
    auth_routes.py        -- /auth prefix
    remittance_routes.py  -- /remittance prefix

Route handlers contain no business logic. They:
1. Parse and validate the incoming request schema.
2. Call exactly one service function.
3. Catch typed exceptions and map to HTTP status codes.
4. Return the service result.

Role-based access control is enforced at the route level using a FastAPI Dependency
that calls auth_service.get_current_user() and checks the role field.

### 2.9 Authentication Design

Implementation: JWT (JSON Web Tokens) using python-jose.
Password storage: bcrypt hashing using passlib.

Flow:
1. POST /auth/register -- creates user, returns 201.
2. POST /auth/login    -- verifies password, returns JWT token.
3. Protected routes    -- FastAPI Depends(get_current_user) extracts and validates token.

Token payload contains: user_id, username, role, exp.
Token is stored in localStorage on the frontend.

Why JWT over sessions:
- Stateless: backend needs no session store.
- Works naturally with two independent frontend panels on different ports.
- Simple to implement with python-jose.

### 2.10 Remittance Design

The remittance layer is deliberately thin. It records a transaction and marks the bill paid.
No blockchain infrastructure is built. The stablecoin concept is represented as a
currency field (defaulting to "USDT") in the remittance_transactions table.

pay_bill_via_remittance(bill_id, sender_user_id, amount, currency):
1. Fetch the bill, assert it is UNPAID.
2. Assert amount >= bill.total_amount.
3. Insert a row into remittance_transactions with status COMPLETED.
4. Call update_bill_status(bill_id, STATUS_PAID).
5. Return the transaction record.

This is intentionally simple and can be extended later for multi-step flows.

---

## 3. Database Design

### 3.1 bills Table (existing, minor addition)

The bills table is retained without structural changes.
One column is added: user_id INT NULL (FK -> users.id).
NULL is allowed for backward compatibility with the existing seed data.

### 3.2 users Table (new)

    id           INT AUTO_INCREMENT PRIMARY KEY
    username     VARCHAR(100) UNIQUE NOT NULL
    password_hash VARCHAR(255) NOT NULL
    role         VARCHAR(20) NOT NULL
    created_at   DATETIME DEFAULT CURRENT_TIMESTAMP

Roles are enforced at the application layer, not via separate database tables.
This keeps the schema simple.

### 3.3 remittance_transactions Table (new)

    transaction_id      INT AUTO_INCREMENT PRIMARY KEY
    bill_id             INT NOT NULL (FK -> bills.id)
    sender_user_id      INT NOT NULL (FK -> users.id)
    beneficiary_user_id INT NOT NULL (FK -> users.id)
    amount              DECIMAL(10,2) NOT NULL
    currency            VARCHAR(20) DEFAULT 'USDT'
    transaction_status  VARCHAR(20) NOT NULL
    payment_method      VARCHAR(50) DEFAULT 'stablecoin'
    created_at          DATETIME DEFAULT CURRENT_TIMESTAMP

---

## 4. Frontend Architecture

### 4.1 Dual Panel Structure

Two completely independent static frontend panels.
Each is served by a separate Python http.server process on a different port.

    receiver_panel  --> port 3000  (beneficiary / family member)
    sender_panel    --> port 3001  (remitter / sender abroad)

Why separate directories rather than one SPA with role-based routing:
- Simulates real-world multi-user access during demo.
- Each panel loads only the HTML, CSS, and JS it needs.
- No shared state between panels (they are genuinely different browser sessions).
- Simpler to demo: open two browser windows, each on a different port.

### 4.2 Multi-Page Application (MPA) Structure

Each panel has distinct HTML pages. Each page loads only the JavaScript it needs.
No SPA routing. No hidden div toggling. Real browser navigation via anchor tags.

Receiver panel pages:
    login.html      loads: auth.js
    register.html   loads: auth.js
    dashboard.html  loads: dashboard.js
    bills.html      loads: bills.js
    create.html     loads: create.js
    history.html    loads: history.js

This directly solves the current problem of dashboard.js importing 9 modules and
wiring 15 event listeners for sections that may not even exist on the current view.

### 4.3 config.js — Per-Panel Configuration

Each panel has its own config.js that exports:

    export const API_BASE_URL = "http://127.0.0.1:8000";
    export const PANEL_PORT = 3000;

All other JS files import API_BASE_URL from config.js.
This eliminates the hardcoded string "http://127.0.0.1:8000" in core/api.js.

### 4.4 auth_guard.js — Route Protection

Every protected page entry JS file starts with:

    import { guardRoute } from '../core/auth_guard.js';
    guardRoute();

guardRoute() reads the JWT from localStorage. If absent or expired,
it immediately redirects to login.html. No page content loads for unauthenticated users.

### 4.5 core/api.js — Authorization Header Injection

All API calls inject the Authorization header automatically:

    async function requestJson(path, options = {}) {
        const token = localStorage.getItem('token');
        const headers = { ...options.headers };
        if (token) headers['Authorization'] = `Bearer ${token}`;
        const response = await fetch(`${API_BASE_URL}${path}`, { ...options, headers });
        ...
    }

No individual feature file manually appends auth headers. One place, one responsibility.

### 4.6 Preserved Visual Identity

The CSS files are migrated unchanged from frontend/css/ into each panel's css/ directory.
No visual changes. The existing color palette, typography, calendar glows, table styles,
modal animations, and layout grid are all preserved exactly.

The only structural HTML changes are:
- Login page: form action changed from "dashboard.html" to calling auth.js submit handler.
- Dashboard: create modal HTML removed (moved to create.html as a dedicated page).
- Bills list: now its own page, not a dashboard section.

### 4.7 Frontend Responsibility Boundaries

What stays in the frontend (unchanged from current approach):
- Calendar rendering (calendar.js) -- pure client-side UI, correct to keep frontend.
- Recurring bill projections (utils.js) -- visual-only projections, correct to keep frontend.
- Selection state (state.js) -- transient UI state, correct to keep frontend.
- Modal open/close behavior (modal.js) -- pure UI, correct to keep frontend.

What moves to the backend (new):
- Bill filtering by month: GET /bills?month=YYYY-MM
- Bill sorting: GET /bills?sort=due_date_asc
- Aggregations for history totals: SQL SUM() in remittance service
- Role-based access enforcement: FastAPI dependencies on routes
- Validation: paid bill deletion prevention moved to mark_bill_status service

---

## 5. Test Architecture

### 5.1 Three-Layer Structure

    test_db/       -- tests the database context manager in isolation
    test_services/ -- tests service functions with mocked query calls
    test_api/      -- tests route handlers with mocked service calls (TestClient)

Each layer mocks the layer below it. No test in test_api/ touches the database.
No test in test_services/ starts an HTTP server.

### 5.2 Naming Convention

Test files mirror the source files they test:
    bill_service.py  -->  test_bill_service.py
    auth_routes.py   -->  test_auth_routes.py

Test function names follow the pattern:
    test_<function_name>_<scenario>
    Example: test_create_bill_missing_name, test_login_wrong_password

### 5.3 Existing Test Coverage Preserved

All existing test cases from test_api_server.py and test_services_no_api.py
are migrated without modification into the new test structure.
No coverage is dropped. New tests are added for auth and remittance.

---

## 6. Configuration and Environment

### 6.1 .env Additions

    RECEIVER_PANEL_PORT=3000
    SENDER_PANEL_PORT=3001
    JWT_SECRET_KEY=<random 32-char string>
    JWT_ALGORITHM=HS256
    JWT_EXPIRE_MINUTES=480

### 6.2 Makefile Additions

    start-receiver:
        cd frontend/receiver_panel && python -m http.server 3000

    start-sender:
        cd frontend/sender_panel && python -m http.server 3001

    start-all:
        Runs backend, receiver panel, and sender panel concurrently.

    run-tests:
        cd project root && pytest tests/ -v

The venv path is corrected from the hardcoded external path
(../Assigments/remitpy3-10/bin/activate) to a project-local .venv/bin/activate.

---

## 7. Naming Conventions

### Python

- Module names: lowercase_with_underscores (bill_service.py, auth_routes.py)
- Function names: lowercase_with_underscores (create_bill, mark_bill_status)
- Class names: PascalCase (BillCreateRequest, AuthenticationError)
- Constants: UPPERCASE_WITH_UNDERSCORES (STATUS_PAID, ROLE_SENDER)
- Private helpers: leading underscore (_format_bill_row)
- Exception names: descriptive PascalCase ending in Error (BillNotFoundError)

### JavaScript

- File names: camelCase for entry points (dashboard.js, billCreation.js)
- Function names: camelCase verbs (fetchAndRenderBills, handleCreateBillSubmit)
- Exported namespaces: PascalCase alias (import * as BillService from ...)
- Constants: SCREAMING_SNAKE_CASE (API_BASE_URL, PANEL_PORT)
- DOM element variables: suffix El (billsContainerEl, calendarGridEl)
- State object keys: camelCase (selectedBill, currentMonth, currentUser)

### SQL

- Table names: lowercase_with_underscores (bills, users, remittance_transactions)
- Column names: lowercase_with_underscores (due_date, transaction_status, created_at)
- Flag columns: Is_PascalCase retained for backward compat (Is_deleted, Is_expired)

---

## 8. What is Intentionally Not Done

- No message queue or async task system (not needed at this scale).
- No Redis session store (JWT is stateless, sufficient for demo).
- No Docker (out of scope for this refactor phase).
- No frontend build step / bundler (vanilla JS is correct for this project).
- No blockchain / Web3 library (stablecoin is represented as a DB field only).
- No frontend-side role enforcement only (role is always re-checked on each API call).
- No complex frontend routing library (real browser navigation is simpler and correct).
- No ORM (raw SQL with parameterized queries is explicit, readable, and educational).

---
