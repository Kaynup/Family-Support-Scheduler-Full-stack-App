import app.db.queries as dbq

def _value_validation(id, status):
    if not isinstance(id, int) or id <= 0:
        raise ValueError("bill id is to be a positive integer")
    if status.upper().strip() not in ("PAID", "UNPAID"):
        raise ValueError("status must be PAID or UNPAID")

def mark_bill_status_service(id, status):
    _value_validation()

    update_bill_status(id, status)

    return {
        "OK": True,
        "message": "bill status updated successfully",
        "data": {
            "id": id,
            "status": status
        }
    }