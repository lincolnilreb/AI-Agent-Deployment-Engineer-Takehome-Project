"""Judge module for evaluating stories and parsing JSON output."""
from __future__ import annotations

import json
import logging
from typing import Any

from src import config
from src.exceptions import JudgeParseError
from src.llm_client import call_chat_completion
from src.prompts import build_judge_rubric_prompt, build_judge_system_prompt
from src.schemas import ChatMessage, JudgeResult

logger = logging.getLogger(__name__)


def _failure_result(reason: str) -> JudgeResult:
    return JudgeResult(
        age_appropriate=False,
        safe=False,
        reason_age=reason,
        reason_safety=reason,
        coherence=1,
        story_arc=1,
        language_simplicity=1,
        suggestions=["Return valid JSON matching the rubric."],
    )


def _coerce_judge_fields(payload: dict[str, Any]) -> JudgeResult:
    try:
        age_appropriate = bool(payload["age_appropriate"])
        safe = bool(payload["safe"])
        reason_age = str(payload["reason_age"])
        reason_safety = str(payload["reason_safety"])
        coherence = int(payload["coherence"])
        story_arc = int(payload["story_arc"])
        language_simplicity = int(payload["language_simplicity"])
    except Exception as exc:
        raise JudgeParseError("Missing or invalid judge fields") from exc

    if any(score < 1 or score > 5 for score in (coherence, story_arc, language_simplicity)):
        raise JudgeParseError("Judge scores must be between 1 and 5")

    suggestions_raw = payload.get("suggestions", [])
    if not isinstance(suggestions_raw, list):
        raise JudgeParseError("Suggestions must be a list")

    suggestions = [str(item) for item in suggestions_raw if str(item).strip()][:3]
    if not suggestions:
        suggestions = ["Keep sentences short and gentle."]

    return JudgeResult(
        age_appropriate=age_appropriate,
        safe=safe,
        reason_age=reason_age,
        reason_safety=reason_safety,
        coherence=coherence,
        story_arc=story_arc,
        language_simplicity=language_simplicity,
        suggestions=suggestions,
    )


def parse_judge_json(raw_text: str) -> JudgeResult:
    """Parse judge output into a JudgeResult with relaxed fallback."""

    if not isinstance(raw_text, str):
        return _failure_result("Judge output was not a string")

    try:
        payload = json.loads(raw_text)
        return _coerce_judge_fields(payload)
    except Exception as exc:
        logger.warning("Strict judge parse failed: %s", exc)

    start = raw_text.find("{")
    end = raw_text.rfind("}")
    if start != -1 and end != -1 and end > start:
        try:
            payload = json.loads(raw_text[start : end + 1])
            return _coerce_judge_fields(payload)
        except Exception as exc:
            logger.warning("Relaxed judge parse failed: %s", exc)

    return _failure_result("Judge JSON parsing failed")


def judge_story(user_request: str, story_text: str) -> JudgeResult:
    """Call the judge LLM and return a parsed JudgeResult."""

    if not user_request.strip():
        raise ValueError("user_request must be non-empty")
    if not story_text.strip():
        raise ValueError("story_text must be non-empty")

    system_prompt = build_judge_system_prompt()
    rubric_prompt = build_judge_rubric_prompt()

    messages: list[ChatMessage] = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": (
                f"Evaluate the story for this request: {user_request}\n\n"
                f"Story:\n{story_text}\n\n"
                f"{rubric_prompt}"
            ),
        },
    ]

    raw = call_chat_completion(
        messages,
        max_tokens=config.max_tokens_judge(),
        temperature=config.temperature_judge(),
    )
    return parse_judge_json(raw)
