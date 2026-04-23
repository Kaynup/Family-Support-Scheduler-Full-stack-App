# Bill Services

## Navigation

- Hub: [../index.md](../index.md)
- Routes: [api_endpoints.md](api_endpoints.md)
- SQL: [sql_queries.md](sql_queries.md)
- Errors: [error_handling.md](error_handling.md)

## Service Layer Intent

The service layer is where request meaning becomes application behavior. It sits between the route and the query layer. The route already knows the HTTP shape, and the query layer already knows SQL. The service layer answers the middle question: what should the backend do with this request before and after the database call?

## Bill Creation Service

### Function

- `create_bill_service(name, due_date, total_amount, creation_date=None, category=None, status="UNPAID")`

### What it is trying to achieve

Create a bill row while normalizing the date fields and preserving the response shape the API expects.

### How it works

1. If `creation_date` is not passed, it uses `date.today()`.
2. It converts `due_date` from ISO text into a Python `date`.
3. It calls `insert_bill()` with the cleaned values.
4. If the database layer raises a connector error, it re-raises it as a `ValueError` so the route can map it cleanly.
5. It returns a success dictionary with `OK`, `message`, and `data`.

### Response shape

- `OK`: `True`
- `message`: includes the creation date
- `data`:
  - `name`
  - `due_date`
  - `total_amount`
  - `status`
  - `category`

### Why the service keeps the response simple

The service is not trying to expose raw DB metadata. It returns the business-facing data that a route or caller needs after creation.

## Bill Listing Service

### Function

- `list_bills_service(upcoming_only=False, days=3)`

### What it does

Read rows from the query layer and convert them into dictionaries with stable field names.

### Important behavior

- When `upcoming_only` is `False`, it uses `select_all()`.
- When `upcoming_only` is `True`, it uses `select_num_day_dues(days)`.
- Each tuple row is converted into a dictionary with string dates and float amounts.

### Helper used internally

- `_format_tuple(row)`

This helper is not a business rule by itself. Its job is to reshape the database tuple into a JSON-friendly object.

## Bill Status Service

### Function

- `mark_bill_status_service(id_, status)`

### What it does

Change the status of a single bill and return the id of the affected bill.

### Important behavior

- It delegates the actual update to `update_bill_status()`.
- If the query layer reports a MySQL error, the service raises `ValueError`.
- The service response contains the id only in its `data` block.

### Why it returns only the id

The service does not re-read the row after the update because the caller already knows which bill was targeted. The function exists to confirm the operation and pass back the identity of the row that was acted on.

## Bill Deletion Service

### Function

- `delete_bill_service(id)`

### What it does

Delete the chosen bill and confirm the deleted id in the response.

### Important behavior

- The query layer performs the delete and row-count validation.
- The service converts connector errors into `ValueError`.
- The service response returns the deleted id only.

## Service Contract Summary

- Services accept already-shaped values from routes or tests.
- Services do minimal transformation only where the data must match Python/SQL expectations.
- Services do not build SQL strings.
- Services are responsible for the business meaning of the operation, not the wire protocol.

