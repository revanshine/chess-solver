"""Utility functions for codex_template."""

import asyncio
import hashlib
import secrets
import time
from collections.abc import AsyncGenerator, Callable, Coroutine
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from functools import wraps
from pathlib import Path
from typing import Any, TypeVar

import structlog

logger = structlog.get_logger()

T = TypeVar("T")


def generate_id(prefix: str = "", length: int = 8) -> str:
    """Generate a random ID with optional prefix.

    Args:
        prefix: Optional prefix for the ID.
        length: Length of the random part.

    Returns:
        Generated ID string.
    """
    random_part = secrets.token_urlsafe(length)[:length]
    return f"{prefix}{random_part}" if prefix else random_part


def hash_string(value: str, algorithm: str = "sha256") -> str:
    """Hash a string using the specified algorithm.

    Args:
        value: String to hash.
        algorithm: Hashing algorithm to use.

    Returns:
        Hexadecimal hash string.
    """
    hasher = hashlib.new(algorithm)
    hasher.update(value.encode("utf-8"))
    return hasher.hexdigest()


def utc_now() -> datetime:
    """Get current UTC datetime.

    Returns:
        Current UTC datetime.
    """
    return datetime.now(timezone.utc)


def safe_filename(filename: str) -> str:
    """Convert a string to a safe filename.

    Args:
        filename: Original filename.

    Returns:
        Safe filename string.
    """
    # Remove or replace unsafe characters
    safe_chars = []
    for char in filename:
        if char.isalnum() or char in "._-":
            safe_chars.append(char)
        elif char in " \t":
            safe_chars.append("_")

    result = "".join(safe_chars)
    # Ensure it doesn't start with a dot
    if result.startswith("."):
        result = "_" + result[1:]

    return result or "unnamed"


def ensure_directory(path: Path) -> Path:
    """Ensure a directory exists, creating it if necessary.

    Args:
        path: Directory path to ensure.

    Returns:
        The directory path.
    """
    path.mkdir(parents=True, exist_ok=True)
    return path


def retry_async(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: tuple[type[Exception], ...] = (Exception,),
) -> Callable[
    [Callable[..., Coroutine[Any, Any, T]]],
    Callable[..., Coroutine[Any, Any, T]],
]:
    """Decorator for retrying async functions with exponential backoff.

    Args:
        max_attempts: Maximum number of retry attempts.
        delay: Initial delay between retries in seconds.
        backoff: Backoff multiplier for delay.
        exceptions: Tuple of exceptions to catch and retry on.

    Returns:
        Decorated function with retry logic.
    """

    def decorator(
        func: Callable[..., Coroutine[Any, Any, T]],
    ) -> Callable[..., Coroutine[Any, Any, T]]:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> T:
            current_delay = delay
            last_exception = None

            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt == max_attempts - 1:
                        # Last attempt, re-raise the exception
                        raise

                    logger.warning(
                        "Function call failed, retrying",
                        function=func.__name__,
                        attempt=attempt + 1,
                        max_attempts=max_attempts,
                        delay=current_delay,
                        error=str(e),
                    )

                    await asyncio.sleep(current_delay)
                    current_delay *= backoff

            # This should never be reached, but just in case
            if last_exception:
                raise last_exception

            # This should also never be reached
            raise RuntimeError("Retry decorator failed unexpectedly")

        return wrapper

    return decorator


def timing_decorator(func: Callable[..., T]) -> Callable[..., T]:
    """Decorator to log function execution time.

    Args:
        func: Function to time.

    Returns:
        Decorated function with timing.
    """

    @wraps(func)
    def sync_wrapper(*args: Any, **kwargs: Any) -> T:
        start_time = time.perf_counter()
        try:
            result = func(*args, **kwargs)
            execution_time = time.perf_counter() - start_time
            logger.info(
                "Function executed",
                function=func.__name__,
                execution_time_ms=round(execution_time * 1000, 2),
            )
            return result
        except Exception as e:
            execution_time = time.perf_counter() - start_time
            logger.error(
                "Function failed",
                function=func.__name__,
                execution_time_ms=round(execution_time * 1000, 2),
                error=str(e),
            )
            raise

    @wraps(func)
    async def async_wrapper(*args: Any, **kwargs: Any) -> T:
        start_time = time.perf_counter()
        try:
            result = await func(*args, **kwargs)
            execution_time = time.perf_counter() - start_time
            logger.info(
                "Async function executed",
                function=func.__name__,
                execution_time_ms=round(execution_time * 1000, 2),
            )
            return result
        except Exception as e:
            execution_time = time.perf_counter() - start_time
            logger.error(
                "Async function failed",
                function=func.__name__,
                execution_time_ms=round(execution_time * 1000, 2),
                error=str(e),
            )
            raise

    if asyncio.iscoroutinefunction(func):
        return async_wrapper  # type: ignore
    else:
        return sync_wrapper  # type: ignore


@asynccontextmanager
async def async_timeout(seconds: float) -> AsyncGenerator[None, None]:
    """Async context manager for timeouts.

    Args:
        seconds: Timeout in seconds.

    Yields:
        None

    Raises:
        asyncio.TimeoutError: If timeout is exceeded.
    """
    try:
        async with asyncio.timeout(seconds):
            yield
    except asyncio.TimeoutError:
        logger.error("Operation timed out", timeout_seconds=seconds)
        raise


class AsyncRateLimiter:
    """Simple async rate limiter using token bucket algorithm."""

    def __init__(self, rate: float, burst: int = 1) -> None:
        """Initialize the rate limiter.

        Args:
            rate: Tokens per second.
            burst: Maximum burst size.
        """
        self.rate = rate
        self.burst = burst
        self.tokens = burst
        self.last_update = time.monotonic()
        self._lock = asyncio.Lock()

    async def acquire(self, tokens: int = 1) -> None:
        """Acquire tokens from the bucket.

        Args:
            tokens: Number of tokens to acquire.

        Raises:
            ValueError: If tokens requested exceeds burst size.
        """
        if tokens > self.burst:
            raise ValueError(
                f"Requested tokens ({tokens}) exceeds burst size ({self.burst})"
            )

        async with self._lock:
            now = time.monotonic()
            elapsed = now - self.last_update

            # Add tokens based on elapsed time
            self.tokens = min(self.burst, self.tokens + elapsed * self.rate)
            self.last_update = now

            # Wait if not enough tokens
            if self.tokens < tokens:
                wait_time = (tokens - self.tokens) / self.rate
                await asyncio.sleep(wait_time)
                self.tokens = 0
            else:
                self.tokens -= tokens
