from unittest.mock import patch

import pytest

from app.constants import STATUS_PAID, STATUS_UNPAID
from app.core.exceptions import RemittanceValidationError
from app.services.remittance_service import (
    get_remittance_history_for_sender,
    pay_bill_via_remittance,
)


@patch("app.services.remittance_service.dbq")
def test_pay_bill_success(mock_dbq):
    mock_dbq.select_bill_by_id.return_value = (
        1,
        "Rent",
        STATUS_UNPAID,
        2,
        "2026-01-01",
        "2026-01-05",
        500.0,
        "Housing",
        "NONE",
        "N",
    )
    mock_dbq.insert_remittance_transaction.return_value = 101

    out = pay_bill_via_remittance(1, sender_user_id=1, amount=500.0)

    assert out["OK"] is True
    assert out["data"]["transaction_id"] == 101
    assert out["data"]["beneficiary_user_id"] == 2
    mock_dbq.update_bill_status.assert_called_with(1, STATUS_PAID)


@patch("app.services.remittance_service.dbq")
def test_pay_bill_already_paid(mock_dbq):
    mock_dbq.select_bill_by_id.return_value = (
        1,
        "Rent",
        STATUS_PAID,
        2,
        "2026-01-01",
        "2026-01-05",
        500.0,
        "Housing",
        "NONE",
        "N",
    )

    with pytest.raises(RemittanceValidationError, match="already PAID"):
        pay_bill_via_remittance(1, sender_user_id=1, amount=500.0)


@patch("app.services.remittance_service.dbq")
def test_pay_bill_insufficient_amount(mock_dbq):
    mock_dbq.select_bill_by_id.return_value = (
        1,
        "Rent",
        STATUS_UNPAID,
        2,
        "2026-01-01",
        "2026-01-05",
        500.0,
        "Housing",
        "NONE",
        "N",
    )

    with pytest.raises(RemittanceValidationError, match="less than the bill total"):
        pay_bill_via_remittance(1, sender_user_id=1, amount=100.0)


@patch("app.services.remittance_service.dbq")
def test_get_history_for_sender(mock_dbq):
    # Mock transaction: id, bill_id, sender_id, beneficiary_id, amount, currency, status, method, date
    mock_dbq.select_remittance_by_sender_id.return_value = [
        (101, 1, 1, 2, 500.0, "USDT", "COMPLETED", "stablecoin", "2026-01-01 12:00:00")
    ]
    out = get_remittance_history_for_sender(1)
    assert out["OK"] is True
    assert out["total_count"] == 1
    assert out["data"][0]["transaction_id"] == 101
