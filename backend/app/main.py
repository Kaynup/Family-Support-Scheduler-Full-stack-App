from fastapi import FastAPI
from .routes import api_endpoints as bill_routes

app = FastAPI()
app.include_router(bill_routes.router)

@app.get("/health")
def status():
    return {"message":"backend is live"}