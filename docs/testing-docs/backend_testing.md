# Backend Testing

## Navigation

- Index: [../index.md](../index.md)
- API docs: [API endpoints](../backend-docs/api_endpoints.md)
- Services: [Bill Services](../backend-docs/bill_services.md)
- SQL: [SQL Queries](../backend-docs/sql_queries.md)


1. The query layer writes and reads the database as expected.
2. The service layer shapes data and applies application behavior.
3. The API layer accepts requests and returns correct HTTP responses.

## Test scripts

#### `tests/test_raw_sql_queries.py`

This file checks the query layer directly against the database.

> Test Functions:

- `test_select_all_returns_list()`
	- tests that select-all query returns a Python list.
- `test_insert_bill()`
	- tests `insert_bill()` returns the generated integer id.
- `test_select_num_day_dues()`
	- tests due-soon filtering includes a bill that belongs in the window.
- `test_update_bill_status()`
	- tests the status update reaches the database and changes the row.
- `test_delete_bill_by_id()`
	- tests delete removes the row and the row no longer appears in later reads.

> Helper function:

- `_create_test_bill()`
	- creates a temporary row using `insert_bill()` and returns the created id.
- every created row is deleted inside a `finally` block so the test does not leave the table dirty.


#### `tests/test_services_no_api.py`

This file checks business logic without HTTP.

> Test Functions:

- `test_create_bill_service()`
	- tests the service can create a bill.
- `test_list_bills_service()`
	- tests the list service returns a successful wrapper and a count.
- `test_mark_bill_status_service()`
	- tests the status-change service updates the row and returns the id.
- `test_delete_bill_service()`
	- tests the deletion service removes the row and returns the deleted id.
- `test_list_bills_service_upcoming_boundary_days_3()`
	- tests the upcoming-bills window includes the near-due bill and excludes the too-far bill.

> Helper function:

- `_create_test_bill_with_due_days(days_ahead=1)`
	- creates a test row using the service layer so the test starts from the services.
- all created ids are removed in cleanup code so the database returns to its prior state.

#### `tests/test_api_server.py`

This file checks the HTTP layer through real requests.

> Test Functions:

- `test_create_bill()`
	- tests the API can create a bill and the created row can later be found.
- `test_update_status()`
	- tests the PUT route accepts a status change and returns a successful JSON response.
- `test_delete_bill()`
	- tests the DELETE route removes the row and returns success.

> Help function:

- `_create_temp_bill_via_api()`
	- creates a bill through HTTP so the API path is exercised end to end.

## Data Safety Rules

- Tests create temporary rows with unique names.
- Deletion of test samples with the generated id.
- Essentially, tests are written to avoid leaving permanent rows in the bill table.

## Run Commands

```bash
PYTHONPATH=. pytest tests/test_raw_sql_queries.py 
```

```bash
PYTHONPATH=. pytest tests/test_services_no_api.py
```

```bash
PYTHONPATH=. pytest tests/test_api_server.py
```

```bash
PYTHONPATH=. pytest -v
```

```bash
PYTHONPATH=. pytest -s -v
```

---