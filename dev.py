#!/usr/bin/env python3

"""
Development script for codex-template.

This script provides convenient commands for development tasks.
"""

import argparse
import subprocess
import sys
from pathlib import Path


def run_command(command: str, description: str = None) -> None:
    """Run a shell command."""
    if description:
        print(f"🔄 {description}")

    result = subprocess.run(command, shell=True, cwd=Path(__file__).parent)
    if result.returncode != 0:
        print(f"❌ Command failed: {command}")
        sys.exit(1)
    print("✅ Done")


def install_deps():
    """Install dependencies."""
    run_command("uv sync", "Installing dependencies")


def format_code():
    """Format code using black and isort."""
    run_command("uv run black .", "Formatting code with black")
    run_command("uv run isort .", "Sorting imports with isort")


def lint():
    """Run linting."""
    run_command("uv run ruff check .", "Running ruff linter")
    run_command("uv run mypy src/", "Running mypy type checker")


def test():
    """Run tests."""
    run_command("uv run pytest", "Running tests")


def test_cov():
    """Run tests with coverage."""
    run_command(
        "uv run pytest --cov=src/codex_template --cov-report=html",
        "Running tests with coverage",
    )


def serve():
    """Run the development server."""
    run_command(
        "uv run uvicorn src.codex_template.main:app --reload",
        "Starting development server",
    )


def docs_serve():
    """Serve documentation."""
    run_command("uv run mkdocs serve", "Starting documentation server")


def docs_build():
    """Build documentation."""
    run_command("uv run mkdocs build", "Building documentation")


def clean():
    """Clean build artifacts."""
    run_command(
        "rm -rf .pytest_cache .mypy_cache .coverage htmlcov dist build *.egg-info",
        "Cleaning build artifacts",
    )


def all_checks():
    """Run all checks (format, lint, test)."""
    format_code()
    lint()
    test()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Development commands for codex-template"
    )
    parser.add_argument(
        "command",
        choices=[
            "install",
            "format",
            "lint",
            "test",
            "test-cov",
            "serve",
            "docs-serve",
            "docs-build",
            "clean",
            "check-all",
        ],
        help="Command to run",
    )

    args = parser.parse_args()

    commands = {
        "install": install_deps,
        "format": format_code,
        "lint": lint,
        "test": test,
        "test-cov": test_cov,
        "serve": serve,
        "docs-serve": docs_serve,
        "docs-build": docs_build,
        "clean": clean,
        "check-all": all_checks,
    }

    commands[args.command]()


if __name__ == "__main__":
    main()
