"""
SELECT operations on the users table.
"""

from ..connection import get_db_connection


def select_user_by_username(username):
    """Returns the full user row for the given username, or None if not found."""
    query = "SELECT user_id, user_name, user_pass, user_role, user_created_on FROM users WHERE user_name = %s"

    with get_db_connection() as (conn, cursor):
        cursor.execute(query, (username,))
        return cursor.fetchone()


def select_user_by_id(user_id):
    """Returns the full user row for the given id, or None if not found."""
    query = "SELECT user_id, user_name, user_pass, user_role, user_created_on FROM users WHERE user_id = %s"

    with get_db_connection() as (conn, cursor):
        cursor.execute(query, (user_id,))
        return cursor.fetchone()
