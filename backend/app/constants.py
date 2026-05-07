"""
Central store for all magic strings and reusable constant values used
across the backend. Import from here instead of writing raw string literals.
"""

STATUS_PAID = "PAID"
STATUS_UNPAID = "UNPAID"

ROLE_SENDER = "sender"
ROLE_BENEFICIARY = "beneficiary"

INTERVAL_NONE = "NONE"
INTERVAL_WEEKLY = "WEEKLY"
INTERVAL_MONTHLY = "MONTHLY"

SOFT_DELETE_YES = "Y"
SOFT_DELETE_NO = "N"

EXPIRED_YES = "Y"
EXPIRED_NO = "N"

CURRENCY_USDT = "USDT"
CURRENCY_USDC = "USDC"

TRANSACTION_PENDING = "PENDING"
TRANSACTION_COMPLETED = "COMPLETED"
TRANSACTION_FAILED = "FAILED"

PAYMENT_METHOD_STABLECOIN = "stablecoin"
