"""
Database connection pool and context manager.

All query functions must use get_db_connection() as a context manager.
Commit, rollback, cursor close, and connection close are all guaranteed
by this one place — callers never manage these manually.
"""

import mysql.connector
from mysql.connector import pooling
from contextlib import contextmanager
from ..core.config import settings

_conn_pool = pooling.MySQLConnectionPool(
    pool_name="userpool",
    pool_size=settings.db_conn_pooling,
    host=settings.db_host,
    user=settings.db_user,
    password=settings.db_password,
    database=settings.db_name,
)


@contextmanager
def get_db_connection():
    """
    Yields a (connection, cursor) pair inside a managed transaction.

    On normal exit:    commits the transaction.
    On any exception:  rolls back the transaction and re-raises.
    Always:            closes the cursor and returns the connection to the pool.
    """
    conn = _conn_pool.get_connection()
    cursor = conn.cursor()
    try:
        yield conn, cursor
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()