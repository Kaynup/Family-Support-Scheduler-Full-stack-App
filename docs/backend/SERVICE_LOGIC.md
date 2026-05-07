# Service Logic

The `app/services/` layer contains all core business logic, decoupled from HTTP and database details.

## Auth Service (`auth_service.py`)
Handles password hashing (bcrypt) and JWT encoding/decoding (python-jose).
- `register_user`: Hashes password, saves user to DB.
- `login_user`: Verifies credentials against DB hash, issues JWT.
- `get_current_user` / `require_role`: Checks token validity and permissions.

## Bill Service (`bill_service.py`)
Consolidates all bill lifecycle logic.
- `create_bill`, `list_bills`, `mark_bill_status`, `delete_bill`, `search_bills_by_name`.
- Utilizes `_format_bill_row` to standardize database outputs into response dicts.

## Remittance Service (`remittance_service.py`)
Handles the payment workflow.
- `pay_bill_via_remittance`: Validates bill is unpaid and amount covers total. Inserts a `COMPLETED` transaction record and updates bill status to `PAID` within a consistent flow.
- `get_remittance_history_for_sender`: Retrieves outgoing transactions.
