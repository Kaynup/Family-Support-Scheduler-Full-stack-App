"""
Application entry point.

Registers all routers and configures CORS middleware.
All configurations are read from .core.config.settings
"""

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from .core.config import settings
from .core.logging_config import configure_logging, logger
from .db.connection import get_db_connection
from .routes import auth_routes, bill_routes, remittance_routes, user_routes

configure_logging()

app = FastAPI(title="API")

logger.info("Backend application starting")

app.exception_handler(RequestValidationError)(auth_routes.auth_validation_exception_handler)

cors_origins = [orig.strip() for orig in settings.allowed_origins.split(",") if orig.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins if cors_origins else [],
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1|.*\.vercel\.app)(:\d+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(bill_routes.router)
app.include_router(auth_routes.router)
app.include_router(remittance_routes.router)
app.include_router(user_routes.router)


@app.get("/health", tags=["health"])
def health_check():
    """Returns a simple liveness indicator for the backend server."""
    logger.info("Health check requested")
    return {"message": "backend is live"}


@app.get("/health/db", tags=["health"])
def health_db_check():
    """Validates connectivity to the active database."""
    logger.info("Database health check requested")
    try:
        with get_db_connection() as (_, cursor):
            cursor.execute("SELECT 1")
            row = cursor.fetchone()
        return {"status": "connected", "result": row[0] if row else None}
    except Exception as exc:
        logger.error("Database health check failed: %s", exc)
        return {"status": "error", "detail": str(exc)}
