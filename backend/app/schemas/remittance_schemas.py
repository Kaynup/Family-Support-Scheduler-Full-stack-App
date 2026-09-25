"""
Pydantic schemas for the remittance domain.

RemittanceCreateRequest  — validates POST /remittance/pay payloads.
RemittanceResponse       — shape of a single remittance transaction in responses.
"""

from pydantic import BaseModel, Field

from ..constants import CURRENCY_USDT, PAYMENT_METHOD_STABLECOIN


class RemittanceCreateRequest(BaseModel):
    bill_id: int
    amount: float = Field(..., gt=0)
    currency: str = Field(default=CURRENCY_USDT)
    payment_method: str = Field(default=PAYMENT_METHOD_STABLECOIN)


class RemittanceResponse(BaseModel):
    transaction_id: int
    bill_id: int
    sender_user_id: int
    beneficiary_user_id: int
    amount: float
    currency: str
    transaction_status: str
    payment_method: str
    created_at: str
