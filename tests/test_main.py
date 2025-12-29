import sys

import main as app


def test_main_interactive_feedback_loop(monkeypatch, capsys) -> None:
    inputs = iter(["Tell me a story", "Make it shorter", ""])

    def fake_input(_prompt: str) -> str:
        return next(inputs)

    calls: list[str | None] = []

    def fake_run(_user_request: str, session=None, verbose: bool = False) -> str:
        calls.append(session.revision_instructions)
        return f"story {len(calls)}"

    monkeypatch.setattr(sys, "argv", ["main.py", "--interactive"])
    monkeypatch.setattr("builtins.input", fake_input)
    monkeypatch.setattr(app, "run", fake_run)

    app.main()

    captured = capsys.readouterr()
    assert "story 1" in captured.out
    assert "story 2" in captured.out
    assert calls == [None, "Make it shorter"]


def test_main_non_interactive_prompt_arg(monkeypatch, capsys) -> None:
    def fake_input(_prompt: str) -> str:
        raise AssertionError("input should not be called")

    calls: list[str] = []

    def fake_run(user_request: str, session=None, verbose: bool = False) -> str:
        calls.append(user_request)
        return "one story"

    monkeypatch.setattr(sys, "argv", ["main.py", "A prompt"])
    monkeypatch.setattr("builtins.input", fake_input)
    monkeypatch.setattr(app, "run", fake_run)

    app.main()

    captured = capsys.readouterr()
    assert "one story" in captured.out
    assert calls == ["A prompt"]
