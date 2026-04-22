from datetime import date
from ..db import queries as dbq

def create_bill_service(name, due_date, total_amount, category=None, status="UNPAID"):
    due_date_obj = date.fromisoformat(due_date)
    
    dbq.insert_bill(
        name=name,
        due_date=due_date_obj,
        total_amount=total_amount,
        status=status,
        category=category
    )

    return {
        "OK": True,
        "message": "bill created successfully",
        "data": {
            "name": name,
            "due_date": due_date,
            "total_amount": total_amount,
            "status": status,
            "category": category
        }
    }