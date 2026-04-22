from backend.app.db.queries import select_all

def get_bill_id_by_name(name):
    rows = select_all()
    bill_id = next((r[0] for r in rows if r[1] == name), None)
    if bill_id is None:
        raise ValueError(f"Bill with name '{name}' not found")
    return bill_id