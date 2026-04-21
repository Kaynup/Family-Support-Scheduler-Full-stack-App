from datetime import date, timedelta
import time

from backend.app.services import *
from backend.app.db.queries import *


def _create_test_bill_via_service():
    name = f"pytest-svc-{time.time_ns()}"
    due_date = date.today() + timedelta(days=1)
    create_bill_service(name=name, due_date=due_date, total_amount=100.0, status="UNPAID", category="test")
    return name


def _get_bill_id_by_name(name):
    rows = select_all()
    return next(r[0] for r in rows if r[1] == name)


def test_create_bill_service():
    name = _create_test_bill_via_service()
    try:
        bill_id = _get_bill_id_by_name(name)
        assert isinstance(bill_id, int)
    finally:
        delete_bill_by_id(_get_bill_id_by_name(name))


def test_list_bills_service():
    out = list_bills_service()
    assert out["OK"] is True
    assert "total_count" in out


def test_mark_bill_status_service():
    name = _create_test_bill_via_service()
    bill_id = _get_bill_id_by_name(name)
    try:
        out = mark_bill_status_service(bill_id, "PAID")
        assert out["OK"] is True
        assert out["data"]["status"] == "PAID"
        assert not any(r[0] == bill_id for r in select_num_day_dues(3))
    finally:
        delete_bill_by_id(bill_id)


def test_delete_bill_service():
    name = _create_test_bill_via_service()
    bill_id = _get_bill_id_by_name(name)
    out = delete_bill_service(bill_id)
    rows = select_all()
    assert out["OK"] is True
    assert out["data"]["id"] == bill_id
    assert not any(r[0] == bill_id for r in rows)