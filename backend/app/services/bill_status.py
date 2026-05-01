import mysql.connector
from ..db import queries as dbq

import calendar
from datetime import timedelta

def mark_bill_status_service(id_, status):
    try:
        bill = dbq.select_bill_by_id(id_)
        if not bill:
            raise ValueError("No bill found")
            
        id_ = dbq.update_bill_status(id_, status)
            
    except mysql.connector.Error as e:
        raise ValueError(str(e))

    return {
        "OK": True,
        "message": "bill status updated successfully",
        "data": {
            "id": id_
        }
    }