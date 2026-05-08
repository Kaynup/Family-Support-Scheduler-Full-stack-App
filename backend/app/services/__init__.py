"""
services/ — public API of the service layer.

Import services only from here; never import directly from sub-modules
in route handlers. This keeps coupling between layers minimal.
"""

from .bill_service import (
    create_bill,
    list_bills,
    get_bill_by_id,
    mark_bill_status,
    delete_bill,
    search_bills_by_name,
)
from .auth_service import (
    register_user,
    login_user,
    get_current_user,
    require_role,
    create_access_token,
    decode_access_token,
)
from .remittance_service import (
    pay_bill_via_remittance,
    get_remittance_history_for_sender,
    get_remittance_history_for_beneficiary,
)

__all__ = [
    "create_bill",
    "list_bills",
    "get_bill_by_id",
    "mark_bill_status",
    "delete_bill",
    "search_bills_by_name",
    "register_user",
    "login_user",
    "get_current_user",
    "require_role",
    "create_access_token",
    "decode_access_token",
    "pay_bill_via_remittance",
    "get_remittance_history_for_sender",
    "get_remittance_history_for_beneficiary",
]