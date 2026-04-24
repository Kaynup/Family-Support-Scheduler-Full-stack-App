# Bill Scheduler - Full-Stack Sequence Diagrams

## Overview

This document describes the sequence of interactions between frontend, backend layers, and database for all major operations in the Bill Scheduler application.

---

## Diagram Legend

- **Frontend:** React UI application in browser
- **API Routes:** HTTP endpoint layer (api_endpoints.py)
- **Schemas:** Pydantic request/response validation (schemas.py)
- **Services:** Business logic and validation (services/)
- **Queries:** Direct SQL execution (queries.py)
- **Database:** MySQL bill storage

All communications include both success and error paths.

---

## Sequence 1: Create Bill (Happy Path)

```mermaid
sequenceDiagram
    actor User
    participant Frontend as 🌐 Frontend<br/>React App
    participant API as 🔶 API Route<br/>POST /bills/new
    participant Schema as 📋 Pydantic<br/>BillCreateRequest
    participant Service as ⚙️ Service<br/>bill_creation
    participant Query as 🔍 Query Layer<br/>insert_bill()
    participant DB as 💾 MySQL<br/>bills table

    User->>Frontend: Fill bill form & submit
    Frontend->>API: POST /bills/new<br/>{name, creation_date,<br/>due_date, total_amount,<br/>category, status}
    
    API->>Schema: Validate payload
    Schema->>Schema: Check name not empty ✓
    Schema->>Schema: Check due_date >= today ✓
    Schema->>Schema: Check creation_date <= due_date ✓
    Schema->>Schema: Check status in (PAID, UNPAID) ✓
    
    API->>Service: Call create_bill_service()<br/>with validated data<br/>(convert date → ISO string)<br/>(convert enum → string value)
    
    Service->>Service: Re-validate all inputs
    Service->>Service: Parse dates
    Service->>Query: Call insert_bill()<br/>(name, creation_date,<br/>due_date, total_amount,<br/>category, status)
    
    Query->>DB: INSERT INTO bills<br/>VALUES (...)
    DB->>Query: Return lastrowid = 42
    Query->>Service: Return bill_id = 42
    
    Service->>Service: Format response
    Service->>API: Return {OK: true,<br/>data: {id, name,<br/>creation_date, ...}}
    
    API->>Frontend: HTTP 200 OK<br/>JSON: bill object
    Frontend->>User: Display success<br/>Show new bill in list

    Note over DB: Bill 42 now exists<br/>status: UNPAID/PAID
```

---

## Sequence 2: Create Bill (Validation Error)

```mermaid
sequenceDiagram
    actor User
    participant Frontend as 🌐 Frontend<br/>React App
    participant API as 🔶 API Route<br/>POST /bills/new
    participant Schema as 📋 Pydantic<br/>BillCreateRequest
    participant ErrorHandler as ⚠️ Error<br/>Mapper

    User->>Frontend: Submit form with<br/>due_date in past
    Frontend->>API: POST /bills/new<br/>{..., due_date: "2026-04-20", ...}
    
    API->>Schema: Validate payload
    Schema->>Schema: Check due_date >= today
    Schema->>Schema: ✗ FAIL: 2026-04-20 < today
    Schema->>API: Raise ValidationError<br/>"Due date must be today or later"
    
    API->>ErrorHandler: Catch validation error
    ErrorHandler->>Frontend: HTTP 400 Bad Request<br/>{detail: "Due date must be<br/>today or later"}
    
    Frontend->>User: Display error message
    User->>Frontend: Fix date and resubmit

    Note over Schema: Validation happens FIRST<br/>No database access
```

---

## Sequence 3: List Bills (Happy Path)

```mermaid
sequenceDiagram
    actor User
    participant Frontend as 🌐 Frontend<br/>React App
    participant API as 🔶 API Route<br/>GET /bills/all
    participant Service as ⚙️ Service<br/>bill_listing
    participant Query as 🔍 Query Layer<br/>select_all()
    participant DB as 💾 MySQL<br/>bills table

    User->>Frontend: Click "View All Bills"
    Frontend->>API: GET /bills/all<br/>(optional: ?upcoming_only=true)
    
    API->>Service: Call list_bills_service()<br/>(upcoming_only: false)
    
    Service->>Query: Call select_all()
    Query->>DB: SELECT * FROM bills<br/>ORDER BY due_date ASC
    DB->>Query: Return list of<br/>42 tuples
    
    Query->>Service: Return:<br/>[(1, 'Electricity',<br/>'2026-04-30', 150.00, ...),<br/>(2, 'Rent',<br/>'2026-05-01', 1000.00, ...), ...]
    
    Service->>Service: Convert tuples to dicts
    Service->>Service: Format dates as ISO strings
    Service->>API: Return {OK: true,<br/>total_count: 42,<br/>data: [bill_obj, ...]}
    
    API->>Frontend: HTTP 200 OK<br/>JSON: list response
    Frontend->>Frontend: Render bill list
    Frontend->>User: Display 42 bills<br/>in table/cards

    Note over DB: No data modified<br/>Read-only operation
```

---

## Sequence 4: List Bills with Upcoming Filter

```mermaid
sequenceDiagram
    actor User
    participant Frontend as 🌐 Frontend<br/>React App
    participant API as 🔶 API Route<br/>GET /bills/all
    participant Service as ⚙️ Service<br/>bill_listing
    participant Query as 🔍 Query Layer<br/>select_num_day_dues()
    participant DB as 💾 MySQL<br/>bills table

    User->>Frontend: Click "Upcoming Bills"<br/>(next 3 days)
    Frontend->>API: GET /bills/all<br/>?upcoming_only=true
    
    API->>Service: Call list_bills_service()<br/>(upcoming_only: true)
    
    Service->>Query: Call select_num_day_dues(3)
    Query->>DB: SELECT * FROM bills<br/>WHERE status = 'UNPAID'<br/>AND due_date <= today + 3 days<br/>ORDER BY due_date ASC
    DB->>Query: Return 5 tuples<br/>(bills due soon)
    
    Query->>Service: Return filtered list
    Service->>Service: Format tuples to dicts
    Service->>API: Return {OK: true,<br/>total_count: 5,<br/>data: [urgent_bills]}
    
    API->>Frontend: HTTP 200 OK<br/>JSON: filtered list
    Frontend->>Frontend: Render upcoming bills
    Frontend->>User: Display 5 bills<br/>due in next 3 days

    Note over Query: Filters: UNPAID only<br/>+ due_date within window
```

---

## Sequence 5: Update Bill Status (Happy Path)

```mermaid
sequenceDiagram
    actor User
    participant Frontend as 🌐 Frontend<br/>React App
    participant API as 🔶 API Route<br/>PUT /bills/{bill_id}
    participant Schema as 📋 Pydantic<br/>BillUpdateRequest
    participant Service as ⚙️ Service<br/>bill_status
    participant Query as 🔍 Query Layer<br/>update_bill_status()
    participant DB as 💾 MySQL<br/>bills table

    User->>Frontend: Click "Mark as Paid"<br/>on bill #42
    Frontend->>API: PUT /bills/42<br/>{status: "PAID"}
    
    API->>Schema: Validate payload
    Schema->>Schema: Check status in (PAID, UNPAID) ✓
    Schema->>API: Return parsed payload
    
    API->>Service: Call update_status_service()<br/>(bill_id: 42,<br/>status: "PAID")
    
    Service->>Service: Validate bill_id is integer
    Service->>Service: Validate status is valid
    Service->>Query: Call update_bill_status(42, "PAID")
    
    Query->>DB: UPDATE bills<br/>SET status = 'PAID'<br/>WHERE id = 42
    DB->>Query: rows_affected = 1
    Query->>Query: ✓ Confirm 1 row updated
    Query->>Service: Return bill_id = 42
    
    Service->>API: Return {OK: true,<br/>data: {id: 42}}
    
    API->>Frontend: HTTP 200 OK<br/>JSON: {OK: true, data: {id: 42}}
    Frontend->>Frontend: Update bill in state
    Frontend->>User: Show "Bill marked as paid"

    Note over DB: Bill 42 status changed<br/>to PAID (committed)
```

---

## Sequence 6: Update Bill Status (Bill Not Found)

```mermaid
sequenceDiagram
    actor User
    participant Frontend as 🌐 Frontend<br/>React App
    participant API as 🔶 API Route<br/>PUT /bills/{bill_id}
    participant Schema as 📋 Pydantic<br/>BillUpdateRequest
    participant Service as ⚙️ Service<br/>bill_status
    participant Query as 🔍 Query Layer<br/>update_bill_status()
    participant DB as 💾 MySQL<br/>bills table
    participant ErrorHandler as ⚠️ Error<br/>Mapper

    User->>Frontend: Attempt to update<br/>deleted bill #999
    Frontend->>API: PUT /bills/999<br/>{status: "PAID"}
    
    API->>Schema: Validate payload ✓
    API->>Service: Call update_status_service(999, ...)
    
    Service->>Query: Call update_bill_status(999, "PAID")
    Query->>DB: UPDATE bills<br/>SET status = 'PAID'<br/>WHERE id = 999
    DB->>Query: rows_affected = 0
    
    Query->>Query: ✗ Check: rows_affected == 0
    Query->>Query: Raise ValueError<br/>("No bill found with id 999")
    Query->>Service: ValueError raised
    
    Service->>API: ValueError bubbles up
    API->>ErrorHandler: Catch ValueError
    ErrorHandler->>ErrorHandler: Check message text
    ErrorHandler->>Frontend: HTTP 404 Not Found<br/>{detail: "No bill found..."}
    
    Frontend->>User: Display "Bill not found"

    Note over DB: No data modified<br/>Transaction rolled back
```

---

## Sequence 7: Delete Bill (Happy Path)

```mermaid
sequenceDiagram
    actor User
    participant Frontend as 🌐 Frontend<br/>React App
    participant API as 🔶 API Route<br/>DELETE /bills/{bill_id}
    participant Service as ⚙️ Service<br/>bill_deletion
    participant Query as 🔍 Query Layer<br/>delete_bill_by_id()
    participant DB as 💾 MySQL<br/>bills table

    User->>Frontend: Click "Delete Bill" #42<br/>Confirm deletion
    Frontend->>API: DELETE /bills/42
    
    API->>Service: Call delete_bill_service(42)
    
    Service->>Service: Validate bill_id is integer
    Service->>Query: Call delete_bill_by_id(42)
    
    Query->>DB: DELETE FROM bills<br/>WHERE id = 42
    DB->>Query: rows_affected = 1
    Query->>Query: ✓ Confirm 1 row deleted
    Query->>Service: Return bill_id = 42
    
    Service->>API: Return {OK: true,<br/>data: {id: 42}}
    
    API->>Frontend: HTTP 200 OK<br/>JSON: {OK: true, data: {id: 42}}
    Frontend->>Frontend: Remove bill from state
    Frontend->>User: Show "Bill deleted"

    Note over DB: Bill 42 record deleted<br/>from database (permanent)
```

---

## Sequence 8: Transaction & Rollback (Database Error)

```mermaid
sequenceDiagram
    participant Query as 🔍 Query Layer<br/>with Transaction
    participant DB as 💾 MySQL<br/>Connection

    Query->>Query: Start transaction
    
    Query->>DB: UPDATE bills SET ... ✓
    
    Query->>DB: INSERT INTO history ...<br/>CONSTRAINT VIOLATION!
    DB->>Query: Database error
    
    Query->>Query: Exception caught
    Query->>DB: ROLLBACK
    DB->>Query: Transaction rolled back
    
    Query->>Query: All changes undone
    Query->>Query: Raise error to service

    Note over DB: Atomicity guaranteed<br/>Either all changes<br/>or none
```

---

## Request/Response Format Examples

### POST /bills/new - Request
```json
{
  "name": "Electricity Bill",
  "creation_date": "2026-04-24",
  "due_date": "2026-05-10",
  "total_amount": 150.50,
  "category": "Utilities",
  "status": "UNPAID"
}
```

### POST /bills/new - Response (200 OK)
```json
{
  "OK": true,
  "data": {
    "id": 42,
    "name": "Electricity Bill",
    "creation_date": "2026-04-24",
    "due_date": "2026-05-10",
    "total_amount": 150.50,
    "category": "Utilities",
    "status": "UNPAID",
    "created_at": "2026-04-24T14:30:22.123456"
  }
}
```

### PUT /bills/{bill_id} - Request
```json
{
  "status": "PAID"
}
```

### PUT /bills/{bill_id} - Response (200 OK)
```json
{
  "OK": true,
  "data": {
    "id": 42
  }
}
```

### Error Response (400 Bad Request)
```json
{
  "detail": "Due date must be today or later"
}
```

### Error Response (404 Not Found)
```json
{
  "detail": "No bill found with that id"
}
```

---

## Layer Interaction Summary

| Layer | Responsibility | Input | Output | Error Handling |
|-------|---|---|---|---|
| Frontend (React) | UI rendering, user interaction | User clicks/input | HTTP requests | Display error messages |
| API Routes | HTTP mapping, error translation | HTTP request + Pydantic validation | HTTP response + status code | ValueError → 404, Other ValueError → 400, Exception → 500 |
| Schemas (Pydantic) | Request validation | Raw JSON payload | Typed objects (date, enum) | ValidationError → 400 |
| Services | Business logic, input re-validation | Typed objects OR strings | Response dict/bool | ValueError → caught by routes |
| Queries | Raw SQL execution, transaction management | Parameters | Rows/rowcount | Database errors → ValueError/Exception |
| Database | Data persistence | SQL statements | Result sets | SQL constraint violations |

---

## Key Design Patterns

### 1. Validation at Multiple Layers
- **Schema Layer:** Catches type/format errors early (400 before service runs)
- **Service Layer:** Re-validates business logic (ensures safety if service called directly)
- **Query Layer:** Confirms rowcount for UPDATE/DELETE (ensures operations succeeded)

### 2. Error Translation
- **Query Layer:** Raises ValueError with descriptive message on row not found
- **Service Layer:** Lets ValueError bubble up (validation errors)
- **Route Layer:** Maps ValueError with "No bill found" to 404, others to 400

### 3. Type Adaptation at Route Layer
- Converts Pydantic `date` objects to ISO strings for services
- Converts Pydantic `enum` values to string values for services
- Maintains backwards compatibility with existing service implementations

### 4. Atomicity Guarantees
- Each transaction either commits all changes or rolls back all
- Connection pool ensures transaction isolation
- rowcount validation prevents silent failures

---

## Summary

The full-stack sequence shows:
1. **Frontend → API:** User action triggers HTTP request with JSON payload
2. **API → Schema:** Pydantic validates types, formats, enums before processing
3. **API → Service:** Validated data passed to business logic layer
4. **Service → Query:** Business logic calls raw SQL layer with parameters
5. **Query → DB:** SQL executes in transaction, rowcount validated
6. **DB → Query:** Result set or error returned
7. **Query → Service:** Result formatted and returned
8. **Service → API:** Response prepared
9. **API → Frontend:** HTTP response with status code and JSON payload
10. **Frontend → User:** UI updated with success/error message

All layers are loosely coupled, with clear contracts (request/response formats) and comprehensive error handling at each level.
