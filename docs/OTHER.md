# Root Configuration and Orchestration

This document details the configuration files and orchestration elements located in
the project's root directory. These files act as the glue binding the discrete
sub-systems (Frontend, Backend, Database, Scripts, and Tests) into a unified application.

---

## 1. Global Environment Configuration (`.env`)

The `.env` file at the root of the project acts as the primary configuration registry
for the backend server. It ensures that sensitive credentials and environment-specific
routing variables are not hardcoded into the source code.

### Database Connection Parameters
    DB_HOST=localhost
    DB_USER=root
    DB_PASSWORD=root
    DB_NAME=family_supp_sche
    DB_TABLE='bills'
    DB_CONN_POOLING=5

- **Cross-system impact**: These variables are consumed exclusively by the Python
  backend via `backend/app/db/connection.py`.
- **Pooling**: `DB_CONN_POOLING=5` instructs the MySQL connection adapter to maintain
  5 persistent connections in memory. This is critical for the FastAPI backend,
  allowing it to serve parallel HTTP requests concurrently without the latency of
  establishing a new TCP connection to MySQL for every query.
- **Table Name Isolation**: Defining `DB_TABLE='bills'` as an environment variable
  is a defensive programming strategy. It allows developers to swap out the active
  table (e.g., to a `bills_archive` or `bills_test` table) without altering a
  single line of SQL in `queries.py`.

### API and Frontend Routing Parameters
    API_BASE_URL="http://127.0.0.1:8000"
    FE_URL="http://127.0.0.1:8080"
    FE_LOCAL_URL="http://localhost:8080"

- **API_BASE_URL**: Used by the backend tests (`tests/test_api_server.py`) to
  determine where the uvicorn server is listening. The Bash automation scripts
  also resolve and source this root `.env` file to ensure a single source
  of truth, eliminating redundancy and preventing out-of-sync configurations.
- **CORS Allow-listing**: The frontend URLs (`FE_URL`, `FE_LOCAL_URL`) are read by
  the backend's `main.py` to configure CORS (Cross-Origin Resource Sharing) middleware.
  This prevents malicious external websites from making cross-origin AJAX requests
  to the backend while explicitly authorizing the legitimate frontend domain.

---

## 2. Process Orchestration (`Makefile`)

The `Makefile` serves as the developer's execution hub. It abstracts away the
complexity of activating Python virtual environments and launching multi-threaded
servers into simple, memorable commands.

### Backend Startup (`make start-backend`)
    bash -c "source ../Assigments/remitpy3-10/bin/activate && cd backend && uvicorn app.main:app --reload"

- **Virtual Environment**: It assumes the existence of a virtual environment located
  at `../Assigments/remitpy3-10/`. This external dependency path implies that this
  project is part of a larger organizational structure on the host machine.
- **Live Reload**: Uses uvicorn's `--reload` flag, instructing the ASGI server to watch
  the `backend/` directory for filesystem changes and automatically restart the server
  when Python files are modified. This drastically accelerates the development loop.

### Frontend Startup (`make start-frontend`)
    bash -c "source ../Assigments/remitpy3-10/bin/activate && cd frontend && python -m http.server 8080"

- **Static Serving**: The frontend is a vanilla JS application requiring no build step
  (no Webpack, no Vite). Therefore, it uses Python's built-in, lightweight HTTP
  server module to serve the static HTML/CSS/JS files over port 8080.
- **Port Offset**: By serving the frontend on 8080 and the backend on 8000, the two
  sub-systems avoid port conflicts while running concurrently on the same host.

### Database Console (`make start-database`)
    bash -c "sudo mysql -u root -p"

- Provides a quick shortcut into the MySQL interactive terminal for debugging or
  manual inspection of the `family_supp_sche` schema.

---

## 3. Dependency Management (`requirements.txt`)

The `requirements.txt` file is exceptionally lean, declaring only six direct dependencies.
This minimalistic approach significantly reduces the application's attack surface and
simplifies deployment.

- `fastapi` & `uvicorn`: The core HTTP framework and ASGI web server.
- `mysql-connector-python`: The official Oracle driver for communicating with the database.
- `python-dotenv`: Parses the `.env` file and injects it into `os.environ`.
- `pytest` & `requests`: The testing framework and synchronous HTTP client, utilized
  by the suite in the `tests/` directory.

Because the frontend is pure vanilla JavaScript and CSS, there is no `package.json`
or `node_modules` directory in this project. All dependencies are strictly Python-based.

---

## 4. Source Control Configuration (`.gitignore`)

The `.gitignore` file enforces repository hygiene, ensuring that ephemeral, sensitive,
and environment-specific artifacts are not committed to Git.

### Python Artifacts
    __pycache__/
    *.py[cod]
    *$py.class
    .pytest*

Prevents the repository from being polluted by Python's compiled bytecode (`.pyc`)
and pytest's test-run metadata caches. This ensures that every clone of the repository
starts with a clean execution state.

### Security and Secrets
    **/.env

The most critical security directive in the project. The `**/` syntax ensures that
the root `.env` file and any potentially nested configuration files are ignored.
This guarantees that database passwords and internal routing IPs never leak into
the version control history.

### Documentation Artifacts
    *.pdf
    dev-docs/
    docs/

Ignores the generated documentation directories and PDF design specs. This suggests
a workflow where documentation is treated as build artifacts or localized developer
notes, rather than source truth that must be synchronized across the team via git.
