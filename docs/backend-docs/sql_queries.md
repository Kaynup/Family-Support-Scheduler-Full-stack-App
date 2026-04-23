# SQL Queries

## Navigation

- Hub: [../index.md](../index.md)
- Services: [bill_services.md](bill_services.md)
- API: [api_endpoints.md](api_endpoints.md)
- Errors: [error_handling.md](error_handling.md)

## Query Layer Intent

This module is the only place that should know SQL syntax and transaction mechanics. It is intentionally lower-level than the service layer and does not format responses for HTTP clients.

## Connection Behavior

- `get_connection()` comes from `backend/app/db/connection.py`.
- Every query function opens a connection and cursor, runs exactly one operation, then closes both in `finally`.
- The pool is created once in the connection module and reused.

## Function Notes

### `insert_bill(name, due_date, total_amount, creation_date, status='UNPAID', category=None)`

What it does:

- Inserts one row into the bill table.
- Uses the provided `creation_date`, `due_date`, amount, status, and category.
- Returns `lastrowid` so the caller gets the id created by MySQL.

Why it matters:

- The application treats the auto-generated id as the authoritative bill identity.

Transaction behavior:

- Commit on success.
- Roll back on connector error.

### `select_all()`

What it does:

- Reads every row from the table.
- Returns a list of tuples in the order MySQL provides.

Why it matters:

- Service code and tests use this for broad verification and cleanup checks.

### `select_num_day_dues(num_days=3)`

What it does:

- Filters rows where `status = 'UNPAID'`.
- Returns bills whose due date falls between today and today + `num_days`.
- Orders results by `due_date` ascending.

Why it matters:

- This powers the due-soon listing behavior.

### `select_bill_by_id(id_)`

What it does:

- Reads one row by primary key.
- Returns a single tuple or `None`.

Why it matters:

- Useful for identity lookups without scanning the full table.

### `update_bill_status(id_, status)`

What it does:

- Updates the status field for one row.
- Checks `rowcount` before commit so a missing id becomes an error.
- Returns the updated id on success.

Why it matters:

- The function should not silently succeed if the target row does not exist.

### `delete_bill_by_id(id_)`

What it does:

- Deletes one row by id.
- Checks `rowcount` so a missing row becomes an error.

Why it matters:

- Deleting a non-existent row should be visible to the caller.

## How The Query Layer Interacts With The Rest Of The App

1. Route passes validated values to service.
2. Service calls a query function.
3. Query executes SQL and either returns data or raises a connector error.
4. Service converts that failure into a simple exception type for the route.

## Query Guarantees

- No query function leaves a connection open.
- Write queries commit only after the database acknowledges an affected row.
- Missing-row updates and deletes are not treated as successful operations.

