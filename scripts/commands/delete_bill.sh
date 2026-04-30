#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../../.env"

read -p "Enter Bill ID to delete: " id

curl -s -X DELETE "$API_BASE_URL/bills/$id" | jq