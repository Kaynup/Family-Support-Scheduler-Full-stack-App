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

DELETE FROM bills;

INSERT INTO bills (name, creation_date, due_date, total_amount, status, category, recurring_interval, Is_expired) VALUES
('Rent',             '2026-04-28', '2026-05-03', 15000.00,'UNPAID', 'Housing',   'MONTHLY', 'N'),
('Mobile Recharge',  '2026-04-28', '2026-05-04', 299.00,  'PAID',   'Telecom',   'NONE',    'N'),
('DTH Recharge',     '2026-04-28', '2026-05-05', 450.00,  'UNPAID', 'Entertainment', 'NONE', 'N'),
('Groceries',        '2026-04-28', '2026-05-06', 2500.00, 'PAID',   'Food',      'NONE',    'N'),
('Insurance',        '2026-04-28', '2026-05-07', 5000.00, 'UNPAID', 'Finance',   'MONTHLY', 'N'),
('Gym Fee',          '2026-04-28', '2026-05-08', 1200.00, 'PAID',   'Health',    'MONTHLY', 'N'),
('School Fee',       '2026-04-28', '2026-05-09', 8000.00, 'UNPAID', 'Education', 'NONE',    'N'),
('Car EMI',          '2026-04-28', '2026-05-10', 10000.00,'UNPAID', 'Loan',      'MONTHLY', 'N');
