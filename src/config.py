"""Environment configuration parsing and validation."""
from __future__ import annotations

import logging
import os

from src.exceptions import ConfigurationError

logger = logging.getLogger(__name__)


def load_dotenv(path: str = ".env") -> None:
    """Load environment variables from a local .env file if present."""

    if not os.path.isfile(path):
        return

    try:
        with open(path, "r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip().strip("\"'")  # handle simple quoted values
                if key and key not in os.environ:
                    os.environ[key] = value
    except OSError as exc:
        logger.warning("Failed to read %s: %s", path, exc)


def _get_env_value(name: str) -> str | None:
    value = os.getenv(name)
    if value is None:
        return None
    value = value.strip()
    return value if value != "" else None


def get_int(name: str, default: int, min: int | None = None, max: int | None = None) -> int:
    """Return an int environment variable with bounds checking."""

    raw = _get_env_value(name)
    if raw is None:
        return default
    try:
        value = int(raw)
    except ValueError as exc:
        raise ConfigurationError(f"{name} must be an int") from exc
    if min is not None and value < min:
        raise ConfigurationError(f"{name} must be >= {min}")
    if max is not None and value > max:
        raise ConfigurationError(f"{name} must be <= {max}")
    return value


def get_float(
    name: str, default: float, min: float | None = None, max: float | None = None
) -> float:
    """Return a float environment variable with bounds checking."""

    raw = _get_env_value(name)
    if raw is None:
        return default
    try:
        value = float(raw)
    except ValueError as exc:
        raise ConfigurationError(f"{name} must be a float") from exc
    if min is not None and value < min:
        raise ConfigurationError(f"{name} must be >= {min}")
    if max is not None and value > max:
        raise ConfigurationError(f"{name} must be <= {max}")
    return value


def get_str(name: str, default: str | None = None) -> str | None:
    """Return a string environment variable or a default."""

    raw = _get_env_value(name)
    return raw if raw is not None else default


def max_rounds() -> int:
    """Return MAX_ROUNDS with validation (1-5)."""

    return get_int("MAX_ROUNDS", default=3, min=1, max=5)


def quality_threshold() -> float:
    """Return QUALITY_THRESHOLD with validation (0.0-5.0)."""

    return get_float("QUALITY_THRESHOLD", default=4.0, min=0.0, max=5.0)


def max_tokens_story() -> int:
    """Return MAX_TOKENS_STORY with validation."""

    return get_int("MAX_TOKENS_STORY", default=2000, min=1, max=4000)


def max_tokens_judge() -> int:
    """Return MAX_TOKENS_JUDGE with validation."""

    return get_int("MAX_TOKENS_JUDGE", default=1000, min=1, max=2000)


def temperature_story() -> float:
    """Return TEMPERATURE_STORY with validation (0.0-1.0)."""

    return get_float("TEMPERATURE_STORY", default=0.6, min=0.0, max=1.0)


def temperature_judge() -> float:
    """Return TEMPERATURE_JUDGE with validation (0.0-1.0)."""

    return get_float("TEMPERATURE_JUDGE", default=0.0, min=0.0, max=1.0)
