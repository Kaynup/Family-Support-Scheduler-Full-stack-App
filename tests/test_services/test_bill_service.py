from datetime import date, timedelta
from unittest.mock import patch

import pytest

from app.constants import INTERVAL_NONE, STATUS_PAID, STATUS_UNPAID
from app.core.exceptions import BillNotFoundError
from app.services.bill_service import (
    create_bill,
    delete_bill,
    list_bills,
    mark_bill_status,
    search_bills_by_name,
)


@patch("app.services.bill_service.dbq.insert_bill")
def test_create_bill(mock_insert_bill):
    mock_insert_bill.return_value = 1
    out = create_bill(
        name="test",
        due_date=date.today().isoformat(),
        total_amount=100.0,
        status=STATUS_UNPAID,
        category="test",
        recurring_interval=INTERVAL_NONE,
    )
    assert out["OK"] is True
    assert out["data"]["id"] == 1


@patch("app.services.bill_service.dbq.select_all_bills")
def test_list_bills(mock_select_all):
    mock_select_all.return_value = [
        (
            1,
            "test",
            STATUS_UNPAID,
            1,
            date.today(),
            date.today(),
            100.0,
            "test",
            INTERVAL_NONE,
            "N",
        )
    ]
    out = list_bills()
    assert out["OK"] is True
    assert out["total_count"] == 1


@patch("app.services.bill_service.dbq.update_bill_status")
@patch("app.services.bill_service.dbq.select_bill_by_id")
def test_mark_bill_status(mock_select_bill, mock_update):
    mock_select_bill.return_value = (
        1,
        "test",
        STATUS_UNPAID,
        1,
        date.today(),
        date.today(),
        100.0,
        "test",
        INTERVAL_NONE,
        "N",
    )

    out = mark_bill_status(1, STATUS_PAID)
    assert out["OK"] is True

    mock_update.assert_called_with(1, STATUS_PAID)


@patch("app.services.bill_service.dbq.select_bill_by_id")
def test_mark_bill_status_not_found(mock_select_bill):
    mock_select_bill.return_value = None
    with pytest.raises(BillNotFoundError):
        mark_bill_status(999, STATUS_PAID)


@patch("app.services.bill_service.dbq.soft_delete_bill_by_id")
def test_delete_bill(mock_delete):
    out = delete_bill(1)
    assert out["OK"] is True
    mock_delete.assert_called_with(1)


@patch("app.services.bill_service.dbq.soft_delete_bill_by_id")
def test_delete_bill_not_found(mock_delete):
    import mysql.connector

    mock_delete.side_effect = mysql.connector.Error("No row")
    with pytest.raises(BillNotFoundError):
        delete_bill(999)


@patch("app.services.bill_service.dbq.select_upcoming_bills")
def test_list_bills_upcoming(mock_select_upcoming):
    mock_select_upcoming.return_value = [
        (
            1,
            "test2",
            STATUS_UNPAID,
            1,
            date.today(),
            date.today() + timedelta(days=2),
            100.0,
            "test",
            INTERVAL_NONE,
            "N",
        ),
        (
            2,
            "test3",
            STATUS_UNPAID,
            1,
            date.today(),
            date.today() + timedelta(days=3),
            100.0,
            "test",
            INTERVAL_NONE,
            "N",
        ),
    ]
    out = list_bills(upcoming_only=True, days=3)
    assert len(out["data"]) == 2


@patch("app.services.bill_service.dbq.select_bills_by_name")
def test_search_bills_by_name(mock_select_by_name):
    mock_select_by_name.return_value = [
        (
            1,
            "search-test",
            STATUS_UNPAID,
            1,
            date.today(),
            date.today(),
            100.0,
            "test",
            INTERVAL_NONE,
            "N",
        )
    ]
    out = search_bills_by_name("search")
    assert out["OK"] is True
    assert len(out["data"]) == 1
