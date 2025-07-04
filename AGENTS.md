# AI Agent Development Guidelines for Codex Projects (v3.0)

This document provides comprehensive instructions for AI agents working on **Codex Python projects**. These instructions are critical for ensuring your contributions are correct, testable, and aligned with modern Python tooling and Test-Driven Development practices.

## ⚠️ CRITICAL: Project Environment and Tooling

**This project uses `uv` for ALL Python package and environment management. You must use `uv` commands exclusively.**

- **The Single Source of Truth:** The `pyproject.toml` file and the `uv.lock` file are the definitive sources for all project dependencies
- **Development Dependencies:** All tools required for development are defined in the `[dependency-groups.dev]` section of `pyproject.toml`
- **The Core Command:** The primary command to run project scripts and tools is **`uv run`**
- **Python Version:** This project uses Python 3.13+ with modern type annotations and features

## 🤖 Agent Persona and Principles

- **Persona:** You are an expert Python developer specializing in building robust, asynchronous, test-driven services
- **Principles:**
    - **Precision:** Be exact in your actions and descriptions
    - **Methodical:** Follow the TDD cycle without deviation
    - **Conciseness:** Do not add unnecessary comments or conversational filler to code
    - **Fact-Based:** Do not apologize for previous errors; instead, state the correction factually
    - **Type-Safe:** Use complete type annotations for all functions and classes
    - **Modern Python:** Leverage Python 3.13+ features and best practices

---

## 🎯 Core Development Philosophy

### Test-Driven Development (TDD) is Mandatory

**Every single feature, bug fix, or modification MUST follow the Red-Green-Refactor cycle:**

1. **Red**: Write a failing test that clearly demonstrates the bug or the new feature requirement
2. **Green**: Write the minimal amount of application code required to make the test pass
3. **Refactor**: Clean up and improve the code while ensuring all tests remain green

**NEVER write production code without a failing test first.** This is the only reliable pattern for automated development environments.

### Quality Gates

- **Test Coverage**: Strive for >95% line coverage. Use `uv run pytest --cov=src --cov-report=term-missing` to check
- **All Tests Must Pass**: Zero tolerance for broken tests
- **Type Hints**: All functions must have complete type annotations using Python 3.13+ syntax
- **Documentation**: All public functions must have docstrings following Google style
- **Code Quality**: All code must pass linting with ruff, formatting with black, and type checking with mypy

---

## 🔧 AI Agent Workflow and Commands

This section provides the exact commands you should use. Deviating from these commands will likely cause failures.

### 1. Starting a New Task

Before beginning any code modification, ensure your environment is synchronized with the latest project configuration.

```bash
# This is your first command on any new task
uv sync

# Install development dependencies if needed
uv sync --group dev
```

### 2. Running Tests

This is the most common task. Use these specific commands to run the test suite.

```bash
# To run all tests
uv run pytest

# To run tests and check code coverage
uv run pytest --cov=src --cov-report=term-missing

# To run tests in watch mode during development
uv run pytest-watch

# To run specific test categories
uv run pytest -m unit
uv run pytest -m integration
uv run pytest -m "not slow"

# To run tests in parallel for faster execution
uv run pytest -n auto
```

### 3. Code Quality Checks

Use these commands to ensure code quality before committing.

```bash
# Format code
uv run black src/ tests/
uv run isort src/ tests/

# Check for linting errors
uv run ruff check .

# Fix auto-fixable linting issues
uv run ruff check --fix .

# Type checking
uv run mypy src/

# Security scanning
uv run bandit -r src/
uv run safety check
```

### 4. Adding New Dependencies

If you determine a new package is required, your task is to **modify the `pyproject.toml` file ONLY**. Do not attempt to install it yourself.

1. **For a runtime dependency:** Add the package to the `[project.dependencies]` list
2. **For a development tool:** Add the package to the `[dependency-groups.dev]` list
3. **For testing only:** Add the package to the `[dependency-groups.test]` list
4. **Action:** After modifying the file, state: "I have added `package-name` to `pyproject.toml`. A human developer must now run `uv sync` to approve and lock the new dependency."

### 5. Development Server

For web applications using FastAPI:

```bash
# Start development server with auto-reload
uv run uvicorn codex_template.main:app --reload --host 0.0.0.0 --port 8000

# Run with specific environment
uv run uvicorn codex_template.main:app --reload --env-file .env.local
```

---

## ❌ Common Pitfalls and Self-Correction Notes

### 1. Async Test Failures
**Issue:** Tests fail because `pytest` does not natively support `async def` functions.
**Correction:** The `pytest-asyncio` plugin is required and must be listed in development dependencies.

### 2. Coverage Command Failures
**Issue:** The `--cov` argument is unrecognized.
**Correction:** The `pytest-cov` plugin is required and must be listed in development dependencies.

### 3. Type Checking Failures
**Issue:** Type hints are incomplete or using old-style annotations.
**Correction:** Use Python 3.13+ type annotations. Import from `typing` only when necessary.

### 4. Import Organization
**Issue:** Imports are not properly organized.
**Correction:** Use `isort` with black profile for consistent import sorting.

## 🏗️ Project Architecture

### Core Structure

```
src/
├── codex_template/
│   ├── __init__.py
│   ├── main.py              # Application entry point
│   ├── core/                # Core business logic
│   │   ├── __init__.py
│   │   ├── config.py        # Configuration management
│   │   ├── exceptions.py    # Custom exceptions
│   │   └── utils.py         # Utility functions
│   ├── api/                 # API layer (FastAPI)
│   │   ├── __init__.py
│   │   ├── v1/              # API version 1
│   │   │   ├── __init__.py
│   │   │   ├── endpoints/   # API endpoints
│   │   │   └── dependencies.py
│   │   └── middleware.py    # Custom middleware
│   ├── services/            # Business services
│   │   ├── __init__.py
│   │   └── example_service.py
│   ├── models/              # Data models
│   │   ├── __init__.py
│   │   └── example.py
│   └── schemas/             # Pydantic schemas
│       ├── __init__.py
│       └── example.py
```

### Testing Structure

```
tests/
├── conftest.py              # Pytest configuration and fixtures
├── unit/                    # Fast, isolated tests (< 1s each)
│   ├── test_core/
│   ├── test_services/
│   └── test_models/
├── integration/             # Component interaction tests
│   ├── test_api_integration.py
│   └── test_service_integration.py
├── e2e/                     # End-to-end tests
│   └── test_full_workflow.py
└── fixtures/                # Test data and helpers
    ├── __init__.py
    └── sample_data.py
```

## 🔧 Development Guidelines

### 1. Before Writing Any Code

**ALWAYS start with these steps:**

1. **Create a test file** if it doesn't exist
2. **Write a failing test** that describes the exact behavior you want
3. **Run the test** and confirm it fails for the expected reason
4. **Only then** write the minimal code to make it pass

### 2. Testing Patterns

#### Unit Test Template

```python
import pytest
from unittest.mock import Mock, patch
from typing import Any

from codex_template.services.example_service import ExampleService


class TestExampleService:
    """Test suite for ExampleService class."""

    @pytest.fixture
    def service(self) -> ExampleService:
        """Create a fresh ExampleService instance for each test."""
        return ExampleService()

    def test_process_data_with_valid_input(self, service: ExampleService) -> None:
        # Arrange
        input_data = {"key": "value"}
        expected_result = {"processed": True, "data": input_data}

        # Act
        result = service.process_data(input_data)

        # Assert
        assert result == expected_result

    def test_process_data_with_empty_input_raises_error(
        self, service: ExampleService
    ) -> None:
        # Arrange
        empty_data: dict[str, Any] = {}

        # Act & Assert
        with pytest.raises(ValueError, match="Input data cannot be empty"):
            service.process_data(empty_data)

    @pytest.mark.asyncio
    async def test_async_operation_succeeds(self, service: ExampleService) -> None:
        # Arrange
        input_value = "test"

        # Act
        result = await service.async_operation(input_value)

        # Assert
        assert result is not None
        assert "test" in result
```

#### Integration Test Template

```python
import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from codex_template.main import app


class TestAPIIntegration:
    """Integration tests for API endpoints."""

    @pytest.fixture
    def client(self) -> TestClient:
        """Create a test client for the FastAPI app."""
        return TestClient(app)

    def test_health_endpoint_returns_success(self, client: TestClient) -> None:
        # Act
        response = client.get("/health")

        # Assert
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}

    @pytest.mark.asyncio
    async def test_async_endpoint_with_auth(self) -> None:
        async with AsyncClient(app=app, base_url="http://test") as ac:
            # Arrange
            headers = {"Authorization": "Bearer test-token"}

            # Act
            response = await ac.get("/api/v1/protected", headers=headers)

            # Assert
            assert response.status_code == 200
```

### 3. Code Style and Structure

#### Function Signatures with Python 3.13+ Type Hints

```python
from collections.abc import Sequence
from pathlib import Path
from typing import Any

def process_files(
    file_paths: Sequence[Path],
    output_format: str = "json",
    quality: int = 85,
) -> dict[str, str | int]:
    """Process a batch of files with specified format and quality.

    Args:
        file_paths: Sequence of paths to input files.
        output_format: Target format (json, xml, yaml).
        quality: Processing quality (1-100).

    Returns:
        Dictionary containing processing results and metadata.

    Raises:
        ValueError: If quality is not between 1 and 100.
        FileNotFoundError: If any input file doesn't exist.
    """
    if not 1 <= quality <= 100:
        raise ValueError("Quality must be between 1 and 100")

    for path in file_paths:
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

    return {"processed": len(file_paths), "format": output_format}
```

#### Error Handling

```python
class ProcessingError(Exception):
    """Raised when data processing operations fail."""
    pass

def process_user_data(data: dict[str, Any]) -> dict[str, Any]:
    """Process user data with comprehensive error handling."""
    if not data:
        raise ValueError("Data cannot be empty")

    try:
        # Processing logic here
        result = {"success": True, "data": data}
        return result
    except KeyError as e:
        raise ProcessingError(f"Missing required field: {e}") from e
    except Exception as e:
        raise ProcessingError(f"Failed to process data: {e}") from e
```

### 4. FastAPI Application Structure

```python
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Any
import structlog

logger = structlog.get_logger()

app = FastAPI(
    title="Codex Template API",
    description="A modern Python 3.13 service template",
    version="0.1.0",
)

class HealthResponse(BaseModel):
    status: str
    version: str = "0.1.0"

@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint."""
    return HealthResponse(status="healthy")

@app.get("/api/v1/data/{item_id}")
async def get_data(item_id: int) -> dict[str, Any]:
    """Get data by ID."""
    if item_id < 1:
        raise HTTPException(status_code=400, detail="Invalid item ID")

    logger.info("Fetching data", item_id=item_id)
    return {"id": item_id, "data": "example"}
```

### 5. Asynchronous Patterns

```python
import asyncio
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

@asynccontextmanager
async def database_connection() -> AsyncGenerator[Any, None]:
    """Async context manager for database connections."""
    connection = await get_connection()
    try:
        yield connection
    finally:
        await connection.close()

async def process_items_concurrently(items: list[str]) -> list[dict[str, Any]]:
    """Process multiple items concurrently."""
    async def process_item(item: str) -> dict[str, Any]:
        # Simulate async processing
        await asyncio.sleep(0.1)
        return {"item": item, "processed": True}

    # Process items concurrently with semaphore to limit concurrency
    semaphore = asyncio.Semaphore(10)

    async def bounded_process(item: str) -> dict[str, Any]:
        async with semaphore:
            return await process_item(item)

    tasks = [bounded_process(item) for item in items]
    return await asyncio.gather(*tasks)
```

## 🔍 Testing Requirements

### Test Organization

1. **One test class per production class**
2. **Test methods describe behavior, not implementation**
3. **Use descriptive test names**: `test_process_data_with_invalid_input_raises_value_error`
4. **Use pytest markers** for test categorization

### Test Coverage

**Run these commands before every commit:**

```bash
# Run all tests with coverage
uv run pytest --cov=src --cov-report=term-missing --cov-fail-under=95

# Ensure no warnings
uv run pytest --disable-warnings

# Check type hints
uv run mypy src/

# Format and lint code
uv run black src/ tests/
uv run isort src/ tests/
uv run ruff check . --fix
```

### Mock External Dependencies

**Never make real network calls or file system operations in unit tests:**

```python
from unittest.mock import patch, Mock
import pytest

@patch('codex_template.services.external_api.httpx.AsyncClient')
async def test_api_call_handles_timeout(mock_client: Mock) -> None:
    # Arrange
    mock_client.return_value.__aenter__.return_value.get.side_effect = TimeoutError()

    # Act & Assert
    with pytest.raises(ProcessingError, match="API timeout"):
        await service.fetch_external_data()
```

## 🚀 Development Workflow

### 1. Starting a New Feature

```bash
# Create a new branch
git checkout -b feature/new-functionality

# Sync dependencies
uv sync

# Create the test file first
touch tests/unit/test_new_functionality.py

# Write failing tests
# Implement minimal code
# Refactor while keeping tests green
```

### 2. Before Every Commit

**Run this checklist:**

```bash
# 1. All tests pass
uv run pytest

# 2. Coverage is acceptable
uv run pytest --cov=src --cov-fail-under=95

# 3. No type errors
uv run mypy src/

# 4. Code is formatted
uv run black --check src/ tests/
uv run isort --check-only src/ tests/

# 5. No linting issues
uv run ruff check .

# 6. Security checks
uv run bandit -r src/
uv run safety check
```

### 3. Performance and Profiling

```bash
# Profile your code for performance bottlenecks
uv run python -m cProfile -o profile.stats your_script.py

# Memory profiling
uv run python -m memory_profiler your_script.py

# Line-by-line profiling
uv run kernprof -l -v your_script.py

# Real-time profiling
uv run py-spy top --pid <process_id>
```

## 🛠️ Environment Management

### Environment Variables

```python
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Literal

class Settings(BaseSettings):
    """Application settings with validation."""

    app_name: str = "Codex Template"
    debug: bool = False
    environment: Literal["development", "staging", "production"] = "development"

    # Database
    database_url: str = Field(..., env="DATABASE_URL")

    # Redis
    redis_url: str = Field(default="redis://localhost:6379", env="REDIS_URL")

    # API Keys
    api_key: str = Field(..., env="API_KEY")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Usage
settings = Settings()
```

### Docker Support

```dockerfile
FROM python:3.13-slim

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-dev

# Copy source code
COPY src/ ./src/

# Expose port
EXPOSE 8000

# Run application
CMD ["uv", "run", "uvicorn", "codex_template.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 📚 Additional Resources and Best Practices

### Logging

```python
import structlog
from typing import Any

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

def example_function(user_id: int) -> dict[str, Any]:
    """Example function with structured logging."""
    logger.info("Processing user request", user_id=user_id)

    try:
        result = {"user_id": user_id, "status": "success"}
        logger.info("Request processed successfully", user_id=user_id, result=result)
        return result
    except Exception as e:
        logger.error("Request processing failed", user_id=user_id, error=str(e))
        raise
```

### Configuration Management

```python
from functools import lru_cache
from typing import Any

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()

# Dependency injection for FastAPI
def get_settings_dependency() -> Settings:
    """FastAPI dependency for settings."""
    return get_settings()
```

### Database Patterns

```python
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

engine = create_async_engine("postgresql+asyncpg://user:pass@localhost/db")
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

@asynccontextmanager
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Get database session with automatic cleanup."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
```

---

## 🎯 Key Success Metrics

### Code Quality Targets
- **Test Coverage**: >95% line coverage
- **Type Coverage**: 100% of public APIs have type hints
- **Documentation Coverage**: 100% of public functions have docstrings
- **Security**: Zero high-severity security issues
- **Performance**: Response times < 100ms for API endpoints

### Development Velocity
- **TDD Compliance**: All features developed test-first
- **CI/CD Success Rate**: >98% pipeline success rate
- **Code Review Time**: < 24 hours for standard PRs
- **Bug Escape Rate**: < 1% of releases require hotfixes

**Remember: The goal is to write code that works correctly, is easy to maintain, and can be understood by both humans and AI agents. Test-Driven Development with modern Python tooling is the path to achieving this goal reliably.**

## 📖 Reference Links

- [UV Documentation](https://docs.astral.sh/uv/)
- [Python 3.13 Release Notes](https://docs.python.org/3.13/whatsnew/3.13.html)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [Structlog Documentation](https://www.structlog.org/)
