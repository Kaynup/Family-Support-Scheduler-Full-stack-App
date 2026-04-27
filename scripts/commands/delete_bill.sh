#!/bin/bash
source ../.env

read -p "Enter Bill ID to delete: " id

curl -s -X DELETE "$API_BASE_URL/bills/$id" | jq