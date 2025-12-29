"""CLI entrypoint for the bedtime storyteller."""
from __future__ import annotations

import argparse
import logging

from src.controller import run
from src.session import StorySession

logger = logging.getLogger(__name__)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Bedtime Storyteller")
    parser.add_argument("prompt", nargs="?", help="Story request")
    parser.add_argument("--age", dest="age", default=None)
    parser.add_argument("--style", dest="style", default=None)
    parser.add_argument("--interactive", action="store_true", default=True)
    parser.add_argument("--verbose", action="store_true")
    return parser.parse_args()


def main() -> None:
    """Read user input and print the final story."""

    args = _parse_args()
    logging.basicConfig(level=logging.INFO if args.verbose else logging.WARNING)

    try:
        if args.prompt:
            user_input = args.prompt
        else:
            user_input = input("What kind of story do you want to hear? ")

        if not user_input.strip():
            raise ValueError("Prompt must be non-empty")

        session = StorySession(user_request=user_input)
        story = run(user_input, session=session, verbose=args.verbose)
        print(story)

        if args.interactive:
            while True:
                feedback = input(
                    "Any changes? (press Enter to finish, or type 'quit') "
                ).strip()
                if not feedback:
                    break
                if feedback.lower() in {"quit", "q", "exit"}:
                    break
                session.revision_instructions = feedback
                story = run(session.user_request, session=session, verbose=args.verbose)
                print(story)
    except Exception as exc:
        logger.error("Failed to generate story: %s", exc)
        print("Sorry, something went wrong. Please try again.")


if __name__ == "__main__":
    main()
