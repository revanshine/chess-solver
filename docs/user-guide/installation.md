# Installation

## Prerequisites

- Python 3.12+
- UV package manager
- PostgreSQL (optional, for database features)
- Redis (optional, for Celery tasks)

## Quick Installation

The fastest way to get started is using UV:

```bash
# Clone the repository
git clone https://github.com/yourusername/codex-template.git
cd codex-template

# Install dependencies
uv sync

# Set up environment variables
cp .env.example .env
```

## Detailed Installation

### 1. Install UV

UV is a fast Python package installer and resolver:

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Clone and Set Up Project

```bash
git clone https://github.com/yourusername/codex-template.git
cd codex-template
```

### 3. Install Dependencies

```bash
# Install all dependencies (including dev dependencies)
uv sync

# Install only production dependencies
uv sync --no-dev
```

### 4. Database Setup (Optional)

If you plan to use database features:

```bash
# Install PostgreSQL
# macOS
brew install postgresql

# Ubuntu/Debian
sudo apt-get install postgresql postgresql-contrib

# Create database
createdb codex_template_dev
```

### 5. Redis Setup (Optional)

For Celery task queue support:

```bash
# macOS
brew install redis

# Ubuntu/Debian
sudo apt-get install redis-server

# Start Redis
redis-server
```

### 6. Environment Configuration

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/codex_template_dev
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key-here
```

### 7. Initialize Database

```bash
# Run migrations (if using Alembic)
uv run alembic upgrade head
```

### 8. Verify Installation

```bash
# Run tests to verify everything works
uv run pytest

# Start the development server
uv run uvicorn src.codex_template.main:app --reload
```

Visit [http://localhost:8000/docs](http://localhost:8000/docs) to see the API documentation.

## Docker Installation

For a containerized setup:

```bash
# Build the image
docker build -t codex-template .

# Run with docker-compose
docker-compose up -d
```

## Development Installation

For development, you'll also want to set up pre-commit hooks:

```bash
# Install pre-commit hooks
uv run pre-commit install

# Run pre-commit on all files
uv run pre-commit run --all-files
```

## Troubleshooting

### Common Issues

**UV not found:**
```bash
# Make sure UV is in your PATH
export PATH="$HOME/.local/bin:$PATH"
```

**Database connection error:**
```bash
# Check PostgreSQL is running
sudo service postgresql status

# Check connection details in .env
```

**Redis connection error:**
```bash
# Check Redis is running
redis-cli ping
```

**Permission errors:**
```bash
# On macOS/Linux, ensure proper permissions
chmod +x dev.py
```
