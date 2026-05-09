# Variables & Functions (Backend)

The backend utilizes strict typing and constants across the service execution layer.

## Core Constants (Defined in `backend/app/constants.py`)
- `ROLE_SENDER = "sender"`
- `ROLE_BENEFICIARY = "beneficiary"`
- `STATUS_UNPAID = "UNPAID"`
- `STATUS_PAID = "PAID"`
- `RECURRING_NONE = "NONE"`
- `RECURRING_WEEKLY = "WEEKLY"`
- `RECURRING_MONTHLY = "MONTHLY"`

## Critical Functions

### `auth_service.py`
- **`create_access_token(user_id, username, role)`**: Generates a JWT. The `user_id` is embedded in the `sub` claim.
- **`verify_password(plain_password, hashed_password)`**: Uses `passlib` to cryptographically compare strings.

### `remittance_service.py`
- **`pay_bill_via_remittance(bill_id, sender_user_id, amount, currency, payment_method)`**:
  The most complex function in the application. It:
  1. Validates the bill exists and is `UNPAID`.
  2. Inserts a record into the `remittance` table.
  3. Updates the `bill_status` to `PAID`.
  4. Automatically calculates the next occurrence for `MONTHLY` or `WEEKLY` intervals using `calendar.monthrange` or `timedelta(days=7)`.
  5. Inserts a new, identical `UNPAID` bill directly into the database assigned to the beneficiary.

### `bill_service.py`
- **`list_bills(upcoming_only=False, expired_only=False, days=3, beneficiary_id=None)`**:
  Central routing logic for querying bills. Used dynamically by `/bills/all`, `/bills/upcoming`, and `/bills/expired` endpoints.

### `dependencies.py`
- **`get_current_user_dependency(credentials)`**: Decodes the Bearer token.
- **`require_beneficiary_role(current_user)`**: Dependency that raises an HTTP `403 Forbidden` if the `current_user["role"]` is not `beneficiary`.
