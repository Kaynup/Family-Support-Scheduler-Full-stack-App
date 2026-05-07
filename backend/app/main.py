"""
Application entry point.

Registers all routers and configures CORS middleware.
All configuration is read from .core.config.settings — no raw os.getenv calls here.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import bill_routes, auth_routes, remittance_routes
from .core.config import settings

app = FastAPI(title="Family Support Scheduler API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.fe_url,
        settings.fe_local_url,
        settings.receiver_panel_url,
        settings.receiver_panel_local_url,
        settings.sender_panel_url,
        settings.sender_panel_local_url,
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(bill_routes.router)
app.include_router(auth_routes.router)
app.include_router(remittance_routes.router)


@app.get("/health", tags=["health"])
def health_check():
    """Returns a simple liveness indicator for the backend server."""
    return {"message": "backend is live"}