#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../../.env"

DAYS=${1:-3}

echo "[Upcoming Bills in $DAYS days]"

curl -s "$API_BASE_URL/bills/upcoming?days=$DAYS" \
| jq -r '.data[] | " * \(.name) due on \(.due_date) | ₹\(.total_amount)"'