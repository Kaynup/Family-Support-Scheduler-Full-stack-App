import mysql.connector
from mysql.connector import pooling
from dotenv import load_dotenv
import os

load_dotenv()
DB_C_P = int(os.getenv('DB_CONN_POOLING'))

dbconfig = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
}

conn_pool = pooling.MySQLConnectionPool(
    pool_name = "userpool",
    pool_size = DB_C_P,
    **dbconfig
)

def get_connection():
    return conn_pool.get_connection()