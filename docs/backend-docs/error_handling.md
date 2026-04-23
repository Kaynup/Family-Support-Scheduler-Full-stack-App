# Error Handling

## Navigation

- Hub: [../index.md](../index.md)
- Routes: [api_endpoints.md](api_endpoints.md)
- Services: [bill_services.md](bill_services.md)
- SQL: [sql_queries.md](sql_queries.md)

## Failure Path Explained

The backend handles failure in layers rather than in one giant place.

### 1. Query layer

This is where actual MySQL interaction happens. If the SQL engine errors, the query function rolls the transaction back and re-raises the connector exception. This layer also checks `rowcount` for update and delete operations so the backend can detect a no-op write.

### 2. Service layer

The service layer catches connector errors and converts them into `ValueError`. That keeps the service interface simple for the routes and tests while still preserving the error message.

### 3. Route layer

The route layer turns `ValueError` into HTTP responses.

- `No bill found for given id` becomes `404`.
- Other value errors become `400`.
- Unexpected errors become `500`.

## Why this split exists

- The query layer understands SQL facts.
- The service layer understands application meaning.
- The route layer understands HTTP meaning.

This avoids mixing SQL rules, application rules, and network rules in one function.

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

## What Is Not Treated As A Separate Error Class

- There is no custom exception class file anymore.
- The project intentionally keeps error handling simple with built-in exceptions and message-based HTTP mapping.

## Mental Model For Debugging

If something fails, ask these questions in order:

1. Did the query layer roll back and re-raise?
2. Did the service convert the exception into `ValueError`?
3. Did the route map the message to the correct HTTP status code?

