"""Custom exceptions for codex_template."""

from typing import Any


class CodexTemplateError(Exception):
    """Base exception for all codex_template errors."""

    def __init__(self, message: str, details: dict[str, Any] | None = None) -> None:
        """Initialize the exception.

        Args:
            message: Error message.
            details: Additional error details.
        """
        super().__init__(message)
        self.message = message
        self.details = details or {}


class ValidationError(CodexTemplateError):
    """Raised when data validation fails."""

    pass


class ConfigurationError(CodexTemplateError):
    """Raised when configuration is invalid."""

    pass


class ServiceError(CodexTemplateError):
    """Raised when a service operation fails."""

    pass


class DatabaseError(CodexTemplateError):
    """Raised when database operations fail."""

    pass


class ExternalServiceError(CodexTemplateError):
    """Raised when external service calls fail."""

    pass


class AuthenticationError(CodexTemplateError):
    """Raised when authentication fails."""

    pass


class AuthorizationError(CodexTemplateError):
    """Raised when authorization fails."""

    pass


class NotFoundError(CodexTemplateError):
    """Raised when a requested resource is not found."""

    pass


class ConflictError(CodexTemplateError):
    """Raised when a resource conflict occurs."""

    pass
