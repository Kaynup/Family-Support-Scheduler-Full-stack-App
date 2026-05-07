# Files Involved in Backend

All backend logic resides in the `backend/app/` directory:

- `main.py`: Application entry point and router registration.
- `dependencies.py`: Role-based access control and JWT validation.
- `constants.py`: Enums and constant strings.
- `core/config.py`: Environment variable loading.
- `core/exceptions.py`: Typed exceptions for clean error handling.
- `db/connection.py`: Context manager for database pooling.
- `db/queries/`: Split operations (`bill_insert.py`, `bill_select.py`, `user_select.py`, etc.)
- `schemas/`: Pydantic validation schemas.
- `services/`: Business logic implementations (`bill_service.py`, `auth_service.py`, `remittance_service.py`).
- `routes/`: FastAPI endpoints connecting schemas to services.
