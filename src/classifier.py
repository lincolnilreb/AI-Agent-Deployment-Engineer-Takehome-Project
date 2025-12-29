"""Classifier module for routing requests to category templates."""
from __future__ import annotations

import json
import logging

from src.llm_client import call_chat_completion
from src.prompts import CATEGORY_TEMPLATES, build_classifier_prompt
from src.schemas import ChatMessage, ClassificationResult

logger = logging.getLogger(__name__)

DEFAULT_CATEGORY = "gentle_bedtime"


def _parse_classification(raw_text: str) -> ClassificationResult:
    if not isinstance(raw_text, str):
        return ClassificationResult(category=DEFAULT_CATEGORY, reason="non-string output")

    try:
        payload = json.loads(raw_text)
        category = str(payload.get("category", "")).strip()
        reason = str(payload.get("reason", "")).strip()
    except Exception as exc:
        logger.warning("Classifier JSON parse failed: %s", exc)
        return ClassificationResult(category=DEFAULT_CATEGORY, reason="parse failure")

    if category not in CATEGORY_TEMPLATES:
        logger.warning("Classifier returned unknown category: %s", category)
        return ClassificationResult(category=DEFAULT_CATEGORY, reason="unknown category")

    if not reason:
        reason = "classified request"

    return ClassificationResult(category=category, reason=reason)


def classify_request(user_request: str) -> ClassificationResult:
    """Classify the request into a known category with JSON-only output."""

    if not user_request.strip():
        raise ValueError("user_request must be non-empty")

    categories = list(CATEGORY_TEMPLATES.keys())
    system_prompt = (
        "You are a strict classifier for bedtime story requests. "
        "Output JSON only with no extra text."
    )
    user_prompt = build_classifier_prompt(user_request, categories)

    messages: list[ChatMessage] = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    raw = call_chat_completion(
        messages,
        max_tokens=120,
        temperature=0.0,
    )
    return _parse_classification(raw)
