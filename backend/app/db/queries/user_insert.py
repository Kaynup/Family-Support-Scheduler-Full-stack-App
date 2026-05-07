"""
INSERT operations on the users table.
"""

from ..connection import get_db_connection


def insert_user(username, password_hash, role):
    """
    Inserts a new user and returns the auto-generated id.
    Raises mysql.connector.IntegrityError if username already exists (UNIQUE constraint).
    """
    query = """
    INSERT INTO users (username, password_hash, role)
    VALUES (%s, %s, %s)
    """

    with get_db_connection() as (conn, cursor):
        cursor.execute(query, (username, password_hash, role))
        return cursor.lastrowid
