# Relatable Files (Backend)

The backend is strictly organized into decoupled layers to separate transport (HTTP) from business logic and database access.

## 1. Entry and Configuration
- **`backend/main.py`**: The application entry point. Configures the FastAPI app, attaches CORS middleware, and mounts routers.
- **`backend/app/core/config.py`**: Loads environment variables from `.env` via Pydantic's `BaseSettings`.
- **`backend/app/core/exceptions.py`**: Custom domain exceptions (e.g., `BillNotFoundError`, `AuthenticationError`) allowing the service layer to fail cleanly.

## 2. API Routes (Controllers)
- **`backend/app/routes/auth_routes.py`**: Handles `/auth/login` and `/auth/register`.
- **`backend/app/routes/bill_routes.py`**: Handles `/bills/*` operations. Extracts user context via `Depends(get_current_user_dependency)` to enforce beneficiary isolation.
- **`backend/app/routes/remittance_routes.py`**: Handles `/remittance/pay` and `/remittance/history/*`.

## 3. Business Logic (Services)
- **`backend/app/services/auth_service.py`**: Manages password hashing, JWT encoding/decoding.
- **`backend/app/services/bill_service.py`**: Formats database queries into structured JSON responses. Handlers filtering arrays.
- **`backend/app/services/remittance_service.py`**: Handles the transaction sequence. Crucially, implements the **Auto-Generation of Recurring Bills** workflow.

## 4. Database Access (Queries)
- **`backend/app/db/connection.py`**: Context manager for acquiring and releasing `mysql.connector` handles.
- **`backend/app/db/queries/*`**: Broken down into `auth_select.py`, `bill_insert.py`, `bill_update.py`, `remittance_insert.py`, etc.

## 5. Security and Schemas
- **`backend/app/dependencies.py`**: FastAPI dependency injection functions. Verifies JWT tokens and asserts `require_sender_role` or `require_beneficiary_role`.
- **`backend/app/schemas/*`**: Pydantic models for incoming request bodies to ensure strict type validation.
