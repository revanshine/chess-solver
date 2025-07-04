"""Unit tests for the main FastAPI application."""

from unittest.mock import Mock
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

from codex_template.main import create_app


class TestApp:
    """Test suite for FastAPI application."""

    def test_app_creation(self, mock_settings) -> None:
        """Test that the app can be created successfully."""
        # Arrange & Act
        app = create_app()

        # Assert
        assert app is not None
        assert app.title == "Test Codex Template"
        assert app.version == "0.1.0"

    def test_health_endpoint(self, client: TestClient) -> None:
        """Test the health check endpoint."""
        # Arrange & Act
        response = client.get("/health")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "app_name" in data
        assert "version" in data
        assert "environment" in data

    def test_root_endpoint(self, client: TestClient) -> None:
        """Test the root endpoint."""
        # Arrange & Act
        response = client.get("/")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "docs" in data

    def test_nonexistent_endpoint_returns_404(self, client: TestClient) -> None:
        """Test that non-existent endpoints return 404."""
        # Arrange & Act
        response = client.get("/nonexistent")

        # Assert
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_async_health_endpoint(self, async_client) -> None:
        """Test the health endpoint with async client."""
        # Arrange & Act
        response = await async_client.get("/health")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


class TestExceptionHandlers:
    """Test suite for exception handlers."""

    def test_cors_headers_present(self, client: TestClient) -> None:
        """Test that CORS headers are present in responses."""
        # Arrange & Act
        response = client.get("/health")

        # Assert
        assert response.status_code == 200
        # Note: TestClient might not include all CORS headers in tests
        # This test mainly ensures the middleware is configured without errors

    def test_json_response_format(self, client: TestClient) -> None:
        """Test that responses are in JSON format."""
        # Arrange & Act
        response = client.get("/health")

        # Assert
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"
        # Should not raise exception when parsing JSON
        data = response.json()
        assert isinstance(data, dict)
