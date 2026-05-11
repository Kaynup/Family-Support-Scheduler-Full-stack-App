-- Create or select database
CREATE DATABASE IF NOT EXISTS family_supp_sche;
USE family_supp_sche;

-- Drop tables in reverse dependency
DROP TABLE IF EXISTS remittance_transactions;
DROP TABLE IF EXISTS bills;
DROP TABLE IF EXISTS users;


-- Users table
CREATE TABLE IF NOT EXISTS users (
    user_id          INT AUTO_INCREMENT PRIMARY KEY,
    user_name        VARCHAR(100) NOT NULL UNIQUE,
    user_pass        VARCHAR(255) NOT NULL,
    user_role        VARCHAR(20)  NOT NULL,
    user_created_on  DATETIME DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT check_user_role CHECK (user_role IN ('sender', 'beneficiary'))
);


-- Bills table
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
);


-- Remittance transactions table
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

    CONSTRAINT fk_remittance_bill    FOREIGN KEY (bill_id)             REFERENCES bills(bill_id),
    CONSTRAINT fk_remittance_sender  FOREIGN KEY (sender_user_id)      REFERENCES users(user_id),
    CONSTRAINT fk_remittance_beneficiary FOREIGN KEY (beneficiary_user_id) REFERENCES users(user_id)
);