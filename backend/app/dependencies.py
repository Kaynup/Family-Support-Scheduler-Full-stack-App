"""
FastAPI dependency functions for authentication and role enforcement.

These are passed to route handlers via Depends(). They extract the token
from the Authorization header, decode it, and optionally assert a role.
Placing all dependency logic here keeps route files free of auth wiring.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .services.auth_service import get_current_user
from .core.exceptions import AuthenticationError
from .constants import ROLE_SENDER, ROLE_BENEFICIARY

_bearer_scheme = HTTPBearer()


def get_current_user_dependency(credentials: HTTPAuthorizationCredentials = Depends(_bearer_scheme)):
    """
    Extracts and validates the JWT from the Authorization: Bearer header.
    Raises 401 if the token is missing, malformed, or expired.
    Returns the decoded token payload dict.
    """
    try:
        return get_current_user(credentials.credentials)
    except AuthenticationError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc))


def require_beneficiary_role(current_user: dict = Depends(get_current_user_dependency)):
    """
    Asserts the authenticated user holds the beneficiary role.
    Raises 403 if the role does not match.
    Returns the current user payload dict on success.
    """
    if current_user.get("role") != ROLE_BENEFICIARY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"This action requires the '{ROLE_BENEFICIARY}' role.",
        )
    return current_user


def require_sender_role(current_user: dict = Depends(get_current_user_dependency)):
    """
    Asserts the authenticated user holds the sender role.
    Raises 403 if the role does not match.
    Returns the current user payload dict on success.
    """
    if current_user.get("role") != ROLE_SENDER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"This action requires the '{ROLE_SENDER}' role.",
        )
    return current_user
