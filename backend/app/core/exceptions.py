"""
Application-specific exception classes.

Using typed exceptions instead of generic ValueError with string messages
lets route handlers catch specific error types and map them to precise
HTTP status codes without fragile string matching.
"""


class BillNotFoundError(Exception):
    """Raised when a bill ID does not exist or has been soft-deleted."""


class BillAlreadyPaidError(Exception):
    """Raised when an operation requires an UNPAID bill but the bill is already PAID."""


class RemittanceValidationError(Exception):
    """Raised when a remittance payment fails a business rule check."""


class AuthenticationError(Exception):
    """Raised when login credentials are invalid or a JWT cannot be decoded."""


class UnauthorizedRoleError(Exception):
    """Raised when an authenticated user's role does not permit the requested action."""