from .connection import get_connection
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()
DB_T = os.getenv('DB_TABLE')

def insert_bill(name, due_date, total_amount, creation_date, status='UNPAID', category=None):
    conn = get_connection()
    curr = conn.cursor()

    query = f"""
    INSERT INTO {DB_T} (name, creation_date, due_date, total_amount, status, category)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    values = (name, creation_date, due_date, total_amount, status, category)
    try:
        curr.execute(query, values)
        id_ = curr.lastrowid
        conn.commit()
    except mysql.connector.Error as e:
        conn.rollback()
        raise
    finally:
        curr.close()
        conn.close()

    return id_

def select_all():
    conn = get_connection()
    curr = conn.cursor()

    query = f"SELECT * from {DB_T} WHERE Is_deleted = %s"
    curr.execute(query, ('N', ))

    data = curr.fetchall()
    
    curr.close()
    conn.close()

    return data

def select_num_day_dues(num_days=3):
    conn = get_connection()
    curr = conn.cursor()

    query = f"""
    SELECT * from {DB_T} WHERE status = %s
    AND Is_deleted = %s
    AND due_date <= DATE_ADD(CURDATE(), INTERVAL %s DAY)
    ORDER BY due_date ASC
    """
    curr.execute(query, ('UNPAID', 'N', num_days))

    data = curr.fetchall()
    
    curr.close()
    conn.close()

    return data


def select_bill_by_id(id_):
    conn = get_connection()
    curr = conn.cursor()

    query = f"SELECT * FROM {DB_T} WHERE id = %s AND Is_deleted = %s"
    curr.execute(query, (id_, 'N'))
    data = curr.fetchone()

    curr.close()
    conn.close()

    return data

def update_bill_status(id_, status):
    conn = get_connection()
    curr = conn.cursor()

    query = f"UPDATE {DB_T} SET status = %s WHERE id = %s AND Is_deleted = %s"
    try:
        curr.execute(query, (status, id_, 'N'))
        if curr.rowcount == 0:
            raise mysql.connector.Error("No bill found for given id")
        conn.commit()
    except mysql.connector.Error as e:
        conn.rollback()
        raise
    finally:
        curr.close()
        conn.close()

    return id_

def delete_bill_by_id(id_):
    conn = get_connection()
    curr = conn.cursor()

    query = f"UPDATE {DB_T} SET Is_deleted = %s WHERE id = %s;"
    try:
        curr.execute(query, ('Y', id_))
        if curr.rowcount == 0:
            raise mysql.connector.Error("No bill found for given id")
        conn.commit()
    except mysql.connector.Error as e:
        conn.rollback()
        raise
    finally:
        curr.close()
        conn.close()

def delete_bill_by_id_HARD(id_):
    conn = get_connection()
    curr = conn.cursor()

    query = f"DELETE FROM {DB_T} WHERE id = %s;"
    try:
        curr.execute(query, (id_, ))
        if curr.rowcount == 0:
            raise mysql.connector.Error("No bill found for given id")
        conn.commit()
    except mysql.connector.Error as e:
        conn.rollback()
        raise
    finally:
        curr.close()
        conn.close()