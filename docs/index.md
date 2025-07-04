# Codex Template

A modern, production-ready Python project template with FastAPI, SQLAlchemy, Celery, and comprehensive development tools.

## Features

- 🚀 **FastAPI** - Modern, fast web framework for building APIs
- 🗄️ **SQLAlchemy** - Powerful SQL toolkit and ORM
- 📊 **Celery** - Distributed task queue
- 📡 **MQTT** - Lightweight messaging protocol support
- 🧪 **Comprehensive Testing** - pytest with coverage and parallel execution
- 📝 **Documentation** - MkDocs with Material theme and API docs
- 🔧 **Development Tools** - Black, isort, Ruff, mypy, pre-commit hooks
- 📦 **Modern Package Management** - UV for fast dependency resolution
- 🐳 **Docker Support** - Production-ready containerization
- 🔄 **CI/CD Ready** - GitHub Actions workflows
- 📈 **Monitoring** - Built-in logging and metrics
- 🔒 **Security** - JWT authentication, password hashing, security headers

## Quick Start

```bash
# Clone the template
git clone https://github.com/yourusername/codex-template.git
cd codex-template

# Install dependencies
uv sync

# Start development server
uv run uvicorn src.codex_template.main:app --reload
```

Visit [http://localhost:8000/docs](http://localhost:8000/docs) to see the interactive API documentation.

## Project Structure

```
codex-template/
├── src/codex_template/          # Main package
│   ├── core/                    # Core functionality
│   ├── api/                     # API routes
│   ├── models/                  # Database models
│   ├── services/                # Business logic
│   └── utils/                   # Utilities
├── tests/                       # Test suite
├── docs/                        # Documentation
├── scripts/                     # Utility scripts
└── docker/                      # Docker configuration
```

## Development

The project includes a convenient development script:

```bash
# Install dependencies
python dev.py install

# Format code
python dev.py format

# Run linting
python dev.py lint

# Run tests
python dev.py test

# Run tests with coverage
python dev.py test-cov

# Start development server
python dev.py serve

# Serve documentation
python dev.py docs-serve

# Run all checks
python dev.py check-all
```

## Configuration

Copy `.env.example` to `.env` and adjust the settings:

```bash
cp .env.example .env
```

Key configuration options:

- `DATABASE_URL` - Database connection string
- `REDIS_URL` - Redis connection for Celery
- `SECRET_KEY` - JWT secret key
- `MQTT_BROKER_HOST` - MQTT broker host

## Testing

The project includes comprehensive testing with pytest:

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src/codex_template

# Run specific test file
uv run pytest tests/test_core.py

# Run tests in parallel
uv run pytest -n auto
```

## Documentation

Documentation is built with MkDocs and includes:

- User guides
- API reference (auto-generated)
- Development guides

```bash
# Serve documentation locally
uv run mkdocs serve

# Build documentation
uv run mkdocs build
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run the test suite
5. Submit a pull request

See [Contributing Guide](development/contributing.md) for detailed instructions.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
