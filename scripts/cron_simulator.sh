#!/bin/bash
source .env

echo "BILL ALERT"

while true; do
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Checking for bills due in < 3 days..."
    
    UPCOMING_BILLS=$(curl -s "$API_BASE_URL/bills/upcoming?days=3" | jq -r '.data[] | "\(.name) due on \(.due_date) | Rs.\(.total_amount)"')

    if [ -n "$UPCOMING_BILLS" ]; then
        echo -e "\nALERT: YOU HAVE UPCOMING BILLS!"
        echo "$UPCOMING_BILLS"
    else
        echo "No upcoming bills in the next 3 days."
    fi
    
    echo "----------------------------------------"

    # Change to a smaller number like 10 for testing
    sleep 10
done
