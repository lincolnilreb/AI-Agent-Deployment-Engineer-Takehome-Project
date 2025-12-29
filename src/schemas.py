"""Shared schemas and dataclasses."""
from __future__ import annotations

from dataclasses import dataclass
from typing import TypedDict


class ChatMessage(TypedDict):
    """Typed structure for OpenAI chat messages."""

    role: str
    content: str


@dataclass(frozen=True)
class JudgeResult:
    """Structured judge output with scoring helpers."""

    age_appropriate: bool
    safe: bool
    reason_age: str
    reason_safety: str
    coherence: int
    story_arc: int
    language_simplicity: int
    suggestions: list[str]

    def avg_score(self) -> float:
        """Return average of coherence, story_arc, and language_simplicity."""

        return (self.coherence + self.story_arc + self.language_simplicity) / 3.0

    def hard_pass(self) -> bool:
        """Return True when safety and age appropriateness both pass."""

        return self.safe and self.age_appropriate

    def passed(self, threshold: float) -> bool:
        """Return True when hard pass and avg_score meets threshold."""

        if threshold < 0:
            raise ValueError("threshold must be non-negative")
        return self.hard_pass() and self.avg_score() >= threshold


@dataclass(frozen=True)
class ClassificationResult:
    """Structured classifier output."""

    category: str
    reason: str
