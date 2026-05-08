"""
Application configuration loaded once at startup from the .env file.

All modules that need environment values must import `settings` from here.
No other module should call os.getenv() directly.
"""

from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    """
    Holds every environment variable the application depends on.
    Attributes are read once at import time so startup failures are immediate.
    """

    def __init__(self):
        self.db_host: str = os.getenv("DB_HOST")
        self.db_user: str = os.getenv("DB_USER")
        self.db_password: str = os.getenv("DB_PASSWORD")
        self.db_name: str = os.getenv("DB_NAME")
        self.db_table: str = os.getenv("DB_TABLE")
        self.db_conn_pooling: int = int(os.getenv("DB_CONN_POOLING", "5"))

        self.jwt_secret_key: str = os.getenv("JWT_SECRET_KEY")
        self.jwt_algorithm: str = os.getenv("JWT_ALGORITHM")
        self.jwt_expire_minutes: int = int(os.getenv("JWT_EXPIRE_MINUTES", "480"))


settings = Settings()
