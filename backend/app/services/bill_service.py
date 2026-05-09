"""
All bill-domain business logic in one cohesive module.

Each function has a single named responsibility. Shared formatting
logic (_format_bill_row) is defined once here, eliminating the
duplication that existed across the old bill_listing.py and bill_search.py.
"""

from datetime import date
import mysql.connector
from ..db import queries as dbq
from ..constants import STATUS_UNPAID
from ..core.exceptions import BillNotFoundError


def _format_bill_row(row):
    """Converts a raw database tuple into a consistent bill dictionary."""
    return {
        "id":                 row[0],
        "name":               row[1],
        "status":             row[2],
        "creation_date":      str(row[4]),
        "due_date":           str(row[5]),
        "total_amount":       float(row[6]),
        "category":           row[7],
        "recurring_interval": row[8] if len(row) > 7 else "NONE",
        "is_expired":         row[10] if len(row) > 8 else "N",
    }


def create_bill(name, due_date, total_amount, creation_date=None, category=None, recurring_interval="NONE", status=STATUS_UNPAID):
    """
    Inserts a new bill record into the database.
    Returns a response envelope containing the created bill's id and fields.
    """
    if creation_date is None:
        creation_date = date.today()

    due_date_obj = date.fromisoformat(due_date) if isinstance(due_date, str) else due_date

    try:
        new_id = dbq.insert_bill(
            name=name,
            due_date=due_date_obj,
            total_amount=total_amount,
            creation_date=creation_date,
            status=status,
            category=category,
            recurring_interval=recurring_interval,
        )
    except mysql.connector.Error as exc:
        raise ValueError(str(exc))

    return {
        "OK": True,
        "message": f"bill created successfully on {creation_date}",
        "data": {
            "id":                 new_id,
            "name":               name,
            "due_date":           str(due_date_obj),
            "total_amount":       total_amount,
            "creation_date":      str(creation_date),
            "status":             status,
            "category":           category,
            "recurring_interval": recurring_interval,
        },
    }


def list_bills(upcoming_only=False, expired_only=False, days=3, beneficiary_id=None):
    """
    Returns all bills, or a filtered subset.

    upcoming_only — bills due within the next `days` days (UNPAID only).
    expired_only  — bills that are past due and still UNPAID.
    Default       — all non-deleted bills.
    """
    if expired_only and beneficiary_id is not None:
        rows = dbq.select_expired_bills()
        rows = [r for r in rows if r[3] == beneficiary_id]
    elif upcoming_only and beneficiary_id is not None:
        rows = dbq.select_upcoming_bills(days)
        rows = [r for r in rows if r[3] == beneficiary_id]
    elif beneficiary_id is not None:
        rows = dbq.select_bills_by_beneficiary(beneficiary_id)
    elif expired_only:
        rows = dbq.select_expired_bills()
    elif upcoming_only:
        rows = dbq.select_upcoming_bills(days)
    else:
        rows = dbq.select_all_bills()

    return {
        "OK":          True,
        "total_count": len(rows),
        "data":        [_format_bill_row(r) for r in rows],
    }


def get_bill_by_id(bill_id):
    """
    Returns a single formatted bill dict.
    Raises BillNotFoundError if the bill does not exist or is soft-deleted.
    """
    row = dbq.select_bill_by_id(bill_id)
    if not row:
        raise BillNotFoundError(f"No bill found with id {bill_id}")
    return _format_bill_row(row)


def mark_bill_status(bill_id, new_status):
    """
    Updates the status of one bill.
    Raises BillNotFoundError if the bill does not exist.
    Returns a response envelope containing the updated id.
    """
    row = dbq.select_bill_by_id(bill_id)
    if not row:
        raise BillNotFoundError(f"No bill found with id {bill_id}")

    try:
        dbq.update_bill_status(bill_id, new_status)
    except mysql.connector.Error as exc:
        raise ValueError(str(exc))

    return {
        "OK":      True,
        "message": "bill status updated successfully",
        "data":    {"id": bill_id},
    }


def delete_bill(bill_id):
    """
    Soft-deletes one bill by setting Is_deleted = 'Y'.
    Raises BillNotFoundError if the bill does not exist.
    Returns a response envelope containing the deleted id.
    """
    try:
        dbq.soft_delete_bill_by_id(bill_id)
    except mysql.connector.Error as exc:
        raise BillNotFoundError(str(exc))

    return {
        "OK":      True,
        "message": "bill deleted successfully",
        "data":    {"id": bill_id},
    }


def search_bills_by_name(name):
    """
    Returns all non-deleted bills whose name contains `name` (case-insensitive).
    Returns an empty data list when no matches are found.
    """
    rows = dbq.select_bills_by_name(name)
    return {
        "OK":          True,
        "total_count": len(rows),
        "data":        [_format_bill_row(r) for r in rows],
    }
