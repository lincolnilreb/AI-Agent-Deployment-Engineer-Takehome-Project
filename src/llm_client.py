"""OpenAI chat completion wrapper."""
from __future__ import annotations

import logging
import os
from typing import Any

import openai

from src import config
from src.exceptions import LLMRequestError, MissingAPIKeyError
from src.schemas import ChatMessage

logger = logging.getLogger(__name__)

DEFAULT_MODEL = "gpt-3.5-turbo"


def call_chat_completion(
    messages: list[ChatMessage],
    *,
    max_tokens: int,
    temperature: float,
    model: str = DEFAULT_MODEL,
) -> str:
    """Call OpenAI ChatCompletion with a fixed model and return assistant text."""

    config.load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise MissingAPIKeyError("OPENAI_API_KEY is not set")

    if max_tokens <= 0:
        raise ValueError("max_tokens must be positive")
    if not 0.0 <= temperature <= 1.0:
        raise ValueError("temperature must be between 0.0 and 1.0")

    openai.api_key = api_key

    try:
        response: Any = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            request_timeout=20,
        )
    except Exception as exc:  # openai.error.OpenAIError is not always importable
        raise LLMRequestError("LLM request failed") from exc

    try:
        content = response.choices[0].message["content"]
    except Exception as exc:
        raise LLMRequestError("LLM response missing content") from exc

    if not isinstance(content, str) or not content.strip():
        raise LLMRequestError("LLM response content is empty")

    return content.strip()
