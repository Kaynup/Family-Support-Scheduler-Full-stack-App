# Database Variable Flow

## Scope
This folder defines the MySQL schema and seed data used by the backend query helpers.

## Real Variables
- Database name: `family_supp_sche`.
- Tables: `users`, `bills`, and `remittance_transactions`.
- User fields: `user_id`, `user_name`, `user_pass`, `user_role`, `user_created_on`.
- Bill fields: `bill_id`, `bill_name`, `bill_status`, `user_id`, `creation_date`, `due_date`, `total_amount`, `category`, `recurring_interval`, `is_deleted`.
- Remittance fields: `transaction_id`, `bill_id`, `sender_user_id`, `beneficiary_user_id`, `amount`, `currency`, `transaction_status`, `payment_method`, `transaction_on`.
- Constraint values:
	- `user_role` must be `sender` or `beneficiary`.
	- `bill_status` must be `PAID` or `UNPAID`.
	- `recurring_interval` must be `NONE`, `WEEKLY`, or `MONTHLY`.

## Flow
1. `schema.sql` drops tables in dependency order, then recreates them.
2. The backend inserts or reads rows through the query layer in `backend/app/db/queries`.
3. Bills are soft-deleted via `is_deleted = 'N'/'Y'` rather than hard removal.
4. Remittance inserts link a sender, a beneficiary, and the bill that was paid.

## Notes
Keep this file aligned with any schema column rename, new constraint, or foreign key change.