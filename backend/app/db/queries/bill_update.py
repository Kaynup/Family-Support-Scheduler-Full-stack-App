"""
UPDATE operations on the bills table.
"""

import mysql.connector
from ..connection import get_db_connection
from ...core.config import settings
from ...constants import SOFT_DELETE_NO

_TABLE = settings.db_table


def update_bill_status(bill_id, status):
    """
    Updates the status column for one non-deleted bill.
    Returns the bill_id on success.
    Raises mysql.connector.Error if no row was matched.
    """
    query = f"UPDATE {_TABLE} SET bill_status = %s WHERE bill_id = %s AND is_deleted = %s"

    with get_db_connection() as (conn, cursor):
        cursor.execute(query, (status, bill_id, SOFT_DELETE_NO))
        if cursor.rowcount == 0:
            raise mysql.connector.Error(f"No bill found for id {bill_id}")
        return bill_id
