"""
Database Bootstrapper for Cloud MySQL (TiDB Cloud Serverless / Managed MySQL).

Reads connection details from environment variables or .env file,
creates the schema tables if they do not exist, and optionally seeds initial users.
"""

import os
import sys
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "4000" if "tidbcloud" in os.getenv("DB_HOST", "") else "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "family_supp_sche")
DB_SSL = os.getenv("DB_SSL", "true" if DB_PORT == 4000 else "false").lower() in ("true", "1", "yes")

TABLES_SQL = [
    """
    CREATE TABLE IF NOT EXISTS users (
        user_id          INT AUTO_INCREMENT PRIMARY KEY,
        user_name        VARCHAR(100) NOT NULL UNIQUE,
        user_pass        VARCHAR(255) NOT NULL,
        user_role        VARCHAR(20)  NOT NULL,
        user_created_on  DATETIME DEFAULT CURRENT_TIMESTAMP,
        CONSTRAINT check_user_role CHECK (user_role IN ('sender', 'beneficiary'))
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS bills (
        bill_id             INT AUTO_INCREMENT PRIMARY KEY,
        bill_name           VARCHAR(200)  NOT NULL,
        bill_status         VARCHAR(10)   NOT NULL,
        user_id             INT           NULL,
        creation_date       DATE          NOT NULL,
        due_date            DATE          NOT NULL,
        total_amount        DECIMAL(10,2) NOT NULL,
        category            VARCHAR(50)   NULL,
        recurring_interval  VARCHAR(10)   NOT NULL DEFAULT 'NONE',
        is_deleted          CHAR(1)       NOT NULL DEFAULT 'N',
        CONSTRAINT check_bill_status CHECK (bill_status IN ('PAID', 'UNPAID')),
        CONSTRAINT check_valid_category CHECK (recurring_interval IN ('NONE', 'WEEKLY', 'MONTHLY')),
        CONSTRAINT fk_bill_owner FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS remittance_transactions (
        transaction_id      INT AUTO_INCREMENT PRIMARY KEY,
        bill_id             INT NOT NULL,
        sender_user_id      INT NOT NULL,
        beneficiary_user_id INT,
        amount              DECIMAL(10,2) NOT NULL,
        currency            VARCHAR(20) NOT NULL DEFAULT 'USDT',
        transaction_status  VARCHAR(20) NOT NULL DEFAULT 'COMPLETED',
        payment_method      VARCHAR(50) NOT NULL DEFAULT 'stablecoin',
        transaction_on      DATETIME DEFAULT CURRENT_TIMESTAMP,
        CONSTRAINT fk_remittance_bill FOREIGN KEY (bill_id) REFERENCES bills(bill_id),
        CONSTRAINT fk_remittance_sender FOREIGN KEY (sender_user_id) REFERENCES users(user_id),
        CONSTRAINT fk_remittance_beneficiary FOREIGN KEY (beneficiary_user_id) REFERENCES users(user_id)
    )
    """,
]


def init_database():
    print(f"Connecting to database at {DB_HOST}:{DB_PORT}/{DB_NAME} (SSL={DB_SSL})...")
    conn_kwargs = {
        "host": DB_HOST,
        "port": DB_PORT,
        "user": DB_USER,
        "password": DB_PASSWORD,
        "database": DB_NAME,
    }
    if DB_SSL:
        conn_kwargs["ssl_disabled"] = False

    try:
        conn = mysql.connector.connect(**conn_kwargs)
        cursor = conn.cursor()

        print("Creating tables...")
        for table_sql in TABLES_SQL:
            cursor.execute(table_sql)
        conn.commit()

        print("✓ All tables initialized successfully!")
        cursor.close()
        conn.close()
    except Exception as exc:
        print(f"✗ Database initialization error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    init_database()
