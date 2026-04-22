from fastapi import FastAPI
from .db.connection import get_connection

app = FastAPI()

@app.get("/health")
def status():
    return {"message":"backend is live"}

@app.get("/db-connection-testing")
def test_db():
    conn = get_connection()
    curr = conn.cursor(dictionary=True)
    curr.execute(f"SELECT * FROM sample_bills")
    
    data = curr.fetchall()

    curr.close()
    conn.close()

    return data