"""Main FastAPI application for codex_template."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .core.config import Settings, get_settings
from .core.exceptions import CodexTemplateError

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
        structlog.processors.JSONRenderer(),
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()


def create_app(settings: Settings | None = None) -> FastAPI:
    """Create and configure the FastAPI application."""
    settings = settings or get_settings()

    @asynccontextmanager
    async def lifespan(_app: FastAPI) -> AsyncGenerator[None]:
        logger.info(
            "Starting application",
            app_name=settings.app_name,
            version=settings.app_version,
        )
        try:
            yield
        finally:
            logger.info("Shutting down application")

    app = FastAPI(
        title=settings.app_name,
        description="A modern Python 3.13 service template for AI-assisted development",
        version=settings.app_version,
        docs_url="/docs" if settings.enable_docs else None,
        redoc_url="/redoc" if settings.enable_docs else None,
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.exception_handler(CodexTemplateError)
    async def codex_template_exception_handler(
        request, exc: CodexTemplateError
    ) -> JSONResponse:
        logger.error(
            "Application error",
            error_type=type(exc).__name__,
            message=exc.message,
            details=exc.details,
            path=str(request.url),
        )
        return JSONResponse(
            status_code=400,
            content={
                "error": type(exc).__name__,
                "message": exc.message,
                "details": exc.details,
            },
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request, exc: Exception) -> JSONResponse:
        logger.error(
            "Unexpected error",
            error_type=type(exc).__name__,
            message=str(exc),
            path=str(request.url),
        )
        return JSONResponse(
            status_code=500,
            content={
                "error": "InternalServerError",
                "message": "An unexpected error occurred",
            },
        )

    @app.get("/health")
    async def health_check() -> dict[str, Any]:
        return {
            "status": "healthy",
            "app_name": settings.app_name,
            "version": settings.app_version,
            "environment": settings.environment,
        }

    @app.get("/")
    async def root() -> dict[str, str]:
        return {
            "message": f"Welcome to {settings.app_name}",
            "version": settings.app_version,
            "docs": "/docs" if settings.enable_docs else "disabled",
        }

    return app


# Entry point for running the application
def main() -> None:
    """Main entry point for running the application.

    This function is used when running the application directly
    or via the CLI command defined in pyproject.toml.
    """
    import uvicorn

    settings = get_settings()
    uvicorn.run(
        "codex_template.main:create_app",
        factory=True,
        host=settings.host,
        port=settings.port,
        reload=settings.is_development,
        log_level=settings.log_level.lower(),
    )


if __name__ == "__main__":
    main()
