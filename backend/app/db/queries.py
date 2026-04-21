from .connection import get_connection
import mysql.connector
from dotenv import load_dotenv
import os
from datetime import date

load_dotenv()
DB_C_P = int(os.getenv('DB_CONN_POOLING'))
DB_T = os.getenv('DB_TABLE')

def insert_bill(name, due_date, total_amount, creation_date=date.today(), status='UNPAID', category=None):
    conn = get_connection(DB_C_P)
    curr = conn.cursor()

    query = f"""
    INSERT INTO {DB_T} (name, creation_date, due_date, total_amount, status, category)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    values = (name, creation_date, due_date, total_amount, status, category)
    try:
        curr.execute(query, values)
    except mysql.connector.Error as e:
        conn.rollback()
        raise
    else:
        conn.commit()
    
    curr.close()
    conn.close()