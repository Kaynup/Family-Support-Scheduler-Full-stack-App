from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app

# Create a client, we will override auth dependencies for tests that need it
client = TestClient(app)


def override_require_beneficiary_role():
    return {"sub": "1", "username": "testuser", "role": "beneficiary"}


app.dependency_overrides[app.dependency_overrides.get("require_beneficiary_role", lambda: None)] = (
    override_require_beneficiary_role
)


@patch("app.routes.bill_routes.create_bill")
def test_create_bill(mock_create_bill):
    mock_create_bill.return_value = {
        "OK": True,
        "data": {"id": 1},
        "message": "Success",
    }
    payload = {
        "name": "test-api",
        "due_date": "2099-05-01",
        "creation_date": "2099-04-30",
        "total_amount": 200.0,
        "category": "testing",
        "recurring_interval": "NONE",
        "status": "UNPAID",
    }
    # Need to override dependencies to pass role check
    from app.dependencies import require_beneficiary_role

    app.dependency_overrides[require_beneficiary_role] = override_require_beneficiary_role

    response = client.post("/bills/new", json=payload)
    assert response.status_code == 201
    assert response.json()["OK"] is True
    mock_create_bill.assert_called_once()

    app.dependency_overrides.clear()


@patch("app.routes.bill_routes.mark_bill_status")
def test_update_status(mock_mark_status):
    mock_mark_status.return_value = {
        "OK": True,
        "data": {"id": 1},
        "message": "Status updated",
    }
    payload = {"status": "PAID"}
    response = client.put("/bills/1", json=payload)
    assert response.status_code == 200
    assert response.json()["OK"] is True
    mock_mark_status.assert_called_with(1, "PAID")


@patch("app.routes.bill_routes.delete_bill")
def test_delete_bill(mock_delete_bill):
    mock_delete_bill.return_value = {
        "OK": True,
        "data": {"id": 1},
        "message": "Deleted",
    }

    from app.dependencies import require_beneficiary_role

    app.dependency_overrides[require_beneficiary_role] = override_require_beneficiary_role

    response = client.delete("/bills/1")
    assert response.status_code == 200
    assert response.json()["OK"] is True
    mock_delete_bill.assert_called_with(1)

    app.dependency_overrides.clear()


@patch("app.routes.bill_routes.search_bills_by_name")
def test_api_search_bills(mock_search_bills):
    mock_search_bills.return_value = {
        "OK": True,
        "data": [{"id": 1, "name": "pytest-api", "user_id": 1}],
        "message": "Found",
        "total_count": 1,
    }
    from app.dependencies import get_current_user_dependency

    app.dependency_overrides[get_current_user_dependency] = override_require_beneficiary_role

    response = client.get("/bills/search?name=pytest-api")
    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
    mock_search_bills.assert_called_with(name="pytest-api")

    app.dependency_overrides.clear()


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"message": "backend is live"}
