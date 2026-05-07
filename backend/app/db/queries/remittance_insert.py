"""
INSERT operations on the remittance_transactions table.
"""

from ..connection import get_db_connection


def insert_remittance_transaction(bill_id, sender_user_id, beneficiary_user_id, amount, currency, payment_method):
    """
    Records a new remittance transaction and returns the auto-generated transaction_id.
    transaction_status is set to COMPLETED immediately on insert (simple synchronous flow).
    """
    query = """
    INSERT INTO remittance_transactions
        (bill_id, sender_user_id, beneficiary_user_id, amount, currency, transaction_status, payment_method)
    VALUES (%s, %s, %s, %s, %s, 'COMPLETED', %s)
    """
    values = (bill_id, sender_user_id, beneficiary_user_id, amount, currency, payment_method)

    with get_db_connection() as (conn, cursor):
        cursor.execute(query, values)
        return cursor.lastrowid
