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

def get_connection(pool_sz):
    conn_pool = pooling.MySQLConnectionPool(
        pool_name = "userpool",
        pool_size = pool_sz,
        **dbconfig
    )

    return conn_pool.get_connection()