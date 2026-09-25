"""
schemas/ — Pydantic request and response models organized by domain.

Re-exports all schema classes so routes import from a single location:
    from app.schemas import BillCreateRequest, LoginRequest, ...
"""

from .auth_schemas import LoginRequest, RegisterRequest, TokenResponse, UserResponse
from .bill_schemas import (
    BillCreateRequest,
    BillListResponse,
    BillResponse,
    BillUpdateRequest,
)
from .remittance_schemas import RemittanceCreateRequest, RemittanceResponse

__all__ = [
    "BillCreateRequest",
    "BillListResponse",
    "BillResponse",
    "BillUpdateRequest",
    "LoginRequest",
    "RegisterRequest",
    "RemittanceCreateRequest",
    "RemittanceResponse",
    "TokenResponse",
    "UserResponse",
]
