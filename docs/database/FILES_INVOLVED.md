# Files Involved in the Database Sub-system

This document maps every file that participates in the database layer,
from schema definition to query execution.

---

## 1. database/schema.sql

The canonical schema definition file.

- Creates the `family_supp_sche` database if it does not exist.
- Drops and recreates the `bills` table on every run (destructive reset).
- Defines all columns, types, defaults, and the temporal constraint.
- Seeds the table with 12 test records covering all category and status combinations.
- Executed manually via `sudo mysql -u root -p < database/schema.sql` from the project root.
- This file is the single source of truth for the table structure.

---

## 2. database/README.md

A short reference file containing the exact command to initialize the database.
Points the developer to the `.env` file for the MySQL root password.

---

## 3. backend/app/db/connection.py

The connection pool initializer.

- Reads `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`, and `DB_CONN_POOLING` from `.env`.
- Creates a `MySQLConnectionPool` named "userpool" at module import time.
- Exposes a single function `get_connection()` that checks out a pooled connection.
- Every other file in the database layer depends on this module for its connection handle.
- No query logic lives here -- it is purely infrastructure.

---

## 4. backend/app/db/queries.py

The raw SQL execution layer. This is the only file that writes SQL strings.

- `insert_bill()` -- Inserts a new bill record with all fields.
- `select_all()` -- Returns all non-deleted bills.
- `select_num_day_dues()` -- Returns UNPAID, non-deleted bills due within N days.
- `select_expired_bills()` -- Returns UNPAID, non-deleted bills that are overdue.
- `select_bill_by_id()` -- Fetches a single non-deleted bill by primary key.
- `select_by_name_match()` -- Case-insensitive LIKE search on the name column.
- `update_bill_status()` -- Flips the status field for a given bill ID.
- `delete_bill_by_id()` -- Soft deletes a bill by setting Is_deleted to Y.
- `delete_bill_by_id_HARD()` -- Physically removes a row. Not exposed via any endpoint.
- Every function follows the same pattern: get connection, execute, commit/rollback, close.
- All queries filter on `Is_deleted = 'N'` to respect soft deletion.
- The table name is read from the `DB_TABLE` environment variable.
