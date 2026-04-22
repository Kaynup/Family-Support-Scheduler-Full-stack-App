from datetime import date, timedelta
import time
from backend.app.db.queries import (
    insert_bill,
    select_all,
    select_num_day_dues,
    update_bill_status,
    delete_bill_by_id
)
from backend.app.services_utils import get_bill_id_by_name

# Utils
def _create_test_bill():
    name = f"pytest-{time.time_ns()}"
    due = date.today() + timedelta(days=1)
    insert_bill(name=name, due_date=due, total_amount=100.0, status="UNPAID", category="test")
    return name


# Tests
def test_select_all_returns_list():
    rows = select_all()
    print("\n\nrows:", rows)
    assert isinstance(rows, list)

def test_insert_bill():
    name = _create_test_bill()
    try:
        bill_id = get_bill_id_by_name(name)
        assert isinstance(bill_id, int)
    finally:
        rows = select_all()
        bill_ids = [r[0] for r in rows if r[1] == name]
        for bill_id in bill_ids:
            delete_bill_by_id(bill_id)


def test_select_num_day_dues():
    name = _create_test_bill()
    bill_id = get_bill_id_by_name(name)
    try:
        assert any(r[0] == bill_id for r in select_num_day_dues(3))
    finally:
        delete_bill_by_id(bill_id)


def test_update_bill_status():
    name = _create_test_bill()
    bill_id = get_bill_id_by_name(name)
    try:
        assert any(r[0] == bill_id for r in select_num_day_dues(3))
        update_bill_status(bill_id, "PAID")

        row = next(r for r in select_all() if r[0] == bill_id)
        assert row[5] == "PAID"
        assert not any(r[0] == bill_id for r in select_num_day_dues(3))
    finally:
        delete_bill_by_id(bill_id)


def test_delete_bill_by_id():
    name = _create_test_bill()
    bill_id = get_bill_id_by_name(name)
    try:
        delete_bill_by_id(bill_id)
        rows = select_all()
        assert not any(r[0] == bill_id for r in rows)
    finally:
        rows = select_all()
        for row in rows:
            if row[1] == name:
                delete_bill_by_id(row[0])