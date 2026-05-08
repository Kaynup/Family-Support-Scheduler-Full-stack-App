"""
Authentication route handlers — /auth prefix.

POST /auth/register  — creates a new user account.
POST /auth/login     — validates credentials and returns a JWT token.
"""

from fastapi import APIRouter, HTTPException
from ..services.auth_service import register_user, login_user
from ..schemas.auth_schemas import RegisterRequest, LoginRequest, TokenResponse, UserResponse
from ..core.exceptions import AuthenticationError

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse, status_code=201)
def register_route(payload: RegisterRequest):
    """
    Registers a new user with a hashed password.
    Returns 400 if the username is already taken or the role is invalid.
    """
    if not payload.role_is_valid():
        raise HTTPException(status_code=400, detail=f"Invalid role '{payload.role}'.")
    try:
        return register_user(
            username=payload.username,
            password=payload.password,
            role=payload.role,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/login", response_model=TokenResponse)
def login_route(payload: LoginRequest):
    """
    Authenticates a user and returns a JWT bearer token.
    Returns 401 if credentials are invalid.
    """
    try:
        return login_user(
            username=payload.username,
            password=payload.password
            )
    except AuthenticationError as exc:
        raise HTTPException(status_code=401, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
