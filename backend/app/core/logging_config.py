"""
Shared logging configuration for the backend application.

Import `logger` from this module in services and routes, and call
`configure_logging()` once from the application entrypoint.
"""

import logging


def configure_logging(level: int = logging.INFO) -> None:
    """Initializes the root logging configuration if it has not been set yet."""
    if logging.getLogger().handlers:
        return

    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )


logger = logging.getLogger("backend")
