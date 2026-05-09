# Variables & Functions (Automation)

The automation layer utilizes Python standard libraries to handle tasks outside the API scope.

## Automation Functions

### `scripts/cron_simulate.py`
- **`simulate_daily_cron()`**:
  A procedural function that establishes a database cursor and runs:
  ```sql
  UPDATE bills 
  SET is_expired = 'Y' 
  WHERE due_date < CURDATE() 
    AND bill_status = 'UNPAID' 
    AND is_deleted = 'N'
  ```
  It prints an operational summary to the console detailing how many rows were updated. It is designed to be executable repeatedly via `make cron-simulate` without adverse effects.

### `scripts/start_frontend.py`
- **`CORSRequestHandler`**:
  A class inheriting from `http.server.SimpleHTTPRequestHandler`. Overrides the `end_headers()` method to inject cross-origin headers, preventing restrictive browser behavior during MPA local development.

## Testing Interfaces

### `tests/conftest.py` (Implicit)
- **`TestClient`**: 
  Imported via `fastapi.testclient`. Wraps the FastAPI `app` to permit mock HTTP requests natively in Python (e.g., `client.post("/auth/login", json=...)`).

### `unittest.mock` usage
- **`@patch("backend.app.db.queries.bill_select.select_bill_by_id")`**:
  A critical decorator pattern used across the suite to intercept database interactions. It swaps out actual row fetches with predefined Python dictionaries, isolating the service logic tests (like the recurring date calculation) from database integrity constraints.
