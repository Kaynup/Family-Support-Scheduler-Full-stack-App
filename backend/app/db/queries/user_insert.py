"""
INSERT operations on the users table.
"""

from ..connection import get_db_connection


def insert_user(username, password, role):
    """
    Inserts a new user and returns the auto-generated id.
    Raises mysql.connector.IntegrityError if username already exists (UNIQUE constraint).
    """
    query = """
    INSERT INTO users (user_name, user_pass, user_role)
    VALUES (%s, %s, %s)
    """

    with get_db_connection() as (_conn, cursor):
        cursor.execute(query, (username, password, role))
        return cursor.lastrowid
