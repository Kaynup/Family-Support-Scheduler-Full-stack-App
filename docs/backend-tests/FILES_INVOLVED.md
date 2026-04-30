# Files Involved in the Backend Tests Sub-system

This document provides a detailed breakdown of every file located within the
project's root `tests/` directory, detailing its purpose, imported dependencies,
and specific execution patterns.

---

## 1. Test Modules

### `tests/test_raw_sql_queries.py`

Validates the lowest-level database access object (DAO) logic.
- **Lines**: 88
- **Purpose**: To guarantee that raw SQL statements are syntactically correct,
  that MySQL parameters are properly bound, and that basic CRUD logic works
  without relying on higher-level service abstractions.
- **Key Imports**:
  - `backend.app.db.queries`: Imports every CRUD function (`insert_bill`,
    `select_all`, `select_bill_by_id`, `update_bill_status`, etc.) directly.
  - `datetime.date`, `datetime.timedelta`: Used to generate dates relative
    to today for testing the "upcoming bills" logic.
  - `time`: Used for generating unique identifiers.
- **Helper Functions**:
  - `_create_test_bill(category="test")`: A private utility function that calls
    `insert_bill` with a unique name prefix (`pytest-sql-{timestamp}`) and
    returns the integer primary key.
- **Execution Context**: Runs locally via `pytest`. Requires a running MySQL
  database with the correct schema loaded, as defined by the backend `.env` file.
  Does NOT require the FastAPI server to be running.

### `tests/test_services_no_api.py`

Validates the business logic layer and data transformation rules using mocks.
- **Lines**: ~60
- **Purpose**: To test complex temporal calculations, boundary conditions, and
  side-effect automation (like recurring bill generation) in isolation from both
  the HTTP routing layer and the physical database.
- **Key Imports**:
  - `backend.app.services.*`: Imports the service wrapper functions
    (`create_bill_service`, `list_bills_service`, `mark_bill_status_service`, etc.).
  - `unittest.mock.patch`: Used to aggressively mock the underlying database
    query functions.
- **Execution Context**: Runs locally via `pytest`. Does NOT require a running
  MySQL database or a FastAPI server.

### `tests/test_api_server.py`

Validates the complete routing and validation layer via simulated HTTP requests.
- **Lines**: ~40
- **Purpose**: To guarantee that the FastAPI router correctly parses incoming JSON
  payloads, routes them to the correct service, and serializes the response back
  into valid JSON with the correct HTTP status codes, all without invoking real
  business logic.
- **Key Imports**:
  - `fastapi.testclient.TestClient`: Used to simulate HTTP requests against the
    FastAPI app without binding to a physical network port.
  - `unittest.mock.patch`: Used to mock the `backend.app.services` layer.
- **Execution Context**: Runs locally via `pytest`. Does NOT require a running
  MySQL database or a running FastAPI uvicorn server.

---

## 2. Directory Structure and Execution

While the project structure has evolved, the testing suite is centralized.
The framework expects the tests to be located at the project root level, allowing
the Python imports to resolve the `backend.app` namespace correctly.

    InternshipProject/
    ├── backend/
    │   └── app/
    │       ├── db/
    │       ├── routes/
    │       └── services/
    ├── tests/
    │   ├── __init__.py (implicit or explicit)
    │   ├── test_api_server.py
    │   ├── test_raw_sql_queries.py
    │   └── test_services_no_api.py
    └── requirements.txt

The `pytest` command is executed from the `InternshipProject/` root directory.
It uses auto-discovery to find any python files prefixed with `test_` inside any
directories matching `tests/` or `test/`.

Because the test files directly import the backend application code
(e.g., `from backend.app.db.queries import ...`), the root directory must be
explicitly added to the Python module search path. To ensure these absolute
imports resolve cleanly, tests should be executed with the `PYTHONPATH`
variable set to the current directory (`.`), and typically with the `-v` (verbose)
or `-s` (disable stdout capture) flags for better visibility:

    PYTHONPATH=. pytest -v
    # or
    PYTHONPATH=. pytest -s -v
