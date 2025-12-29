import json

from src import classifier


def test_classifier_returns_known_category(monkeypatch) -> None:
    payload = {"category": "adventure", "reason": "wants exploration"}

    def fake_call_chat_completion(*_args, **_kwargs) -> str:
        return json.dumps(payload)

    monkeypatch.setattr(classifier, "call_chat_completion", fake_call_chat_completion)

    result = classifier.classify_request("Tell an adventurous story.")
    assert result.category == "adventure"
    assert result.reason == "wants exploration"


def test_classifier_falls_back_on_unknown_category(monkeypatch) -> None:
    payload = {"category": "mystery", "reason": "unknown"}

    def fake_call_chat_completion(*_args, **_kwargs) -> str:
        return json.dumps(payload)

    monkeypatch.setattr(classifier, "call_chat_completion", fake_call_chat_completion)

    result = classifier.classify_request("Tell a mysterious story.")
    assert result.category == classifier.DEFAULT_CATEGORY
    assert result.reason == "unknown category"


def test_classifier_falls_back_on_invalid_json(monkeypatch) -> None:
    def fake_call_chat_completion(*_args, **_kwargs) -> str:
        return "not json"

    monkeypatch.setattr(classifier, "call_chat_completion", fake_call_chat_completion)

    result = classifier.classify_request("Tell a story.")
    assert result.category == classifier.DEFAULT_CATEGORY
    assert result.reason == "parse failure"
