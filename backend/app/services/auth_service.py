"""
Authentication business logic.

Responsibilities:
    - Password hashing and verification via passlib/bcrypt
    - JWT creation and decoding via python-jose
    - User registration and login flows
    - Role enforcement helper used by route dependencies

This module never calls route-level constructs directly. It returns plain
dicts or raises typed exceptions. Route handlers map those to HTTP responses.
"""

import hashlib
from datetime import UTC, datetime, timedelta

import mysql.connector
from jose import JWTError, jwt
from passlib.context import CryptContext

from ..constants import ROLE_BENEFICIARY, ROLE_SENDER
from ..core.config import settings
from ..core.exceptions import AuthenticationError, UnauthorizedRoleError
from ..core.logging_config import logger
from ..db import queries as dbq

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password):
    """Returns the raw SHA-256 hex digest of the password."""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(plain_password, hashed_password):
    """Returns True if the plain_password hashes to the stored hashed_password."""
    return hash_password(plain_password) == hashed_password


def create_access_token(user_id, username, role):
    """
    Encodes a JWT containing user_id, username, and role.
    The token expires after jwt_expire_minutes minutes.
    """
    expire = datetime.now(UTC) + timedelta(minutes=settings.jwt_expire_minutes)
    payload = {
        "sub": str(user_id),
        "username": username,
        "role": role,
        "exp": expire,
    }
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def decode_access_token(token):
    """
    Decodes and validates a JWT string.
    Raises AuthenticationError if the token is invalid or expired.
    Returns the decoded payload dict on success.
    """
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        return payload
    except JWTError as exc:
        raise AuthenticationError(f"Invalid or expired token: {exc}")


def register_user(username, password, role):
    """
    Creates a new user with a hashed password.
    Raises ValueError if the username is already taken or the role is invalid.
    Returns a UserResponse-shaped dict on success.
    """
    if role not in (ROLE_SENDER, ROLE_BENEFICIARY):
        raise ValueError(f"Invalid role '{role}'. Must be '{ROLE_SENDER}' or '{ROLE_BENEFICIARY}'.")

    logger.info("Registering user username=%s role=%s", username, role)
    hashed = hash_password(password)
    try:
        new_id = dbq.insert_user(username=username, password=hashed, role=role)
    except mysql.connector.IntegrityError:
        logger.warning("Registration failed: username already exists username=%s", username)
        raise ValueError(f"Username '{username}' is already taken.")

    logger.info("Registered user id=%s username=%s role=%s", new_id, username, role)
    return {"id": new_id, "username": username, "role": role}


def login_user(username, password):
    """
    Verifies credentials and returns a token envelope on success.
    Raises AuthenticationError if the username does not exist or the password is wrong.
    """
    row = dbq.select_user_by_username(username)
    if not row:
        logger.warning("Login failed: unknown username=%s", username)
        raise AuthenticationError("Invalid username or password.")

    user_id, db_username, password_hash, role, _created_at = row

    if not verify_password(password, password_hash):
        logger.warning("Login failed: invalid password username=%s", username)
        raise AuthenticationError("Invalid username or password.")

    token = create_access_token(user_id=user_id, username=db_username, role=role)
    logger.info("Login successful user_id=%s username=%s role=%s", user_id, db_username, role)
    return {
        "access_token": token,
        "token_type": "bearer",
        "role": role,
        "username": db_username,
    }


def get_current_user(token):
    """
    Decodes a bearer token and returns the user payload dict.
    Raises AuthenticationError if the token is invalid.
    Used by FastAPI dependencies in dependencies.py.
    """
    return decode_access_token(token)


def require_role(user_payload, required_role):
    """
    Asserts that the decoded token payload carries the required role.
    Raises UnauthorizedRoleError if the role does not match.
    """
    if user_payload.get("role") != required_role:
        raise UnauthorizedRoleError(f"This action requires the '{required_role}' role.")
