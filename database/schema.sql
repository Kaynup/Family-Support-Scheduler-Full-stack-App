-- Family Support Scheduler - Database Schema
-- Canonical source of truth for the 'bills' table structure.

CREATE DATABASE IF NOT EXISTS family_supp_sche;
USE family_supp_sche;

-- Drop table if it exists to allow for clean schema resets
DROP TABLE IF EXISTS bills;

-- Main table for tracking financial obligations
CREATE TABLE IF NOT EXISTS bills (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    creation_date DATE NOT NULL,
    due_date DATE NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(10) NOT NULL,                 -- 'PAID' or 'UNPAID'
    category VARCHAR(50),                        -- e.g., 'Utilities', 'Housing'
    recurring_interval VARCHAR(20) DEFAULT 'NONE', -- 'NONE', 'WEEKLY', 'MONTHLY'
    Is_deleted CHAR(1) NOT NULL DEFAULT 'N',     -- Soft delete flag ('Y'/'N')
    Is_expired CHAR(1) NOT NULL DEFAULT 'N',     -- Overdue flag ('Y'/'N')

    -- Ensure logical date consistency
    CONSTRAINT chk_due_date CHECK (due_date >= creation_date)
);