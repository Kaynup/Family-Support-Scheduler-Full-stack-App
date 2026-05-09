# Relatable Files (Automation & Testing)

This directory documents the CI/CD and automation tooling designed to keep the project tested and accurately synced with time.

## 1. Automation Scripts
- **`Makefile`**: The central task runner. Masks complex Python shell executions behind simple commands like `make run-tests`.
- **`scripts/cron_simulate.py`**: A standalone Python script connecting directly to the MySQL database. It acts outside the FastAPI boundary to run time-based background updates.
- **`scripts/start_frontend.py`**: A custom implementation of Python's `http.server`. Automatically serves the `frontend/` directory with `Access-Control-Allow-Origin: *` headers for isolated local testing.

## 2. Test Architecture
The test suite utilizes `pytest` and is grouped by domain:
- **`tests/test_api/`**: 
  - `test_auth_routes.py`: Validates `/auth/register` and `/auth/login` token generation.
  - `test_bill_routes.py`: Tests `GET`, `POST`, and `DELETE` endpoints.
  - `test_remittance_routes.py`: Validates role restrictions (e.g., ensuring a beneficiary gets a `403` trying to pay a bill).
- **`tests/test_services/`**:
  - `test_remittance_service.py`: Directly invokes the `pay_bill_via_remittance` function, heavily utilizing `unittest.mock.patch` to verify the auto-generation workflow without hitting the database.
- **`tests/test_db/`**:
  - `test_connection.py`: Verifies the context manager safely handles commits and rollbacks during query executions.
