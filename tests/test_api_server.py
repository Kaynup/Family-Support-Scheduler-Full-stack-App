import os
import requests
from dotenv import load_dotenv
from datetime import date, timedelta

load_dotenv()
BASE_URL = os.getenv('API_BASE_URL')

def test_health():
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise AssertionError(f"Backend must be running at {BASE_URL}") from exc
    
    assert response.json() == {"message":"backend is live"}
    print("\n\n", response.json())

def test_create_bill():
    payload = {
        "name": "test-name",
        "due_date": (date.today() + timedelta(days=3)).isoformat(),
        "total_amount": 200,
        "category": "testing",
        "status": "UNPAID"
        }
    try:
        response = requests.post(f"{BASE_URL}/bills/new", json=payload, timeout=5)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise AssertionError(f"Something went wrong: {exc}")
    
    assert response.json()["OK"] == True
    print(response.json()["message"])