#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../../.env"

echo "[All Bills]"
curl -s "$API_BASE_URL/bills/all" \
| jq -r '.data[] | " * ID : \(.id)       \(.name)       ₹\(.total_amount)          due: \(.due_date)"'