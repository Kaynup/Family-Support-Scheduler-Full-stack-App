#!/bin/bash
source ../.env

read -p "Bill Name: " name
read -p "Amount: " amount
read -p "Due Date (YYYY-MM-DD): " due
read -p "Category of bill: " tag

payload=$(jq -n \
    --arg name "$name" \
    --arg amount "$amount" \
    --arg due "$due" \
    --arg tag "$tag" \
    '{name: $name, total_amount: ($amount|tonumber), due_date: $due, category: $tag}')

curl -s -X POST "$API_BASE_URL/bills/new" \
    -H "Content-Type: application/json" \
    -d "$payload" | jq