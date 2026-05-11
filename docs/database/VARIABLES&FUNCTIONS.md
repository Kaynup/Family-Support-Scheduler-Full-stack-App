# Variables & Functions (Database)

The database schema uses strict ENUMs and constraints to enforce data integrity.

## Table Variables

### `users`
- `id` (INT, PRIMARY KEY, AUTO_INCREMENT)
- `username` (VARCHAR, UNIQUE)
- `password_hash` (VARCHAR)
- `role` (ENUM: `'sender'`, `'beneficiary'`)

### `bills`
- `bill_id` (INT, PRIMARY KEY, AUTO_INCREMENT)
- `user_id` (INT, FOREIGN KEY) - Links to `users.id`
- `bill_name` (VARCHAR)
- `total_amount` (DECIMAL(10,2))
- `due_date` (DATE) - Maps to `YYYY-MM-DD` strings on the frontend.
- `category` (VARCHAR)
- `bill_status` (ENUM: `'UNPAID'`, `'PAID'`) - Default `'UNPAID'`
- `is_deleted` (ENUM: `'N'`, `'Y'`) - Used for Soft Deletes.
- `recurring_interval` (ENUM: `'NONE'`, `'WEEKLY'`, `'MONTHLY'`)


### `remittance`
- `remittance_id` (INT, PRIMARY KEY, AUTO_INCREMENT)
- `sender_user_id` (INT, FOREIGN KEY)
- `beneficiary_user_id` (INT, FOREIGN KEY)
- `bill_id` (INT, FOREIGN KEY)
- `amount_paid` (DECIMAL(10,2))
- `currency` (VARCHAR)
- `payment_method` (VARCHAR)
- `payment_date` (TIMESTAMP)

## Foreign Key Behaviors
- `ON DELETE CASCADE`: Applied to `remittance` relative to `bills` and `users`. However, the application uses **Soft Deletes** (`is_deleted = 'Y'`) explicitly to prevent destructive cascades from wiping out historical remittance ledgers.
