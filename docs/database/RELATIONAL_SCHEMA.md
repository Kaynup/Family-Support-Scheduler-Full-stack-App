# Relational Schema -- `bills` Table

## Table Definition

Database: `family_supp_sche`
Table: `bills`

## Field Reference

| Column              | Type            | Nullable | Default  | Purpose                                                      |
| ------------------- | --------------- | -------- | -------- | ------------------------------------------------------------ |
| `id`                | INT             | NO       | AUTO_INC | Primary key. Auto-incrementing integer.                      |
| `name`              | VARCHAR(200)    | NO       | --       | Descriptive label of the bill (e.g. "Electricity Bill").     |
| `creation_date`     | DATE            | NO       | --       | The date when the bill record was created in the system.     |
| `due_date`          | DATE            | NO       | --       | Deadline for payment. Used for calendar rendering and alerts.|
| `total_amount`      | DECIMAL(10,2)   | NO       | --       | Payment amount in INR. Two decimal places for paisa.         |
| `status`            | VARCHAR(10)     | NO       | --       | Payment state. Values: `PAID` or `UNPAID`.                   |
| `category`          | VARCHAR(50)     | YES      | NULL     | Optional grouping label (Utilities, Housing, Loan, etc).     |
| `recurring_interval`| VARCHAR(20)     | YES      | 'NONE'   | Recurrence type. Values: `NONE`, `WEEKLY`, or `MONTHLY`.     |
| `Is_deleted`        | CHAR(1)         | NO       | 'N'      | Soft delete flag. `Y` marks the record as logically deleted. |
| `Is_expired`        | CHAR(1)         | NO       | 'N'      | Expiration flag. `Y` marks the bill as overdue.              |

## Constraints

| Constraint Name  | Rule                          | Rationale                                     |
| ---------------- | ----------------------------- | --------------------------------------------- |
| `chk_due_date`   | `due_date >= creation_date`   | A bill cannot be due before it was created.   |

## Seed Data

The schema file includes pre-loaded records spanning categories like
Utilities, Housing, Telecom, Entertainment, Food, Finance, Health, Education, and Loan.
These records provide immediate testing coverage for all recurring intervals and status combinations.

---