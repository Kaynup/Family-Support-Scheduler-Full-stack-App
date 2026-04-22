from ..db import queries as dbq

def _value_validation(id, status):
    if not isinstance(id, int) or id <= 0:
        raise ValueError("bill id is to be a positive integer")
    if status.upper().strip() not in ("PAID", "UNPAID"):
        raise ValueError("status must be PAID or UNPAID")

def mark_bill_status_service(id_, status):
    _value_validation(id_, status)

    id_, status = dbq.update_bill_status(id_, status)
    return {
        "OK": True,
        "message": "bill status updated successfully",
        "data": {
            "id": id_,
            "status": status
        }
    }