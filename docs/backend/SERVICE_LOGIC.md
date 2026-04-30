# Service Layer and Business Logic

This document covers every service module in the backend, the business rules
they enforce, and the design decisions behind the service architecture.

---

## Architecture Overview

The service layer sits between the HTTP routes and the database queries.
Its purpose is to contain all business logic so that:

- Routes remain thin (parse request, call service, return response).
- Database queries remain pure (execute SQL, return rows).
- Business rules are testable in isolation.

Every service function follows the same contract:

    Input:  Primitive Python types (strings, ints, dates).
    Output: A dictionary with "OK", "message", and "data" keys.
    Errors: Raise ValueError with a human-readable message.

The route layer catches ValueError and translates it into HTTP status codes.
The service layer never imports FastAPI -- it is framework-agnostic.

---

## Service Registry

The services `__init__.py` file exports four public functions:

    create_bill_service
    list_bills_service
    mark_bill_status_service
    delete_bill_service

A fifth service, `select_by_name_service`, exists in `bill_search.py`
but is imported directly by the routes module rather than through
the registry. This is a minor inconsistency in the codebase.

---

## 1. Bill Creation Service (`bill_creation.py`)

### Responsibility

Accepts validated bill parameters and persists a new record.

### Behavior

- If `creation_date` is not provided, it defaults to today.
- The `due_date` string is converted from ISO format to a Python date object.
- The function delegates the actual INSERT to `queries.insert_bill()`.
- On success, it returns the new bill's ID and all input fields.

### Default Handling

The creation_date default is applied at the service level, not the database level.
This is intentional -- the database schema requires creation_date to be NOT NULL,
so the service must always provide a value. By defaulting to `date.today()` here,
the schema validation layer (which runs before the service) does not need to
know about this default. It can treat creation_date as truly optional.

### Error Wrapping

If the database INSERT fails (e.g., due to a constraint violation on due_date),
the MySQL connector raises `mysql.connector.Error`. The service catches this
and re-raises it as `ValueError` so the route layer can map it to HTTP 400.

### Response Format

    {
        "OK": true,
        "message": "bill created successfully on <date>",
        "data": {
            "id": <int>,
            "name": <string>,
            "due_date": <string>,
            "total_amount": <float>,
            "creation_date": <date>,
            "status": <string>,
            "category": <string or null>
        }
    }

The response does not include `recurring_interval`. This is a minor omission
that does not affect functionality since the frontend fetches the full bill
list after creation anyway.

---

## 2. Bill Listing Service (`bill_listing.py`)

### Responsibility

Retrieves and formats bill records based on filter criteria.

### Behavior

The function accepts three mutually exclusive filter modes:

    1. expired_only=True  -- Returns overdue bills.
    2. upcoming_only=True -- Returns bills due within N days.
    3. Neither            -- Returns all non-deleted bills.

If both `expired_only` and `upcoming_only` are true, `expired_only` takes
priority because it is checked first in the conditional chain. This is an
implicit design decision rather than an explicit validation.

### Tuple-to-Dict Conversion

The database returns raw tuples (rows from SELECT *). The service
converts these into dictionaries using `_format_tuple()`, which maps
positional indices to named keys:

    Index 0 -> id
    Index 1 -> name
    Index 2 -> creation_date (converted to string)
    Index 3 -> due_date (converted to string)
    Index 4 -> total_amount (converted to float)
    Index 5 -> status
    Index 6 -> category
    Index 7 -> recurring_interval (with fallback to "NONE")
    Index 8 -> is_expired (with fallback to "N")

The fallback values for indices 7 and 8 exist for backward compatibility.
If the database schema is ever rolled back to a version without those columns,
the service will still produce valid JSON instead of crashing on an IndexError.

### Date Serialization

Dates are serialized using `str()` which produces ISO 8601 format (YYYY-MM-DD).
This is consumed directly by the frontend's date comparison logic.
The `total_amount` field is explicitly cast to `float` because MySQL's
DECIMAL type maps to Python's `decimal.Decimal`, which is not JSON-serializable
by FastAPI's default encoder.

### Response Format

    {
        "OK": true,
        "total_count": <int>,
        "data": [ { ... }, { ... }, ... ]
    }

The `total_count` field is computed from the length of the result list,
not from a separate COUNT(*) query. This is acceptable for the current
data volume but would need to change for pagination support.

---

## 3. Bill Status Service (`bill_status.py`)

### Responsibility

Updates a bill's payment status and handles recurring bill generation.

This is the most complex service in the system. It has two jobs:
updating the status field, and creating the next bill in a recurring series.

### Behavior -- Status Update

    1. Fetch the bill by ID to verify it exists and to read its metadata.
    2. Execute the UPDATE query to change the status.
    3. If the update affects zero rows, raise ValueError.

### Behavior -- Recurring Bill Generation

After a successful status change to PAID, the service checks whether
the bill has a recurring interval:

    bill[7] -> recurring_interval (positional index from SELECT *)

If the interval is WEEKLY or MONTHLY (and not NONE or null), the service
calculates the next due date:

    WEEKLY:  current due_date + 7 days (timedelta)
    MONTHLY: current due_date + 30 days (timedelta)

Note: MONTHLY uses a flat 30-day offset, not calendar month arithmetic.
This means a bill due on January 31 will next be due on March 2, not
February 28. This is a known simplification. Calendar-accurate month
arithmetic would require the `dateutil.relativedelta` library.

The service then inserts a new bill with:
- The same name, amount, category, and recurring_interval.
- The same creation_date as the original.
- The calculated next due_date.
- Status set to UNPAID.

This creates a self-perpetuating chain: paying a MONTHLY bill on May 3
creates a new UNPAID bill due on June 2, and paying that one creates
one for July 2, and so on.

### Positional Index Dependency

The service accesses bill fields by tuple index (bill[1], bill[3], bill[7], etc.)
rather than by column name. This creates a coupling between the service
and the column order defined in the database schema. If a column is added
or reordered in the schema, the indices in this service must be updated manually.

This is a known trade-off of using raw tuples instead of an ORM.
The system does not use SQLAlchemy or any object-relational mapper.

### Response Format

    {
        "OK": true,
        "message": "bill status updated successfully",
        "data": {
            "id": <int>
        }
    }

The response does not include the new recurring bill's ID if one was created.
The frontend compensates by refetching the full bill list after every status update.

---

## 4. Bill Deletion Service (`bill_deletion.py`)

### Responsibility

Soft-deletes a bill by delegating to the database layer.

### Behavior

The service calls `queries.delete_bill_by_id()`, which sets `Is_deleted = 'Y'`.
If the query affects zero rows (bill not found), a MySQL error is raised,
caught, and re-raised as ValueError.

The service does not check whether the bill is already deleted.
Attempting to delete an already-deleted bill will raise a "No bill found"
error because the query filters on `Is_deleted = 'N'`.

### Response Format

    {
        "OK": true,
        "message": "deleted row successfully",
        "data": {
            "id": <int>
        }
    }

---

## 5. Bill Search Service (`bill_search.py`)

### Responsibility

Performs case-insensitive substring matching on bill names.

### Behavior

The service passes the search term to `queries.select_by_name_match()`,
which executes a LIKE query with wildcards on both sides of the term.

Results include all matching bills regardless of status or deletion state.
This is a notable difference from the listing service, which filters out
deleted bills. The search service returns deleted bills if their name
matches the query. This could be considered a bug or a feature depending
on whether the user needs to find archived records.

### Tuple Format Divergence

The search service has its own `_format_tuple()` function that only maps
7 fields (id through category). It does not include `recurring_interval`
or `is_expired`. This means search results have a different shape than
listing results. The frontend currently handles this gracefully by
treating missing fields as undefined.

### Response Format

    {
        "OK": true,
        "total_count": <int>,
        "data": [ { ... }, { ... }, ... ]
    }

---

## Cross-Cutting Concerns

### Consistency of Response Shape

All services return a dictionary with at least "OK" and "data" keys.
Most include a "message" key for human-readable feedback.
The listing and search services include a "total_count" key.

This near-uniform shape simplifies frontend consumption. The frontend
can always check `response.OK` and iterate over `response.data`
regardless of which endpoint was called.

### Error Propagation

Every service catches `mysql.connector.Error` and converts it to `ValueError`.
This creates a clean boundary: the route layer never sees MySQL-specific
exceptions and does not need to import the MySQL connector.

### Transaction Safety

Write operations (insert, update, delete) use explicit commit/rollback
in the query layer. If the query fails, the transaction is rolled back
before the connection is returned to the pool. This prevents partial
writes from corrupting the database state.

Read operations do not use explicit transactions. MySQL's default
isolation level (REPEATABLE READ) ensures consistent reads within
a single query, which is sufficient for this application's workload.
