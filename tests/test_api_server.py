import os
import requests
from dotenv import load_dotenv
from datetime import date, timedelta
import time

from backend.app.db.queries import delete_bill_by_id, delete_bill_by_id_HARD

load_dotenv()
BASE_URL = os.getenv('API_BASE_URL')


def _create_temp_bill_via_api():
    unique_name = f"pytest-api-{time.time_ns()}"
    payload = {
        "name": unique_name,
        "due_date": (date.today() + timedelta(days=3)).isoformat(),
        "creation_date": date.today().isoformat(),
        "total_amount": 200,
        "category": "testing",
        "recurring_interval": "NONE",
        "status": "UNPAID"
    }
    response = requests.post(f"{BASE_URL}/bills/new", json=payload, timeout=5)
    response.raise_for_status()
    return response.json()['data']['id']


def test_create_bill():
    bill_id = _create_temp_bill_via_api()
    try:
        assert bill_id > 0
    finally:
        delete_bill_by_id_HARD(bill_id)

def test_update_status():
    bill_id = _create_temp_bill_via_api()
    payload = {"id": bill_id, "status": "PAID"}
    try:
        response = requests.put(f"{BASE_URL}/bills/{bill_id}", json=payload, timeout=5)
        response.raise_for_status()
        assert response.json()["OK"] is True
        print(response.json()["message"])
    except requests.RequestException as exc:
        raise AssertionError(f"Something went wrong: {exc}")
    finally:
        delete_bill_by_id_HARD(bill_id)

def test_delete_bill():
    bill_id = _create_temp_bill_via_api()
    try:
        response = requests.delete(f"{BASE_URL}/bills/{bill_id}", timeout=5)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise AssertionError(f"Something went wrong: {exc}")
    finally:
        delete_bill_by_id_HARD(bill_id)
    
    assert response.json()["OK"] == True
    print(response.json()["message"])

def test_api_search_bills():
    bill_id = _create_temp_bill_via_api()
    try:
        # We need the name of the bill we created
        # Instead of fetching it, let's just use the known unique prefix if we can't fetch it easily.
        # But wait, let's just make it simpler.
        response = requests.get(f"{BASE_URL}/bills/search?name=pytest-api", timeout=5)
        response.raise_for_status()
        results = response.json()["data"]
        assert any(b["id"] == bill_id for b in results)
    finally:
        delete_bill_by_id_HARD(bill_id)