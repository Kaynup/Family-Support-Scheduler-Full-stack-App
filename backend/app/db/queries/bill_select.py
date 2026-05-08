"""
SELECT operations on the bills table.
"""

from ..connection import get_db_connection
from ...core.config import settings
from ...constants import STATUS_UNPAID, SOFT_DELETE_NO, EXPIRED_YES

_TABLE = settings.db_table


def select_all_bills():
    """Returns all non-deleted bills ordered by due date ascending."""
    query = f"SELECT * FROM {_TABLE} WHERE is_deleted = %s ORDER BY due_date ASC"

    with get_db_connection() as (conn, cursor):
        cursor.execute(query, (SOFT_DELETE_NO,))
        return cursor.fetchall()


def select_bill_by_id(bill_id):
    """Returns one non-deleted bill row by its primary key, or None if absent."""
    query = f"SELECT * FROM {_TABLE} WHERE bill_id = %s AND is_deleted = %s"

    with get_db_connection() as (conn, cursor):
        cursor.execute(query, (bill_id, SOFT_DELETE_NO))
        return cursor.fetchone()


def select_bills_by_name(name):
    """Returns all non-deleted bills whose name contains the given substring (case-insensitive)."""
    query = f"SELECT * FROM {_TABLE} WHERE LOWER(bill_name) LIKE LOWER(%s) AND is_deleted = %s"

    with get_db_connection() as (conn, cursor):
        cursor.execute(query, (f"%{name}%", SOFT_DELETE_NO))
        return cursor.fetchall()


def select_upcoming_bills(num_days=3):
    """Returns unpaid non-deleted bills due within num_days days, ordered by due date."""
    query = f"""
    SELECT * FROM {_TABLE}
    WHERE bill_status = %s
      AND is_deleted = %s
      AND due_date <= DATE_ADD(CURDATE(), INTERVAL %s DAY)
    ORDER BY due_date ASC
    """

    with get_db_connection() as (conn, cursor):
        cursor.execute(query, (STATUS_UNPAID, SOFT_DELETE_NO, num_days))
        return cursor.fetchall()


def select_bills_by_beneficiary(beneficiary_id):
    """Returns all non-deleted bills belonging to a specific beneficiary ordered by due date."""
    query = f"SELECT * FROM {_TABLE} WHERE user_id = %s AND is_deleted = %s ORDER BY due_date ASC"

    with get_db_connection() as (conn, cursor):
        cursor.execute(query, (beneficiary_id, SOFT_DELETE_NO))
        return cursor.fetchall()


def select_expired_bills():
    """Returns unpaid non-deleted bills that are marked expired or are past their due date."""
    query = f"""
    SELECT * FROM {_TABLE}
    WHERE bill_status = %s
      AND is_deleted = %s
      AND (is_expired = %s OR due_date < CURDATE())
    ORDER BY due_date ASC
    """

    with get_db_connection() as (conn, cursor):
        cursor.execute(query, (STATUS_UNPAID, SOFT_DELETE_NO, EXPIRED_YES))
        return cursor.fetchall()
