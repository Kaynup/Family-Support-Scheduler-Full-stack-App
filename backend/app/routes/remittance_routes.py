"""
Remittance route handlers — /remittance prefix.

POST /remittance/pay                    — sender pays a beneficiary bill via remittance.
GET  /remittance/history                — sender views their outgoing transaction history.
GET  /remittance/history/beneficiary    — beneficiary views incoming payments for their bills.
"""

from fastapi import APIRouter, HTTPException, Depends
from ..services.remittance_service import (
    pay_bill_via_remittance,
    get_remittance_history_for_sender,
    get_remittance_history_for_beneficiary,
)
from ..schemas.remittance_schemas import RemittanceCreateRequest
from ..core.exceptions import BillNotFoundError, RemittanceValidationError
from ..dependencies import require_sender_role, require_beneficiary_role

router = APIRouter(prefix="/remittance", tags=["remittance"])


@router.post("/pay", status_code=201)
def pay_bill_route(payload: RemittanceCreateRequest, current_user: dict = Depends(require_sender_role)):
    """
    Processes a remittance payment for one bill.
    Sender role required. Returns the created transaction record.
    """
    sender_user_id = int(current_user["sub"])
    try:
        return pay_bill_via_remittance(
            bill_id=payload.bill_id,
            sender_user_id=sender_user_id,
            amount=payload.amount,
            currency=payload.currency,
            payment_method=payload.payment_method,
        )
    except BillNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except RemittanceValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/history")
def remittance_history_route(current_user: dict = Depends(require_sender_role)):
    """
    Returns all outgoing remittance transactions for the authenticated sender.
    Sender role required.
    """
    sender_user_id = int(current_user["sub"])
    try:
        return get_remittance_history_for_sender(sender_user_id)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/history/beneficiary")
def remittance_history_beneficiary_route(current_user: dict = Depends(require_beneficiary_role)):
    """
    Returns all incoming remittance transactions for the authenticated beneficiary.
    Beneficiary role required.
    """
    beneficiary_user_id = int(current_user["sub"])
    try:
        return get_remittance_history_for_beneficiary(beneficiary_user_id)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
