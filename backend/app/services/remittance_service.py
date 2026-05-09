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


def _extract_bill_payment_fields(bill_row):
    """Extracts status, total, and beneficiary id from either supported bill tuple layout."""
    # Current DB layout from `bills` table:
    # (id, name, status, user_id, creation_date, due_date, total_amount, ...)
    if len(bill_row) > 6 and bill_row[2] in (STATUS_UNPAID, STATUS_PAID):
        return bill_row[2], float(bill_row[6]), bill_row[3] if len(bill_row) > 3 else None

    # Legacy layout used in older tests/mocks:
    # (id, name, creation_date, due_date, total_amount, status, ..., beneficiary_id)
    if len(bill_row) > 5 and bill_row[5] in (STATUS_UNPAID, STATUS_PAID):
        beneficiary_user_id = bill_row[10] if len(bill_row) > 10 else None
        return bill_row[5], float(bill_row[4]), beneficiary_user_id

    raise RemittanceValidationError("Unsupported bill row format for remittance processing.")


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
        "bill_name":           row[9] if len(row) > 9 else None,
        "other_username":      row[10] if len(row) > 10 else None,
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

    bill_status, bill_total, beneficiary_user_id = _extract_bill_payment_fields(bill_row)

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

    # Auto-generate next projection if recurring
    if len(bill_row) > 8:
        b_interval = bill_row[8]
        if b_interval in ("WEEKLY", "MONTHLY"):
            import datetime
            import calendar
            
            b_name = bill_row[1]
            b_beneficiary_id = bill_row[3] if len(bill_row) > 3 else beneficiary_user_id
            b_due_date = bill_row[5]
            b_total = bill_row[6]
            b_category = bill_row[7]
            
            if isinstance(b_due_date, str):
                b_due_date = datetime.date.fromisoformat(b_due_date)
            
            if b_interval == "WEEKLY":
                next_due_date = b_due_date + datetime.timedelta(days=7)
            else: # MONTHLY
                next_month = b_due_date.month + 1 if b_due_date.month < 12 else 1
                next_year = b_due_date.year if b_due_date.month < 12 else b_due_date.year + 1
                days_in_next_month = calendar.monthrange(next_year, next_month)[1]
                next_day = min(b_due_date.day, days_in_next_month)
                next_due_date = datetime.date(next_year, next_month, next_day)
                
            dbq.insert_bill(
                name=b_name,
                due_date=next_due_date,
                total_amount=b_total,
                creation_date=datetime.date.today(),
                status=STATUS_UNPAID,
                category=b_category,
                recurring_interval=b_interval,
                user_id=b_beneficiary_id
            )

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


def get_remittance_history_for_beneficiary(beneficiary_user_id):
    """Returns all incoming transactions for the given beneficiary, newest first."""
    rows = dbq.select_remittance_by_beneficiary_id(beneficiary_user_id)
    return {
        "OK":          True,
        "total_count": len(rows),
        "data":        [_format_transaction_row(r) for r in rows],
    }