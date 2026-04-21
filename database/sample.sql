-- Generating sample data
USE family_supp_sche;

-- creating a sample table to immitate bills table
CREATE TABLE IF NOT EXISTS sample_bills (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    creation_date DATE NOT NULL,
    due_date DATE NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(10) NOT NULL,
    category VARCHAR(50),

    CHECK (due_date >= creation_date)
);

DELETE FROM sample_bills;

INSERT INTO sample_bills (name, category, total_amount, due_date, status, creation_date)
VALUES
('Internet Bill', 'Utilities', 999, '2026-04-26', 'UNPAID', '2026-04-25'),
('Electricity Bill', 'Utilities', 1500, '2026-04-28', 'UNPAID', '2026-04-25'),
('Netflix Subscription', 'Entertainment', 649, '2026-04-30', 'PAID', '2026-04-20'),
('Water Bill', 'Utilities', 300, '2026-04-27', 'UNPAID', '2026-04-25');