from fastapi import APIRouter, HTTPException, Query
from ..services.bill_creation import create_bill_service
from ..services.bill_listing import list_bills_service
from ..services.bill_status import mark_bill_status_service
from ..services.bill_deletion import delete_bill_service
from ..schemas import BillCreateRequest, BillUpdateRequest

router = APIRouter(prefix="/bills", tags=["bills"])


@router.post("/new")
def create_bill(payload: BillCreateRequest):
    try:
        return create_bill_service(
            name=payload.name,
            due_date=payload.due_date,
            total_amount=payload.total_amount,
            category=payload.category,
            status=payload.status,
        )
    except ValueError as exc:
        if "No bill found" in str(exc):
            raise HTTPException(status_code=404, detail=str(exc))
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/all")
def list_bills(upcoming_only: bool = False, days: int = Query(3, ge=1)):
    return list_bills_service(upcoming_only=upcoming_only, days=days)


@router.put("/{bill_id}")
def update_status(bill_id: int, payload: BillUpdateRequest):
    try:
        return mark_bill_status_service(bill_id, payload.status)
    except ValueError as exc:
        if "No bill found" in str(exc):
            raise HTTPException(status_code=404, detail=str(exc))
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.delete("/{bill_id}")
def delete_bill(bill_id: int):
    try:
        return delete_bill_service(bill_id)
    except ValueError as exc:
        if "No bill found" in str(exc):
            raise HTTPException(status_code=404, detail=str(exc))
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))