from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import api_endpoints as bill_routes

from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://127.0.0.1:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.include_router(bill_routes.router)

@app.get("/health")
def status():
    return {"message":"backend is live"}