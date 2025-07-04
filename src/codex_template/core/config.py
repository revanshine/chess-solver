"""Configuration management for codex_template."""

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field
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
    secret_key: str = Field(
        default="dev-secret-key-change-in-production", env="SECRET_KEY"
    )
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


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance.

    Returns:
        Settings: Application settings instance.
    """
    return Settings()


# Global settings instance
settings = get_settings()
