"""
schemas/ — Pydantic request and response models organized by domain.

Re-exports all schema classes so routes import from a single location:
    from app.schemas import BillCreateRequest, LoginRequest, ...
"""

from .bill_schemas import BillCreateRequest, BillUpdateRequest, BillResponse, BillListResponse
from .auth_schemas import RegisterRequest, LoginRequest, TokenResponse, UserResponse
from .remittance_schemas import RemittanceCreateRequest, RemittanceResponse

__all__ = [
    "BillCreateRequest",
    "BillUpdateRequest",
    "BillResponse",
    "BillListResponse",
    "RegisterRequest",
    "LoginRequest",
    "TokenResponse",
    "UserResponse",
    "RemittanceCreateRequest",
    "RemittanceResponse",
]
