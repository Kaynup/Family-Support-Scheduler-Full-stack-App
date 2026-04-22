from ..db import queries as dbq

def delete_bill_service(id):
    if not isinstance(id, int) or id <= 0:
        raise ValueError("bill id is to be a positive integer")
    
    dbq.delete_bill_by_id(id)

    return {
        "OK": True,
        "message": "deleted row successfully",
        "data": {
            "id": id
        }
    }