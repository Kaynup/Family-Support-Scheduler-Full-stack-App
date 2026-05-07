# Backend Architecture

The backend follows a modular, service-oriented architecture designed for high cohesion and low coupling.

## Core Concepts
- `core/`: Contains cross-cutting concerns like environment configuration (`config.py`) and typed exceptions (`exceptions.py`).
- `constants.py`: Stores all magic strings and enums to prevent typos and ensure consistency.
- `db/queries/`: SQL operations are split by domain (e.g., `bill_insert.py`, `user_select.py`). A context manager (`db/connection.py`) ensures safe transaction handling.
- `schemas/`: Pydantic models for request validation and response shaping.
- `services/`: Business logic. Contains `bill_service.py`, `auth_service.py` (handles JWT and password hashing), and `remittance_service.py` (handles payment workflows).
- `dependencies.py`: FastAPI Depends functions for role-based access control (RBAC).
- `routes/`: FastAPI routers that wire incoming requests to services and map typed exceptions to HTTP status codes.
