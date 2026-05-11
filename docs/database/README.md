# Database Documentation

The system uses a relational **MySQL (8.0)** database without an ORM. All interactions are handled via the `mysql.connector` utilizing raw parameterized SQL queries found in `backend/app/db/queries/`.

## Core Tables
1. **`users`**:
   - Stores `id`, `username`, `password_hash`, and `role` (`sender` or `beneficiary`).
   - Passwords are encrypted using bcrypt.

2. **`bills`**:
   - Stores `bill_id`, `user_id` (foreign key to the beneficiary), `bill_name`, `total_amount`, `due_date`, and `category`.
   - **Status tracking**: Tracks `bill_status` (`UNPAID` or `PAID`).
   - **Soft Delete**: Uses `is_deleted` for safe removal without breaking remittance history.
   - **Recurring metadata**: Stores `recurring_interval` (`NONE`, `WEEKLY`, `MONTHLY`). The database strictly holds only **one** active (UNPAID) instance of a recurring bill at any given time.
   - **Expiration**: Calculated dynamically in the frontend based on the `due_date`.

3. **`remittance`**:
   - The ledger table. Stores historical transaction data linking a `sender_user_id`, a `beneficiary_user_id`, and a `bill_id`.
   - Records the exact `amount_paid`, `currency`, and `payment_method`.

## Setup and Seeding
- `database/schema.sql`: Contains the raw DDL to set up the tables and constraints.
- `database/sample-data.sql`: Contains dummy data to seed the database for local testing and development.
- The `.env` file must be configured with `DB_USER`, `DB_PASSWORD`, `DB_HOST`, and `DB_NAME` to ensure successful connection pooling.
