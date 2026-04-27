#!/bin/bash
source ../.env

bash -e "commands/upcoming.sh"

echo -e "\n"

read -p "Bill ID: " id
read -p "Change Status (paid/unpaid): " status

payload=$(jq -n --arg status "$status" '{status: $status}')

curl -s -X PATCH "$API_BASE_URL/bills/$id" \
    -H "Content-Type: application/json" \
    -d "$payload" | jq