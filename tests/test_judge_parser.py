import json

from src.judge import parse_judge_json


def test_judge_parser_valid_json_minimal_fields() -> None:
    payload = {
        "age_appropriate": True,
        "safe": True,
        "reason_age": "ok",
        "reason_safety": "ok",
        "coherence": 5,
        "story_arc": 4,
        "language_simplicity": 5,
        "suggestions": ["Keep it gentle."],
    }
    result = parse_judge_json(json.dumps(payload))
    assert result.safe is True
    assert result.age_appropriate is True
    assert result.avg_score() == (5 + 4 + 5) / 3.0
    assert result.passed(threshold=4.0) is True


def test_judge_parser_mixed_text_and_json_relaxed_extract() -> None:
    payload = {
        "age_appropriate": True,
        "safe": True,
        "reason_age": "ok",
        "reason_safety": "ok",
        "coherence": 4,
        "story_arc": 4,
        "language_simplicity": 4,
        "suggestions": ["Simplify more.", "Shorten sentences."],
    }
    raw = f"Some extra text\n{json.dumps(payload)}\nTrailing text"
    result = parse_judge_json(raw)
    assert result.safe is True
    assert result.age_appropriate is True
    assert result.coherence == 4


def test_judge_parser_invalid_json_returns_fail_result() -> None:
    raw = "not json at all"
    result = parse_judge_json(raw)
    assert result.safe is False
    assert result.age_appropriate is False
    assert "parsing" in result.reason_age.lower() or "parsing" in result.reason_safety.lower()
