try:
    from pydantic_settings import BaseSettings
    _PYDANTIC_SETTINGS_AVAILABLE = True
except Exception:
    BaseSettings = object
    _PYDANTIC_SETTINGS_AVAILABLE = False

from functools import lru_cache
from urllib.parse import quote_plus
import os


if _PYDANTIC_SETTINGS_AVAILABLE:
    class Settings(BaseSettings):
        """All application settings loaded from .env file and environment variables."""

        # OpenRouter API
        openrouter_api_key: str = os.getenv("OPENROUTER_API_KEY", "")
        openrouter_model: str = os.getenv("OPENROUTER_MODEL", "openai/gpt-3.5-turbo")

        # Database - MySQL 8.x on Azure
        db_host: str = os.getenv("DB_HOST", "campus-test-server.mysql.database.azure.com")
        db_port: int = int(os.getenv("DB_PORT", "3306"))
        db_user: str = os.getenv("DB_USER", "artisetadmin")
        db_password: str = os.getenv("DB_PASSWORD", "")
        db_name: str = os.getenv("DB_NAME", "naukridb")

        # App
        app_env: str = os.getenv("APP_ENV", "development")
        app_port: int = int(os.getenv("APP_PORT", "8000"))
        max_file_size_mb: int = int(os.getenv("MAX_FILE_SIZE_MB", "10"))
        allowed_extensions: str = os.getenv("ALLOWED_EXTENSIONS", "pdf,docx")

        @property
        def database_url(self) -> str:
            """Builds SQLAlchemy connection string for MySQL 8.x."""
            user = quote_plus(self.db_user)
            password = quote_plus(self.db_password)
            return f"mysql+pymysql://{user}:{password}@{self.db_host}:{self.db_port}/{self.db_name}?charset=utf8mb4"
        
        def get_db_config_summary(self) -> dict:
            """Returns database configuration summary (without password)."""
            return {
                "driver": "MySQL 8.x",
                "host": self.db_host,
                "port": self.db_port,
                "user": self.db_user,
                "database": self.db_name,
                "environment": self.app_env
            }

        @property
        def allowed_extensions_list(self) -> list[str]:
            return [ext.strip().lower() for ext in self.allowed_extensions.split(",")]

        class Config:
            env_file = ".env"
            env_file_encoding = "utf-8"


    @lru_cache()
    def get_settings() -> Settings:
        """Returns cached settings instance."""
        return Settings()

else:
    class Settings:
        """Lightweight fallback settings when pydantic-settings is unavailable."""

        def __init__(self):
            # OpenRouter API
            self.openrouter_api_key = os.getenv("OPENROUTER_API_KEY", "")
            self.openrouter_model = os.getenv("OPENROUTER_MODEL", "openai/gpt-3.5-turbo")

            # Database - MySQL 8.x on Azure
            self.db_host = os.getenv("DB_HOST", "campus-test-server.mysql.database.azure.com")
            self.db_port = int(os.getenv("DB_PORT", "3306"))
            self.db_user = os.getenv("DB_USER", "artisetadmin")
            self.db_password = os.getenv("DB_PASSWORD", "")
            self.db_name = os.getenv("DB_NAME", "naukridb")

            # App
            self.app_env = os.getenv("APP_ENV", "development")
            self.app_port = int(os.getenv("APP_PORT", "8000"))
            self.max_file_size_mb = int(os.getenv("MAX_FILE_SIZE_MB", "10"))
            self.allowed_extensions = os.getenv("ALLOWED_EXTENSIONS", "pdf,docx")

        @property
        def database_url(self) -> str:
            user = quote_plus(self.db_user)
            password = quote_plus(self.db_password)
            return f"mysql+pymysql://{user}:{password}@{self.db_host}:{self.db_port}/{self.db_name}?charset=utf8mb4"

        def get_db_config_summary(self) -> dict:
            return {
                "driver": "MySQL 8.x",
                "host": self.db_host,
                "port": self.db_port,
                "user": self.db_user,
                "database": self.db_name,
                "environment": self.app_env
            }

        @property
        def allowed_extensions_list(self) -> list[str]:
            return [ext.strip().lower() for ext in self.allowed_extensions.split(",")]


    @lru_cache()
    def get_settings() -> Settings:
        return Settings()
