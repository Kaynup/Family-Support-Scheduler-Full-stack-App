from unittest.mock import patch
from datetime import date, timedelta
from backend.app.services.bill_creation import create_bill_service
from backend.app.services.bill_listing import list_bills_service
from backend.app.services.bill_status import mark_bill_status_service
from backend.app.services.bill_deletion import delete_bill_service
from backend.app.services.bill_search import select_by_name_service

@patch('backend.app.services.bill_creation.dbq.insert_bill')
def test_create_bill_service(mock_insert_bill):
    mock_insert_bill.return_value = 1
    out = create_bill_service(
        name="test", due_date=date.today().isoformat(),
        total_amount=100.0, status="UNPAID", category="test", recurring_interval="NONE"
    )
    assert out["OK"] is True
    assert out["data"]["id"] == 1

@patch('backend.app.services.bill_listing.dbq.select_all')
def test_list_bills_service(mock_select_all):
    mock_select_all.return_value = [
        (1, "test", date.today(), date.today(), 100.0, "UNPAID", "test", "NONE", "N")
    ]
    out = list_bills_service()
    assert out["OK"] is True
    assert out["total_count"] == 1

@patch('backend.app.services.bill_status.dbq.insert_bill')
@patch('backend.app.services.bill_status.dbq.update_bill_status')
@patch('backend.app.services.bill_status.dbq.select_bill_by_id')
def test_mark_bill_status_service(mock_select_bill, mock_update, mock_insert):
    # Mock a WEEKLY recurring bill
    mock_select_bill.return_value = (1, "test", date.today(), date.today(), 100.0, "UNPAID", "test", "WEEKLY", "N")
    
    out = mark_bill_status_service(1, "PAID")
    assert out["OK"] is True
    
    # Verify status was updated
    mock_update.assert_called_with(1, "PAID")
    
    # CRITICAL: Verify NO new bill was inserted (recurrence logic is now frontend-only)
    mock_insert.assert_not_called()

@patch('backend.app.services.bill_deletion.dbq.delete_bill_by_id')
def test_delete_bill_service(mock_delete):
    out = delete_bill_service(1)
    assert out["OK"] is True
    mock_delete.assert_called_with(1)

@patch('backend.app.services.bill_listing.dbq.select_num_day_dues')
def test_list_bills_service_upcoming_boundary_days_3(mock_select_num_day_dues):
    mock_select_num_day_dues.return_value = [
        (1, "test2", date.today(), date.today() + timedelta(days=2), 100.0, "UNPAID", "test", "NONE", "N"),
        (2, "test3", date.today(), date.today() + timedelta(days=3), 100.0, "UNPAID", "test", "NONE", "N"),
    ]
    out = list_bills_service(upcoming_only=True, days=3)
    assert len(out["data"]) == 2

@patch('backend.app.services.bill_search.dbq.select_by_name_match')
def test_select_by_name_service(mock_select_by_name):
    mock_select_by_name.return_value = [
        (1, "search-test", date.today(), date.today(), 100.0, "UNPAID", "test", "NONE", "N")
    ]
    out = select_by_name_service("search")
    assert out["OK"] is True
    assert len(out["data"]) == 1