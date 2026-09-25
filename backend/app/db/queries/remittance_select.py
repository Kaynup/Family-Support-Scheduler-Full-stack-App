"""
SELECT operations on the remittance_transactions table.
"""

from ..connection import get_db_connection


def select_remittance_by_bill_id(bill_id):
    """Returns all remittance transactions associated with a specific bill."""
    query = """
    SELECT transaction_id, bill_id, sender_user_id, beneficiary_user_id,
           amount, currency, transaction_status, payment_method, transaction_on
    FROM remittance_transactions
    WHERE bill_id = %s
    ORDER BY transaction_on DESC
    """

    with get_db_connection() as (_conn, cursor):
        cursor.execute(query, (bill_id,))
        return cursor.fetchall()


def select_remittance_by_sender_id(sender_user_id):
    """Returns all remittance transactions sent by a specific sender with bill and beneficiary details."""
    query = """
    SELECT rt.transaction_id, rt.bill_id, rt.sender_user_id, rt.beneficiary_user_id,
           rt.amount, rt.currency, rt.transaction_status, rt.payment_method, rt.transaction_on,
           b.bill_name,
           u.user_name as beneficiary_username
    FROM remittance_transactions rt
    LEFT JOIN bills b ON rt.bill_id = b.bill_id
    LEFT JOIN users u ON rt.beneficiary_user_id = u.user_id
    WHERE rt.sender_user_id = %s
    ORDER BY rt.transaction_on DESC
    """

    with get_db_connection() as (_conn, cursor):
        cursor.execute(query, (sender_user_id,))
        return cursor.fetchall()


def select_remittance_by_beneficiary_id(beneficiary_user_id):
    """Returns all remittance transactions received by a specific beneficiary with bill and sender details."""
    query = """
    SELECT rt.transaction_id, rt.bill_id, rt.sender_user_id, rt.beneficiary_user_id,
           rt.amount, rt.currency, rt.transaction_status, rt.payment_method, rt.transaction_on,
           b.bill_name,
           u.user_name as sender_username
    FROM remittance_transactions rt
    LEFT JOIN bills b ON rt.bill_id = b.bill_id
    LEFT JOIN users u ON rt.sender_user_id = u.user_id
    WHERE rt.beneficiary_user_id = %s
    ORDER BY rt.transaction_on DESC
    """

    with get_db_connection() as (_conn, cursor):
        cursor.execute(query, (beneficiary_user_id,))
        return cursor.fetchall()
