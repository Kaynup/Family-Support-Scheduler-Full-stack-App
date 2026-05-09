# Backend Documentation

The backend is built with **FastAPI** and **Python 3.10**. It serves as a stateless RESTful API for both the sender and receiver panels.

## Directory Structure
- `app/routes/`: Controllers that map HTTP endpoints to service functions.
- `app/services/`: Core business logic (authentication, bill processing, remittance logic).
- `app/schemas/`: Pydantic models for request validation and response formatting.
- `app/db/`: Database connection management and raw SQL query functions.
- `app/core/`: Configuration (`settings`) and custom exception definitions.

## Key Concepts

### 1. Route-to-Service Decoupling
Routes (`*_routes.py`) are strictly responsible for HTTP semantics: parsing parameters, calling the service layer, and raising HTTPExceptions. All business logic and database interactions reside exclusively in the `services/` directory.

### 2. Authentication & Authorization
Authentication is handled via JWT and bcrypt. The `dependencies.py` file exposes `require_sender_role` and `require_beneficiary_role`, which extract the user ID (`sub` claim) and role from the JWT header to enforce secure API access.

### 3. Auto-Generation of Recurring Bills
When a sender pays a recurring bill via the `/remittance/pay` endpoint, `remittance_service.py` executes a transaction that:
1. Records the payment in the `remittance` ledger.
2. Marks the current bill as `PAID`.
3. If the bill has a `MONTHLY` or `WEEKLY` interval, it automatically spawns the next `UNPAID` instance with the newly calculated due date.
