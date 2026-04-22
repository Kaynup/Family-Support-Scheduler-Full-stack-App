from datetime import date, timedelta
import time

from backend.app.services.bill_creation import create_bill_service
from backend.app.services.bill_listing import list_bills_service
from backend.app.services.bill_status import mark_bill_status_service
from backend.app.services.bill_deletion import delete_bill_service
from backend.app.db.queries import select_all, select_num_day_dues, delete_bill_by_id
from backend.app.services_utils import get_bill_id_by_name


def _create_test_bill_with_due_days(days_ahead=1):
    name = f"pytest-svc-upcoming-{days_ahead}-{time.time_ns()}"
    due_date = (date.today() + timedelta(days=days_ahead)).isoformat()
    create_bill_service(name=name, due_date=due_date, total_amount=100.0, status="UNPAID", category="test")
    return name


def test_create_bill_service():
    name = _create_test_bill_with_due_days()
    try:
        bill_id = get_bill_id_by_name(name)
        assert isinstance(bill_id, int)
    finally:
        rows = select_all()
        for row in rows:
            if row[1] == name:
                delete_bill_by_id(row[0])


def test_list_bills_service():
    out = list_bills_service()
    assert out["OK"] is True
    assert "total_count" in out


def test_mark_bill_status_service():
    name = _create_test_bill_with_due_days()
    bill_id = get_bill_id_by_name(name)
    try:
        out = mark_bill_status_service(bill_id, "PAID")
        assert out["OK"] is True
        assert out["data"]["status"] == "PAID"
        assert not any(r[0] == bill_id for r in select_num_day_dues(3))
    finally:
        delete_bill_by_id(bill_id)


def test_delete_bill_service():
    name = _create_test_bill_with_due_days()
    bill_id = get_bill_id_by_name(name)
    try:
        out = delete_bill_service(bill_id)
        rows = select_all()
        assert out["OK"] is True
        assert out["data"]["id"] == bill_id
        assert not any(r[0] == bill_id for r in rows)
    finally:
        rows = select_all()
        for row in rows:
            if row[1] == name:
                delete_bill_by_id(row[0])


def test_list_bills_service_upcoming_boundary_days_3():
    name2 = _create_test_bill_with_due_days(2)
    name3 = _create_test_bill_with_due_days(3)
    name4 = _create_test_bill_with_due_days(4)

    created_ids = []
    try:
        id2 = get_bill_id_by_name(name2)
        id3 = get_bill_id_by_name(name3)
        id4 = get_bill_id_by_name(name4)
        created_ids.extend([id2, id3, id4])

        out = list_bills_service(upcoming_only=True, days=3)
        ids = {row["id"] for row in out["date"]}

        assert id2 in ids
        assert id4 not in ids
    finally:
        for bill_id in created_ids:
            delete_bill_by_id(bill_id)