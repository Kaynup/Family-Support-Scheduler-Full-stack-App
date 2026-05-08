"""
Pydantic schemas for the authentication domain.

RegisterRequest  — validates POST /auth/register payloads.
LoginRequest     — validates POST /auth/login payloads.
TokenResponse    — shape of the successful login response.
UserResponse     — public user data returned after registration.
"""

from pydantic import BaseModel, Field
from ..constants import ROLE_BENEFICIARY, ROLE_SENDER


class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=100)
    password: str = Field(..., min_length=8)
    role: str = Field(default=ROLE_BENEFICIARY)

    def role_is_valid(self):
        return self.role in (ROLE_SENDER, ROLE_BENEFICIARY)


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    username: str


class UserResponse(BaseModel):
    id: int
    username: str
    role: str
