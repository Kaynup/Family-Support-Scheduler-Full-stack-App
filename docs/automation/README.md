# Automation and Tooling Documentation

The project utilizes automated scripts and Makefiles to streamline startup, simulation, and testing.

## Makefile Commands
The root `Makefile` exposes the primary project commands:
- `make start-backend`: Runs the FastAPI server on port `8000` via Uvicorn with hot-reload enabled.
- `make start-frontend`: Runs a lightweight Python HTTP server on port `8003` out of the `frontend/` directory.
- `make run-tests`: Discovers and executes the Python `pytest` suite inside the `tests/` directory.
- `make cron-simulate`: Manually executes the chronological scheduled jobs simulation script.

## Expiration Automation (Cron)
A background script (`scripts/cron_simulate.py`) is used to simulate a daily chronological job. 
- It scans the database for `UNPAID` bills where the `due_date` has elapsed.
- It updates the database setting `is_expired = 'Y'`.
- In a production environment, this Python script would be registered as a standard Unix `cron` job running nightly at 00:00.

## Testing Architecture
The `tests/` directory contains unit and integration tests built with `pytest`:
- **API Tests**: Utilizes FastAPI's `TestClient` to mock HTTP requests against the router endpoints.
- **Service/Logic Tests**: Employs `unittest.mock` to heavily mock out database queries, ensuring business logic (such as auto-generation calculations and expiration logic) can be executed rapidly without a live database dependency.
