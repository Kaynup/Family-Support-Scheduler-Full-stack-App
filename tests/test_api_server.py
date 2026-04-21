import os
import requests
from dotenv import load_dotenv

load_dotenv()
BASE_URL = os.getenv('API_BASE_URL')

def test_health():
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise AssertionError(f"Backend must be running at {BASE_URL}") from exc
    
    assert response.json() == {"message":"backend is live"}