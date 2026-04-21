from .connection import get_connection
import mysql.connector
from dotenv import load_dotenv
import os
from datetime import date

load_dotenv()
DB_T = os.getenv('DB_TABLE')

def insert_bill(name, due_date, total_amount, creation_date=None, status='UNPAID', category=None):
    if creation_date is None:
        creation_date = date.today()

    conn = get_connection()
    curr = conn.cursor()

    query = f"""
    INSERT INTO {DB_T} (name, creation_date, due_date, total_amount, status, category)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    values = (name, creation_date, due_date, total_amount, status, category)
    try:
        curr.execute(query, values)
        conn.commit()
    except mysql.connector.Error as e:
        conn.rollback()
        raise
    finally:
        curr.close()
        conn.close()

def select_all():
    conn = get_connection()
    curr = conn.cursor()

    query = f"SELECT * from {DB_T}"
    curr.execute(query)

    data = curr.fetchall()
    
    curr.close()
    conn.close()

    return data

def select_num_day_dues(num_days=3):
    conn = get_connection()
    curr = conn.cursor()

    query = f"""
    SELECT * from {DB_T} WHERE status = %s
    AND due_date BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL %s DAY)
    ORDER BY due_date ASC
    """
    curr.execute(query, ('UNPAID', num_days))

    data = curr.fetchall()
    
    curr.close()
    conn.close()

    return data

def update_bill_status(id_, status):
    conn = get_connection()
    curr = conn.cursor()

    query = f"UPDATE {DB_T} SET status = %s WHERE id = %s"
    try:
        curr.execute(query, (status, id_))
        conn.commit()
    except mysql.connector.Error as e:
        conn.rollback()
        raise
    finally:
        curr.close()
        conn.close()

def delete_bill_by_id(id_):
    conn = get_connection()
    curr = conn.cursor()

    query = f"DELETE FROM {DB_T} WHERE id = %s"
    try:
        curr.execute(query, (id_, ))
        conn.commit()
    except mysql.connector.Error as e:
        conn.rollback()
        raise
    finally:
        curr.close()
        conn.close()