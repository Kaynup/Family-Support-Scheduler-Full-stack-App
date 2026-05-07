-- Family Support Scheduler - Database Schema v2
-- Canonical source of truth for all table structures.
-- Run this file on a fresh database to recreate the full schema.

CREATE DATABASE IF NOT EXISTS family_supp_sche;
USE family_supp_sche;

-- Drop tables in reverse dependency order to avoid FK constraint errors on reset.
DROP TABLE IF EXISTS remittance_transactions;
DROP TABLE IF EXISTS bills;
DROP TABLE IF EXISTS users;


-- Users table.
-- Stores all registered users regardless of role.
-- Passwords are stored as bcrypt hashes, never plain text.
CREATE TABLE IF NOT EXISTS users (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    username     VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role         VARCHAR(20) NOT NULL,
    created_at   DATETIME DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_user_role CHECK (role IN ('sender', 'beneficiary'))
);


-- Bills table.
-- Tracks financial obligations created by beneficiary users.
-- user_id is nullable for backward compatibility with pre-auth seed data.
CREATE TABLE IF NOT EXISTS bills (
    id                  INT AUTO_INCREMENT PRIMARY KEY,
    name                VARCHAR(200) NOT NULL,
    creation_date       DATE NOT NULL,
    due_date            DATE NOT NULL,
    total_amount        DECIMAL(10,2) NOT NULL,
    status              VARCHAR(10) NOT NULL,
    category            VARCHAR(50),
    recurring_interval  VARCHAR(20) DEFAULT 'NONE',
    Is_deleted          CHAR(1) NOT NULL DEFAULT 'N',
    Is_expired          CHAR(1) NOT NULL DEFAULT 'N',
    user_id             INT NULL,

    CONSTRAINT chk_due_date CHECK (due_date >= creation_date),
    CONSTRAINT chk_bill_status CHECK (status IN ('PAID', 'UNPAID')),
    CONSTRAINT fk_bill_owner FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);


-- Remittance transactions table.
-- Records every payment made by a sender on behalf of a beneficiary.
-- The stablecoin concept is represented by the currency column.
CREATE TABLE IF NOT EXISTS remittance_transactions (
    transaction_id      INT AUTO_INCREMENT PRIMARY KEY,
    bill_id             INT NOT NULL,
    sender_user_id      INT NOT NULL,
    beneficiary_user_id INT,
    amount              DECIMAL(10,2) NOT NULL,
    currency            VARCHAR(20) NOT NULL DEFAULT 'USDT',
    transaction_status  VARCHAR(20) NOT NULL DEFAULT 'COMPLETED',
    payment_method      VARCHAR(50) NOT NULL DEFAULT 'stablecoin',
    created_at          DATETIME DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_remittance_bill    FOREIGN KEY (bill_id)             REFERENCES bills(id),
    CONSTRAINT fk_remittance_sender  FOREIGN KEY (sender_user_id)      REFERENCES users(id),
    CONSTRAINT fk_remittance_beneficiary FOREIGN KEY (beneficiary_user_id) REFERENCES users(id)
);