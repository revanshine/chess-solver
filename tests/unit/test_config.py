"""Unit tests for the core configuration module."""

import os
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from codex_template.core.config import Settings, get_settings


class TestSettings:
    """Test suite for Settings class."""

    def test_settings_default_values(self) -> None:
        """Test that settings have correct default values."""
        # Arrange & Act
        settings = Settings(secret_key="test-key")

        # Assert
        assert settings.app_name == "Codex Template"
        assert settings.app_version == "0.1.0"
        assert settings.debug is False
        assert settings.environment == "development"
        assert settings.host == "0.0.0.0"
        assert settings.port == 8000
        assert settings.secret_key == "test-key"

    def test_settings_from_environment_variables(self) -> None:
        """Test that settings can be loaded from environment variables."""
        # Arrange
        env_vars = {
            "SECRET_KEY": "env-secret-key",
            "HOST": "localhost",
            "PORT": "9000",
            "DATABASE_URL": "postgresql://localhost/testdb",
            "DEBUG": "true",
        }

        # Act
        with patch.dict(os.environ, env_vars):
            settings = Settings()

        # Assert
        assert settings.secret_key == "env-secret-key"
        assert settings.host == "localhost"
        assert settings.port == 9000
        assert settings.database_url == "postgresql://localhost/testdb"
        assert settings.debug is True

    def test_is_production_property(self) -> None:
        """Test the is_production property."""
        # Arrange & Act
        dev_settings = Settings(secret_key="test", environment="development")
        prod_settings = Settings(secret_key="test", environment="production")

        # Assert
        assert dev_settings.is_production is False
        assert prod_settings.is_production is True

    def test_is_development_property(self) -> None:
        """Test the is_development property."""
        # Arrange & Act
        dev_settings = Settings(secret_key="test", environment="development")
        prod_settings = Settings(secret_key="test", environment="production")

        # Assert
        assert dev_settings.is_development is True
        assert prod_settings.is_development is False

    def test_project_root_property(self) -> None:
        """Test the project_root property."""
        # Arrange & Act
        settings = Settings(secret_key="test")
        project_root = settings.project_root

        # Assert
        assert isinstance(project_root, Path)
        assert project_root.exists()
        assert project_root.is_dir()

    @pytest.mark.error_handling
    def test_settings_missing_secret_key_raises_error(self) -> None:
        """Test that missing secret key raises validation error."""
        # Arrange, Act & Assert
        with pytest.raises(ValueError, match="field required"):
            Settings()


class TestGetSettings:
    """Test suite for get_settings function."""

    def test_get_settings_returns_settings_instance(self) -> None:
        """Test that get_settings returns a Settings instance."""
        # Arrange & Act
        with patch.dict(os.environ, {"SECRET_KEY": "test-key"}):
            settings = get_settings()

        # Assert
        assert isinstance(settings, Settings)
        assert settings.secret_key == "test-key"

    def test_get_settings_caches_result(self) -> None:
        """Test that get_settings caches the result."""
        # Arrange & Act
        with patch.dict(os.environ, {"SECRET_KEY": "test-key"}):
            settings1 = get_settings()
            settings2 = get_settings()

        # Assert
        assert settings1 is settings2  # Same instance, not just equal

    def test_get_settings_cache_can_be_cleared(self) -> None:
        """Test that get_settings cache can be cleared."""
        # Arrange
        with patch.dict(os.environ, {"SECRET_KEY": "test-key-1"}):
            settings1 = get_settings()

        # Act - Clear cache and change environment
        get_settings.cache_clear()
        with patch.dict(os.environ, {"SECRET_KEY": "test-key-2"}):
            settings2 = get_settings()

        # Assert
        assert settings1 is not settings2
        assert settings1.secret_key == "test-key-1"
        assert settings2.secret_key == "test-key-2"
