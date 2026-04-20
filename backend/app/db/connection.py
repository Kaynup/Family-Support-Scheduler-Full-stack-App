import mysql.connector
from mysql.connector import pooling

from .config import dbconfig

conn_pool = pooling.MySQLConnectionPool(
    pool_name = "userpool",
    pool_size = 5
    **dbconfig()
)

def get_connection():
    return conn_pool.get_connection()