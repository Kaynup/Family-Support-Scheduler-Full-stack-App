"""
Database connection pool and context manager.

All query functions must use get_db_connection() as a context manager.
Commit, rollback, cursor close, and connection close are all guaranteed
by this one place — callers never manage these manually.
"""

import logging
from contextlib import contextmanager

from mysql.connector import pooling

from ..core.config import settings

logger = logging.getLogger(__name__)


def _create_pool():
    kwargs = {
        "pool_name": "userpool",
        "pool_size": settings.db_conn_pooling,
        "host": settings.db_host,
        "port": settings.db_port,
        "user": settings.db_user,
        "password": settings.db_password,
        "database": settings.db_name,
    }
    if settings.db_ssl:
        kwargs["ssl_disabled"] = False
    try:
        return pooling.MySQLConnectionPool(**kwargs)
    except Exception as err:
        logger.error(
            "Failed to initialize MySQLConnectionPool for %s:%s (user=%s, db=%s): %s",
            settings.db_host,
            settings.db_port,
            settings.db_user,
            settings.db_name,
            err,
        )
        return None


_conn_pool = _create_pool()


@contextmanager
def get_db_connection():
    """
    Yields a (connection, cursor) pair inside a managed transaction.

    On normal exit:    commits the transaction.
    On any exception:  rolls back the transaction and re-raises.
    Always:            closes the cursor and returns the connection to the pool.
    """
    global _conn_pool
    if _conn_pool is None:
        _conn_pool = _create_pool()
    if _conn_pool is None:
        raise ConnectionError(
            f"Database connection pool could not be initialized for {settings.db_host}:{settings.db_port}."
        )

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
