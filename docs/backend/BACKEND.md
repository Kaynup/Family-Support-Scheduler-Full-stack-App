# Backend Sub-system

## Framework

Python 3.10.20 with FastAPI v0.135.3.
ASGI server is Uvicorn, launched through the project Makefile.
The backend runs on the default Uvicorn port (8000) and is accessed
by the frontend at http://127.0.0.1:8000.

## Architecture

The backend follows a layered service architecture with strict separation of concerns.
The layers, from outermost to innermost, are:

    1. Routes (HTTP interface)
    2. Schemas (request validation)
    3. Services (business logic)
    4. Database queries (persistence)

Each layer only communicates with the layer directly below it.
Routes never touch queries directly. Services never parse HTTP requests.
This constraint makes the system testable and extensible without cross-contamination.

## Package Structure

The backend is a single Python package rooted at `backend/app/`.
It uses relative imports throughout, so it must be launched as a module
via Uvicorn (`uvicorn app.main:app`) from within the `backend/` directory.
The Makefile handles this automatically.

The package contains four sub-packages:

    backend/app/
        main.py           -- Application factory and middleware
        schemas.py        -- Pydantic models for request validation
        __init__.py       -- Empty, marks as package
        routes/           -- HTTP endpoint definitions
        services/         -- Business logic layer
        db/               -- Connection pooling and raw SQL

## CORS Policy

The application explicitly restricts cross-origin requests to two origins:

    http://localhost:8080
    http://127.0.0.1:8080

These correspond to the frontend development server (Python http.server on port 8080).
All HTTP methods and headers are allowed for these origins.
Credentials are permitted to support future cookie-based authentication.

No wildcard origins are used. This means the API cannot be consumed by
any arbitrary browser client -- only by the designated frontend.

## Server Lifecycle

The startup sequence is:

    1. Makefile activates the Python virtual environment.
    2. Uvicorn imports `app.main:app`.
    3. Module-level code in `connection.py` initializes the MySQL connection pool.
    4. Module-level code in `queries.py` reads the table name from environment.
    5. FastAPI registers the bill router with the `/bills` prefix.
    6. The health check endpoint becomes available at GET `/health`.
    7. The server begins accepting requests on port 8000.

Hot reload is enabled via the `--reload` flag, so code changes in the
backend directory are picked up automatically without restarting the server.

## Manual Execution

While the Makefile is the preferred way to launch the backend, it can be started
manually from the project root by following these steps:

1.  **Activate Environment**: Source the virtual environment (located in the 
    neighboring `Assigments` directory).
    ```bash
    source ../Assigments/remitpy3-10/bin/activate
    ```
2.  **Launch Server**: Run Uvicorn from within the `backend` directory.
    ```bash
    cd backend && uvicorn app.main:app --reload
    ```

Note: The virtual environment directory is intentionally named `Assigments` 
(without the 'n') to match the local filesystem structure.

## Dependencies

The backend depends on six packages, declared in `requirements.txt`:

    requests                -- HTTP client (used for testing)
    uvicorn                 -- ASGI server
    fastapi                 -- Web framework
    python-dotenv           -- Environment variable loading
    mysql-connector-python  -- MySQL driver with connection pooling
    pytest                  -- Test framework

All dependencies are installed into a dedicated virtual environment
located outside the project tree (`../Assigments/remitpy3-10/`).

## Environment Variables

The backend reads the following variables from `.env`:

    DB_HOST       -- MySQL server hostname (typically localhost)
    DB_USER       -- MySQL username
    DB_PASSWORD   -- MySQL password
    DB_NAME       -- Database name (family_supp_sche)
    DB_TABLE      -- Table name (bills)
    DB_CONN_POOLING -- Connection pool size (integer)
