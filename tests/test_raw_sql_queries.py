from datetime import date, timedelta
import os
import sys
import time

from dotenv import load_dotenv

load_dotenv()

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
    insert_bill(name=name, due_date=due, total_amount=100.0, status="UNPAID", category="test")
    return name

def _get_bill_id_by_name(name):
    rows = select_all()
    return next(r[0] for r in rows if r[1] == name)


# Tests
def test_select_all_returns_list():
    rows = select_all()
    print("rows:", rows)
    assert isinstance(rows, list)

def test_insert_bill():
    name = _create_test_bill()
    try:
        bill_id = _get_bill_id_by_name(name)
        assert isinstance(bill_id, int)
    finally:
        delete_bill_by_id(_get_bill_id_by_name(name))


def test_select_num_day_dues():
    name = _create_test_bill()
    bill_id = _get_bill_id_by_name(name)
    try:
        assert any(r[0] == bill_id for r in select_num_day_dues(3))
    finally:
        delete_bill_by_id(bill_id)


def test_update_bill_status():
    name = _create_test_bill()
    bill_id = _get_bill_id_by_name(name)
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
    bill_id = _get_bill_id_by_name(name)
    delete_bill_by_id(bill_id)
    rows = select_all()
    assert not any(r[0] == bill_id for r in rows)