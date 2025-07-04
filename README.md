# Codex Template: Modern Python 3.13 Service Template

A **professional-grade Python 3.13 template** designed for AI-assisted development using Test-Driven Development (TDD) with UV package management. This template provides a solid foundation for building modern Python services with comprehensive tooling, testing, and development workflows optimized for AI agent collaboration.

Built for developers who want to leverage cutting-edge Python features while maintaining production-quality standards through automated testing and AI-assisted development.

## 🎯 Vision

Create a standardized, modern Python project template that serves as the foundation for all future Codex projects. This template incorporates lessons learned from successful AI-assisted development patterns and provides a proven structure for building reliable, maintainable Python services.

### Core Philosophy

- **Test-Driven Development**: Every feature is built with tests first, ensuring reliability and maintainability
- **AI-Native Development**: Designed specifically for AI agent interaction patterns with comprehensive guidance
- **Modern Python**: Leverages Python 3.13+ features, type hints, and contemporary tooling
- **Zero-Config Setup**: Works out of the box with sensible defaults and comprehensive tooling

## 🚀 Features

### Current Capabilities

- **Modern Python 3.13+**: Latest Python features with comprehensive type annotations
- **UV Package Management**: Fast, reliable dependency management with lock files
- **Comprehensive Testing**: pytest-based testing with >95% coverage targets
- **Code Quality Tooling**: Black, isort, ruff, mypy, bandit integration
- **FastAPI Ready**: Pre-configured for building modern REST APIs
- **Async-First**: Built-in support for asynchronous programming patterns
- **Structured Logging**: JSON-based logging with structlog
- **Container Ready**: Docker configuration for development and production
- **AI Agent Guidelines**: Comprehensive AGENTS.md with development workflows

### Development Tools Included

- **Testing Framework**: pytest with asyncio, coverage, and mocking support
- **Code Formatting**: Black and isort for consistent code style
- **Linting**: Ruff for fast, comprehensive Python linting
- **Type Checking**: mypy for static type analysis
- **Security**: Bandit for security vulnerability scanning
- **Documentation**: MkDocs with Material theme for beautiful docs
- **Performance**: Profiling tools for optimization

## 🏗️ Architecture

```
codex-template/
├── src/
│   └── codex_template/
│       ├── __init__.py
│       ├── main.py              # FastAPI application entry point
│       ├── core/                # Core business logic
│       │   ├── config.py        # Configuration management
│       │   ├── exceptions.py    # Custom exceptions
│       │   └── utils.py         # Utility functions
│       ├── api/                 # API layer
│       │   ├── v1/              # API version 1
│       │   │   └── endpoints/   # API endpoints
│       │   └── middleware.py    # Custom middleware
│       ├── services/            # Business services
│       ├── models/              # Data models
│       └── schemas/             # Pydantic schemas
├── tests/
│   ├── conftest.py              # Pytest configuration
│   ├── unit/                    # Fast, isolated tests
│   ├── integration/             # Component interaction tests
│   ├── e2e/                     # End-to-end tests
│   └── fixtures/                # Test data and helpers
├── docs/                        # Documentation
├── AGENTS.md                    # AI development guidelines
├── README.md                    # This file
├── pyproject.toml              # Modern Python project configuration
└── Dockerfile                  # Container configuration
```

## 📋 Requirements

### Development Environment
- **Python**: 3.13+ (managed with `uv`)
- **UV**: Latest version for package management
- **Docker**: Optional, for containerized development

### System Dependencies
- **Git**: For version control
- **Make**: Optional, for convenience commands

## 🚀 Quick Start

### 1. Create New Project from Template

```bash
# Clone the template
git clone https://github.com/yourusername/codex-template.git my-new-project
cd my-new-project

# Remove template git history
rm -rf .git
git init

# Update project configuration
# Edit pyproject.toml to change project name, description, etc.
```

### 2. Setup Development Environment

```bash
# Install UV if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install dependencies
uv sync

# Install development dependencies
uv sync --group dev

# Activate the virtual environment (optional, uv run handles this)
source .venv/bin/activate
```

### 3. Verify Installation

```bash
# Run tests to verify everything works
uv run pytest

# Check code quality
uv run black --check src/ tests/
uv run ruff check .
uv run mypy src/

# Start the development server (if using FastAPI)
uv run uvicorn codex_template.main:app --reload
```

### 4. AI Agent Setup

Review the comprehensive AI development guidelines:

```bash
# Read the AI agent instructions
cat AGENTS.md

# Verify AI-compatible commands work
uv run pytest --cov=src --cov-report=term-missing
```

## 🧪 Testing

This template follows **strict Test-Driven Development** practices with comprehensive testing tools:

```bash
# Run all tests with coverage
uv run pytest --cov=src --cov-report=html --cov-report=term

# Run tests in watch mode during development
uv run pytest-watch

# Run specific test categories
uv run pytest -m unit
uv run pytest -m integration
uv run pytest -m "not slow"

# Run tests in parallel
uv run pytest -n auto

# Generate coverage report
uv run pytest --cov=src --cov-report=html
open htmlcov/index.html
```

**Coverage Target**: >95% line coverage for all production code

## 🔧 Development Workflow

### Code Quality Commands

```bash
# Format code
uv run black src/ tests/
uv run isort src/ tests/

# Lint code
uv run ruff check . --fix

# Type checking
uv run mypy src/

# Security scanning
uv run bandit -r src/
uv run safety check

# All quality checks at once
uv run pytest && \
uv run black --check src/ tests/ && \
uv run isort --check-only src/ tests/ && \
uv run ruff check . && \
uv run mypy src/ && \
uv run bandit -r src/
```

### Documentation

```bash
# Build documentation
uv run mkdocs build

# Serve documentation locally
uv run mkdocs serve

# Deploy documentation to GitHub Pages
uv run mkdocs gh-deploy
```

### Performance Profiling

```bash
# Profile application performance
uv run python -m cProfile -o profile.stats src/codex_template/main.py

# Memory profiling
uv run python -m memory_profiler src/codex_template/main.py

# Real-time profiling
uv run py-spy top --pid <process_id>
```

## 🐳 Docker Support

### Development Container

```bash
# Build development image
docker build -t codex-template:dev .

# Run container with live reload
docker run -p 8000:8000 -v $(pwd):/app codex-template:dev

# Run tests in container
docker run --rm -v $(pwd):/app codex-template:dev uv run pytest
```

### Production Container

```bash
# Build production image
docker build -f Dockerfile.prod -t codex-template:prod .

# Run production container
docker run -p 8000:8000 codex-template:prod
```

## 🤖 AI Agent Development

This template is specifically designed for AI-assisted development. See `AGENTS.md` for comprehensive guidelines.

### Key AI-Friendly Features

- **Clear Command Patterns**: All development commands use `uv run` prefix
- **Comprehensive Test Coverage**: AI agents can verify changes with test suite
- **Type Safety**: Complete type annotations for better AI understanding
- **Structured Documentation**: Clear patterns and examples for AI learning
- **Quality Gates**: Automated checks ensure code quality without human intervention

### AI Development Workflow

1. **Read AGENTS.md**: Comprehensive development guidelines for AI agents
2. **Follow TDD**: Red-Green-Refactor cycle for all changes
3. **Use Standard Commands**: All development through `uv run` commands
4. **Maintain Quality**: Automated testing and linting for every change
5. **Document Changes**: Clear commit messages and documentation updates

## 📚 Project Structure Explained

### Source Code Organization

- **`src/codex_template/`**: Main package directory following PEP 561
- **`core/`**: Core business logic, configuration, and utilities
- **`api/`**: REST API endpoints and middleware (FastAPI)
- **`services/`**: Business service layer for complex operations
- **`models/`**: Data models and database schemas
- **`schemas/`**: Pydantic schemas for API validation

### Testing Organization

- **`tests/unit/`**: Fast, isolated unit tests
- **`tests/integration/`**: Component integration tests
- **`tests/e2e/`**: End-to-end workflow tests
- **`tests/fixtures/`**: Shared test data and utilities
- **`conftest.py`**: Pytest configuration and shared fixtures

### Configuration Files

- **`pyproject.toml`**: Complete project configuration (PEP 621)
- **`uv.lock`**: Locked dependency versions for reproducible builds
- **`Dockerfile`**: Container configuration for deployment
- **`.gitignore`**: Version control exclusions
- **`AGENTS.md`**: AI development guidelines

## 🔒 Security Best Practices

### Built-in Security Features

- **Dependency Scanning**: Bandit and Safety for vulnerability detection
- **Input Validation**: Pydantic schemas for all API inputs
- **Environment Variables**: Secure configuration management
- **Type Safety**: Complete type annotations prevent common errors
- **Automated Testing**: Comprehensive test coverage for security-critical code

### Security Commands

```bash
# Scan for security vulnerabilities
uv run bandit -r src/

# Check for known vulnerable dependencies
uv run safety check

# Update dependencies to latest secure versions
uv sync --upgrade
```

## 🚀 Deployment

### Environment Configuration

```bash
# Development
export ENVIRONMENT=development
export DEBUG=true

# Production
export ENVIRONMENT=production
export DEBUG=false
export DATABASE_URL=postgresql://...
export REDIS_URL=redis://...
```

### Production Deployment

```bash
# Build optimized container
docker build -f Dockerfile.prod -t codex-template:latest .

# Deploy to your platform of choice
# - AWS ECS/Fargate
# - Google Cloud Run
# - Kubernetes
# - Railway/Heroku
```

## 📈 Monitoring and Observability

### Built-in Monitoring

- **Structured Logging**: JSON logs with correlation IDs
- **Health Checks**: Standard /health endpoint
- **Metrics**: Prometheus-compatible metrics (optional)
- **Performance Tracking**: Built-in profiling tools

### Monitoring Setup

```python
# Example structured logging
import structlog

logger = structlog.get_logger()
logger.info("User action", user_id=123, action="login", duration_ms=45)
```

## 🤝 Contributing

This template is designed for collaborative development with AI agents:

### Development Guidelines

1. **Follow TDD**: Write tests first, then implement features
2. **Use Type Hints**: Complete type annotations for all code
3. **Maintain Coverage**: >95% test coverage target
4. **Document Changes**: Update documentation with code changes
5. **AI-Friendly**: Follow patterns in AGENTS.md for AI collaboration

### Pull Request Process

1. Create feature branch from main
2. Follow TDD cycle for all changes
3. Ensure all quality checks pass
4. Update documentation as needed
5. Submit PR with clear description

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

Built with inspiration from:
- [UV](https://docs.astral.sh/uv/) - Modern Python package management
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [Pydantic](https://docs.pydantic.dev/) - Data validation with Python type hints
- [pytest](https://docs.pytest.org/) - Python testing framework
- Professional Python development practices from the community

---

## 🗺️ Roadmap

### Phase 1: Core Template (Completed)
- [x] Modern Python 3.13+ setup with UV
- [x] Comprehensive testing framework
- [x] Code quality tooling integration
- [x] AI agent development guidelines
- [x] FastAPI application structure
- [x] Docker containerization
- [x] Documentation template

### Phase 2: Enhanced Features (Planned)
- [ ] Database integration templates (PostgreSQL, MongoDB)
- [ ] Authentication and authorization patterns
- [ ] Background job processing (Celery/RQ)
- [ ] Microservices communication patterns
- [ ] Advanced monitoring and observability
- [ ] CI/CD pipeline templates

### Phase 3: Specialized Templates (Future)
- [ ] Machine Learning service template
- [ ] GraphQL API template
- [ ] WebSocket/real-time service template
- [ ] CLI application template
- [ ] Package/library template

*This template represents a commitment to modern Python development practices while providing the foundation for AI-assisted development workflows. It's designed to be both a starting point for new projects and a learning resource for best practices.*
