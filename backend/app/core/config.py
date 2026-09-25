"""
Application configuration loaded once at startup from the .env file.

All modules that need environment values must import `settings` from here.
No other module should call os.getenv() directly.
"""

import logging
import os
import secrets

from dotenv import load_dotenv

load_dotenv()


class Settings:
    """
    Holds every environment variable the application depends on.
    Attributes are read once at import time so startup failures are immediate.
    """

    def __init__(self):
        self.db_host: str = os.getenv("DB_HOST", "localhost")
        self.db_port: int = int(os.getenv("DB_PORT", "3306"))
        self.db_user: str = os.getenv("DB_USER", "root")
        self.db_password: str = os.getenv("DB_PASSWORD", "")
        self.db_name: str = os.getenv("DB_NAME", "family_supp_sche")
        self.db_table: str = os.getenv("DB_TABLE", "bills")
        self.db_conn_pooling: int = int(os.getenv("DB_CONN_POOLING", "5"))
        self.db_ssl: bool = os.getenv("DB_SSL", "false").lower() in ("true", "1", "yes")

        jwt_key = os.getenv("JWT_SECRET_KEY")
        if not jwt_key:
            logging.warning(
                "JWT_SECRET_KEY not set in environment. Generating ephemeral secret. Instance-isolated!"
            )
            jwt_key = secrets.token_hex(32)
        self.jwt_secret_key: str = jwt_key
        self.jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
        self.jwt_expire_minutes: int = int(os.getenv("JWT_EXPIRE_MINUTES", "480"))
        self.allowed_origins: str = os.getenv("ALLOWED_ORIGINS", "")


settings = Settings()
