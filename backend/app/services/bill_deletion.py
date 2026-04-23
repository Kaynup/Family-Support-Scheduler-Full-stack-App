import mysql.connector
from ..db import queries as dbq

def delete_bill_service(id):
    try:
        dbq.delete_bill_by_id(id)
    except mysql.connector.Error as e:
        raise ValueError(str(e))

    return {
        "OK": True,
        "message": "deleted row successfully",
        "data": {
            "id": id
        }
    }