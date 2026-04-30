# Testing Strategy and Methodologies

This document outlines the strategic approach taken to validate the
backend sub-system, focusing on how different layers of the application
are isolated and verified.

---

## 1. The Pyramid Approach

The testing suite relies on a three-tiered architecture. By separating tests
into discrete layers, the suite can pinpoint exactly where a failure occurs.

If `test_raw_sql_queries.py` passes but `test_api_server.py` fails, the developer
knows immediately that the database connection and SQL syntax are fine, and the
bug must exist in the Pydantic schemas or the FastAPI routing logic.

This isolation is achieved by avoiding "god tests" that try to test everything
at once.

### Layer 1: Data Access Object (DAO) Testing
The lowest level of tests (`test_raw_sql_queries.py`) interacts purely with Python
functions that execute SQL strings. These tests verify:
- Connection pooling acquisition and release.
- SQL syntax correctness (preventing `mysql.connector.errors.ProgrammingError`).
- Proper mapping of Python parameters (`%s`) to MySQL data types.
- Correct return structures (e.g., ensuring `select_all` returns a list of tuples,
  not a list of dicts or a raw cursor object).

### Layer 2: Business Logic Testing
The middle level (`test_services_no_api.py`) tests the core logic. These tests verify:
- Complex temporal calculations (e.g., ensuring the upcoming bills filter correctly
  includes a bill due in 2 days but excludes one due in 4 days).
- Multi-step operations (e.g., the recurring bill generation, which involves an
  UPDATE followed immediately by an INSERT).
- Tuple-to-Dict conversion formatting (ensuring the `_format_tuple` helper correctly
  maps the raw database array into a JSON-serializable dictionary).

### Layer 3: Contract and Integration Testing
The highest level (`test_api_server.py`) tests the HTTP boundary. These tests verify:
- HTTP Status Code correctness (e.g., ensuring the backend returns 200 OK, not 500
  Internal Server Error).
- Content-Type headers and JSON serialization.
- That the FastAPI server is actually bound to the correct port and processing requests.
- That the HTTP methods (POST, PUT, DELETE, GET) are correctly mapped to their handlers.

---

## 2. Mocking over Physical DB Operations

A unique aspect of this testing suite is its reliance on aggressive dependency
mocking for the Service and API layers, completely eliminating the risk of database
pollution and integration bloat.

Instead of performing physical `INSERT` and `DELETE` operations for every
HTTP test, the suite uses Python's `unittest.mock.patch` to intercept
database calls. This dual-strategy ensures:

1. **Instant Execution**: API tests run in milliseconds because they do not
   wait for TCP connections or disk I/O.
2. **Zero Pollution**: There is no risk of soft-deleted "test bills" filling up
   the database or accidentally appearing in the frontend calendar.
3. **Pure Routing Validation**: By mocking the service return values, the API
   tests purely validate the HTTP layer (Pydantic models, status codes, and
   JSON serialization) without re-testing the underlying business logic.

However, the lowest level (`test_raw_sql_queries.py`) still executes against
the active database. To prevent pollution here, the `finally` block of every SQL
test calls a specialized `delete_bill_by_id_HARD()` function. This completely
removes the row from the MySQL database engine, leaving no trace of the test's
execution.

---

## 3. Dynamic Test Data Generation

For the physical SQL tests, tests never rely on hardcoded IDs or assumed database
states. Because tests are often run in parallel or repeatedly on the same database,
relying on a specific bill existing would lead to flaky tests.

Instead, SQL tests generate their own ephemeral data using unique timestamps:

    unique_name = f"pytest-sql-{time.time_ns()}"

The `time.time_ns()` function generates a nanosecond-precision integer. By appending
this to the bill name, the tests ensure that two tests running at the exact same
millisecond will not collide.

---

## 4. Test State Independence

The testing suite strictly adheres to the principle of test isolation.
No test depends on the outcome or residual state of another test.

For example, `test_update_status` does not assume that `test_create_bill` has
already run. Instead, `test_update_status` explicitly mocks the state it needs
to perform the update assertion independently.

This independence allows developers to run specific tests in isolation
(e.g., `pytest tests/test_api_server.py::test_update_status`) without needing
to run the entire suite in a specific sequence.
