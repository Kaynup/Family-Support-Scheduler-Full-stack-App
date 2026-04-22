from ..db import queries as dbq

def delete_bill_service(id):
    dbq.delete_bill_by_id(id)

    return {
        "OK": True,
        "message": "deleted row successfully",
        "data": {
            "id": id
        }
    }