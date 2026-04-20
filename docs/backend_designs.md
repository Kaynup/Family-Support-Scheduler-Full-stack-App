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

## `backend/app/main.py`
Entrypoint for FastAPI application
- /health (GET): checks status of backend
- /db-connection-testing (GET): checks database connection by retrieving all data in 'sample_bills' table