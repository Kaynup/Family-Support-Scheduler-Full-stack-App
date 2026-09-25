"""
User route handlers — /users prefix.

GET /users?role=beneficiary  — returns users with the requested role.
"""

from fastapi import APIRouter, Query

from ..db import queries as dbq

router = APIRouter(prefix="/users", tags=["users"])


@router.get("")
def list_users_route(role: str = Query(None)):
    """Returns users optionally filtered by role."""
    if role:
        rows = dbq.select_users_by_role(role)
    else:
        # simplest: return empty list when no role specified
        rows = []

    # map to simple dicts
    return {
        "OK": True,
        "total_count": len(rows),
        "data": [{"id": r[0], "username": r[1], "role": r[2]} for r in rows],
    }
