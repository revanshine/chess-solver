"""Pytest configuration and shared fixtures for codex_template tests."""

import asyncio
import sys
from collections.abc import AsyncGenerator, Generator
from pathlib import Path
from typing import Any
from unittest.mock import Mock

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from codex_template.core.config import Settings
from codex_template.main import create_app


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop]:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def test_settings() -> Settings:
    """Create test settings with safe defaults."""
    return Settings(
        app_name="Test Codex Template",
        environment="development",
        debug=True,
        secret_key="test-secret-key-not-for-production",
        database_url="sqlite:///./test.db",
        redis_url="redis://localhost:6379/1",  # Use different DB for tests
        enable_docs=False,  # Disable docs in tests
        enable_metrics=False,  # Disable metrics in tests
    )


@pytest.fixture
def mock_settings(test_settings: Settings) -> Generator[Settings]:
    """Mock the get_settings function with test settings."""
    import codex_template.core.config
    import codex_template.main

    original_get_settings = codex_template.core.config.get_settings

    def mock_get_settings() -> Settings:
        return test_settings

    # Patch the function in both modules
    codex_template.core.config.get_settings = mock_get_settings
    codex_template.main.get_settings = mock_get_settings

    try:
        yield test_settings
    finally:
        # Restore original function
        codex_template.core.config.get_settings = original_get_settings
        codex_template.main.get_settings = original_get_settings


@pytest.fixture
def app(mock_settings: Settings):
    """Create a test FastAPI application."""
    return create_app()


@pytest.fixture
def client(app) -> TestClient:
    """Create a test client for the FastAPI application."""
    return TestClient(app)


@pytest_asyncio.fixture
async def async_client(app) -> AsyncGenerator[AsyncClient]:
    """Create an async test client for the FastAPI application."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def sample_user_data() -> dict[str, Any]:
    """Sample user data for testing."""
    return {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com",
        "full_name": "Test User",
        "is_active": True,
    }


@pytest.fixture
def sample_api_response() -> dict[str, Any]:
    """Sample API response data for testing."""
    return {
        "status": "success",
        "data": {"message": "Operation completed successfully"},
        "timestamp": "2024-01-01T00:00:00Z",
    }


@pytest.fixture
def mock_external_service() -> Mock:
    """Mock external service for testing."""
    mock = Mock()
    mock.fetch_data.return_value = {"status": "ok", "data": []}
    mock.send_notification.return_value = True
    return mock


@pytest.fixture
def temp_file(tmp_path: Path) -> Path:
    """Create a temporary file for testing."""
    test_file = tmp_path / "test_file.txt"
    test_file.write_text("This is a test file content")
    return test_file


@pytest.fixture
def temp_directory(tmp_path: Path) -> Path:
    """Create a temporary directory with some test files."""
    test_dir = tmp_path / "test_directory"
    test_dir.mkdir()

    # Create some test files
    (test_dir / "file1.txt").write_text("Content 1")
    (test_dir / "file2.txt").write_text("Content 2")
    (test_dir / "subdir").mkdir()
    (test_dir / "subdir" / "file3.txt").write_text("Content 3")

    return test_dir


# Pytest configuration
def pytest_configure(config: pytest.Config) -> None:
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "unit: Unit tests")
    config.addinivalue_line("markers", "integration: Integration tests")
    config.addinivalue_line("markers", "e2e: End-to-end tests")
    config.addinivalue_line("markers", "slow: Slow running tests")
    config.addinivalue_line("markers", "async: Async tests")
    config.addinivalue_line("markers", "error_handling: Error handling tests")


# Async test utilities
@pytest.fixture
def anyio_backend() -> str:
    """Use asyncio backend for anyio tests."""
    return "asyncio"
