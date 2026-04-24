# API Endpoints

## Navigation

- Index: [../index.md](../index.md)
- Services: [Bill Services](bill_services.md)
- SQL layer: [SQL Queries](sql_queries.md)
- Errors: [Error Handling](error_handling.md)

## Intent

- accept request data in the shape FastAPI expects from service layer
- translating the service errors into HTTP responses
- expose the route contract that a client or test can call.

## Route-by-Route Breakdown

> Pydantic models are used for validation of fields and integrity `backend/app/schemas.py`

### `GET /health`

- Purpose: Backend status checkup.
- Function: `status()` in `backend/app/main.py`.
- Output: `{"message": "backend is live"}`.

### `POST /bills/new`

- Purpose: create a bill record.
- Function: `create_bill(payload: BillCreateRequest)`.
- Input model: `BillCreateRequest`.
- Payload fields used by the route:
	- `name`
	- `creation_date`
	- `due_date`
	- `total_amount`
	- `category`
	- `status`
- What the route does:
	- receives a validated Pydantic model,
	- forwards the values to `create_bill_service()`,
	- returns the service response when successful.
- Error handling:
	- `ValueError` with `No bill found` is treated as 404,
	- other `ValueError` instances become 400,
	- any unexpected exception becomes 500.

### `GET /bills/all`

- Purpose: list stored bills.
- Function: `list_bills(upcoming_only: bool = False, days: int = Query(3, ge=1))`.
- Query arguments:
	- `upcoming_only`: switches between full listing and due-soon listing.
	- `days`: controls the upcoming window and is constrained to be at least 1.
- The route passes the query flags to `list_bills_service()`.
- The service decides how rows are formatted; the route only passes the request through.

### `PUT /bills/{bill_id}`

- Purpose: change a bill status.
- Function: `update_status(bill_id: int, payload: BillUpdateRequest)`.
- Path parameter:
	- `bill_id`: the unique row identifier.
- Body model:
	- `BillUpdateRequest`.
- Behavior:
	- forwards the id and normalized status to `mark_bill_status_service()`.
- Failure handling:
	- same mapping as the create route.

### `DELETE /bills/{bill_id}`

- Purpose: remove a bill row.
- Function: `delete_bill(bill_id: int)`.
- Behavior:
	- forwards the id to `delete_bill_service()`.
- Failure handling:
	- same mapping as the create route.

## Request Contract Notes

### `BillCreateRequest`

- `name`: required, non-empty, trimmed string.
- `creation_date`: required date.
- `due_date`: required date.
- `total_amount`: numeric value greater than zero.
- `category`: optional text field.
- `status`: enum `BillStatus` with values `PAID` or `UNPAID`.
- date integrity rule: `creation_date` cannot be greater than `due_date`.
- due date rule: `due_date` cannot be in the past.

### `BillUpdateRequest`

- `status`: required enum `BillStatus` (`PAID` or `UNPAID`).

## Route Execution Path

1. FastAPI parses the request.
2. Pydantic validates body data where models are used.
3. The route calls the service function.
4. The service talks to the query layer.
5. The query layer executes the MySQL operation.
6. The route maps failures into HTTP responses.

## Things This File Does Not Do

- It does not compute bill rules.
- It does not open database connections.
- It does not format query rows.
- It does not decide business meaning for a failed operation.