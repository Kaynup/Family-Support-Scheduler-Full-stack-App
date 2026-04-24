# Error Handling

## Navigation

- Index: [../index.md](../index.md)
- API Routes: [API endpoints](api_endpoints.md)
- Services: [Bill Services](bill_services.md)
- SQL: [SQL Queries](sql_queries.md)

> The backend handles failure in layers

### 1. Query layer

- If the SQL engine give an error, the query function rolls the transaction back and re-raises the connector exception
- This layer also checks `rowcount` for update and delete operations so the backend can detect a no-op write

### 2. Service layer

- The service layer catches connector errors and converts them into `ValueError`
- That keeps the service interface simple for the routes and tests while still preserving the error message

### 3. Route layer

The route layer turns `ValueError` into HTTP responses.

- `No bill found for given id` becomes `404`.
- Other value errors become `400`.
- Unexpected errors become `500`.


## Specific Error Cases In This Project

### Insert failure

- Origin: `insert_bill()`
- Typical cause: database connector issue or invalid DB state
- Handling: rollback and re-raise from query layer, then translate in service/route

### Status update on a missing bill

- Origin: `update_bill_status()`
- Trigger: `rowcount == 0`
- Raised exception: `mysql.connector.Error("No bill found for given id")`
- Route response: HTTP 404

### Delete on a missing bill

- Origin: `delete_bill_by_id()`
- Trigger: `rowcount == 0`
- Raised exception: `mysql.connector.Error("No bill found for given id")`
- Route response: HTTP 404


## Layered Debugging

> The error handling is regressive therefore detectable:

- Query layer Error -> Service layer Error -> API layer Error
- Service layer Error -> API layer Error
- API layer Error -> HTTP error

---