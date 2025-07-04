"""Configuration management for codex_template."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Literal

from pydantic import Field, ValidationError
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with validation and environment variable support."""

    # Basic app settings
    app_name: str = "Codex Template"
    app_version: str = "0.1.0"
    debug: bool = False
    environment: Literal["development", "staging", "production"] = "development"

    # Server settings
    host: str = Field(default="0.0.0.0", env="HOST")
    port: int = Field(default=8000, env="PORT")

    # Database settings
    database_url: str = Field(
        default="sqlite:///./codex_template.db", env="DATABASE_URL"
    )

    # Redis settings
    redis_url: str = Field(default="redis://localhost:6379", env="REDIS_URL")

    # Security settings
    secret_key: str = Field(..., env="SECRET_KEY")
    access_token_expire_minutes: int = Field(
        default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES"
    )

    # API settings
    api_v1_prefix: str = "/api/v1"
    cors_origins: list[str] = Field(default=["*"], env="CORS_ORIGINS")

    # Logging settings
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    log_format: Literal["json", "pretty"] = "json"

    # Feature flags
    enable_docs: bool = True
    enable_metrics: bool = True

    def __init__(self, **data: object) -> None:  # noqa: D401
        """Initialize settings and ensure secret_key is provided."""
        if "secret_key" not in data and os.getenv("SECRET_KEY") is None:
            raise ValueError("field required")
        super().__init__(**data)

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }

    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment == "production"

    @property
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.environment == "development"

    @property
    def project_root(self) -> Path:
        """Get project root directory."""
        return Path(__file__).parent.parent.parent.parent


_cached_settings: Settings | None = None
_cached_secret_key: str | None = None


def get_settings() -> Settings:
    """Return cached settings instance respecting environment changes."""
    global _cached_settings, _cached_secret_key

    current_secret = os.getenv("SECRET_KEY")
    if _cached_settings is None or _cached_secret_key != current_secret:
        try:
            _cached_settings = Settings()
            _cached_secret_key = _cached_settings.secret_key
        except ValidationError as exc:
            raise ValueError("field required") from exc

    assert _cached_settings is not None
    return _cached_settings


def clear_settings_cache() -> None:
    """Clear the cached settings instance."""
    global _cached_settings, _cached_secret_key
    _cached_settings = None
    _cached_secret_key = None


get_settings.cache_clear = clear_settings_cache  # type: ignore[attr-defined]
