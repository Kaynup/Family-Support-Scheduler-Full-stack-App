from datetime import date
import mysql.connector
from ..db import queries as dbq

def create_bill_service(name, due_date, total_amount, creation_date=None, category=None, status="UNPAID"):

    if creation_date is None:
        creation_date = date.today()
    due_date_iso = date.fromisoformat(due_date)
    
    try:
        id_ = dbq.insert_bill(
            name=name,
            due_date=due_date_iso,
            total_amount=total_amount,
            creation_date=creation_date,
            status=status,
            category=category
        )
    except mysql.connector.Error as e:
        raise ValueError(str(e))

    return {
        "OK": True,
        "message": f"bill created successfully on {creation_date}",
        "data": {
            "name": name,
            "due_date": due_date,
            "total_amount": total_amount,
            "status": status,
            "category": category
        }
    }