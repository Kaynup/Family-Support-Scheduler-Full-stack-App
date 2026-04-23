from datetime import date, timedelta
import time
from backend.app.db.queries import (
    insert_bill,
    select_all,
    select_num_day_dues,
    update_bill_status,
    delete_bill_by_id
)

# Utils
def _create_test_bill():
    name = f"pytest-{time.time_ns()}"
    due = date.today() + timedelta(days=1)
    bill_id = insert_bill(
        name=name,
        due_date=due,
        total_amount=100.0,
        creation_date=date.today(),
        status="UNPAID",
        category="test"
    )
    return bill_id


# Tests
def test_select_all_returns_list():
    rows = select_all()
    print("\n\nrows:", rows)
    assert isinstance(rows, list)

def test_insert_bill():
    bill_id = _create_test_bill()
    try:
        assert isinstance(bill_id, int)
    finally:
        delete_bill_by_id(bill_id)


def test_select_num_day_dues():
    bill_id = _create_test_bill()
    try:
        assert any(r[0] == bill_id for r in select_num_day_dues(3))
    finally:
        delete_bill_by_id(bill_id)


def test_update_bill_status():
    bill_id = _create_test_bill()
    try:
        assert any(r[0] == bill_id for r in select_num_day_dues(3))
        update_bill_status(bill_id, "PAID")

        row = next(r for r in select_all() if r[0] == bill_id)
        assert row[5] == "PAID"
        assert not any(r[0] == bill_id for r in select_num_day_dues(3))
    finally:
        delete_bill_by_id(bill_id)


def test_delete_bill_by_id():
    bill_id = _create_test_bill()
    try:
        delete_bill_by_id(bill_id)
        rows = select_all()
        assert not any(r[0] == bill_id for r in rows)
    finally:
        rows = select_all()
        if any(r[0] == bill_id for r in rows):
            delete_bill_by_id(bill_id)