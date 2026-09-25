"""
DELETE (soft) operations on the bills table.

Hard deletes are not exposed through the service layer. Soft delete
sets Is_deleted = 'Y' so historical records are preserved.
"""

import mysql.connector

from ...constants import SOFT_DELETE_YES
from ...core.config import settings
from ..connection import get_db_connection

_TABLE = settings.db_table


def soft_delete_bill_by_id(bill_id):
    """
    Marks one bill as deleted by setting Is_deleted = 'Y'.
    Returns the bill_id on success.
    Raises mysql.connector.Error if no row was matched.
    """
    query = f"UPDATE {_TABLE} SET is_deleted = %s WHERE bill_id = %s"

    with get_db_connection() as (_conn, cursor):
        cursor.execute(query, (SOFT_DELETE_YES, bill_id))
        if cursor.rowcount == 0:
            raise mysql.connector.Error(f"No bill found for id {bill_id}")
        return bill_id
