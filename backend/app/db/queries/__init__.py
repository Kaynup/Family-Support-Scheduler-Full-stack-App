"""
queries/ — one file per SQL operation type per domain object.

Re-exports every query function so callers continue using:
    from app.db import queries as dbq
    dbq.insert_bill(...)
"""

from .bill_delete import soft_delete_bill_by_id
from .bill_insert import insert_bill
from .bill_select import (
    select_all_bills,
    select_bill_by_id,
    select_bills_by_beneficiary,
    select_bills_by_name,
    select_expired_bills,
    select_upcoming_bills,
)
from .bill_update import update_bill_status
from .remittance_insert import insert_remittance_transaction
from .remittance_select import (
    select_remittance_by_beneficiary_id,
    select_remittance_by_bill_id,
    select_remittance_by_sender_id,
)
from .user_insert import insert_user
from .user_select import (
    select_user_by_id,
    select_user_by_username,
    select_users_by_role,
)

__all__ = [
    "insert_bill",
    "insert_remittance_transaction",
    "insert_user",
    "select_all_bills",
    "select_bill_by_id",
    "select_bills_by_beneficiary",
    "select_bills_by_name",
    "select_expired_bills",
    "select_remittance_by_beneficiary_id",
    "select_remittance_by_bill_id",
    "select_remittance_by_sender_id",
    "select_upcoming_bills",
    "select_user_by_id",
    "select_user_by_username",
    "select_users_by_role",
    "soft_delete_bill_by_id",
    "update_bill_status",
]
