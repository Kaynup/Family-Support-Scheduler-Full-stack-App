# Objectives of Application

- Design tool for family bills specifically
- Users can log upcoming expenses
- they can categorize them
- they can set due dates for the bills.
- manage their status for paid or not

1. Since all bills are unique we require an ID as Primary key that self increments on addition of new data
2. Since logging in necessary we need a field for due dates for every bill. Along with creation date as a field also
3. All bills have status field, necessary and will be tracked by the notification system
4. All bills have category field, optional for the user - it may include home bills, subscription plans, financial bills etc.
5. The bills have final amounts as a field
6. All bills will be having name field

ID (Integer) | name (String) | creation_date (Datetime) | due_date (Datetime) | total_amount (Float) | status (String) | category (String)
------------|------------|------------|------------|------------|------------|------------|
Incremental ID in integer | title of the bill | date of creation of bill in database | due date set by the user | amount specified in the bill | PAID or UNPAID | categories made by user like home bills, financial bills, subscriptions etc.