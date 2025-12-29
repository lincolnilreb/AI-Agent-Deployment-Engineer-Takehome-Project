"""Controller module orchestrating storytelling and judging."""
from __future__ import annotations

import logging

from src import config
from src.classifier import classify_request
from src.judge import judge_story
from src.prompts import get_category_template
from src.schemas import JudgeResult
from src.session import StorySession
from src.storyteller import generate_blueprint, write_story

logger = logging.getLogger(__name__)

SAFE_FALLBACK_STORY = (
    "Once upon a time, a little fox found a cozy blanket under the stars. "
    "The fox listened to the quiet night sounds and felt calm and safe. "
    "Soon the fox yawned, curled up, and fell asleep with a happy smile."
)

MAX_PARSE_FAILURES = 2


def _parse_failure_result(reason: str) -> JudgeResult:
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


def _is_parse_failure(result: JudgeResult) -> bool:
    return (
        not result.safe
        and not result.age_appropriate
        and "parsing" in (result.reason_age + result.reason_safety).lower()
    )


def run(
    user_request: str,
    session: StorySession | None = None,
    verbose: bool = False,
) -> str:
    """Run the storyteller-judge loop and return the final story."""

    if not user_request.strip():
        raise ValueError("user_request must be non-empty")

    if session is None:
        session = StorySession(user_request=user_request)

    if not session.user_request:
        session.user_request = user_request

    max_rounds = config.max_rounds()
    threshold = config.quality_threshold()

    if not session.category:
        classification = classify_request(session.user_request)
        session.category = classification.category
        if verbose:
            logger.info("Classifier category: %s", classification.category)

    category_template = get_category_template(session.category)

    if session.blueprint is None:
        if verbose:
            logger.info("Stage: blueprint generation")
        session.blueprint = generate_blueprint(session.user_request, category_template)
        if verbose:
            logger.info("Stage: blueprint complete")

    candidates: list[tuple[str, JudgeResult, float]] = []
    parse_failures = 0
    revision_instructions: str | None = session.revision_instructions

    for _ in range(max_rounds):
        if verbose:
            logger.info("Stage: storyteller")
        story = write_story(
            session.user_request,
            session.blueprint,
            revision_instructions,
            category_template,
        )
        session.last_story = story
        try:
            if verbose:
                logger.info("Stage: judge")
            result = judge_story(session.user_request, story)
        except Exception as exc:
            logger.warning("Judge failed: %s", exc)
            result = _parse_failure_result("Judge JSON parsing failed")
        avg_score = result.avg_score()
        if verbose:
            logger.info(
                "Judge summary: safe=%s age=%s avg_score=%.2f",
                result.safe,
                result.age_appropriate,
                avg_score,
            )
            if result.suggestions:
                logger.info("Judge suggestions: %s", " | ".join(result.suggestions))

        if result.hard_pass():
            candidates.append((story, result, avg_score))

        if _is_parse_failure(result):
            parse_failures += 1
            logger.warning("Judge parse failure count: %s", parse_failures)

        if result.hard_pass() and avg_score >= threshold:
            if verbose:
                logger.info("Stop reason: threshold met")
            return story

        if parse_failures >= MAX_PARSE_FAILURES:
            logger.warning("Falling back after repeated judge failures")
            if verbose:
                logger.info("Stop reason: fallback after judge failures")
            return SAFE_FALLBACK_STORY

        if result.suggestions:
            revision_instructions = " ".join(result.suggestions)
        else:
            revision_instructions = "Simplify language and improve story arc."
        session.revision_instructions = revision_instructions

    if candidates:
        best_story, _best_result, _best_score = max(candidates, key=lambda item: item[2])
        if verbose:
            logger.info("Stop reason: max rounds reached, best candidate selected")
        return best_story

    if verbose:
        logger.info("Stop reason: max rounds reached, fallback used")
    return SAFE_FALLBACK_STORY
