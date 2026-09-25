"""
services/ — public API of the service layer.

Import services only from here; never import directly from sub-modules
in route handlers. This keeps coupling between layers minimal.
"""

from .auth_service import (
    create_access_token,
    decode_access_token,
    get_current_user,
    login_user,
    register_user,
    require_role,
)
from .bill_service import (
    create_bill,
    delete_bill,
    get_bill_by_id,
    list_bills,
    mark_bill_status,
    search_bills_by_name,
)
from .remittance_service import (
    get_remittance_history_for_beneficiary,
    get_remittance_history_for_sender,
    pay_bill_via_remittance,
)

__all__ = [
    "create_access_token",
    "create_bill",
    "decode_access_token",
    "delete_bill",
    "get_bill_by_id",
    "get_current_user",
    "get_remittance_history_for_beneficiary",
    "get_remittance_history_for_sender",
    "list_bills",
    "login_user",
    "mark_bill_status",
    "pay_bill_via_remittance",
    "register_user",
    "require_role",
    "search_bills_by_name",
]
