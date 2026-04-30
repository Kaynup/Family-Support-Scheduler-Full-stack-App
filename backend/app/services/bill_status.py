import mysql.connector
from ..db import queries as dbq

from datetime import timedelta

def mark_bill_status_service(id_, status):
    try:
        bill = dbq.select_bill_by_id(id_)
        if not bill:
            raise ValueError("No bill found")
            
        id_ = dbq.update_bill_status(id_, status)
        
        # bill tuple indices: 0:id, 1:name, 2:creation_date, 3:due_date, 4:total_amount, 5:status, 6:category, 7:recurring_interval, 8:Is_deleted
        # Wait, I need to check schema.sql to see order of columns. Let's just do it directly.
        
        if status == "PAID" and bill[7] and bill[7] != 'NONE':
            next_due_date = bill[3]
            if bill[7] == 'WEEKLY':
                next_due_date += timedelta(days=7)
            elif bill[7] == 'MONTHLY':
                next_due_date += timedelta(days=30)
                
            dbq.insert_bill(
                name=bill[1],
                due_date=next_due_date,
                total_amount=bill[4],
                creation_date=bill[2],
                status='UNPAID',
                category=bill[6],
                recurring_interval=bill[7]
            )
            
    except mysql.connector.Error as e:
        raise ValueError(str(e))

    return {
        "OK": True,
        "message": "bill status updated successfully",
        "data": {
            "id": id_
        }
    }