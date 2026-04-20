import mysql.connector
from mysql.connector import pooling
from dotenv import load_dotenv
import os

load_dotenv()

dbconfig = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
}

conn_pool = pooling.MySQLConnectionPool(
    pool_name = "userpool",
    pool_size = 5,
    **dbconfig
)

def get_connection():
    return conn_pool.get_connection()