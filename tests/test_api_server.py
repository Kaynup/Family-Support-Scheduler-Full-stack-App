from fastapi.testclient import TestClient
from unittest.mock import patch
from backend.app.main import app

client = TestClient(app)

@patch('backend.app.routes.api_endpoints.create_bill_service')
def test_create_bill(mock_create_service):
    mock_create_service.return_value = {"OK": True, "data": {"id": 1}, "message": "Success"}
    payload = {
        "name": "test-api",
        "due_date": "2099-05-01",
        "creation_date": "2099-04-30",
        "total_amount": 200,
        "category": "testing",
        "recurring_interval": "NONE",
        "status": "UNPAID"
    }
    response = client.post("/bills/new", json=payload)
    assert response.status_code == 200
    assert response.json()["OK"] is True
    mock_create_service.assert_called_once()

@patch('backend.app.routes.api_endpoints.mark_bill_status_service')
def test_update_status(mock_mark_status):
    mock_mark_status.return_value = {"OK": True, "data": {"id": 1}, "message": "Status updated"}
    payload = {"id": 1, "status": "PAID"}
    response = client.put("/bills/1", json=payload)
    assert response.status_code == 200
    assert response.json()["OK"] is True
    mock_mark_status.assert_called_with(1, "PAID")

@patch('backend.app.routes.api_endpoints.delete_bill_service')
def test_delete_bill(mock_delete_service):
    mock_delete_service.return_value = {"OK": True, "data": {"id": 1}, "message": "Deleted"}
    response = client.delete("/bills/1")
    assert response.status_code == 200
    assert response.json()["OK"] is True
    mock_delete_service.assert_called_with(1)

@patch('backend.app.routes.api_endpoints.select_by_name_service')
def test_api_search_bills(mock_search_service):
    mock_search_service.return_value = {"OK": True, "data": [{"id": 1, "name": "pytest-api"}], "message": "Found"}
    response = client.get("/bills/search?name=pytest-api")
    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
    mock_search_service.assert_called_with(name="pytest-api")

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"message": "backend is live"}