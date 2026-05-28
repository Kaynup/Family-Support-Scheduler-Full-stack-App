"""
Authentication route handlers — /auth prefix.

POST /auth/register  — creates a new user account.
POST /auth/login     — validates credentials and returns a JWT token.
"""

from fastapi import APIRouter, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from ..services.auth_service import register_user, login_user
from ..schemas.auth_schemas import RegisterRequest, LoginRequest, TokenResponse, UserResponse
from ..core.exceptions import AuthenticationError
from ..core.logging_config import logger

router = APIRouter(prefix="/auth", tags=["auth"])


async def auth_validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Cleaner, structured error object for authentication routes.
    Returns a dictionary of { field_name: message } in the 'errors' key.
    """
    errors = {}
    for error in exc.errors():
        field = error.get("loc", [])[-1]
        msg = error.get("msg")
        errors[field] = msg
    
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Validation failed",
            "errors": errors
        }
    )


@router.post("/register", response_model=UserResponse, status_code=201)
def register_route(payload: RegisterRequest):
    """
    Registers a new user with a hashed password.
    Returns 400 if the username is already taken or the role is invalid.
    """
    logger.info("Register route called username=%s role=%s", payload.username, payload.role)
    if not payload.role_is_valid():
        logger.warning("Register route rejected invalid role username=%s role=%s", payload.username, payload.role)
        raise HTTPException(status_code=400, detail=f"Invalid role '{payload.role}'.")
    try:
        return register_user(
            username=payload.username,
            password=payload.password,
            role=payload.role,
        )
    except ValueError as exc:
        logger.warning("Register route failed username=%s error=%s", payload.username, exc)
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        logger.exception("Unexpected register route error username=%s", payload.username)
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/login", response_model=TokenResponse)
def login_route(payload: LoginRequest):
    """
    Authenticates a user and returns a JWT bearer token.
    Returns 401 if credentials are invalid.
    """
    logger.info("Login route called username=%s", payload.username)
    try:
        return login_user(
            username=payload.username,
            password=payload.password
            )
    except AuthenticationError as exc:
        logger.warning("Login route unauthorized username=%s error=%s", payload.username, exc)
        raise HTTPException(status_code=401, detail=str(exc))
    except ValueError as exc:
        logger.warning("Login route bad request username=%s error=%s", payload.username, exc)
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        logger.exception("Unexpected login route error username=%s", payload.username)
        raise HTTPException(status_code=500, detail=str(exc))
