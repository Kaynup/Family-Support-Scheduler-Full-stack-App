"""
INSERT operations on the bills table.
"""

from ...core.config import settings
from ..connection import get_db_connection

_TABLE = settings.db_table


def insert_bill(
    name,
    due_date,
    total_amount,
    creation_date,
    status,
    category,
    recurring_interval,
    user_id=None,
):
    """
    Inserts a new bill row and returns the auto-generated id.
    Raises on any database error; the context manager handles rollback.
    """
    if user_id is not None:
        query = f"""
        INSERT INTO {_TABLE}
            (bill_name, creation_date, due_date, total_amount, bill_status, category, recurring_interval, user_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            name,
            creation_date,
            due_date,
            total_amount,
            status,
            category,
            recurring_interval,
            user_id,
        )
    else:
        query = f"""
        INSERT INTO {_TABLE}
            (bill_name, creation_date, due_date, total_amount, bill_status, category, recurring_interval)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            name,
            creation_date,
            due_date,
            total_amount,
            status,
            category,
            recurring_interval,
        )

    with get_db_connection() as (_conn, cursor):
        cursor.execute(query, values)
        return cursor.lastrowid
