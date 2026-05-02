# Files Involved in the Backend Sub-system

This document maps every file that participates in the backend layer,
organized by architectural role.

---

## 1. Application Entry Point

### backend/app/main.py

The FastAPI application factory. This file is the target of the Uvicorn
server command (`uvicorn app.main:app`).

Responsibilities:
- Creates the FastAPI application instance.
- Configures CORS middleware with an explicit allowlist of frontend origins.
  Only http://localhost:8080 and http://127.0.0.1:8080 are permitted.
  All methods and headers are allowed. Credentials are enabled.
- Registers the bill router from the routes sub-package.
  The router carries the `/bills` prefix, so all bill endpoints
  become available under that path.
- Defines a standalone health check endpoint at GET /health.
  This endpoint returns a simple JSON message and is used to verify
  that the server is running without touching the database.
- Loads environment variables from .env via python-dotenv.
  This must happen before any other module reads os.getenv(),
  which is why it runs at module import time.

This file contains no business logic. It is purely infrastructure.

### backend/app/__init__.py

Empty file. Marks the `app` directory as a Python package so that
relative imports work throughout the sub-packages.

---

## 2. Validation Layer

### backend/app/schemas.py

Defines Pydantic models used to validate incoming HTTP request bodies.

Contains three definitions:

- BillStatus: A string enum restricting status values to PAID and UNPAID.
  This is used by both request models and prevents arbitrary status strings
  from reaching the database.

- BillCreateRequest: The validation model for POST /bills/new.
  Declares all fields with their types, optionality, and constraints.
  The `name` field has a custom field_validator that strips whitespace
  and rejects empty strings. The `total_amount` field uses Field(gt=0)
  to enforce positive values. A model_validator (runs after field parsing)
  checks that creation_date is not after due_date and that due_date
  is not in the past. If any validation fails, FastAPI returns a 422
  response with structured error details before the service is called.

- BillUpdateRequest: A minimal model containing only the status field.
  Used by PUT /bills/{bill_id} to validate status change requests.

This file imports from pydantic (BaseModel, Field, field_validator,
model_validator), datetime (date), typing (Optional), and enum (Enum).
It has no dependency on any other project module.

---

## 3. Routing Layer

### backend/app/routes/__init__.py

Package initializer for the routes sub-package.
Exports the four main route functions (create_bill, list_bills,
update_status, delete_bill) for use by other modules.

### backend/app/routes/api_endpoints.py

The HTTP endpoint definitions for all bill operations.

This file creates an APIRouter with prefix `/bills` and tag `bills`.
It imports every service function and both Pydantic schemas.

It defines seven route handlers:

- POST /bills/new: Extracts fields from the validated BillCreateRequest
  payload and passes them as keyword arguments to create_bill_service.
  The due_date is converted to ISO string format before passing.

- GET /bills/search: Takes a `name` query parameter and passes it
  to select_by_name_service. No validation beyond FastAPI's automatic
  type checking.

- GET /bills/all: Accepts optional boolean flags (upcoming_only,
  expired_only) and an integer days parameter with a minimum of 1.
  Passes all three to list_bills_service.

- GET /bills/upcoming: A convenience wrapper that calls list_bills_service
  with upcoming_only hardcoded to True. Only accepts the days parameter.

- GET /bills/expired: A parameterless endpoint that calls list_bills_service
  with expired_only hardcoded to True.

- PUT /bills/{bill_id}: Extracts the bill_id from the URL path and the
  status from the validated BillUpdateRequest body. Passes both to
  mark_bill_status_service.

- DELETE /bills/{bill_id}: Extracts the bill_id from the URL path and
  passes it to delete_bill_service.

Every write-operation handler (POST, PUT, DELETE) uses a consistent
try/except pattern:
  - ValueError with "No bill found" maps to HTTP 404.
  - Any other ValueError maps to HTTP 400.
  - Any other exception maps to HTTP 500.

The read-operation handlers (GET) do not use try/except because
the listing and search services do not raise on empty results --
they return an empty data array with total_count of 0.

---

## 4. Service Layer

### backend/app/services/__init__.py

Package initializer that exports four service functions.
Provides an __all__ list for explicit public API declaration.
The search service (select_by_name_service) is included in this 
registry and exported for use by the routes module.

### backend/app/services/bill_creation.py

Handles the creation of new bill records.
Defaults creation_date to today if not provided.
Converts the due_date string to a Python date object.
Delegates the INSERT to the query layer.
Returns the new bill's ID and metadata on success.
Wraps MySQL errors as ValueError for the route layer.

### backend/app/services/bill_listing.py

Handles retrieval and formatting of bill records.
Supports three filter modes: all, upcoming, and expired.
Contains a _format_tuple function that converts database row tuples
into dictionaries with named keys. This function handles the mapping
of positional indices to field names, including fallback values for
recurring_interval (index 7) and is_expired (index 8).
The total_amount field is explicitly cast from Decimal to float
for JSON serialization compatibility.

### backend/app/services/bill_status.py

Updates the payment status of an existing bill.
Reads the existing bill by ID to access its metadata and verify existence.
Updates the status field in the database.
Does not handle recurring bill generation (this is offloaded to the frontend).
Wraps MySQL errors as ValueError for the route layer.

### backend/app/services/bill_deletion.py

The simplest service file. Delegates the soft delete operation
to the query layer. Does not verify whether the bill is already
deleted -- the query layer handles this by filtering on Is_deleted = 'N'
and raising an error if zero rows are affected.

Performs case-insensitive substring search on bill names.
Contains its own `_format_tuple` function that maps all 9 fields 
for consistency with the listing service.
Filters out deleted bills by delegating to the query layer.

---

## 5. Database Interface Layer

### backend/app/db/__init__.py

Package initializer for the database sub-package.
Exports the connection function and five query functions.
The registry is fully populated, including select_expired_bills 
and select_by_name_match. Service modules import these functions 
through the package interface.

### backend/app/db/connection.py

Initializes the MySQL connection pool at module import time.
Reads all database credentials from environment variables.
Creates a MySQLConnectionPool named "userpool" with configurable size.
Exposes get_connection() which checks out a connection from the pool.
This is the only file in the entire backend that touches the MySQL driver's
connection API. Every other file gets its connection through this function.

### backend/app/db/queries.py

The raw SQL execution layer. Contains nine functions:

- insert_bill: Executes INSERT INTO with 7 columns.
  Returns the auto-generated primary key via cursor.lastrowid.
  Uses explicit commit with rollback on failure.

- select_all: Returns all rows where Is_deleted = 'N'.
  No ordering is applied.

- select_num_day_dues: Returns UNPAID, non-deleted rows whose due_date
  is within N days of today. Uses MySQL's DATE_ADD and CURDATE functions
  for date arithmetic. Results are ordered by due_date ascending.

- select_expired_bills: Returns UNPAID, non-deleted rows that are overdue.
  Uses an OR condition to catch both explicitly flagged (Is_expired = 'Y')
  and implicitly overdue (due_date < CURDATE()) records.
  Results are ordered by due_date ascending.

- select_bill_by_id: Returns a single row by primary key.
  Filters on Is_deleted = 'N'. Returns None if not found.

- select_by_name_match: Case-insensitive LIKE search with wildcards.
  Filters on Is_deleted = 'N' to respect soft deletion.

- update_bill_status: Sets the status column for a given ID.
  Checks rowcount to verify the update affected a row.
  Uses explicit commit with rollback on failure.

- delete_bill_by_id: Soft delete. Sets Is_deleted = 'Y'.
  Checks rowcount to verify the update affected a row.
  Uses explicit commit with rollback on failure.

- delete_bill_by_id_HARD: Physical delete. Executes DELETE FROM.
  Not exposed through any API endpoint. Exists as a maintenance utility.

Every function follows the same lifecycle:
  1. Check out a connection from the pool.
  2. Create a cursor.
  3. Execute the parameterized query.
  4. For writes: commit on success, rollback on failure.
  5. Close the cursor.
  6. Close (return) the connection to the pool.

The table name is read from the DB_TABLE environment variable
and interpolated into query strings using f-strings.
All user-provided values are passed as parameterized placeholders (%s)
to prevent SQL injection.
