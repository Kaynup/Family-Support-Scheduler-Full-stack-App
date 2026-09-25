"""
db/ package public interface.

Exposes get_db_connection for modules that need direct DB access,
and re-exports the queries namespace alias used throughout services.
"""

from . import queries
from .connection import get_db_connection

__all__ = ["get_db_connection", "queries"]
