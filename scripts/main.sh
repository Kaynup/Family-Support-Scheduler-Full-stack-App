#!/bin/bash

source ".env"

echo -e "\n============ Bill Management System ============\n"

# Run health check at startup
bash "commands/health.sh"

echo "+--------------------------------------------+"
echo -e "\n[Commands]"
echo "+--------------------------------------------+"
echo "| all            - View all bills            |"
echo "| upcoming <n>   - Upcoming bills in n days  |"
echo "| add            - Create new bill           |"
echo "| delete         - Delete a bill             |"
echo "| change         - Change bill status        |"
echo "| q / exit       - Quit                      |"
echo "+--------------------------------------------+"


while true; do
    echo -ne "\nEnter command: "
    read -r input

    case "$input" in
        "q"|"exit")
            echo "Exiting..."
            break
            ;;

        "all")
            bash "commands/list_all.sh"
            ;;

        "add")
            bash "commands/add_bill.sh"
            ;;

        "delete")
            bash "commands/delete_bill.sh"
            ;;

        "change")
            bash "commands/change_status.sh"
            ;;

        upcoming*)
            days=$(echo "$input" | awk '{print $2}')
            bash "commands/upcoming.sh" "$days"
            ;;

        *)
            echo "Invalid command"
            ;;
    esac

    echo "+--------------------------------------------+"
    echo "| all | upcoming<n> | add | delete | change  |"
    echo "| q / exit to quit                           |"
    echo "+--------------------------------------------+"


done

echo -e "\n================================================\n"