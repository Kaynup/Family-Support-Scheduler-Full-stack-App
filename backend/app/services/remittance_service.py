"""
Remittance business logic.

The remittance layer is intentionally thin. It verifies that a bill is
payable, records the transaction, marks the bill paid, and returns the
transaction record. The stablecoin concept is represented by the
currency field — no blockchain infrastructure is required.
"""

from ..db import queries as dbq
from ..core.exceptions import BillNotFoundError, RemittanceValidationError
from ..constants import (
    STATUS_UNPAID,
    STATUS_PAID,
    CURRENCY_USDT,
    PAYMENT_METHOD_STABLECOIN,
    TRANSACTION_COMPLETED,
)


def _format_transaction_row(row):
    """Converts a raw remittance_transactions tuple into a response dict."""
    return {
        "transaction_id":      row[0],
        "bill_id":             row[1],
        "sender_user_id":      row[2],
        "beneficiary_user_id": row[3],
        "amount":              float(row[4]),
        "currency":            row[5],
        "transaction_status":  row[6],
        "payment_method":      row[7],
        "created_at":          str(row[8]),
    }


def pay_bill_via_remittance(bill_id, sender_user_id, amount, currency=CURRENCY_USDT, payment_method=PAYMENT_METHOD_STABLECOIN):
    """
    Executes the full remittance payment flow for one bill:

    1. Fetch the bill — raise BillNotFoundError if absent.
    2. Assert the bill is UNPAID — raise RemittanceValidationError if already paid.
    3. Assert the payment amount covers the bill total.
    4. Insert a COMPLETED remittance transaction record.
    5. Mark the bill as PAID.
    6. Return the transaction envelope.
    """
    bill_row = dbq.select_bill_by_id(bill_id)
    if not bill_row:
        raise BillNotFoundError(f"No bill found with id {bill_id}")

    bill_status = bill_row[5]
    bill_total = float(bill_row[4])
    beneficiary_user_id = bill_row[10] if len(bill_row) > 10 else None

    if bill_status != STATUS_UNPAID:
        raise RemittanceValidationError(f"Bill {bill_id} is already {bill_status} and cannot be paid again.")

    if amount < bill_total:
        raise RemittanceValidationError(
            f"Payment amount {amount} is less than the bill total {bill_total}."
        )

    transaction_id = dbq.insert_remittance_transaction(
        bill_id=bill_id,
        sender_user_id=sender_user_id,
        beneficiary_user_id=beneficiary_user_id,
        amount=amount,
        currency=currency,
        payment_method=payment_method,
    )

    dbq.update_bill_status(bill_id, STATUS_PAID)

    return {
        "OK":      True,
        "message": "Payment processed successfully.",
        "data": {
            "transaction_id":      transaction_id,
            "bill_id":             bill_id,
            "sender_user_id":      sender_user_id,
            "beneficiary_user_id": beneficiary_user_id,
            "amount":              amount,
            "currency":            currency,
            "transaction_status":  TRANSACTION_COMPLETED,
            "payment_method":      payment_method,
        },
    }


def get_remittance_history_for_sender(sender_user_id):
    """Returns all outgoing transactions for the given sender, newest first."""
    rows = dbq.select_remittance_by_sender_id(sender_user_id)
    return {
        "OK":          True,
        "total_count": len(rows),
        "data":        [_format_transaction_row(r) for r in rows],
    }


def get_remittance_history_for_bill(bill_id):
    """Returns all transactions associated with a specific bill."""
    rows = dbq.select_remittance_by_bill_id(bill_id)
    return {
        "OK":          True,
        "total_count": len(rows),
        "data":        [_format_transaction_row(r) for r in rows],
    }
