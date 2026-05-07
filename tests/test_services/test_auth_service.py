import pytest
from unittest.mock import patch
from app.services.auth_service import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token,
    register_user,
    login_user
)
from app.core.exceptions import AuthenticationError
from app.constants import ROLE_BENEFICIARY, ROLE_SENDER
import mysql.connector

def test_hash_verify_password():
    pwd = "mysecretpassword"
    hashed = hash_password(pwd)
    assert hashed != pwd
    assert verify_password(pwd, hashed) is True
    assert verify_password("wrong", hashed) is False

def test_create_decode_token():
    token = create_access_token(1, "testuser", ROLE_SENDER)
    payload = decode_access_token(token)
    assert payload["sub"] == "1"
    assert payload["username"] == "testuser"
    assert payload["role"] == ROLE_SENDER
    assert "exp" in payload

def test_decode_expired_token():
    with patch('app.services.auth_service.settings') as mock_settings:
        mock_settings.jwt_expire_minutes = -1 # Expired
        mock_settings.jwt_secret_key = "secret"
        mock_settings.jwt_algorithm = "HS256"
        token = create_access_token(1, "testuser", ROLE_SENDER)
    
    with pytest.raises(AuthenticationError):
        decode_access_token(token)

@patch('app.services.auth_service.dbq.insert_user')
def test_register_user_success(mock_insert):
    mock_insert.return_value = 1
    out = register_user("newuser", "password123", ROLE_BENEFICIARY)
    assert out["id"] == 1
    assert out["username"] == "newuser"
    assert out["role"] == ROLE_BENEFICIARY

@patch('app.services.auth_service.dbq.insert_user')
def test_register_user_duplicate_username(mock_insert):
    mock_insert.side_effect = mysql.connector.IntegrityError("Duplicate entry")
    with pytest.raises(ValueError, match="already taken"):
        register_user("duplicate", "password123", ROLE_BENEFICIARY)

@patch('app.services.auth_service.dbq.select_user_by_username')
@patch('app.services.auth_service.verify_password')
def test_login_user_success(mock_verify, mock_select):
    mock_select.return_value = (1, "testuser", "hashed", ROLE_SENDER, "2026-01-01")
    mock_verify.return_value = True
    
    out = login_user("testuser", "password123")
    assert "access_token" in out
    assert out["token_type"] == "bearer"
    assert out["role"] == ROLE_SENDER

@patch('app.services.auth_service.dbq.select_user_by_username')
@patch('app.services.auth_service.verify_password')
def test_login_user_wrong_password(mock_verify, mock_select):
    mock_select.return_value = (1, "testuser", "hashed", ROLE_SENDER, "2026-01-01")
    mock_verify.return_value = False
    
    with pytest.raises(AuthenticationError):
        login_user("testuser", "wrongpwd")

@patch('app.services.auth_service.dbq.select_user_by_username')
def test_login_user_not_found(mock_select):
    mock_select.return_value = None
    with pytest.raises(AuthenticationError):
        login_user("unknown", "password123")
