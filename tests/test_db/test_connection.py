from unittest.mock import MagicMock, patch

import pytest

from app.db.connection import get_db_connection


@patch("app.db.connection._conn_pool")
def test_get_db_connection_success(mock_conn_pool):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_conn_pool.get_connection.return_value = mock_conn

    with get_db_connection() as (conn, cursor):
        assert conn == mock_conn
        assert cursor == mock_cursor

        # In context, nothing is closed or committed yet
        mock_conn.commit.assert_not_called()
        mock_cursor.close.assert_not_called()

    # After context exit cleanly
    mock_conn.commit.assert_called_once()
    mock_conn.rollback.assert_not_called()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()


@patch("app.db.connection._conn_pool")
def test_get_db_connection_exception(mock_conn_pool):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_conn_pool.get_connection.return_value = mock_conn

    with pytest.raises(ValueError, match="Test error"):
        with get_db_connection() as (_conn, _cursor):
            raise ValueError("Test error")

    # After context exit with exception
    mock_conn.commit.assert_not_called()
    mock_conn.rollback.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()
