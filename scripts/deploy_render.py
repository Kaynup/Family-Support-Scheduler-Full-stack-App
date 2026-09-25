"""
Automated Deployer for Render via Official REST API.

Securely reads the Render API key from ~/.secrets/render_api.txt,
checks for existing services or creates a new Web Service on the Free Tier,
configures environment variables, triggers deployment, and monitors liveness.
"""

import json
import os
import sys
import time
import urllib.error
import urllib.request

API_KEY_FILE = os.path.expanduser("~/.secrets/render_api.txt")
REPO_URL = "https://github.com/Kaynup/Family-Support-Scheduler-Full-stack-App"
SERVICE_NAME = "family-scheduler-api"


def get_api_key():
    if not os.path.exists(API_KEY_FILE):
        print(f"Error: Render API key file not found at {API_KEY_FILE}", file=sys.stderr)
        sys.exit(1)
    with open(API_KEY_FILE) as f:
        key = f.read().strip()
    if not key:
        print("Error: Render API key is empty.", file=sys.stderr)
        sys.exit(1)
    return key


def make_request(method, endpoint, payload=None, api_key=None):
    url = f"https://api.render.com/v1/{endpoint.lstrip('/')}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    data = json.dumps(payload).encode("utf-8") if payload else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req) as resp:
            body = resp.read().decode("utf-8")
            return json.loads(body) if body else {}
    except urllib.error.HTTPError as err:
        error_body = err.read().decode("utf-8")
        print(f"Render API HTTP {err.code} on {method} {endpoint}: {error_body}", file=sys.stderr)
        raise


def get_owner_id(api_key):
    owners = make_request("GET", "owners", api_key=api_key)
    if not owners:
        raise RuntimeError("No Render owners found for this API key.")
    owner_id = owners[0].get("owner", {}).get("id")
    owner_name = owners[0].get("owner", {}).get("name")
    print(f"Authenticated with Render owner: {owner_name} ({owner_id})")
    return owner_id


def extract_service_info(data):
    """Safely extracts service_id and service_url from Render API responses."""
    if not data:
        return None, None
    inner = data.get("service", data)
    sid = inner.get("id")
    details = inner.get("serviceDetails") or {}
    url = details.get("url") or inner.get("url")
    return sid, url


def find_existing_service(owner_id, api_key):
    services = make_request("GET", f"services?ownerId={owner_id}&limit=50", api_key=api_key)
    for s in services:
        srv = s.get("service", s)
        if srv.get("name") == SERVICE_NAME:
            return srv
    return None


def get_latest_deploy(service_id, api_key):
    try:
        deploys = make_request("GET", f"services/{service_id}/deploys?limit=5", api_key=api_key)
        if deploys and len(deploys) > 0:
            first = deploys[0]
            return first.get("deploy", first)
    except Exception as err:
        print(f"Notice: Could not fetch deploy status ({err})")
    return None


def wait_for_deploy(service_id, api_key, target_deploy_id=None, max_wait_sec=180):
    print("\nMonitoring deployment progress on Render...")
    start_time = time.time()
    while time.time() - start_time < max_wait_sec:
        latest = get_latest_deploy(service_id, api_key)
        if latest:
            status = latest.get("status")
            deploy_id = latest.get("id")
            if target_deploy_id and deploy_id != target_deploy_id:
                print(f"  ... Deploy {target_deploy_id} starting (latest: {deploy_id})")
            elif status == "live":
                print(f"  ✓ Deployment {deploy_id} is LIVE!")
                return True
            elif status in ("build_failed", "update_failed", "canceled"):
                print(f"  ⚠️ Deployment {deploy_id} ended with status: {status}")
                return False
            else:
                print(f"  ... Deploy {deploy_id} status: {status} (building...)")
        time.sleep(8)
    return False


ENV_VARS = [
    {"key": "PYTHON_VERSION", "value": "3.11.10"},
    {"key": "PYTHONPATH", "value": "backend"},
    {"key": "DB_HOST", "value": "gateway01.ap-southeast-1.prod.aws.tidbcloud.com"},
    {"key": "DB_PORT", "value": "4000"},
    {"key": "DB_USER", "value": "iVAAKAKjk5Q1VM6.root"},
    {"key": "DB_PASSWORD", "value": "usGtgNF4rMxM1kk0"},
    {"key": "DB_NAME", "value": "family_supp_sche"},
    {"key": "DB_TABLE", "value": "bills"},
    {"key": "DB_CONN_POOLING", "value": "5"},
    {"key": "DB_SSL", "value": "true"},
    {
        "key": "JWT_SECRET_KEY",
        "value": "e83a9f4c71b6205e48d39f21aa47bc95de2c6104f7b24981cae9352e8d076a14",
    },
    {"key": "JWT_ALGORITHM", "value": "HS256"},
    {"key": "JWT_EXPIRE_MINUTES", "value": "480"},
    {
        "key": "ALLOWED_ORIGINS",
        "value": "https://frontend-two-hazel-16.vercel.app,http://localhost:8003,http://127.0.0.1:8003",
    },
]


def sync_env_vars(service_id, api_key):
    """Ensures all production database and security environment variables are set in Render."""
    print(f"Checking environment variables on Render for service {service_id}...")
    try:
        current_vars = make_request("GET", f"services/{service_id}/env-vars", api_key=api_key)
        existing_keys = {
            item.get("envVar", {}).get("key") for item in current_vars if "envVar" in item
        }
        print(f"  Current keys on Render ({len(existing_keys)}): {list(existing_keys)}")

        if "DB_HOST" not in existing_keys or "DB_PASSWORD" not in existing_keys:
            print("  ⚠️ Database variables missing on Render! Syncing via PUT /env-vars...")
            make_request(
                "PUT", f"services/{service_id}/env-vars", payload=ENV_VARS, api_key=api_key
            )
            print("  ✓ Environment variables successfully updated on Render!")
            return True
        else:
            print("  ✓ DB environment variables already configured on Render.")
            return False
    except Exception as err:
        print(f"  Notice during env var check/sync: {err}")
        return False


def create_service(owner_id, api_key):
    print(f"Creating new Render Web Service '{SERVICE_NAME}'...")
    payload = {
        "type": "web_service",
        "name": SERVICE_NAME,
        "ownerId": owner_id,
        "repo": REPO_URL,
        "branch": "main",
        "serviceDetails": {
            "env": "python",
            "plan": "free",
            "region": "singapore",
            "healthCheckPath": "/health",
            "envSpecificDetails": {
                "buildCommand": "pip install -r requirements.txt",
                "startCommand": "uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT",
            },
            "envVars": ENV_VARS,
        },
    }

    resp = make_request("POST", "services", payload=payload, api_key=api_key)
    return resp


def trigger_deploy(service_id, api_key):
    print(f"Triggering manual deploy for service ID: {service_id}...")
    resp = make_request(
        "POST",
        f"services/{service_id}/deploys",
        payload={"clearCache": "do_not_clear"},
        api_key=api_key,
    )
    return resp.get("deploy", resp)


def main():
    api_key = get_api_key()
    owner_id = get_owner_id(api_key)

    srv = find_existing_service(owner_id, api_key)
    if srv:
        service_id, service_url = extract_service_info(srv)
        print(f"✓ Found existing Render service '{SERVICE_NAME}'")
        print(f"  Service ID:  {service_id}")
        print(f"  Service URL: {service_url}")

        sync_env_vars(service_id, api_key)

        deploy_resp = trigger_deploy(service_id, api_key)
        deploy_id = deploy_resp.get("id")
        print(f"  Deployment initiated: {deploy_id}")
        wait_for_deploy(service_id, api_key, target_deploy_id=deploy_id)
    else:
        new_srv = create_service(owner_id, api_key)
        service_id, service_url = extract_service_info(new_srv)
        print(f"✓ Service created successfully! (ID: {service_id}, URL: {service_url})")
        sync_env_vars(service_id, api_key)
        wait_for_deploy(service_id, api_key)

    # Fallback URL if Render hasn't populated serviceDetails.url yet
    if not service_url:
        service_url = f"https://{SERVICE_NAME}.onrender.com"

    print("\n========================================================")
    print(f"🚀 Render Backend Service URL: {service_url}")
    print("========================================================")

    # Health check probe
    print(f"\nProbing health check endpoint: {service_url}/health ...")
    try:
        req = urllib.request.Request(
            f"{service_url.rstrip('/')}/health",
            headers={"User-Agent": "FamilyScheduler-Deployer"},
        )
        with urllib.request.urlopen(req, timeout=8) as resp:
            body = resp.read().decode("utf-8")
            print(f"✓ Health check SUCCESS (HTTP {resp.status}): {body}")
    except Exception as e:
        print(f"ℹ Health check notice: {e}")

    # Database health check probe
    print(f"\nProbing database health check endpoint: {service_url}/health/db ...")
    try:
        req = urllib.request.Request(
            f"{service_url.rstrip('/')}/health/db",
            headers={"User-Agent": "FamilyScheduler-Deployer"},
        )
        with urllib.request.urlopen(req, timeout=8) as resp:
            body = resp.read().decode("utf-8")
            print(f"✓ Database check result (HTTP {resp.status}): {body}")
    except Exception as e:
        print(f"ℹ Database check notice: {e}")


if __name__ == "__main__":
    main()
