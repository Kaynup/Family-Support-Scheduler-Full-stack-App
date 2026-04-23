# Documentation Hub

This folder is the map of the backend project. Each doc is intentionally narrow: one module, one concern, one place to write the full explanation.

## Read Me First

1. Start with [backend-docs/api_endpoints.md](backend-docs/api_endpoints.md) if you want to understand the HTTP entry points.
2. Move to [backend-docs/bill_services.md](backend-docs/bill_services.md) to see how request data becomes business behavior.
3. Read [backend-docs/sql_queries.md](backend-docs/sql_queries.md) for the raw database operations.
4. Read [database-docs/relational_schema.md](database-docs/relational_schema.md) for the table design and the meaning of each column.
5. Read [backend-docs/error_handling.md](backend-docs/error_handling.md) to understand where failures are handled and how they propagate.
6. Use [testing-docs/backend_testing.md](testing-docs/backend_testing.md) to understand how each script proves the code works.

## Documentation Map

### Backend

- [API endpoints](backend-docs/api_endpoints.md): route behavior, request flow, and response contract.
- [Bill services](backend-docs/bill_services.md): business logic, validation, formatting, and service output.
- [SQL queries](backend-docs/sql_queries.md): raw DB access, transaction behavior, and query guarantees.
- [Error handling](backend-docs/error_handling.md): failure path from query layer to HTTP response.

### Database

- [Relational schema](database-docs/relational_schema.md): table layout, field meaning, and why each column exists.

### Testing

- [Backend testing](testing-docs/backend_testing.md): what each test file checks, how cleanup is done, and how to run them.

## Writing Rules For This Project

- Write what the code actually does now, not what it might do later.
- Keep one topic per document.
- Use nested sections for detail instead of mixing unrelated code paths.
- When a function has a side effect, explain both the input and the effect.
- When a function returns data, explain the shape of the return value and why it exists.

## Current Project Boundary

- Backend is active.
- These docs are meant to track the backend, schema, and tests only.

