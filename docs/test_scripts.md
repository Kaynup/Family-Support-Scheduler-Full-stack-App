# Testing Scripts

Scripts to check functionality of modules

## Dependencies

```bash
pip install pytest requests
```

---

## Test Files

## `tests/test_raw_sql_queries.py`
Raw SQL integration tests for `backend/app/db/queries.py`

Functions:
- test_insert_bill : creates a test bill, fetches the id by name and asserts if 'int'
- test_select_all : returns all bills
- test_select_num_day_dues : returns all bills with number of days left for due, less than given number of days
- test_update_bill_status :
    - creates a test bill
    - fetches id by name
    - asserts if bill is unpaid
    - asserts status change
    - asserts if bill is in paid status or not
- test_delete_bill_by_id :
    - creates a test bill
    - fetches id by name
    - deletes bill by id
    - asserts bill is deleted

Utils:
- _get_bill_id_by_name : fetches the id of the bill by its name
- _create_test_bill : generate a test bill tuple

Test approach:
- Create temporary test rows
- Assert function output / DB state changes
- Clean up inserted rows

---

## `tests/test_api_server.py`
Backend health integration test for `backend/app/main.py`

Covers:
- GET /health endpoint

Constraint:
- Backend server must be running before this test executes

Expected response:
- Status code: 200
- JSON body: {"message": "backend is live"}

---

## `tests/test_services_no_api.py`

Service functions tests for `backend/app/services/`

Functions:
- test_create_bill_service : creates a test bill, get name by bill id, assert if valid, delete it afterwards
- test_list_bills_service : fetches list of bills, asserts the returned values
- test_mark_bill_status_service : creates a test bill, get name by id, change the status to PAID, asserts the data and the existence in UNPAID due bills bby 3 days
- test_delete_bill_service : creates a test bill, get name by id, delete bill by id, asserts data and validates if bill is in database


- **When scaling up the appilication in future, the assertions will split and harden service logic, raw SQL layer, and DB operations, so that python-side full-data validation can be avoided**

---

## Run Commands

### Start backend server

```bash
cd backend && uvicorn app.main:app --reload
```

### Run all tests from project root

```bash
PYTHONPATH=. pytest -v
```

### Run all tests from root with verbose

```bash
PYTHONPATH=. pytest -s -v
```

---

## Other in-built
- `any()`
    - Checks if at least one item in an iterable is truthy.
    - Returns True if it finds one truthy value, otherwise False

- `next()`
    - Returns the next item from an iterator