-- Family Support Scheduler - Sample Seed Data
-- Provides a diverse set of records for development and testing.

CREATE DATABASE IF NOT EXISTS family_supp_sche;
USE family_supp_sche;

-- Clear existing data before seeding
DELETE FROM bills;

-- Insert records spanning multiple categories, statuses, and recurring intervals.
-- Includes historical (expired) data and future-dated bills.
INSERT INTO bills (name, creation_date, due_date, total_amount, status, category, recurring_interval, Is_expired) VALUES
('March Rent',         '2026-03-01', '2026-03-05', 15000.00,'UNPAID', 'Housing',   'MONTHLY', 'Y'),
('Electricity - Mar',  '2026-03-10', '2026-03-20', 2450.00, 'UNPAID', 'Utilities', 'NONE',    'Y'),
('Old Water Bill',     '2026-02-15', '2026-03-01', 800.00,  'UNPAID', 'Utilities', 'NONE',    'Y'),
('Credit Card - Mar',  '2026-03-15', '2026-04-05', 12000.00,'UNPAID', 'Finance',   'NONE',    'Y'),
('Broadband',          '2026-04-01', '2026-04-10', 999.00,  'PAID',   'Utilities', 'MONTHLY', 'N'),
('Gas Bill',           '2026-04-01', '2026-04-12', 1100.00, 'PAID',   'Utilities', 'MONTHLY', 'N'),
('Spotify Family',     '2026-04-15', '2026-04-15', 179.00,  'PAID',   'Entertainment', 'MONTHLY', 'N'),
('Gym Membership',     '2026-04-01', '2026-04-05', 1200.00, 'PAID',   'Health',    'MONTHLY', 'N'),
('X-Box Console',      '2026-04-28', '2026-05-01', 6000.00,'UNPAID', 'GAMING',   'NONE', 'N'),
('Rent',               '2026-04-28', '2026-05-03', 15000.00,'UNPAID', 'Housing',   'MONTHLY', 'N'),
('Mobile Recharge',    '2026-04-28', '2026-05-04', 299.00,  'PAID',   'Telecom',   'NONE',    'N'),
('DTH Recharge',       '2026-04-28', '2026-05-05', 450.00,  'UNPAID', 'Entertainment', 'NONE', 'N'),
('Groceries',          '2026-04-28', '2026-05-06', 2500.00, 'PAID',   'Food',      'NONE',    'N'),
('Insurance',          '2026-04-28', '2026-05-07', 5000.00, 'UNPAID', 'Finance',   'MONTHLY', 'N'),
('Gym Fee',            '2026-04-28', '2026-05-08', 1200.00, 'PAID',   'Health',    'MONTHLY', 'N'),
('School Fee',         '2026-04-28', '2026-05-09', 8000.00, 'UNPAID', 'Education', 'NONE',    'N'),
('Car EMI',            '2026-04-28', '2026-05-10', 10000.00,'UNPAID', 'Loan',      'MONTHLY', 'N'),
('Netflix',            '2026-04-30', '2026-05-10', 199.00,  'UNPAID', 'Subscriptions', 'MONTHLY', 'N'),
('Laundry Services',   '2026-04-25', '2026-05-12', 450.00,  'UNPAID', 'Misc',      'NONE',    'N'),
('Cloud Storage',      '2026-05-01', '2026-05-15', 210.00,  'UNPAID', 'Subscriptions', 'MONTHLY', 'N'),
('Weekly Milk',        '2026-05-01', '2026-05-07', 350.00,  'UNPAID', 'Food',      'WEEKLY',  'N'),
('Weekly Newspaper',   '2026-05-01', '2026-05-07', 50.00,   'PAID',   'Misc',      'WEEKLY',  'N'),
('Health Checkup',     '2026-05-10', '2026-05-25', 3500.00, 'UNPAID', 'Health',    'NONE',    'N'),
('Property Tax',       '2026-05-01', '2026-06-15', 12000.00,'UNPAID', 'Housing',   'NONE',    'N'),
('Amazon Prime',       '2026-05-20', '2026-06-20', 1499.00, 'UNPAID', 'Entertainment', 'NONE', 'N'),
('Electricity - May',  '2026-05-20', '2026-05-30', 2100.00, 'UNPAID', 'Utilities', 'NONE',    'N'),
('Water Bill - May',   '2026-05-20', '2026-05-28', 750.00,  'UNPAID', 'Utilities', 'NONE',    'N'),
('Pet Food Subscription','2026-05-01', '2026-05-22', 1200.00,'UNPAID', 'Pets',      'MONTHLY', 'N');