from datetime import date
from ..db import queries as dbq

def _value_validation(name, due_date, total_amount, category=None, status="UNPAID"):
    if not name or not str(name).strip():
        raise ValueError("name is a required field")

    if total_amount is None or float(total_amount) <= 0:
        raise ValueError("amount must be at least zero")

    if status not in ("PAID", "UNPAID"):
        raise ValueError("status should be 'PAID' or 'UNPAID'")

    if due_date < date.today():
        raise ValueError("due date cannot be in past")

def create_bill_service(name, due_date, total_amount, category=None, status="UNPAID"):
    _value_validation(name, due_date, total_amount, category=None, status="UNPAID")
    
    dbq.insert_bill(
        name=name.strip(),
        due_date=due_date,
        total_amount=float(total_amount),
        status=status,
        category=category
    )

    return {
        "OK":True,
        "message": "bill created successfully",
        "data": {
            "name": name.strip(),
            "due_date": str(due_date),
            "total_amount": float(total_amount),
            "status": status,
            "category": category
        }
    }