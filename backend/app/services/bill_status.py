from ..db import queries as dbq

def mark_bill_status_service(id_, status):
    id_, status = dbq.update_bill_status(id_, status)

    return {
        "OK": True,
        "message": "bill status updated successfully",
        "data": {
            "id": id_,
            "status": status
        }
    }