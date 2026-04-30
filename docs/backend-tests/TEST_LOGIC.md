# Core Test Logic and Assertions

This document details the specific logical flows and assertion patterns used
to validate the backend's functionality across the three testing layers.

---

## 1. Raw SQL Query Tests (`test_raw_sql_queries.py`)

These tests validate the foundational database interactions.

### `test_select_all_returns_list`
Executes `select_all()` and uses `isinstance(rows, list)` to verify the driver
returns a standard Python list, ensuring downstream service logic won't fail
with unexpected iterator objects.

### `test_insert_bill`
Calls a utility function `_create_test_bill(category="insert")` which wraps the
`insert_bill` query. It asserts that the returned primary key is of type `int`.
This implicitly verifies that the `LAST_INSERT_ID()` logic in the connection
adapter is working correctly.

### `test_select_num_day_dues`
Creates a test bill due in 1 day. Executes `select_num_day_dues(3)`.
It uses a generator expression inside an `any()` function to scan the returned list
of tuples: `any(r[0] == bill_id for r in select_num_day_dues(3))`.
This verifies the SQL `DATE_ADD` logic correctly caught the bill within the window.

### `test_update_bill_status`
The most complex SQL test. It verifies state mutation.
1. Creates an UNPAID bill due tomorrow.
2. Asserts it appears in the `select_num_day_dues(3)` results.
3. Executes `update_bill_status(bill_id, "PAID")`.
4. Fetches the bill directly and asserts `row[5] == "PAID"`.
5. Re-executes `select_num_day_dues(3)` and asserts the bill is NO LONGER present.
This proves that the upcoming bills query correctly filters out PAID bills.

### `test_delete_bill_by_id`
Tests the soft deletion logic.
1. Creates a test bill.
2. Executes `delete_bill_by_id(bill_id)` (which sets `Is_deleted = 'Y'`).
3. Executes `select_all()` and asserts the bill is absent.
This proves that the global `Is_deleted = 'N'` filter applied to all queries is working.

---

## 2. Service Layer Tests (`test_services_no_api.py`)

These tests validate the business logic transformations using `unittest.mock.patch`
to isolate the logic from the database.

### `test_list_bills_service_upcoming_boundary_days_3`
This test verifies the precision of the upcoming bills window calculation.
It mocks `select_num_day_dues` to return a static list of two bills (due in 2
and 3 days). It then calls `list_bills_service(upcoming_only=True, days=3)`
and asserts that the service correctly processes and formats both bills into
its final JSON-serializable dictionary output.

### `test_mark_bill_status_service`
Verifies the complex multi-step state mutation, including the side-effect of
generating a new bill when a recurring bill is paid.
1. It patches `select_bill_by_id`, `update_bill_status`, and `insert_bill`.
2. It sets up `select_bill_by_id` to return a `WEEKLY` recurring bill.
3. It calls `mark_bill_status_service(1, "PAID")`.
4. It asserts `mock_update.assert_called_with(1, "PAID")` to ensure the original
   bill's status was updated.
5. It asserts `mock_insert_bill.assert_called_once()` to verify the system
   correctly identified the `WEEKLY` interval and triggered the generation
   of the next cycle's bill.

---

## 3. API Integration Tests (`test_api_server.py`)

These tests validate the HTTP transport layer and routing using FastAPI's `TestClient`.

### TestClient Usage
Rather than starting a live Uvicorn server and using `requests`, these tests
instantiate `TestClient(app)`. This allows the tests to send simulated HTTP
requests directly to the FastAPI router synchronously, bypassing the network
stack entirely.

### Payload Serialization: `test_create_bill`
Verifies the `POST` request parsing and Pydantic model validation.
1. It patches the underlying `create_bill_service`.
2. It constructs a raw JSON dictionary payload containing the bill details.
3. It executes `client.post("/bills/new", json=payload)`.
4. It asserts the response `status_code == 200`, proving FastAPI successfully
   validated the payload against the Pydantic schema without raising a 422
   Unprocessable Entity error.
5. It asserts `mock_create_service.assert_called_once()`, proving the router
   successfully handed off execution to the service layer.

### Search Route Validation: `test_api_search_bills`
Verifies the GET request with URL query parameters.
1. It patches `select_by_name_service` to return a static dictionary.
2. It sends a GET request to `/bills/search?name=pytest-api`.
3. It asserts the response `status_code == 200`.
4. It asserts `mock_search_service.assert_called_with("pytest-api")`, proving
   FastAPI correctly extracted the `name` parameter from the URL query string
   and passed it to the underlying search service.
