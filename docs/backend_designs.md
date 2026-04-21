# Backend

## Dependencies

```bash
pip install uvicorn fastapi python-dotenv mysql-connector-python
```

---

## `backend/.env`
Stores configuration values
- Database credentials
- Table name

## `backend/app/db/connection.py`
Connection pooling (default=5 users)
- Returns connector object

## `backend/app/db/queries.py`
Raw SQL queries for CRUD operations
- insert_bill : takes name, due date of bill and amount in the bill as parameters and handles other values by default, then inserts the values into the table
- select_all : selects all the tuples from the table
- select_num_day_dues : takes a parameter for number of days due a bill has to be to select the certain bill info
- update_bill_status : updates the bill status to UNPAID or PAID
- delete_bill_by_id : deletes the bill's info

## `backend/app/main.py`
Entrypoint for FastAPI application
- /health (GET): checks status of backend
- /db-connection-testing (GET): checks database connection by retrieving all data in 'sample_bills' table