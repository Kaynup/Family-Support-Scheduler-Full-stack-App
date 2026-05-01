CREATE DATABASE IF NOT EXISTS family_supp_sche;
USE family_supp_sche;

DROP TABLE IF EXISTS bills;

CREATE TABLE IF NOT EXISTS bills (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    creation_date DATE NOT NULL,
    due_date DATE NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(10) NOT NULL,
    category VARCHAR(50),
    recurring_interval VARCHAR(20) DEFAULT 'NONE',
    Is_deleted CHAR(1) NOT NULL DEFAULT 'N',
    Is_expired CHAR(1) NOT NULL DEFAULT 'N',

    CONSTRAINT chk_due_date CHECK (due_date >= creation_date)
);