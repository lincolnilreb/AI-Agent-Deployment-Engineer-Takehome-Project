"""Session container for iterative story revisions."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class StorySession:
    """In-memory session state for a single CLI run."""

    user_request: str
    category: str | None = None
    blueprint: str | None = None
    revision_instructions: str | None = None
    last_story: str | None = None
