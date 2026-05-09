# Relatable Files (Database)

The persistence layer relies on a clean, raw SQL implementation using MySQL.

## 1. Schema Definitions
- **`database/schema.sql`**: 
  The single source of truth for table schemas. Contains DDL commands to `CREATE TABLE` and establishes relationships using `FOREIGN KEY` constraints. It is idempotent (uses `DROP TABLE IF EXISTS`).
- **`database/sample-data.sql`**: 
  Contains mock inserts (`INSERT INTO users ...`, `INSERT INTO bills ...`) to easily bootstrap the platform with predefined senders, beneficiaries, and historical bills for testing the projection and routing algorithms.

## 2. Execution Layer (in `backend/app/db/`)
- **`connection.py`**: 
  Provides the `@contextmanager` function `get_db_connection()`. It connects via `mysql.connector` using `.env` parameters and safely yields the cursor, ensuring connections are closed and committed or rolled back automatically.
- **`queries/auth_select.py`**: 
  Houses queries specific to verifying logins (`select_user_by_username`).
- **`queries/bill_insert.py`**: 
  Contains `insert_bill()`. Crucial for the backend auto-generation service, allowing it to inject new recurring instances assigned to the correct `user_id`.
- **`queries/bill_select.py`**: 
  Contains parameterized queries matching the API endpoints, such as `select_upcoming_bills()`, `select_expired_bills()`, and `select_bills_by_beneficiary()`.
