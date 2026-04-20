-- database creation and usage
CREATE DATABASE IF NOT EXISTS family_supp_sche;
USE family_supp_sche;

-- creating 'bills' table
CREATE TABLE IF NOT EXISTS bills (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    creation_date DATE NOT NULL,
    due_date DATE NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(10) NOT NULL,
    category VARCHAR(50),

    CHECK (due_date >= creation_date)
);

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