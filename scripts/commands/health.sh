#!/bin/bash
source ../.env

echo "[Health Check]"
curl -s "$API_BASE_URL/health" | jq