import os
import requests
from dotenv import load_dotenv
from datetime import date, timedelta
import time

from backend.app.db.queries import select_all, delete_bill_by_id

load_dotenv()
BASE_URL = os.getenv('API_BASE_URL')


def _create_temp_bill_via_api():
    unique_name = f"api-test-{time.time_ns()}"
    payload = {
        "name": unique_name,
        "due_date": (date.today() + timedelta(days=3)).isoformat(),
        "total_amount": 200,
        "category": "testing",
        "status": "UNPAID",
    }
    response = requests.post(f"{BASE_URL}/bills/new", json=payload, timeout=5)
    response.raise_for_status()
    return unique_name


def _get_bill_id_by_name(name):
    rows = select_all()
    return next(r[0] for r in rows if r[1] == name)

def test_health():
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise AssertionError(f"Backend must be running at {BASE_URL}") from exc
    
    assert response.json() == {"message":"backend is live"}
    print("\n\n", response.json())

def test_update_status():
    name = _create_temp_bill_via_api()
    bill_id = _get_bill_id_by_name(name)
    payload = {"status": "PAID"}
    try:
        response = requests.put(f"{BASE_URL}/bills/{bill_id}", json=payload, timeout=5)
        response.raise_for_status()
        assert response.json()["OK"] is True
        print(response.json()["message"])
    except requests.RequestException as exc:
        raise AssertionError(f"Something went wrong: {exc}")
    finally:
        delete_bill_by_id(bill_id)

def test_delete_bill():
    name = _create_temp_bill_via_api()
    bill_id = _get_bill_id_by_name(name)
    try:
        response = requests.delete(f"{BASE_URL}/bills/{bill_id}", timeout=5)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise AssertionError(f"Something went wrong: {exc}")
    
    assert response.json()["OK"] == True
    print(response.json()["message"])

def test_create_bill():
    payload = {
        "name": f"test-name-{time.time_ns()}",
        "due_date": (date.today() + timedelta(days=3)).isoformat(),
        "total_amount": 200,
        "category": "testing",
        "status": "UNPAID",
    }
    try:
        response = requests.post(f"{BASE_URL}/bills/new", json=payload, timeout=5)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise AssertionError(f"Something went wrong: {exc}")
    
    assert response.json()["OK"] is True
    print(response.json()["message"])

    bill_id = _get_bill_id_by_name(payload["name"])
    delete_bill_by_id(bill_id)