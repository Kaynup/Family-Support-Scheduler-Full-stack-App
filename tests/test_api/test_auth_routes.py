from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@patch("app.routes.auth_routes.register_user")
def test_register_endpoint_success(mock_register):
    mock_register.return_value = {"id": 1, "username": "newuser", "role": "beneficiary"}
    payload = {"username": "newuser", "password": "password123", "role": "beneficiary"}
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 201
    assert response.json() == {"id": 1, "username": "newuser", "role": "beneficiary"}


@patch("app.routes.auth_routes.login_user")
def test_login_endpoint_success(mock_login):
    mock_login.return_value = {
        "access_token": "token123",
        "token_type": "bearer",
        "role": "sender",
        "username": "testuser",
    }
    payload = {"username": "testuser", "password": "password123"}
    response = client.post("/auth/login", json=payload)
    assert response.status_code == 200
    assert response.json()["access_token"] == "token123"
    assert response.json()["role"] == "sender"


@patch("app.routes.auth_routes.login_user")
def test_login_endpoint_invalid_credentials(mock_login):
    from app.core.exceptions import AuthenticationError

    mock_login.side_effect = AuthenticationError("Invalid username or password.")
    payload = {"username": "wrong", "password": "wrong"}
    response = client.post("/auth/login", json=payload)
    assert response.status_code == 401
    assert "Invalid username" in response.json()["detail"]
