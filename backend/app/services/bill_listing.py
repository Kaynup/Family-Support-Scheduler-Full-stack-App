from ..db import queries as dbq

def _format_tuple(row):
    return {
        "id": row[0],
        "name": row[1],
        "creation_date": str(row[2]),
        "due_date": str(row[3]),
        "total_amount": float(row[4]),
        "status": row[5],
        "category": row[6],
    }

def list_bills_service(upcoming_only=False, days=3):
    if upcoming_only:
        rows = dbq.select_num_day_dues(days)
    else:
        rows = dbq.select_all()
    return {
        "OK":True,
        "total_count": len(rows),
        "data": [_format_tuple(r) for r in rows]
    }