"""
queries/ — one file per SQL operation type per domain object.

Re-exports every query function so callers continue using:
    from app.db import queries as dbq
    dbq.insert_bill(...)
"""

from .bill_insert import insert_bill
from .bill_select import (
    select_all_bills,
    select_bill_by_id,
    select_bills_by_name,
    select_upcoming_bills,
    select_expired_bills,
)
from .bill_update import update_bill_status
from .bill_delete import soft_delete_bill_by_id
from .user_insert import insert_user
from .user_select import select_user_by_username, select_user_by_id
from .remittance_insert import insert_remittance_transaction
from .remittance_select import (
    select_remittance_by_bill_id,
    select_remittance_by_sender_id,
)

__all__ = [
    "insert_bill",
    "select_all_bills",
    "select_bill_by_id",
    "select_bills_by_name",
    "select_upcoming_bills",
    "select_expired_bills",
    "update_bill_status",
    "soft_delete_bill_by_id",
    "insert_user",
    "select_user_by_username",
    "select_user_by_id",
    "insert_remittance_transaction",
    "select_remittance_by_bill_id",
    "select_remittance_by_sender_id",
]
