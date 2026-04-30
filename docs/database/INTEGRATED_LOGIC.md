# Integrated Logic and Persistence Patterns

This document covers the business rules enforced at the database level,
the persistence strategies used, and how the query layer interacts with the schema.

---

## 1. Temporal Constraint: `chk_due_date`

The only schema-level constraint beyond primary key uniqueness is the temporal check:

    due_date >= creation_date

This prevents a logically impossible state where a bill is "due" before it even existed.
The constraint fires at INSERT and UPDATE time within MySQL itself.
No application code is needed to enforce this -- any violating write will be rejected
with a MySQL constraint violation error before it reaches the disk.

This is important because the system allows users to create bills with arbitrary dates
through the frontend modal. Without this guard, a user could accidentally set a past
creation date with an even earlier due date, producing nonsensical calendar entries.

---

## 2. Soft Deletion Pattern

Bills are never physically removed from the database.

When a user clicks "Delete" in the frontend, the backend executes:

    UPDATE bills SET Is_deleted = 'Y' WHERE id = <id>

The record stays on disk. Every SELECT query in the system appends the filter:

    WHERE Is_deleted = 'N'

This means deleted bills are invisible to the application but recoverable.
The motivation behind this design is data preservation -- a family budgeting tool
should never permanently lose payment history, even if the user decides to remove
a bill from their active view. A future "Archived Bills" or "Payment History"
feature can be built by simply querying for `Is_deleted = 'Y'` records.

The hard delete function (`delete_bill_by_id_HARD`) exists in the query layer
as a maintenance utility but is not exposed through any API endpoint.

---

## 3. Expiration Tracking

The `Is_expired` column serves as a database-level flag for overdue bills.
A bill is considered expired when its due date has passed and it remains UNPAID.

The system uses a dual-check approach for expiration:

- Database level: The `Is_expired` field can be set to 'Y' explicitly.
- Frontend level: The calendar rendering logic independently compares
  each bill's `due_date` against the current date. If a bill is UNPAID
  and `due_date < today`, it is treated as expired regardless of the
  database flag value.

This redundancy is intentional. The database flag is useful for batch queries
(the `/bills/expired` endpoint filters on it), while the frontend comparison
ensures real-time accuracy without waiting for a background process to flip
the flag at midnight.

The expired bills query in the database layer uses an OR condition:

    WHERE status = 'UNPAID' AND Is_deleted = 'N'
    AND (Is_expired = 'Y' OR due_date < CURDATE())

This catches both explicitly flagged records and implicitly overdue ones.

---

## 4. Recurring Bill Projection

The `recurring_interval` column stores the recurrence type for each bill.
Valid values are `NONE`, `WEEKLY`, and `MONTHLY`.

When a bill with a recurring interval is marked as PAID, the backend service
automatically creates the next bill in the series by calculating the next due date:

- WEEKLY: current due_date + 7 days
- MONTHLY: current due_date + 30 days

The new bill is inserted with status UNPAID and the same recurring_interval,
creating a self-perpetuating chain of bills.

Additionally, the frontend projects future recurring instances into the calendar
without waiting for the database to contain them. This projection is purely visual --
the projected entries are generated in-memory from the latest real bill and are
marked with an `isProjected` flag so the UI can distinguish them from actual records.

---

## 5. Connection Pooling

The database connection layer does not use one-off connections.

A `MySQLConnectionPool` is initialized at backend startup with a configurable pool size.
Every query function follows the same lifecycle:

    1. Check out a connection from the pool.
    2. Create a cursor.
    3. Execute the query.
    4. Commit or rollback.
    5. Close the cursor.
    6. Close (return) the connection to the pool.

This pattern prevents connection exhaustion under concurrent frontend requests.
The pool size is set via the `DB_CONN_POOLING` environment variable, defaulting
to a value suitable for single-user local development.

---

## 6. Query Offloading

Date arithmetic is performed by MySQL, not by Python.

The upcoming bills query uses MySQL's `DATE_ADD` function:

    due_date <= DATE_ADD(CURDATE(), INTERVAL <days> DAY)

This is more efficient than fetching all bills and filtering in Python because:

- MySQL evaluates the date comparison using its internal date index.
- Only matching rows are transferred over the connection.
- The application layer receives a pre-filtered result set.

The same principle applies to the expired bills query, which uses `CURDATE()`
for the overdue comparison directly within the WHERE clause.
