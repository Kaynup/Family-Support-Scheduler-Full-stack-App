# Backend Testing

## Navigation

- Hub: [../index.md](../index.md)
- API docs: [../backend-docs/api_endpoints.md](../backend-docs/api_endpoints.md)
- Services: [../backend-docs/bill_services.md](../backend-docs/bill_services.md)
- SQL: [../backend-docs/sql_queries.md](../backend-docs/sql_queries.md)

## What The Test Suite Is Proving

The tests are not just checking if a function returns something. They are proving three different layers behave correctly:

1. The query layer writes and reads the database as expected.
2. The service layer shapes data and applies application behavior.
3. The API layer accepts requests and returns correct HTTP responses.

## Test Files In The Project

### `tests/test_raw_sql_queries.py`

This file checks the query layer directly against the database.

What each function proves:

- `test_select_all_returns_list()`
	- proves the select-all query returns a Python list.
- `test_insert_bill()`
	- proves `insert_bill()` returns the generated integer id.
- `test_select_num_day_dues()`
	- proves due-soon filtering includes a bill that belongs in the window.
- `test_update_bill_status()`
	- proves the status update reaches the database and changes the row.
- `test_delete_bill_by_id()`
	- proves delete removes the row and the row no longer appears in later reads.

Helper behavior:

- `_create_test_bill()`
	- creates a temporary row using `insert_bill()` and returns the created id.

Cleanup expectation:

- every created row is deleted inside a `finally` block so the test does not leave the table dirty.

### `tests/test_services_no_api.py`

This file checks business logic without HTTP.

What each function proves:

- `test_create_bill_service()`
	- proves the service can create a bill and the created name can be found in the database.
- `test_list_bills_service()`
	- proves the list service returns a successful wrapper and a count.
- `test_mark_bill_status_service()`
	- proves the status-change service updates the row and returns the id.
- `test_delete_bill_service()`
	- proves the deletion service removes the row and returns the deleted id.
- `test_list_bills_service_upcoming_boundary_days_3()`
	- proves the upcoming-bills window includes the near-due bill and excludes the too-far bill.

Helper behavior:

- `_create_test_bill_with_due_days(days_ahead=1)`
	- creates a test row using the service layer so the test starts from the business path, not from raw SQL.

Cleanup expectation:

- all created ids are removed in cleanup code so the database returns to its prior state.

### `tests/test_api_server.py`

This file checks the HTTP layer through real requests.

What each function proves:

- `test_create_bill()`
	- proves the API can create a bill and the created row can later be found.
- `test_update_status()`
	- proves the PUT route accepts a status change and returns a successful JSON response.
- `test_delete_bill()`
	- proves the DELETE route removes the row and returns success.

Helper behavior:

- `_create_temp_bill_via_api()`
	- creates a bill through HTTP so the API path is exercised end to end.

## Data Safety Rules

- Tests create temporary rows with unique names.
- Cleanup happens after each test.
- Deletion uses the generated id, not the display name, once the row has been created.
- The tests are written to avoid leaving permanent rows in the bill table.

## Run Commands

```bash
PYTHONPATH=. pytest -v
```

```bash
PYTHONPATH=. pytest -s -v
```

## How To Read Failures

- If raw SQL tests fail, inspect the query layer first.
- If service tests fail, inspect validation or formatting in the service layer.
- If API tests fail, inspect route parameter handling and HTTP error mapping.

## What These Tests Are Trying To Protect

- id generation and lookup behavior,
- due-soon filtering,
- status update correctness,
- deletion correctness,
- response shape stability,
- and cleanup discipline after every run.