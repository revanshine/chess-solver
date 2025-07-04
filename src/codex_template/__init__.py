"""Codex Template: Modern Python 3.13 Service Template.

A professional-grade Python template designed for AI-assisted development
using Test-Driven Development (TDD) with UV package management.
"""

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

# Re-export commonly used items for convenience
from .core.config import get_settings
from .core.exceptions import CodexTemplateError, ValidationError

__all__ = [
    "__version__",
    "__author__",
    "__email__",
    "get_settings",
    "CodexTemplateError",
    "ValidationError",
]
