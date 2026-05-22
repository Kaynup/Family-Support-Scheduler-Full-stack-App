# Backend Variable Flow

## Scope
The backend is organized around FastAPI routes, service functions, and SQL query helpers under `backend/app`.

## Real Variables and Data
- `app` in `main.py` is the FastAPI application that registers middleware, routes, and the health check.
- `settings` in `backend/app/core/config.py` supplies JWT and runtime configuration.
- `current_user` is the decoded JWT payload injected by `Depends(...)` in protected routes.
- `payload` objects in the route handlers are Pydantic request models such as `RegisterRequest`, `LoginRequest`, `BillCreateRequest`, `BillUpdateRequest`, and `RemittanceCreateRequest`.
- JWT payloads carry `sub`, `username`, `role`, and `exp`.
- Bill records carry `bill_id`, `bill_name`, `bill_status`, `user_id`, `creation_date`, `due_date`, `total_amount`, `category`, `recurring_interval`, and `is_deleted`.
- Remittance records carry `transaction_id`, `bill_id`, `sender_user_id`, `beneficiary_user_id`, `amount`, `currency`, `transaction_status`, and `payment_method`.

## Flow
1. `get_current_user_dependency` reads the `Authorization: Bearer ...` header and decodes the JWT.
2. Route handlers in `auth_routes.py`, `bill_routes.py`, `remittance_routes.py`, and `user_routes.py` validate the request and extract the relevant payload.
3. Service functions apply domain rules, such as role checks, bill filtering, payment validation, and password verification.
4. Query helpers in `backend/app/db/queries` execute the actual SQL operations.
5. The route converts typed exceptions into HTTP responses.

## Notes
The important state boundary is route -> service -> query. Keep new variables in the layer that owns the rule.