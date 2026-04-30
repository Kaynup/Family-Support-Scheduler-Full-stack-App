CREATE DATABASE IF NOT EXISTS family_supp_sche;
USE family_supp_sche;

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

    CONSTRAINT chk_due_date CHECK (due_date >= creation_date),
    CONSTRAINT chk_is_deleted CHECK (Is_deleted IN ('Y','N'))
);

DELETE FROM bills;

INSERT INTO bills (name, creation_date, due_date, total_amount, status, category) VALUES
('Electricity Bill', '2026-04-28', '2026-04-29', 1200.50, 'UNPAID', 'Utilities'),
('Water Bill',       '2026-04-28', '2026-04-30', 300.75,  'UNPAID',    'Utilities'),
('Internet Bill',    '2026-04-28', '2026-05-01', 999.00,  'UNPAID', 'Utilities'),
('Gas Bill',         '2026-04-28', '2026-05-02', 450.20,  'PAID',    'Utilities'),
('Rent',             '2026-04-28', '2026-05-03', 15000.00,'UNPAID', 'Housing'),
('Mobile Recharge',  '2026-04-28', '2026-05-04', 299.00,  'PAID',    'Telecom'),
('DTH Recharge',     '2026-04-28', '2026-05-05', 450.00,  'UNPAID', 'Entertainment'),
('Groceries',        '2026-04-28', '2026-05-06', 2500.00, 'PAID',    'Food'),
('Insurance',        '2026-04-28', '2026-05-07', 5000.00, 'UNPAID', 'Finance'),
('Gym Fee',          '2026-04-28', '2026-05-08', 1200.00, 'PAID',    'Health'),
('School Fee',       '2026-04-28', '2026-05-09', 8000.00, 'UNPAID', 'Education'),
('Car EMI',          '2026-04-28', '2026-05-10', 10000.00,'UNPAID', 'Loan');
