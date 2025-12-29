"""Custom exceptions for the bedtime storyteller system."""


class ConfigurationError(Exception):
    """Raised when configuration values are missing or invalid."""


class MissingAPIKeyError(Exception):
    """Raised when OPENAI_API_KEY is not set."""


class LLMRequestError(Exception):
    """Raised when an LLM request fails or returns invalid data."""


class JudgeParseError(Exception):
    """Raised when judge JSON cannot be parsed."""
