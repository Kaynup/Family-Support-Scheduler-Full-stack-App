from fastapi import FastAPI
from .db.connection import get_connection
from dotenv import load_dotenv
import os

load_dotenv()
DB_T = os.getenv('DB_TABLE')

app = FastAPI()

@app.get("/health")
def status():
    return {"message":"backend is live"}

@app.get("/db-connection-testing")
def test_db():
    conn = get_connection()
    curr = conn.cursor(dictionary=True)
    curr.execute(f"SELECT * FROM {DB_T}")
    
    data = curr.fetchall()

    curr.close()
    conn.close()

    return data