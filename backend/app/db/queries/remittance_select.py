"""
SELECT operations on the remittance_transactions table.
"""

from ..connection import get_db_connection


def select_remittance_by_bill_id(bill_id):
    """Returns all remittance transactions associated with a specific bill."""
    query = """
    SELECT transaction_id, bill_id, sender_user_id, beneficiary_user_id,
           amount, currency, transaction_status, payment_method, created_at
    FROM remittance_transactions
    WHERE bill_id = %s
    ORDER BY created_at DESC
    """

    with get_db_connection() as (conn, cursor):
        cursor.execute(query, (bill_id,))
        return cursor.fetchall()


def select_remittance_by_sender_id(sender_user_id):
    """Returns all remittance transactions sent by a specific sender, newest first."""
    query = """
    SELECT transaction_id, bill_id, sender_user_id, beneficiary_user_id,
           amount, currency, transaction_status, payment_method, created_at
    FROM remittance_transactions
    WHERE sender_user_id = %s
    ORDER BY created_at DESC
    """

    with get_db_connection() as (conn, cursor):
        cursor.execute(query, (sender_user_id,))
        return cursor.fetchall()
