#!/bin/bash
# Family Support Scheduler - Terminal Alert Script

# Ensure standard paths are available
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# Load environment variables
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/.env"

# Fetch upcoming bills (due in 3 days)
UPCOMING_BILLS=$(curl -s --max-time 2 "$API_BASE_URL/bills/upcoming?days=3" | jq -r '.data[] | "\(.name) due on \(.due_date) | Rs.\(.total_amount)"')

# Fetch expired bills
EXPIRED_BILLS=$(curl -s --max-time 2 "$API_BASE_URL/bills/expired" | jq -r '.data[] | "\(.name) was due on \(.due_date) | Rs.\(.total_amount)"')

if [ -n "$EXPIRED_BILLS" ] || [ -n "$UPCOMING_BILLS" ]; then
    echo -e "\n--------------------------------------------------------------------------"
    echo -e "[FAMILY SUPPORT SCHEDULER] ALERT: BILLS NEED ATTENTION!"
    
    if [ -n "$EXPIRED_BILLS" ]; then
        echo -e "\n[!!! EXPIRED BILLS !!!]"
        echo -e "$EXPIRED_BILLS"
    fi
    
    if [ -n "$UPCOMING_BILLS" ]; then
        echo -e "\n[Upcoming Due Bills]"
        echo -e "$UPCOMING_BILLS"
    fi
    
    echo -e "--------------------------------------------------------------------------\n"
else
    # Case where no due bills exist
    echo -e "\n[FAMILY SUPPORT SCHEDULER] All caught up! No upcoming or expired bills found.\n"
fi