from fastapi import APIRouter, HTTPException, Query
from ..services import *

router = APIRouter(prefix="/bills", tags=["bills"])


@router.get("")
def status():
    return {"message":"healthy"}

@router.post("/new")
def create_bill(payload: dict):
    try:
        return create_bill_service(
            name=payload["name"],
            due_date=payload["due_date"],
            total_amount=payload["total_amount"],
            category=payload.get("category"),
            status=payload.get("status", "UNPAID"),
        )
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("/all")
def list_bills(upcoming_only: bool = False, days: int = Query(3, ge=1)):
    return list_bills_service(upcoming_only=upcoming_only, days=days)


@router.put("/{bill_id}")
def update_status(bill_id: int, payload: dict):
    try:
        return mark_bill_status_service(bill_id, payload["status"])
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.delete("/{bill_id}")
def delete_bill(bill_id: int):
    try:
        return delete_bill_service(bill_id)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))