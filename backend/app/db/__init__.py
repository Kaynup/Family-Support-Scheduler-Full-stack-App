"""
db/ package public interface.

Exposes get_db_connection for modules that need direct DB access,
and re-exports the queries namespace alias used throughout services.
"""

from .connection import get_db_connection
from . import queries

__all__ = ["get_db_connection", "queries"]