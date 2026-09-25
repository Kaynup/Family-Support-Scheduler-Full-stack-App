from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def override_require_sender_role():
    return {"sub": "1", "username": "senderuser", "role": "sender"}


def override_require_beneficiary_role():
    from fastapi import HTTPException

    raise HTTPException(status_code=403, detail="This action requires the 'sender' role.")


@patch("app.routes.remittance_routes.pay_bill_via_remittance")
def test_pay_endpoint_sender_role_success(mock_pay):
    mock_pay.return_value = {"OK": True, "data": {"transaction_id": 101}}

    from app.dependencies import require_sender_role

    app.dependency_overrides[require_sender_role] = override_require_sender_role

    payload = {"bill_id": 1, "amount": 500.0}
    response = client.post("/remittance/pay", json=payload)

    assert response.status_code == 201
    assert response.json()["OK"] is True
    mock_pay.assert_called_once()

    app.dependency_overrides.clear()


def test_pay_endpoint_beneficiary_role_rejected():
    from app.dependencies import require_sender_role

    app.dependency_overrides[require_sender_role] = override_require_beneficiary_role

    payload = {"bill_id": 1, "amount": 500.0}
    response = client.post("/remittance/pay", json=payload)

    assert response.status_code == 403

    app.dependency_overrides.clear()


@patch("app.routes.remittance_routes.get_remittance_history_for_sender")
def test_history_endpoint_success(mock_history):
    mock_history.return_value = {"OK": True, "data": []}

    from app.dependencies import require_sender_role

    app.dependency_overrides[require_sender_role] = override_require_sender_role

    response = client.get("/remittance/history")

    assert response.status_code == 200
    assert response.json()["OK"] is True
    mock_history.assert_called_with(1)

    app.dependency_overrides.clear()
