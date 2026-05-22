# Backend Classes and Functions

## Scope
There are no custom OOP service classes here; the backend is built around route handlers, service functions, dependencies, and query helpers.

## Main Functions
- `main.py`: `health_check()` returns the liveness payload and the module registers `bill_routes`, `auth_routes`, `remittance_routes`, and `user_routes`.
- `auth_routes.py`: `register_route()`, `login_route()`, and `auth_validation_exception_handler()`.
- `bill_routes.py`: `create_bill_route()`, `search_bills_route()`, `list_bills_route()`, `list_upcoming_bills_route()`, `list_expired_bills_route()`, `update_bill_status_route()`, and `delete_bill_route()`.
- `remittance_routes.py`: `pay_bill_route()`, `remittance_history_route()`, and `remittance_history_beneficiary_route()`.
- `user_routes.py`: `list_users_route()`.
- `dependencies.py`: `get_current_user_dependency()`, `require_beneficiary_role()`, and `require_sender_role()`.

## Service Functions
- `auth_service.py`: `hash_password()`, `verify_password()`, `create_access_token()`, `decode_access_token()`, `register_user()`, `login_user()`, `get_current_user()`, and `require_role()`.
- `bill_service.py`: `_format_bill_row()`, `create_bill()`, `list_bills()`, `get_bill_by_id()`, `mark_bill_status()`, `delete_bill()`, and `search_bills_by_name()`.
- `remittance_service.py`: `_extract_bill_payment_fields()`, `_format_transaction_row()`, `pay_bill_via_remittance()`, `get_remittance_history_for_sender()`, and `get_remittance_history_for_beneficiary()`.

## Query Layer
- `backend/app/db/queries/__init__.py` re-exports the SQL helpers so service code can use `dbq.*` consistently.
- The exported query names include `insert_user`, `select_user_by_username`, `select_user_by_id`, `select_users_by_role`, `insert_bill`, `select_all_bills`, `select_bill_by_id`, `select_bills_by_name`, `select_bills_by_beneficiary`, `select_upcoming_bills`, `select_expired_bills`, `update_bill_status`, `soft_delete_bill_by_id`, `insert_remittance_transaction`, `select_remittance_by_bill_id`, `select_remittance_by_sender_id`, and `select_remittance_by_beneficiary_id`.

## Notes
When you add a new endpoint, document the route handler, the service function it calls, and the query helper it depends on.