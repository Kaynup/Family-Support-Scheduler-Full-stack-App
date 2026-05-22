# Database Classes and Functions

## Scope
The database layer is SQL-first. There are no Python classes here; the useful callables are the query helpers that map to the tables in `schema.sql`.

## Query Functions Re-Exported by `backend/app/db/queries/__init__.py`
- User queries: `insert_user`, `select_user_by_username`, `select_user_by_id`, `select_users_by_role`.
- Bill queries: `insert_bill`, `select_all_bills`, `select_bill_by_id`, `select_bills_by_name`, `select_bills_by_beneficiary`, `select_upcoming_bills`, `select_expired_bills`, `update_bill_status`, `soft_delete_bill_by_id`.
- Remittance queries: `insert_remittance_transaction`, `select_remittance_by_bill_id`, `select_remittance_by_sender_id`, `select_remittance_by_beneficiary_id`.

## SQL Files
- `database/schema.sql` defines the actual tables, constraints, and foreign keys.
- `database/sample-data.sql` seeds development data for local testing.

## Notes
When query behavior changes, update the corresponding service documentation in `docs/backend/` at the same time.