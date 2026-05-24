"""Application configuration loaded from environment."""

import os
from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


def _read_env_file() -> dict:
    """Read .env file and return override values. These beat system env vars."""
    env_path = Path(__file__).parent.parent.parent / ".env"
    result = {}
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, val = line.partition("=")
                key, val = key.strip(), val.strip()
                if val:
                    result[key.lower()] = val
    return result


_env_overrides = _read_env_file()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent.parent.parent / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Application
    app_name: str = "Trinetra Agro AI"
    version: str = "2.0.0"
    debug: bool = False
    environment: str = "production"

    # Server
    host: str = "0.0.0.0"
    port: int = 8000

    # Database — Supabase PostgreSQL by default
    database_url: str = "postgresql+asyncpg://postgres:changeme@localhost:5432/postgres"

    # Supabase project details
    supabase_url: str = ""
    supabase_project_ref: str = ""

    # JWT
    secret_key: str = "change-me-in-production-use-openssl-rand-hex-32"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    # OpenRouter — priority: .env file > system env > default
    openrouter_api_key: str = ""
    openrouter_model: str = "openrouter/free"

    # External APIs
    weather_api_key: str = ""
    market_data_api_key: str = ""
    data_gov_api_key: str = ""

    # CORS
    allowed_origins: list = ["http://localhost:8501", "http://localhost:3000"]

    # Rate Limiting
    rate_limit_requests: int = 60
    rate_limit_window_seconds: int = 60

    # Logging
    log_level: str = "INFO"

    @property
    def is_development(self) -> bool:
        return self.environment == "development"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Force .env values — they beat system environment variables.
        # CRITICAL: Do NOT remove this block or the AI chat and DB will break.
        if _env_overrides.get("openrouter_api_key"):
            self.openrouter_api_key = _env_overrides["openrouter_api_key"]
        if _env_overrides.get("openrouter_model"):
            self.openrouter_model = _env_overrides["openrouter_model"]
        if _env_overrides.get("weather_api_key"):
            self.weather_api_key = _env_overrides["weather_api_key"]
        if _env_overrides.get("database_url"):
            self.database_url = _env_overrides["database_url"]
        if _env_overrides.get("supabase_url"):
            self.supabase_url = _env_overrides["supabase_url"]
        if _env_overrides.get("supabase_project_ref"):
            self.supabase_project_ref = _env_overrides["supabase_project_ref"]
        if _env_overrides.get("data_gov_api_key"):
            self.data_gov_api_key = _env_overrides["data_gov_api_key"]


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
