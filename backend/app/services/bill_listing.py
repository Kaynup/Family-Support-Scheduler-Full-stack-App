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
        "recurring_interval": row[7] if len(row) > 7 else "NONE",
        "is_expired": row[8] if len(row) > 8 else "N"
    }

def list_bills_service(upcoming_only=False, expired_only=False, days=3):
    if expired_only:
        rows = dbq.select_expired_bills()
    elif upcoming_only:
        rows = dbq.select_num_day_dues(days)
    else:
        rows = dbq.select_all()
    return {
        "OK":True,
        "total_count": len(rows),
        "data": [_format_tuple(r) for r in rows]
    }