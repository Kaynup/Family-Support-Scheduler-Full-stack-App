"""
Bill route handlers — /bills prefix.

Each handler does exactly three things:
    1. Receives and validates the request (Pydantic does this automatically).
    2. Calls one service function.
    3. Maps typed exceptions to appropriate HTTP status codes.

No business logic lives here.
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from ..services.bill_service import (
    create_bill,
    list_bills,
    mark_bill_status,
    delete_bill,
    search_bills_by_name,
)
from ..schemas.bill_schemas import BillCreateRequest, BillUpdateRequest
from ..core.exceptions import BillNotFoundError
from ..dependencies import get_current_user_dependency, require_beneficiary_role

router = APIRouter(prefix="/bills", tags=["bills"])


@router.post("/new", status_code=201)
def create_bill_route(payload: BillCreateRequest, current_user: dict = Depends(require_beneficiary_role)):
    """Creates a new bill. Beneficiary role required."""
    try:
        return create_bill(
            name=payload.name,
            due_date=payload.due_date.isoformat(),
            total_amount=payload.total_amount,
            creation_date=payload.creation_date,
            category=payload.category,
            recurring_interval=payload.recurring_interval,
            status=payload.status.value,
        )
    except BillNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/search")
def search_bills_route(name: str, current_user: dict = Depends(get_current_user_dependency)):
    """Searches bills by name substring. Scoped to the user's own bills if beneficiary."""
    beneficiary_id = int(current_user["sub"]) if current_user["role"] == "beneficiary" else None
    results = search_bills_by_name(name=name)
    if beneficiary_id is not None:
        # Filter results to only include the beneficiary's own bills
        filtered = [b for b in results.get("data", []) if b.get("user_id") == beneficiary_id]
        return {"OK": True, "total_count": len(filtered), "data": filtered}
    return results


@router.get("/all")
def list_bills_route(
    upcoming_only: bool = False,
    expired_only: bool = False,
    days: int = Query(3, ge=1),
    beneficiary_id: int | None = None,
    current_user: dict = Depends(get_current_user_dependency),
):
    """Returns all bills or a filtered subset based on query parameters."""
    if current_user["role"] == "beneficiary":
        beneficiary_id = int(current_user["sub"])
    return list_bills(upcoming_only=upcoming_only, expired_only=expired_only, days=days, beneficiary_id=beneficiary_id)


@router.get("/upcoming")
def list_upcoming_bills_route(days: int = Query(3, ge=1), current_user: dict = Depends(get_current_user_dependency)):
    """Returns unpaid bills due within the given number of days."""
    beneficiary_id = int(current_user["sub"]) if current_user["role"] == "beneficiary" else None
    return list_bills(upcoming_only=True, days=days, beneficiary_id=beneficiary_id)


@router.get("/expired")
def list_expired_bills_route(current_user: dict = Depends(get_current_user_dependency)):
    """Returns unpaid bills that are past their due date."""
    beneficiary_id = int(current_user["sub"]) if current_user["role"] == "beneficiary" else None
    return list_bills(expired_only=True, beneficiary_id=beneficiary_id)


@router.put("/{bill_id}")
def update_bill_status_route(bill_id: int, payload: BillUpdateRequest):
    """Updates the status of one bill."""
    try:
        return mark_bill_status(bill_id, payload.status.value)
    except BillNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.delete("/{bill_id}")
def delete_bill_route(bill_id: int, current_user: dict = Depends(require_beneficiary_role)):
    """Soft-deletes one bill. Beneficiary role required."""
    try:
        return delete_bill(bill_id)
    except BillNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
