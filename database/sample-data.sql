-- Family Support Scheduler - Sample Seed Data v2
-- Inserts users, bills owned by those users, and sample remittance transactions.
-- Run schema.sql first to create all tables before seeding.

USE family_supp_sche;

-- Clear all data in reverse dependency order before seeding.
DELETE FROM remittance_transactions;
DELETE FROM bills;
DELETE FROM users;


-- Sample users.
-- Passwords are bcrypt hashes.
-- Plain-text values for local development:
--   ravi_sender    -> password: sender123
--   priya_family   -> password: family123
--   anita_family   -> password: family123
INSERT INTO users (username, password_hash, role) VALUES
(
    'ravi_sender',
    '$2b$12$KIX9ZuOAi9H.n2MZOJm.aO0FzMJyFwhS0vEWIXGdCUIDiFbS5YJom',
    'sender'
),
(
    'priya_family',
    '$2b$12$6xyzABCDefghIJKLMNopqOT2v5YJ1pSCwJqxdQjkKlfJmlR6nOXaW',
    'beneficiary'
),
(
    'anita_family',
    '$2b$12$9mnpQRSTuvwxYZabCDEfgOD3w6ZK2qTDxKryeRkLgmS7oPS7oQYbX',
    'beneficiary'
);


-- Sample bills.
-- Covers multiple categories, statuses, and recurring intervals.
-- user_id 2 = priya_family, user_id 3 = anita_family.
INSERT INTO bills (name, creation_date, due_date, total_amount, status, category, recurring_interval, Is_expired, user_id) VALUES
('March Rent',            '2026-03-01', '2026-03-05', 15000.00, 'UNPAID', 'Housing',        'MONTHLY', 'Y', 2),
('Electricity - Mar',     '2026-03-10', '2026-03-20',  2450.00, 'UNPAID', 'Utilities',      'NONE',    'Y', 2),
('Old Water Bill',        '2026-02-15', '2026-03-01',   800.00, 'UNPAID', 'Utilities',      'NONE',    'Y', 3),
('Credit Card - Mar',     '2026-03-15', '2026-04-05', 12000.00, 'UNPAID', 'Finance',        'NONE',    'Y', 2),
('Broadband',             '2026-04-01', '2026-04-10',   999.00, 'PAID',   'Utilities',      'MONTHLY', 'N', 2),
('Gas Bill',              '2026-04-01', '2026-04-12',  1100.00, 'PAID',   'Utilities',      'MONTHLY', 'N', 3),
('Spotify Family',        '2026-04-15', '2026-04-15',   179.00, 'PAID',   'Entertainment',  'MONTHLY', 'N', 2),
('Gym Membership',        '2026-04-01', '2026-04-05',  1200.00, 'PAID',   'Health',         'MONTHLY', 'N', 3),
('X-Box Console',         '2026-04-28', '2026-05-01',  6000.00, 'UNPAID', 'Gaming',         'NONE',    'N', 2),
('Rent',                  '2026-04-28', '2026-05-03', 15000.00, 'UNPAID', 'Housing',        'MONTHLY', 'N', 2),
('Mobile Recharge',       '2026-04-28', '2026-05-04',   299.00, 'PAID',   'Telecom',        'NONE',    'N', 3),
('DTH Recharge',          '2026-04-28', '2026-05-05',   450.00, 'UNPAID', 'Entertainment',  'NONE',    'N', 3),
('Groceries',             '2026-04-28', '2026-05-06',  2500.00, 'PAID',   'Food',           'NONE',    'N', 2),
('Insurance',             '2026-04-28', '2026-05-07',  5000.00, 'UNPAID', 'Finance',        'MONTHLY', 'N', 2),
('Gym Fee',               '2026-04-28', '2026-05-08',  1200.00, 'PAID',   'Health',         'MONTHLY', 'N', 3),
('School Fee',            '2026-04-28', '2026-05-09',  8000.00, 'UNPAID', 'Education',      'NONE',    'N', 2),
('Car EMI',               '2026-04-28', '2026-05-10', 10000.00, 'UNPAID', 'Loan',           'MONTHLY', 'N', 3),
('Netflix',               '2026-04-30', '2026-05-10',   199.00, 'UNPAID', 'Subscriptions',  'MONTHLY', 'N', 2),
('Laundry Services',      '2026-04-25', '2026-05-12',   450.00, 'UNPAID', 'Misc',           'NONE',    'N', 3),
('Cloud Storage',         '2026-05-01', '2026-05-15',   210.00, 'UNPAID', 'Subscriptions',  'MONTHLY', 'N', 2),
('Weekly Milk',           '2026-05-01', '2026-05-07',   350.00, 'UNPAID', 'Food',           'WEEKLY',  'N', 3),
('Weekly Newspaper',      '2026-05-01', '2026-05-07',    50.00, 'PAID',   'Misc',           'WEEKLY',  'N', 3),
('Health Checkup',        '2026-05-10', '2026-05-25',  3500.00, 'UNPAID', 'Health',         'NONE',    'N', 2),
('Property Tax',          '2026-05-01', '2026-06-15', 12000.00, 'UNPAID', 'Housing',        'NONE',    'N', 2),
('Amazon Prime',          '2026-05-20', '2026-06-20',  1499.00, 'UNPAID', 'Entertainment',  'NONE',    'N', 3),
('Electricity - May',     '2026-05-20', '2026-05-30',  2100.00, 'UNPAID', 'Utilities',      'NONE',    'N', 2),
('Water Bill - May',      '2026-05-20', '2026-05-28',   750.00, 'UNPAID', 'Utilities',      'NONE',    'N', 3),
('Pet Food Subscription', '2026-05-01', '2026-05-22',  1200.00, 'UNPAID', 'Pets',           'MONTHLY', 'N', 2);


-- Sample remittance transactions.
-- sender_user_id 1 = ravi_sender paying bills for priya (2) and anita (3).
-- References bills that are already PAID above (Broadband id=5, Gas Bill id=6).
INSERT INTO remittance_transactions (bill_id, sender_user_id, beneficiary_user_id, amount, currency, transaction_status, payment_method) VALUES
(5,  1, 2,  999.00, 'USDT', 'COMPLETED', 'stablecoin'),
(6,  1, 3, 1100.00, 'USDT', 'COMPLETED', 'stablecoin');