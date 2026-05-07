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
        self.db_host: str = os.getenv("DB_HOST", "localhost")
        self.db_user: str = os.getenv("DB_USER", "root")
        self.db_password: str = os.getenv("DB_PASSWORD", "")
        self.db_name: str = os.getenv("DB_NAME", "family_supp_sche")
        self.db_table: str = os.getenv("DB_TABLE", "bills")
        self.db_conn_pooling: int = int(os.getenv("DB_CONN_POOLING", "5"))

        self.fe_url: str = os.getenv("FE_URL", "http://127.0.0.1:8080")
        self.fe_local_url: str = os.getenv("FE_LOCAL_URL", "http://localhost:8080")

        self.receiver_panel_url: str = os.getenv("RECEIVER_PANEL_URL", "http://127.0.0.1:3000")
        self.sender_panel_url: str = os.getenv("SENDER_PANEL_URL", "http://127.0.0.1:3001")
        self.receiver_panel_local_url: str = os.getenv("RECEIVER_PANEL_LOCAL_URL", "http://localhost:3000")
        self.sender_panel_local_url: str = os.getenv("SENDER_PANEL_LOCAL_URL", "http://localhost:3001")

        self.jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "changeme_in_production")
        self.jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
        self.jwt_expire_minutes: int = int(os.getenv("JWT_EXPIRE_MINUTES", "480"))


settings = Settings()
