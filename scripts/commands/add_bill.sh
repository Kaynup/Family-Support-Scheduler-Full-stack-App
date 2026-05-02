#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../../.env"

read -p "Bill Name: " name
read -p "Amount: " amount
read -p "Due Date (YYYY-MM-DD): " due
read -p "Category of bill: " tag
read -p "Recurring interval (NONE/WEEKLY/MONTHLY): " interval

payload=$(jq -n \
    --arg name "$name" \
    --arg amount "$amount" \
    --arg due "$due" \
    --arg tag "$tag" \
    --arg interval "$interval" \
    '{name: $name, total_amount: ($amount|tonumber), due_date: $due, category: $tag, recurring_interval: $interval}')

curl -s -X POST "$API_BASE_URL/bills/new" \
    -H "Content-Type: application/json" \
    -d "$payload" | jq