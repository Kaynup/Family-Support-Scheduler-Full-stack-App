-- Select database
USE family_supp_sche;

-- Clear all data in reverse dependency
DELETE FROM remittance_transactions;
DELETE FROM bills;
DELETE FROM users;


-- Users
INSERT INTO users (user_name, user_pass, user_role) VALUES
('Ramesh', SHA2('sender123', 256), 'sender'),
('Karan', SHA2('family123', 256), 'beneficiary'),
('Raghav', SHA2('family123', 256), 'beneficiary');


-- Sample bills
INSERT INTO bills (bill_name, creation_date, due_date, total_amount, bill_status, category, recurring_interval, user_id) VALUES
('March Rent',            '2026-04-01', '2026-05-05', 15000.00, 'UNPAID', 'Housing',        'MONTHLY', 2),
('Electricity - Mar',     '2026-04-10', '2026-05-20',  2450.00, 'UNPAID', 'Utilities',      'NONE',    2),
('Old Water Bill',        '2026-04-15', '2026-05-01',   800.00, 'UNPAID', 'Utilities',      'NONE',    3),
('Credit Card - Mar',     '2026-04-15', '2026-05-05', 12000.00, 'UNPAID', 'Finance',        'NONE',    2),
('Broadband',             '2026-04-01', '2026-05-10',   999.00, 'UNPAID', 'Utilities',      'MONTHLY', 2),
('Gas Bill',              '2026-04-01', '2026-05-12',  1100.00, 'UNPAID', 'Utilities',      'MONTHLY', 3),
('Rent',                  '2026-04-28', '2026-05-03', 15000.00, 'UNPAID', 'Housing',        'MONTHLY', 2),
('Mobile Recharge',       '2026-05-28', '2026-06-04',   299.00, 'UNPAID', 'Telecom',        'NONE',    3),
('DTH Recharge',          '2026-05-28', '2026-06-05',   450.00, 'UNPAID', 'Entertainment',  'NONE',    3),
('Groceries',             '2026-05-28', '2026-06-06',  2500.00, 'UNPAID', 'Food',           'NONE',    2),
('Insurance',             '2026-05-28', '2026-06-07',  5000.00, 'UNPAID', 'Finance',        'MONTHLY', 2),
('School Fee',            '2026-05-28', '2026-06-09',  8000.00, 'UNPAID', 'Education',      'NONE',    2),
('Car EMI',               '2026-04-28', '2026-05-10', 10000.00, 'UNPAID', 'Loan',           'MONTHLY', 3),
('Laundry Services',      '2026-04-25', '2026-05-12',   450.00, 'UNPAID', 'Misc',           'NONE',    3),
('Weekly Milk',           '2026-05-01', '2026-06-07',   350.00, 'UNPAID', 'Food',           'WEEKLY',  3),
('Weekly Newspaper',      '2026-05-01', '2026-06-07',    50.00, 'UNPAID', 'Misc',           'WEEKLY',  3),
('Health Checkup',        '2026-05-10', '2026-06-25',  3500.00, 'UNPAID', 'Health',         'NONE',    2),
('Property Tax',          '2026-05-01', '2026-06-15', 12000.00, 'UNPAID', 'Housing',        'NONE',    2),
('Electricity - May',     '2026-05-20', '2026-06-30',  2100.00, 'UNPAID', 'Utilities',      'NONE',    2),
('Water Bill - May',      '2026-05-20', '2026-05-28',   750.00, 'UNPAID', 'Utilities',      'NONE',    3);
