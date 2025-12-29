"""Storyteller module for blueprint and story generation."""
from __future__ import annotations

import logging

from src import config
from src.llm_client import call_chat_completion
from src.prompts import build_blueprint_prompt, build_storyteller_system_prompt
from src.schemas import ChatMessage

logger = logging.getLogger(__name__)


def generate_blueprint(user_request: str, category_template: str | None = None) -> str:
    """Generate a JSON blueprint for the requested story."""

    if not user_request.strip():
        raise ValueError("user_request must be non-empty")

    system_prompt = build_storyteller_system_prompt(
        age_hint=None,
        style_hint=None,
        max_tokens=config.max_tokens_story(),
        category_template=category_template,
    )
    user_prompt = build_blueprint_prompt(user_request)

    messages: list[ChatMessage] = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    return call_chat_completion(
        messages,
        max_tokens=config.max_tokens_story(),
        temperature=config.temperature_story(),
    )


def write_story(
    user_request: str,
    blueprint: str | None,
    revision_instructions: str | None,
    category_template: str | None = None,
) -> str:
    """Write a story using the blueprint and optional revision guidance."""

    if not user_request.strip():
        raise ValueError("user_request must be non-empty")

    system_prompt = build_storyteller_system_prompt(
        age_hint=None,
        style_hint=None,
        max_tokens=config.max_tokens_story(),
        category_template=category_template,
    )

    messages: list[ChatMessage] = [
        {"role": "system", "content": system_prompt},
    ]

    if revision_instructions:
        messages.append(
            {
                "role": "user",
                "content": f"Revise the story with these instructions: {revision_instructions}",
            }
        )

    if blueprint:
        messages.append(
            {"role": "user", "content": f"Blueprint JSON: {blueprint}"}
        )

    messages.append({"role": "user", "content": user_request})

    return call_chat_completion(
        messages,
        max_tokens=config.max_tokens_story(),
        temperature=config.temperature_story(),
    )
