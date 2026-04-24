# Bill Services

## Navigation

- Hub: [Index](../index.md)
- SQL: [sql_queries.md](sql_queries.md)
- API Routes: [API endpoints](api_endpoints.md)
- Errors: [Error Handling](error_handling.md)

## Intent

The service layer is where application behaviour is defined. It sits between the api layer and the query layer. The route already does the HTTP part, and the query layer does the SQL.
The services layers handling and arranges the query functions from the query layer and makes required usable functions, that return outputs that are api layer suitable.

## Bill Creation Service `backend/app/services/bill_creation.py`

#### - `create_bill_service(name, due_date, total_amount, creation_date=None, category=None, status="UNPAID")`

- Creates a bill row while normalizing the date fields and preserving the response shape the API expects.

#### Working

1. If `creation_date` is not passed, it uses `date.today()`.
2. It converts `due_date` from ISO text into a Python `date`.
3. It calls `insert_bill()` with the cleaned values.
4. If the database layer raises a connector error, it re-raises it as a `ValueError` so the route can map it cleanly.
5. It returns a success dictionary with `OK`, `message`, and `data`.

#### Response

- `OK`: `True`
- `message`: includes the creation date
- `data`:
  - `name`
  - `due_date`
  - `total_amount`
  - `creation_date`
  - `status`
  - `category`

## Bill Listing Service

#### - `list_bills_service(upcoming_only=False, days=3)`

> Important behavior:

- When `upcoming_only` is `False`, it uses `select_all()`.
- When `upcoming_only` is `True`, it uses `select_num_day_dues(days)`.
- Each tuple row is converted into a dictionary with string dates and float amounts.

> Helper function

- `_format_tuple(row)`

Reshape the database tuple into a JSON-friendly object.

## Bill Status Service

#### - `mark_bill_status_service(id_, status)`

- Changes the status of a single bill and return the id of the affected bill.
- It delegates the actual update to `update_bill_status()`.
- If the query layer reports a MySQL error, the service raises `ValueError`.
- The service response returns the `id`.

## Bill Deletion Service

#### - `delete_bill_service(id)`

- Deletes the chosen bill by given bill id.
- The query layer performs the delete and row-count validation.
- The service converts connector errors into `ValueError`.
- The service response returns the deleted id only.

## What do Services do in the Application

- Services accept already-shaped values from routes or tests.
- Services do minimal transformation only where the data must match Python/SQL expectations.

---