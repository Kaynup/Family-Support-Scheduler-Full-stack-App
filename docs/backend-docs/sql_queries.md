# SQL Queries

## Navigation
- Index: [../index.md](../index.md)
- Services: [Services](bill_services.md)
- API Routes: [API endpoints](api_endpoints.md)
- Errors: [Error Handling](error_handling.md)

## Modules `backend/app/db/*`
The SQL handles the connection of the python functions to the SQL functions with minimal error handling

### `backend/app/db/connection.py`
- callable function `get_connection()` that returns a `PooledMySQLConnection`
- The pool is created once in the connection module and reused in `~/db/queries.py`
- uses `dotenv` to get environmental variables from `.env` at root

#### About Pooling
- The object behaves almost exactly like standard MySQLConnection or CMySQLConnection objects e.g., they support cursor(), commit(), rollback()
- When close() is called on a PooledMySQLConnection, it does not close the underlying connection to the database. Instead, it resets the session and returns the connection to the pool for reuse
> pros
- By reusing open connections, it avoids the heavy overhead of repeatedly creating and destroying TCP connections to the MySQL server
- It manages the maximum number of connections, preventing an application from exhausting the database with too many simultaneous requests
> cons
- A pooled connection cannot be reconfigured using its config() method; changes must be handled through the pool object itself


### `backend/app/db/queries.py`

#### - `insert_bill(name, due_date, total_amount, creation_date, status='UNPAID', category=None)`

- Inserts one row into the bill table with given parameters from service layer `~/services/*`
- Returns `lastrowid` so the caller gets the id created by MySQL
- Commit on success
- Roll back on connector error

#### - `select_all()`

- Reads every row from the table
- Returns a list of tuples in the order MySQL provides

#### - `select_num_day_dues(num_days=3)`

- Filters rows where `status = 'UNPAID'`
- Returns bills whose due date falls between `CURDATE()` and `CURDATE()` + `DATE_ADD(CURDATE(), INTERVAL %s DAY)`
- `%s` being `num_days`
- Results order by `due_date` in ascending, powers the due-soon listing behavior

#### - `select_bill_by_id(id_)`

- Reads one row by primary key `id`
- Returns a single list of tuple or `None`
- Useful for identity lookups without scanning the full table

#### - `update_bill_status(id_, status)`

- Updates the status field for one row
- Checks `rowcount` before commit so a missing id becomes an error
- Returns the updated id on success
- Raises error if bill not found with the current id

#### - `delete_bill_by_id(id_)`

What it does:

- Deletes one row by id.
- Checks `rowcount` so a missing row becomes an error.
- Raises error if bill not found with the current id

## How The Query Layer Interacts With The Application

- Service calls a query function
- Query executes SQL and either returns data or raises a connector error

---