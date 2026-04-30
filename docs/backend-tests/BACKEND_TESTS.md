# Backend Tests Sub-system

## Environment and Technology

The backend testing suite is built using `pytest`, a robust and scalable
testing framework for Python. It is designed to automatically discover
and execute all test cases defined within the `tests/` directory.

The primary tools and libraries utilized within this environment are:
- `pytest`: The core test runner and assertion framework.
- `requests`: A synchronous HTTP client used exclusively in the API tests
  to send real HTTP requests to the running backend server.
- `python-dotenv`: Used to load the `API_BASE_URL` from the `.env` file,
  ensuring the API tests can dynamically target different server instances
  (e.g., local development vs. CI/CD environments).
- `datetime` and `time`: Built-in Python modules used extensively to
  generate dynamic dates and unique timestamps for test data.

The tests are fully integrated with the project's dependency management,
meaning running `pip install -r backend/requirements.txt` installs the
necessary testing tools alongside the production backend code.

## Architecture

The testing architecture follows a layered testing pyramid, focusing
on three distinct levels of the backend application:

1. **Database Layer Tests**: `test_raw_sql_queries.py`
   These tests directly import the raw SQL functions from `backend.app.db.queries`.
   They bypass the service and routing layers entirely, ensuring that the
   underlying SQL syntax, parameter binding, and connection pooling are functioning
   correctly.

2. **Service Layer Tests**: `test_services_no_api.py`
   These tests import the business logic functions from `backend.app.services`.
   They bypass the FastAPI routing and HTTP serialization layers. Crucially, they
   mock the underlying database queries (`backend.app.db.queries`) using `unittest.mock.patch`.
   This allows the tests to verify complex business rules (like recurring bill
   auto-generation) instantly without the overhead of network requests or real
   database connections.

3. **API Integration Tests**: `test_api_server.py`
   These are routing tests that use FastAPI's `TestClient` to send mock HTTP
   POST, GET, PUT, and DELETE requests directly to the application. They mock
   the underlying service layer (`backend.app.services`), allowing them to verify
   that the routing, Pydantic schema validation, and JSON serialization are
   all correctly wired together without invoking any database mutations.

## Test Data Lifecycle Management

Because the Service and API tests are entirely mocked, they never interact with
the physical database, completely eliminating the risk of database pollution and
integration bloat.

However, the Raw SQL queries (`test_raw_sql_queries.py`) still execute against
the active development database. To prevent these tests from leaving garbage data
behind (which would pollute the frontend calendar and automation scripts), they
employ a rigorous `try/finally` block structure.

Every SQL test creates its own unique data, performs its assertions within a `try`
block, and physically deletes the data in a `finally` block using a specialized
`delete_bill_by_id_HARD` function. This ensures that even if an assertion fails
and the test crashes, the test data is still purged from the database.

## Test Naming Conventions

The tests use highly specific naming conventions to ensure that test data
can be easily identified if a `finally` block were to somehow fail:
- API Tests use: `pytest-api-{timestamp}`
- Service Tests use: `pytest-serve-{days}-{timestamp}`
- SQL Tests use: `pytest-sql-{timestamp}`

This convention ensures uniqueness (preventing tests from interfering with
each other during parallel execution) and provides immediate traceability.
