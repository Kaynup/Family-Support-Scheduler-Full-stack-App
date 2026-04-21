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

## Run Commands

### Start backend server

```bash
cd backend && uvicorn app.main:app --reload
```

### Run all tests from project root

```bash
cd .. && PYTHONPATH=. pytest -v
```

### 

---

## Other in-built
- `any()`
    - Checks if at least one item in an iterable is truthy.
    - Returns True if it finds one truthy value, otherwise False

- `next()`
    - Returns the next item from an iterator