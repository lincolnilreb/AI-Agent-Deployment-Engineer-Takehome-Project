from src import controller
from src.schemas import ClassificationResult, JudgeResult


def _make_result(
    *,
    safe: bool,
    age: bool,
    coherence: int,
    arc: int,
    simplicity: int,
    reason: str = "ok",
) -> JudgeResult:
    return JudgeResult(
        age_appropriate=age,
        safe=safe,
        reason_age=reason,
        reason_safety=reason,
        coherence=coherence,
        story_arc=arc,
        language_simplicity=simplicity,
        suggestions=["Simplify language."],
    )


def test_controller_stopping_condition_max_rounds(monkeypatch) -> None:
    monkeypatch.setenv("MAX_ROUNDS", "2")
    monkeypatch.setenv("QUALITY_THRESHOLD", "5.0")

    call_counts = {"write": 0, "judge": 0}

    def fake_generate_blueprint(_: str, __: str | None = None) -> str:
        return "blueprint"

    def fake_write_story(
        _: str,
        __: str | None,
        ___: str | None,
        ____: str | None = None,
    ) -> str:
        call_counts["write"] += 1
        return f"story {call_counts['write']}"

    def fake_judge_story(_: str, __: str) -> JudgeResult:
        call_counts["judge"] += 1
        if call_counts["judge"] == 1:
            return _make_result(safe=True, age=True, coherence=3, arc=3, simplicity=3)
        return _make_result(safe=True, age=True, coherence=4, arc=4, simplicity=4)

    monkeypatch.setattr(controller, "generate_blueprint", fake_generate_blueprint)
    monkeypatch.setattr(controller, "write_story", fake_write_story)
    monkeypatch.setattr(controller, "judge_story", fake_judge_story)
    monkeypatch.setattr(
        controller,
        "classify_request",
        lambda _: ClassificationResult(category="gentle_bedtime", reason="test"),
    )

    result = controller.run("Tell me a story")
    assert call_counts["write"] == 2
    assert result == "story 2"


def test_controller_accepts_immediately_when_pass_and_high_score(monkeypatch) -> None:
    monkeypatch.setenv("MAX_ROUNDS", "3")
    monkeypatch.setenv("QUALITY_THRESHOLD", "4.0")

    call_counts = {"write": 0}

    def fake_generate_blueprint(_: str, __: str | None = None) -> str:
        return "blueprint"

    def fake_write_story(
        _: str,
        __: str | None,
        ___: str | None,
        ____: str | None = None,
    ) -> str:
        call_counts["write"] += 1
        return "first story"

    def fake_judge_story(_: str, __: str) -> JudgeResult:
        return _make_result(safe=True, age=True, coherence=5, arc=5, simplicity=5)

    monkeypatch.setattr(controller, "generate_blueprint", fake_generate_blueprint)
    monkeypatch.setattr(controller, "write_story", fake_write_story)
    monkeypatch.setattr(controller, "judge_story", fake_judge_story)
    monkeypatch.setattr(
        controller,
        "classify_request",
        lambda _: ClassificationResult(category="gentle_bedtime", reason="test"),
    )

    result = controller.run("Tell me a story")
    assert call_counts["write"] == 1
    assert result == "first story"


def test_controller_fallback_after_repeated_judge_failures(monkeypatch) -> None:
    monkeypatch.setenv("MAX_ROUNDS", "3")
    monkeypatch.setenv("QUALITY_THRESHOLD", "4.0")

    def fake_generate_blueprint(_: str, __: str | None = None) -> str:
        return "blueprint"

    def fake_write_story(
        _: str,
        __: str | None,
        ___: str | None,
        ____: str | None = None,
    ) -> str:
        return "story"

    def fake_judge_story(_: str, __: str) -> JudgeResult:
        return _make_result(
            safe=False,
            age=False,
            coherence=1,
            arc=1,
            simplicity=1,
            reason="Judge JSON parsing failed",
        )

    monkeypatch.setattr(controller, "generate_blueprint", fake_generate_blueprint)
    monkeypatch.setattr(controller, "write_story", fake_write_story)
    monkeypatch.setattr(controller, "judge_story", fake_judge_story)
    monkeypatch.setattr(
        controller,
        "classify_request",
        lambda _: ClassificationResult(category="gentle_bedtime", reason="test"),
    )

    result = controller.run("Tell me a story")
    assert result == controller.SAFE_FALLBACK_STORY
