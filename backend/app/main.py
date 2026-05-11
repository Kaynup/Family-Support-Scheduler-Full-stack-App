"""
Application entry point.

Registers all routers and configures CORS middleware.
All configuration is read from .core.config.settings — no raw os.getenv calls here.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from .routes import bill_routes, auth_routes, remittance_routes, user_routes
from .core.config import settings

app = FastAPI(title="Family Support Scheduler API")

app.exception_handler(RequestValidationError)(auth_routes.auth_validation_exception_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?$",
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
    return {"message": "backend is live"}