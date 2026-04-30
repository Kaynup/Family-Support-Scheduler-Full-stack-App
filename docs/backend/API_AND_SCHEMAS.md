# API Endpoints and Validation Schemas

## Router Configuration

All bill endpoints are grouped under a single FastAPI APIRouter
with the prefix `/bills` and the tag `bills`.
This means every endpoint documented below is relative to `/bills`.

The router is registered in `main.py` via `app.include_router()`.

In addition to the bill router, a standalone health check endpoint
exists at `GET /health` which returns `{"message": "backend is live"}`.
This endpoint is not part of the bill router and has no prefix.

---

## Endpoint Reference

### POST /bills/new

Creates a new bill record.

Request body (JSON):

| Field               | Type    | Required | Default   | Notes                                  |
| ------------------- | ------- | -------- | --------- | -------------------------------------- |
| name                | string  | YES      | --        | Must be non-empty after trimming.      |
| due_date            | date    | YES      | --        | ISO format. Cannot be in the past.     |
| creation_date       | date    | NO       | today     | If omitted, defaults to current date.  |
| total_amount        | float   | YES      | --        | Must be greater than zero.             |
| category            | string  | NO       | null      | Free-text grouping label.              |
| recurring_interval  | string  | NO       | "NONE"    | One of: NONE, WEEKLY, MONTHLY.         |
| status              | string  | NO       | "UNPAID"  | One of: PAID, UNPAID.                  |

Response (success):

    {
        "OK": true,
        "message": "bill created successfully on <creation_date>",
        "data": { "id": <int>, "name": ..., "due_date": ..., ... }
    }

Error responses:

    400 -- Validation failure (empty name, negative amount, past due date)
    500 -- Database error

---

### GET /bills/all

Returns all non-deleted bills in the system.

Query parameters:

| Parameter     | Type  | Default | Notes                                       |
| ------------- | ----- | ------- | ------------------------------------------- |
| upcoming_only | bool  | false   | If true, filters to UNPAID bills due soon.  |
| expired_only  | bool  | false   | If true, filters to overdue UNPAID bills.   |
| days          | int   | 3       | Number of days for upcoming window. Min: 1. |

Response:

    {
        "OK": true,
        "total_count": <int>,
        "data": [ { bill objects... } ]
    }

Each bill object contains: id, name, creation_date, due_date,
total_amount, status, category, recurring_interval, is_expired.

---

### GET /bills/upcoming

Convenience endpoint. Equivalent to `/bills/all?upcoming_only=true`.

Returns UNPAID, non-deleted bills whose due date falls within
the next N days (default 3). Results are ordered by due_date ascending.

This is the endpoint consumed by the automation shell script.

Query parameters:

| Parameter | Type | Default | Notes                    |
| --------- | ---- | ------- | ------------------------ |
| days      | int  | 3       | Lookahead window in days.|

---

### GET /bills/expired

Returns all UNPAID, non-deleted bills that are overdue.

A bill is considered overdue if:
- Its `Is_expired` field is set to 'Y' in the database, OR
- Its `due_date` is strictly before the current date (CURDATE()).

No query parameters. Results are ordered by due_date ascending.

This is the endpoint consumed by the automation shell script
for the expired bills section of the terminal alert.

---

### GET /bills/search

Case-insensitive substring search on the bill name field.

Query parameters:

| Parameter | Type   | Required | Notes                         |
| --------- | ------ | -------- | ----------------------------- |
| name      | string | YES      | The search term to match on.  |

The search uses SQL LIKE with wildcards on both sides,
so searching for "elect" will match "Electricity Bill".
The comparison is case-insensitive.

Response:

    {
        "OK": true,
        "total_count": <int>,
        "data": [ { bill objects... } ]
    }

---

### PUT /bills/{bill_id}

Updates the status of an existing bill.

Path parameters:

| Parameter | Type | Notes              |
| --------- | ---- | ------------------ |
| bill_id   | int  | The bill primary key. |

Request body (JSON):

| Field  | Type   | Required | Notes                    |
| ------ | ------ | -------- | ------------------------ |
| status | string | YES      | One of: PAID, UNPAID.    |

Side effects:

When a bill with a recurring_interval (WEEKLY or MONTHLY) is updated
to PAID, the service layer automatically creates the next bill in the series.
The next due date is calculated as:
- WEEKLY: current due_date + 7 days
- MONTHLY: current due_date + 30 days

The new bill inherits the name, amount, category, and recurring_interval
of the original. Its status is set to UNPAID.

Error responses:

    404 -- No bill found with the given ID
    400 -- Invalid status value
    500 -- Database error

---

### DELETE /bills/{bill_id}

Soft-deletes a bill by setting its Is_deleted flag to 'Y'.

Path parameters:

| Parameter | Type | Notes              |
| --------- | ---- | ------------------ |
| bill_id   | int  | The bill primary key. |

The record remains in the database but is excluded from all
future queries. There is no undo endpoint -- to recover a
soft-deleted bill, a direct database UPDATE is required.

Error responses:

    404 -- No bill found with the given ID
    400 -- Database constraint violation
    500 -- Database error

---

## Validation Schemas (Pydantic)

### BillStatus (Enum)

A string enumeration with two valid values:

    PAID
    UNPAID

Used by both BillCreateRequest and BillUpdateRequest to restrict
the status field to only these two values. Any other string is
rejected at the schema level before reaching the service layer.

### BillCreateRequest

Pydantic BaseModel for bill creation payloads.

Field-level validators:
- `name`: Must have at least 1 character. A custom field_validator
  strips whitespace and rejects empty strings.
- `total_amount`: Must be greater than zero (enforced by Field(gt=0)).

Model-level validators (run after all fields are parsed):
- If `creation_date` is provided, it must not be after `due_date`.
- `due_date` must not be in the past (compared against date.today()).

These validators run before any service code executes.
If validation fails, FastAPI automatically returns a 422 response
with a detailed error body explaining which field failed and why.

### BillUpdateRequest

Minimal Pydantic model containing only the `status` field.
The BillStatus enum restricts it to PAID or UNPAID.

---

## Error Handling Strategy

All route handlers follow a consistent try/except pattern:

    1. Call the service function.
    2. If it raises ValueError with "No bill found", return 404.
    3. If it raises ValueError for any other reason, return 400.
    4. If it raises any other exception, return 500.

This three-tier approach ensures that:
- Client errors (bad input) produce 400.
- Missing resources produce 404.
- Unexpected failures produce 500 without leaking stack traces.

The service layer is responsible for raising ValueError with
descriptive messages. The route layer translates those into
HTTP status codes.
