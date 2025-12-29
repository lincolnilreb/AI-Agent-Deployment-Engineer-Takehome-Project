- Builds a deterministic Storyteller/Judge/Controller pipeline for ages 5–10 with safety and quality controls.
- Uses fixed `gpt-3.5-turbo` via the legacy OpenAI SDK to minimize compatibility risk.
- Centralizes prompts, config parsing, schemas, and error handling for maintainability.
- Enforces judge JSON schema and robust parsing to keep controller decisions stable.

## Assumptions
- Python 3.11+ runtime.
- Dependencies limited to `openai>=0.28.0,<1.0.0` and pytest for tests.
- Tests run locally with no network access; OpenAI calls are mocked.

## Repository Conventions
Directory structure
- `src/` contains all runtime modules.
- `tests/` contains pytest tests, deterministic and isolated.
- `diagrams/` and `examples/` are documentation artifacts.
- `spec/` holds specifications and ticket outputs.

Naming conventions
- Modules: `snake_case.py`
- Tests: `tests/test_<module>.py` (or `tests/<path>/test_<module>.py` when mirroring).
- Public functions/classes: type hints and docstrings required.
- Exceptions: defined in `src/exceptions.py` and imported by callers.

## Execution Plan
Recommended ticket order
1. `requirements.txt`, `.gitignore`, `.env.example`
2. `src/exceptions.py`, `src/schemas.py`, `src/config.py`
3. `src/llm_client.py`, `src/prompts.py`
4. `src/classifier.py`, `src/session.py`
5. `src/storyteller.py`, `src/judge.py`, `src/controller.py`
6. `main.py`
7. `tests/test_judge_parser.py`, `tests/test_controller.py`, `tests/test_classifier.py`, `tests/test_main.py`
8. `diagrams/*`, `examples/*`, `README.md`

Parallelizable vs. serial tickets
- Parallelizable: docs (`README.md`, `diagrams/*`, `examples/*`), `.gitignore`, `.env.example`.
- Serial dependencies: `src/exceptions.py` → `src/schemas.py`/`src/config.py` → `src/llm_client.py`/`src/prompts.py` → `src/classifier.py`/`src/session.py` → `src/storyteller.py`/`src/judge.py` → `src/controller.py` → `main.py` → tests.
- New dependencies: `src/classifier.py` and `src/session.py` feed `src/controller.py` and `main.py`.

### [TICKET-01] Pin Dependencies
Target: requirements.txt (existing)
Owner Responsibilities: Define deterministic runtime dependencies and versions.

Scope
- In scope: OpenAI SDK pin.
- Out of scope: Optional tooling dependencies.

Changes
Add/Modify Functions
- None.

Add/Modify Types / Classes / Constants
- None.

I/O Contracts
Inputs
- Types/schemas: Plain text dependency list.
- Validation rules: Must include OpenAI SDK range.
- Default behaviors: N/A.

Outputs
- Types/schemas: Pip-readable requirements.
- Invariants: OpenAI SDK pinned to `<1.0.0`.
- Serialization (if applicable): N/A.

Side Effects
- File I/O: requirements file content updated.
- Network: None.
- Storage: None.
- Logging/metrics: None.

Error Handling & Edge Cases
- Expected exceptions (type + when raised): N/A.
- Retry behavior (if any): N/A.
- Edge cases to explicitly handle: None.

Dependencies & Integration Points
- Imports from: None.
- Calls into: None.
- External services/libraries: openai SDK.
- Configuration/env vars: None.

Definition of Done (DoD)
- [ ] Implementation complete and type-checked
- [ ] Unit tests added and passing (pytest)
- [ ] Public APIs documented (docstrings)
- [ ] Error handling implemented per contract
- [ ] No unresolved TODOs in scoped areas
- [ ] Lint/style consistent with repo conventions

Tests (pytest)
New/Updated test files
- tests/requirements/test_requirements.py

Test cases
- Case 1: Verify `openai>=0.28.0,<1.0.0` exists.
- Case 2: No other runtime deps added.
- Failure cases: Missing OpenAI pin.

Notes
- Assumptions: Tests for requirements may be omitted if not standard in repo.
- Follow-ups: None.

### [TICKET-02] Git Ignore Rules
Target: .gitignore (existing)
Owner Responsibilities: Prevent committing secrets and transient artifacts.

Scope
- In scope: `.env` and Python cache/venv patterns.
- Out of scope: Tool-specific ignores not used by project.

Changes
Add/Modify Functions
- None.

Add/Modify Types / Classes / Constants
- None.

I/O Contracts
Inputs
- Types/schemas: gitignore patterns.
- Validation rules: Must include `.env`.
- Default behaviors: N/A.

Outputs
- Types/schemas: gitignore text.
- Invariants: `.env` is ignored.
- Serialization (if applicable): N/A.

Side Effects
- File I/O: .gitignore content updated.
- Network: None.
- Storage: None.
- Logging/metrics: None.

Error Handling & Edge Cases
- Expected exceptions (type + when raised): N/A.
- Retry behavior (if any): N/A.
- Edge cases to explicitly handle: None.

Dependencies & Integration Points
- Imports from: None.
- Calls into: None.
- External services/libraries: None.
- Configuration/env vars: None.

Definition of Done (DoD)
- [ ] Implementation complete and type-checked
- [ ] Unit tests added and passing (pytest)
- [ ] Public APIs documented (docstrings)
- [ ] Error handling implemented per contract
- [ ] No unresolved TODOs in scoped areas
- [ ] Lint/style consistent with repo conventions

Tests (pytest)
New/Updated test files
- tests/gitignore/test_gitignore.py

Test cases
- Case 1: `.env` is ignored.
- Case 2: Python cache patterns present.
- Failure cases: `.env` not ignored.

Notes
- Assumptions: Optional to test gitignore content.
- Follow-ups: None.

### [TICKET-03] Environment Template
Target: .env.example (existing)
Owner Responsibilities: Document required environment variables and defaults.

Scope
- In scope: Required env vars per spec.
- Out of scope: Secrets and actual values.

Changes
Add/Modify Functions
- None.

Add/Modify Types / Classes / Constants
- None.

I/O Contracts
Inputs
- Types/schemas: `KEY=VALUE` lines.
- Validation rules: Include all required keys.
- Default behaviors: Empty values allowed.

Outputs
- Types/schemas: env example text.
- Invariants: All config keys present.
- Serialization (if applicable): N/A.

Side Effects
- File I/O: .env.example content updated.
- Network: None.
- Storage: None.
- Logging/metrics: None.

Error Handling & Edge Cases
- Expected exceptions (type + when raised): N/A.
- Retry behavior (if any): N/A.
- Edge cases to explicitly handle: None.

Dependencies & Integration Points
- Imports from: None.
- Calls into: None.
- External services/libraries: None.
- Configuration/env vars: Must include `OPENAI_API_KEY`, `MAX_ROUNDS`, `QUALITY_THRESHOLD`, `MAX_TOKENS_STORY`, `MAX_TOKENS_JUDGE`, `TEMPERATURE_STORY`, `TEMPERATURE_JUDGE`.

Definition of Done (DoD)
- [ ] Implementation complete and type-checked
- [ ] Unit tests added and passing (pytest)
- [ ] Public APIs documented (docstrings)
- [ ] Error handling implemented per contract
- [ ] No unresolved TODOs in scoped areas
- [ ] Lint/style consistent with repo conventions

Tests (pytest)
New/Updated test files
- tests/env/test_env_example.py

Test cases
- Case 1: All required keys present.
- Case 2: Values are empty or defaults.
- Failure cases: Missing key.

Notes
- Assumptions: Testing env template is optional.
- Follow-ups: None.

### [TICKET-04] Package Initialization
Target: src/__init__.py (existing)
Owner Responsibilities: Define package boundary and optional exports.

Scope
- In scope: Package marker, optional `__all__`.
- Out of scope: Business logic.

Changes
Add/Modify Functions
- None.

Add/Modify Types / Classes / Constants
- Optional `__all__` for exports.

I/O Contracts
Inputs
- Types/schemas: N/A.
- Validation rules: N/A.
- Default behaviors: N/A.

Outputs
- Types/schemas: N/A.
- Invariants: Package importable.
- Serialization (if applicable): N/A.

Side Effects
- File I/O: None.
- Network: None.
- Storage: None.
- Logging/metrics: None.

Error Handling & Edge Cases
- Expected exceptions (type + when raised): N/A.
- Retry behavior (if any): N/A.
- Edge cases to explicitly handle: None.

Dependencies & Integration Points
- Imports from: None or selective exports.
- Calls into: None.
- External services/libraries: None.
- Configuration/env vars: None.

Definition of Done (DoD)
- [ ] Implementation complete and type-checked
- [ ] Unit tests added and passing (pytest)
- [ ] Public APIs documented (docstrings)
- [ ] Error handling implemented per contract
- [ ] No unresolved TODOs in scoped areas
- [ ] Lint/style consistent with repo conventions

Tests (pytest)
New/Updated test files
- tests/src/test_init.py

Test cases
- Case 1: `import src` succeeds.
- Case 2: Optional exports available.
- Failure cases: Import errors.

Notes
- Assumptions: Minimal file.
- Follow-ups: None.

### [TICKET-05] Custom Exceptions
Target: src/exceptions.py (new)
Owner Responsibilities: Define project-specific exception types for consistent error handling.

Scope
- In scope: Custom exceptions for config, LLM, parsing, and controller flow.
- Out of scope: Exception logging strategy (handled by callers).

Changes
Add/Modify Functions
- None.

Add/Modify Types / Classes / Constants
- class `ConfigurationError(Exception)`
- class `MissingAPIKeyError(Exception)`
- class `LLMRequestError(Exception)`
- class `JudgeParseError(Exception)`

I/O Contracts
Inputs
- Types/schemas: Exception messages (str).
- Validation rules: Messages should be human-readable.
- Default behaviors: Exceptions can be raised without message.

Outputs
- Types/schemas: Exception instances.
- Invariants: Exceptions subclass `Exception`.
- Serialization (if applicable): N/A.

Side Effects
- File I/O: None.
- Network: None.
- Storage: None.
- Logging/metrics: None.

Error Handling & Edge Cases
- Expected exceptions (type + when raised): N/A (this file defines exceptions).
- Retry behavior (if any): N/A.
- Edge cases to explicitly handle: None.

Dependencies & Integration Points
- Imports from: None.
- Calls into: None.
- External services/libraries: None.
- Configuration/env vars: None.

Definition of Done (DoD)
- [ ] Implementation complete and type-checked
- [ ] Unit tests added and passing (pytest)
- [ ] Public APIs documented (docstrings)
- [ ] Error handling implemented per contract
- [ ] No unresolved TODOs in scoped areas
- [ ] Lint/style consistent with repo conventions

Tests (pytest)
New/Updated test files
- tests/src/test_exceptions.py

Test cases
- Case 1: Exceptions are importable.
- Case 2: Exceptions accept message strings.
- Failure cases: N/A.

Notes
- Assumptions: Used by config, llm_client, judge, controller.
- Follow-ups: None.

### [TICKET-06] Shared Schemas and Types
Target: src/schemas.py (existing)
Owner Responsibilities: Define shared data structures for judge results and message types.

Scope
- In scope: `JudgeResult` dataclass, helper methods, optional `ChatMessage` TypedDict.
- Out of scope: JSON parsing (in `src/judge.py`).

Changes
Add/Modify Functions
- def avg_score(self) -> float:
  - Behavior: Compute mean of coherence, story_arc, language_simplicity.
  - Preconditions/validation: Numeric fields are ints in 1–5.
  - Postconditions/invariants: Return value in [1.0, 5.0].
  - Side effects: None.
- def hard_pass(self) -> bool:
  - Behavior: True if `safe` and `age_appropriate`.
  - Preconditions/validation: Fields are booleans.
  - Postconditions/invariants: Deterministic boolean.
  - Side effects: None.
- def passed(self, threshold: float) -> bool:
  - Behavior: `hard_pass` and `avg_score >= threshold`.
  - Preconditions/validation: threshold >= 0.
  - Postconditions/invariants: Deterministic boolean.
  - Side effects: None.

Add/Modify Types / Classes / Constants
- @dataclass class `JudgeResult`
- Optional `class ChatMessage(TypedDict)` with keys `role`, `content`.

I/O Contracts
Inputs
- Types/schemas: `JudgeResult` fields per rubric.
- Validation rules: Score fields 1–5; suggestions list length 1–3.
- Default behaviors: No defaults unless specified.

Outputs
- Types/schemas: `JudgeResult` methods return computed values.
- Invariants: No mutation of fields in methods.
- Serialization (if applicable): Use `asdict` if needed.

Side Effects
- File I/O: None.
- Network: None.
- Storage: None.
- Logging/metrics: None.

Error Handling & Edge Cases
- Expected exceptions (type + when raised): ValueError if invalid scores (optional).
- Retry behavior (if any): N/A.
- Edge cases to explicitly handle: threshold < 0.

Dependencies & Integration Points
- Imports from: `dataclasses`, `typing`.
- Calls into: None.
- External services/libraries: None.
- Configuration/env vars: None.

Definition of Done (DoD)
- [ ] Implementation complete and type-checked
- [ ] Unit tests added and passing (pytest)
- [ ] Public APIs documented (docstrings)
- [ ] Error handling implemented per contract
- [ ] No unresolved TODOs in scoped areas
- [ ] Lint/style consistent with repo conventions

Tests (pytest)
New/Updated test files
- tests/src/test_schemas.py

Test cases
- Case 1: avg_score computed correctly.
- Case 2: hard_pass and passed behave as expected.
- Failure cases: Invalid score ranges (if validated).

Notes
- Assumptions: `JudgeResult` is central shared type.
- Follow-ups: None.

### [TICKET-07] Configuration Parsing
Target: src/config.py (existing)
Owner Responsibilities: Read and validate environment variables with type casting.

Scope
- In scope: `get_int`, `get_float`, `get_str`, and domain getters.
- Out of scope: `.env` file loading (env vars only).

Changes
Add/Modify Functions
- def get_int(name: str, default: int, min: int | None = None, max: int | None = None) -> int:
  - Behavior: Read env var, cast to int, validate bounds.
  - Preconditions/validation: Value must parse as int and be within bounds.
  - Postconditions/invariants: Returns int within [min, max].
  - Side effects: None.
- def get_float(name: str, default: float, min: float | None = None, max: float | None = None) -> float:
  - Behavior: Read env var, cast to float, validate bounds.
  - Preconditions/validation: Value must parse as float and be within bounds.
  - Postconditions/invariants: Returns float within [min, max].
  - Side effects: None.
- def get_str(name: str, default: str | None = None) -> str | None:
  - Behavior: Read env var as string or return default.
  - Preconditions/validation: None.
  - Postconditions/invariants: Returns str or None.
  - Side effects: None.
- def load_dotenv(path: str = ".env") -> None:
  - Behavior: Read a local `.env` file and set missing keys in `os.environ`.
  - Preconditions/validation: File may not exist; ignore if missing.
  - Postconditions/invariants: Existing env vars are not overwritten.
  - Side effects: Updates `os.environ`.
- def max_rounds() -> int:
  - Behavior: Domain getter for MAX_ROUNDS with bounds 1–5.
  - Preconditions/validation: N/A.
  - Postconditions/invariants: Returns int in [1, 5].
  - Side effects: None.
- def quality_threshold() -> float:
  - Behavior: Domain getter for QUALITY_THRESHOLD.
  - Preconditions/validation: 0.0–5.0.
  - Postconditions/invariants: Returns float in [0.0, 5.0].
  - Side effects: None.
- def max_tokens_story() -> int:
  - Behavior: Domain getter for MAX_TOKENS_STORY.
  - Preconditions/validation: > 0.
  - Postconditions/invariants: Positive int.
  - Side effects: None.
- def max_tokens_judge() -> int:
  - Behavior: Domain getter for MAX_TOKENS_JUDGE.
  - Preconditions/validation: > 0.
  - Postconditions/invariants: Positive int.
  - Side effects: None.
- def temperature_story() -> float:
  - Behavior: Domain getter for TEMPERATURE_STORY.
  - Preconditions/validation: 0.0–1.0.
  - Postconditions/invariants: Returns float in [0.0, 1.0].
  - Side effects: None.
- def temperature_judge() -> float:
  - Behavior: Domain getter for TEMPERATURE_JUDGE.
  - Preconditions/validation: 0.0–1.0.
  - Postconditions/invariants: Returns float in [0.0, 1.0].
  - Side effects: None.

Add/Modify Types / Classes / Constants
- Module-level logger: `logger = logging.getLogger(__name__)`.

I/O Contracts
Inputs
- Types/schemas: Environment variables as strings.
- Validation rules: Enforced min/max bounds.
- Default behaviors: Use provided defaults when unset.

Outputs
- Types/schemas: Typed config values.
- Invariants: Returned values are within bounds.
- Serialization (if applicable): N/A.

Side Effects
- File I/O: None.
- Network: None.
- Storage: None.
- Logging/metrics: Log validation errors at warning or error.

Error Handling & Edge Cases
- Expected exceptions (type + when raised): `ConfigurationError` when invalid or out of range.
- Retry behavior (if any): None.
- Edge cases to explicitly handle: Empty strings, whitespace, negative values.

Dependencies & Integration Points
- Imports from: `os`, `logging`, `src.exceptions`.
- Calls into: None.
- External services/libraries: None.
- Configuration/env vars: All keys in `.env.example`; `.env` may be loaded manually.

Definition of Done (DoD)
- [ ] Implementation complete and type-checked
- [ ] Unit tests added and passing (pytest)
- [ ] Public APIs documented (docstrings)
- [ ] Error handling implemented per contract
- [ ] No unresolved TODOs in scoped areas
- [ ] Lint/style consistent with repo conventions

Tests (pytest)
New/Updated test files
- tests/src/test_config.py

Test cases
- Case 1: Valid int/float parsing.
- Case 2: Out-of-range raises ConfigurationError.
- Failure cases: Non-numeric values.

Notes
- Assumptions: Env vars provided via shell, not dotenv.
- Follow-ups: None.

### [TICKET-08] LLM Client Wrapper
Target: src/llm_client.py (existing)
Owner Responsibilities: Provide a single, fixed-model OpenAI chat call.

Scope
- In scope: Chat completion call using `gpt-3.5-turbo`.
- Out of scope: Model switching or streaming.

Changes
Add/Modify Functions
- def call_chat_completion(messages: list[dict[str, str]], *, max_tokens: int, temperature: float, model: str = "gpt-3.5-turbo") -> str:
  - Behavior: Call OpenAI chat completion and return assistant content.
  - Preconditions/validation: `OPENAI_API_KEY` is set; messages have required keys.
  - Postconditions/invariants: Returns non-empty string on success.
  - Side effects: Network call to OpenAI API.

Add/Modify Types / Classes / Constants
- Module-level logger: `logger = logging.getLogger(__name__)`.
- Optional constant: `DEFAULT_MODEL = "gpt-3.5-turbo"`.

I/O Contracts
Inputs
- Types/schemas: `messages` list with `role` and `content`.
- Validation rules: `max_tokens > 0`, `0.0 <= temperature <= 1.0`.
- Default behaviors: Model fixed unless explicitly passed.

Outputs
- Types/schemas: Assistant content string.
- Invariants: No secrets logged.
- Serialization (if applicable): N/A.

Side Effects
- File I/O: None.
- Network: OpenAI API call.
- Storage: None.
- Logging/metrics: Log request metadata without content or secrets.

Error Handling & Edge Cases
- Expected exceptions (type + when raised): `MissingAPIKeyError` if API key missing; `LLMRequestError` for API failures.
- Retry behavior (if any): Optional 1 retry on transient errors.
- Edge cases to explicitly handle: Empty response content.

Dependencies & Integration Points
- Imports from: `openai`, `os`, `logging`, `src.exceptions`.
- Calls into: OpenAI SDK `openai.ChatCompletion.create`.
- External services/libraries: OpenAI API.
- Configuration/env vars: `OPENAI_API_KEY`.

Definition of Done (DoD)
- [ ] Implementation complete and type-checked
- [ ] Unit tests added and passing (pytest)
- [ ] Public APIs documented (docstrings)
- [ ] Error handling implemented per contract
- [ ] No unresolved TODOs in scoped areas
- [ ] Lint/style consistent with repo conventions

Tests (pytest)
New/Updated test files
- tests/src/test_llm_client.py

Test cases
- Case 1: Missing API key raises MissingAPIKeyError.
- Case 2: Valid mock call returns content.
- Failure cases: Empty content raises LLMRequestError.

Notes
- Assumptions: Tests mock OpenAI SDK calls.
- Follow-ups: None.

### [TICKET-09] Prompt Templates
Target: src/prompts.py (existing)
Owner Responsibilities: Centralize all prompt strings and builders.

Scope
- In scope: Storyteller system prompt, blueprint prompt, judge system prompt, rubric prompt.
- Out of scope: Prompt tuning beyond spec requirements.

Changes
Add/Modify Functions
- def build_storyteller_system_prompt(age_hint: str | None, style_hint: str | None, max_tokens: int) -> str:
  - Behavior: Return system prompt with safety, age, and structure constraints.
  - Preconditions/validation: `max_tokens > 0`.
  - Postconditions/invariants: Includes prompt-injection mitigation line.
  - Side effects: None.
- def build_blueprint_prompt(user_request: str) -> str:
  - Behavior: Return a blueprint request prompt for JSON output.
  - Preconditions/validation: Non-empty user_request.
  - Postconditions/invariants: Includes required fields list.
  - Side effects: None.
- def build_judge_system_prompt() -> str:
  - Behavior: Return strict JSON-only judge system prompt.
  - Preconditions/validation: None.
  - Postconditions/invariants: Prohibits extra text.
  - Side effects: None.
- def build_judge_rubric_prompt() -> str:
  - Behavior: Return explicit JSON schema for judge output.
  - Preconditions/validation: None.
  - Postconditions/invariants: Includes all required fields.
  - Side effects: None.

Add/Modify Types / Classes / Constants
- Module-level logger: `logger = logging.getLogger(__name__)`.

I/O Contracts
Inputs
- Types/schemas: Strings for user request, age/style hints.
- Validation rules: Non-empty user_request.
- Default behaviors: Omit age/style clauses if not provided.

Outputs
- Types/schemas: Prompt strings.
- Invariants: All hard constraints present.
- Serialization (if applicable): N/A.

Side Effects
- File I/O: None.
- Network: None.
- Storage: None.
- Logging/metrics: Optional debug logs without user content.

Error Handling & Edge Cases
- Expected exceptions (type + when raised): ValueError if user_request empty.
- Retry behavior (if any): N/A.
- Edge cases to explicitly handle: None.

Dependencies & Integration Points
- Imports from: `logging`.
- Calls into: None.
- External services/libraries: None.
- Configuration/env vars: None.

Definition of Done (DoD)
- [ ] Implementation complete and type-checked
- [ ] Unit tests added and passing (pytest)
- [ ] Public APIs documented (docstrings)
- [ ] Error handling implemented per contract
- [ ] No unresolved TODOs in scoped areas
- [ ] Lint/style consistent with repo conventions

Tests (pytest)
New/Updated test files
- tests/src/test_prompts.py

Test cases
- Case 1: Storyteller prompt includes safety and age constraints.
- Case 2: Judge prompt includes JSON-only rule and schema.
- Failure cases: Empty user_request for blueprint prompt.

Notes
- Assumptions: Prompt strings are stable and deterministic.
- Follow-ups: None.

### [TICKET-10] Storyteller Module
Target: src/storyteller.py (existing)
Owner Responsibilities: Generate blueprint and story using prompts and LLM client.

Scope
- In scope: Blueprint generation and story writing with optional revisions.
- Out of scope: Judge evaluation.

Changes
Add/Modify Functions
- def generate_blueprint(user_request: str, category_template: str | None = None) -> str:
  - Behavior: Use blueprint prompt and return JSON string.
  - Preconditions/validation: Non-empty user_request.
  - Postconditions/invariants: Non-empty response.
  - Side effects: LLM API call.
- def write_story(user_request: str, blueprint: str | None, revision_instructions: str | None, category_template: str | None = None) -> str:
  - Behavior: Use system prompt plus user request and blueprint; prioritize revision instructions.
  - Preconditions/validation: Non-empty user_request.
  - Postconditions/invariants: Non-empty story text.
  - Side effects: LLM API call.

Add/Modify Types / Classes / Constants
- Module-level logger: `logger = logging.getLogger(__name__)`.

I/O Contracts
Inputs
- Types/schemas: `user_request` string, optional `blueprint`, optional `revision_instructions`.
- Validation rules: `user_request` must be non-empty.
- Default behaviors: If `blueprint` is None, omit blueprint section.

Outputs
- Types/schemas: Story or blueprint text.
- Invariants: Always includes storyteller system prompt.
- Serialization (if applicable): Blueprint is JSON string (not parsed here).

Side Effects
- File I/O: None.
- Network: OpenAI API calls via llm_client.
- Storage: None.
- Logging/metrics: Log call metadata without content.

Error Handling & Edge Cases
- Expected exceptions (type + when raised): `LLMRequestError` for API failure; ValueError for empty responses.
- Retry behavior (if any): Defer to llm_client.
- Edge cases to explicitly handle: revision instructions provided with no blueprint.

Dependencies & Integration Points
- Imports from: `logging`, `src.llm_client`, `src.prompts`, `src.config`.
- Calls into: `call_chat_completion`.
- External services/libraries: OpenAI API (indirect).
- Configuration/env vars: Tokens and temperature via `src.config`.

Definition of Done (DoD)
- [ ] Implementation complete and type-checked
- [ ] Unit tests added and passing (pytest)
- [ ] Public APIs documented (docstrings)
- [ ] Error handling implemented per contract
- [ ] No unresolved TODOs in scoped areas
- [ ] Lint/style consistent with repo conventions

Tests (pytest)
New/Updated test files
- tests/src/test_storyteller.py

Test cases
- Case 1: Revision instructions take priority in messages.
- Case 2: Blueprint call uses blueprint prompt.
- Failure cases: Empty response raises ValueError.

Notes
- Assumptions: LLM responses are plain text strings.
- Follow-ups: None.

### [TICKET-11] Judge Module
Target: src/judge.py (existing)
Owner Responsibilities: Evaluate stories and parse judge output robustly.

Scope
- In scope: `judge_story`, `parse_judge_json`, relaxed parsing, schema enforcement.
- Out of scope: Controller decision logic.

Changes
Add/Modify Functions
- def judge_story(user_request: str, story_text: str) -> JudgeResult:
  - Behavior: Call judge prompt + rubric; return parsed JudgeResult.
  - Preconditions/validation: Non-empty `user_request` and `story_text`.
  - Postconditions/invariants: Always returns a JudgeResult.
  - Side effects: LLM API call.
- def parse_judge_json(raw_text: str) -> JudgeResult:
  - Behavior: Strict parse; on failure attempt relaxed `{...}` extraction; on failure return failing JudgeResult.
  - Preconditions/validation: raw_text is a string.
  - Postconditions/invariants: Never raises JSON parse errors to caller.
  - Side effects: None.
- def _coerce_judge_fields(payload: dict[str, object]) -> JudgeResult:
  - Behavior: Validate and coerce fields to schema; otherwise return failing JudgeResult.
  - Preconditions/validation: payload dict from JSON.
  - Postconditions/invariants: `JudgeResult` always complete.
  - Side effects: None.

Add/Modify Types / Classes / Constants
- Module-level logger: `logger = logging.getLogger(__name__)`.

I/O Contracts
Inputs
- Types/schemas: raw judge output string.
- Validation rules: Schema fields must exist and types be correct.
- Default behaviors: Fail-safe output on parse failure.

Outputs
- Types/schemas: `JudgeResult`.
- Invariants: `safe` and `age_appropriate` are False on parse failure.
- Serialization (if applicable): N/A.

Side Effects
- File I/O: None.
- Network: OpenAI API call for `judge_story`.
- Storage: None.
- Logging/metrics: Log parse failures and judge errors.

Error Handling & Edge Cases
- Expected exceptions (type + when raised): `JudgeParseError` for hard parse failure (optional), but `parse_judge_json` should swallow and return failing result.
- Retry behavior (if any): None.
- Edge cases to explicitly handle: Extra text around JSON, missing fields, wrong types.

Dependencies & Integration Points
- Imports from: `json`, `logging`, `src.llm_client`, `src.prompts`, `src.schemas`, `src.exceptions`, `src.config`.
- Calls into: `call_chat_completion`.
- External services/libraries: OpenAI API (indirect).
- Configuration/env vars: `MAX_TOKENS_JUDGE`, `TEMPERATURE_JUDGE`.

Definition of Done (DoD)
- [ ] Implementation complete and type-checked
- [ ] Unit tests added and passing (pytest)
- [ ] Public APIs documented (docstrings)
- [ ] Error handling implemented per contract
- [ ] No unresolved TODOs in scoped areas
- [ ] Lint/style consistent with repo conventions

Tests (pytest)
New/Updated test files
- tests/test_judge_parser.py

Test cases
- Case 1: Valid JSON parses correctly.
- Case 2: Mixed text + JSON parses via relaxed extraction.
- Failure cases: Invalid JSON returns failing JudgeResult with parse error reason.

Notes
- Assumptions: Judge always returns at least one JSON object on success.
- Follow-ups: None.

### [TICKET-12] Controller Module
Target: src/controller.py (existing)
Owner Responsibilities: Deterministic orchestration with revision loop, best-candidate selection, and fallback.

Scope
- In scope: `run` loop, candidate tracking, stop conditions, safe fallback.
- Out of scope: Prompt content details.

Changes
Add/Modify Functions
- def run(user_request: str) -> str:
  - Behavior: Generate blueprint and story, judge, revise until pass/stop; return best hard-pass or fallback.
  - Preconditions/validation: Non-empty user_request.
  - Postconditions/invariants: Returns a story string every time.
  - Side effects: Multiple LLM API calls.
- def _safe_fallback_story() -> str:
  - Behavior: Return fixed safe bedtime story.
  - Preconditions/validation: None.
  - Postconditions/invariants: Deterministic safe content.
  - Side effects: None.

Add/Modify Types / Classes / Constants
- Module-level logger: `logger = logging.getLogger(__name__)`.
- Optional constant: `MAX_PARSE_FAILURES = 2`.

I/O Contracts
Inputs
- Types/schemas: `user_request` string.
- Validation rules: Non-empty request.
- Default behaviors: Use config defaults for thresholds and rounds.

Outputs
- Types/schemas: Final story string.
- Invariants: Prefer highest-scoring hard-pass candidate.
- Serialization (if applicable): N/A.

Side Effects
- File I/O: None.
- Network: OpenAI API calls via storyteller/judge.
- Storage: None.
- Logging/metrics: Log round decisions and scores.

Error Handling & Edge Cases
- Expected exceptions (type + when raised): `ConfigurationError` if config invalid; internal errors should not crash controller.
- Retry behavior (if any): None beyond LLM client.
- Edge cases to explicitly handle: All judge parse failures, no hard-pass candidates, max rounds reached.

Dependencies & Integration Points
- Imports from: `logging`, `src.storyteller`, `src.judge`, `src.schemas`, `src.config`, `src.exceptions`.
- Calls into: `generate_blueprint`, `write_story`, `judge_story`.
- External services/libraries: None directly.
- Configuration/env vars: `MAX_ROUNDS`, `QUALITY_THRESHOLD`.

Definition of Done (DoD)
- [ ] Implementation complete and type-checked
- [ ] Unit tests added and passing (pytest)
- [ ] Public APIs documented (docstrings)
- [ ] Error handling implemented per contract
- [ ] No unresolved TODOs in scoped areas
- [ ] Lint/style consistent with repo conventions

Tests (pytest)
New/Updated test files
- tests/test_controller.py

Test cases
- Case 1: Stops at MAX_ROUNDS when score remains low.
- Case 2: Accepts immediately on hard-pass with high score.
- Failure cases: Repeated parse failures return fallback.

Notes
- Assumptions: Judge parsing failures are treated as non-pass.
- Follow-ups: None.

### [TICKET-13] CLI Entry Point
Target: main.py (existing)
Owner Responsibilities: Read user input and print final story output.

Scope
- In scope: CLI parsing for input, optional age/style flags, interactive feedback loop, and verbose process logging.
- Out of scope: Core decision logic beyond routing and user I/O.

Changes
Add/Modify Functions
- def main() -> None:
  - Behavior: Parse CLI args or prompt input, call controller, print result, optionally loop for feedback.
  - Preconditions/validation: Non-empty input.
  - Postconditions/invariants: Prints one story per iteration or an error message.
  - Side effects: Stdout output, optional verbose logs.

Add/Modify Types / Classes / Constants
- Module-level logger: `logger = logging.getLogger(__name__)`.

I/O Contracts
Inputs
- Types/schemas: CLI args and/or stdin string.
- Validation rules: Require a non-empty prompt.
- Default behaviors: Prompt user if no input argument provided.

Outputs
- Types/schemas: Printed story text to stdout.
- Invariants: One controller call per iteration.
- Serialization (if applicable): N/A.

Side Effects
- File I/O: None.
- Network: None directly.
- Storage: None.
- Logging/metrics: Log start/end events and optional stage summaries when verbose.

Error Handling & Edge Cases
- Expected exceptions (type + when raised): Catch `Exception` and print a user-friendly message.
- Retry behavior (if any): None.
- Edge cases to explicitly handle: Empty input, controller errors, feedback-only input.

Dependencies & Integration Points
- Imports from: `argparse`, `logging`, `src.controller`.
- Calls into: `run`.
- External services/libraries: None.
- Configuration/env vars: None.

Definition of Done (DoD)
- [ ] Implementation complete and type-checked
- [ ] Unit tests added and passing (pytest)
- [ ] Public APIs documented (docstrings)
- [ ] Error handling implemented per contract
- [ ] No unresolved TODOs in scoped areas
- [ ] Lint/style consistent with repo conventions

Tests (pytest)
New/Updated test files
- tests/test_main.py

Test cases
- Case 1: CLI input routes to controller.
- Case 2: Missing input triggers prompt path.
- Case 3: Interactive feedback triggers a second controller call.
- Case 4: Verbose flag emits stage logs without altering story output.
- Failure cases: Controller exception handled.

Notes
- Assumptions: CLI flags for age/style are optional and non-disruptive.
- Follow-ups: None.

### [TICKET-14] Judge Parser Tests
Target: tests/test_judge_parser.py (new)
Owner Responsibilities: Validate judge JSON parsing and schema handling.

Scope
- In scope: Tests for valid, mixed, and invalid JSON outputs.
- Out of scope: Integration with OpenAI API.

Changes
Add/Modify Functions
- def test_judge_parser_valid_json_minimal_fields() -> None:
  - Behavior: Valid JSON parses and passes.
  - Preconditions/validation: N/A.
  - Postconditions/invariants: Assertions on `JudgeResult`.
  - Side effects: None.
- def test_judge_parser_mixed_text_and_json_relaxed_extract() -> None:
  - Behavior: Mixed text is parsed via relaxed extraction.
  - Preconditions/validation: N/A.
  - Postconditions/invariants: Assertions on parsed fields.
  - Side effects: None.
- def test_judge_parser_invalid_json_returns_fail_result() -> None:
  - Behavior: Invalid JSON yields failing `JudgeResult`.
  - Preconditions/validation: N/A.
  - Postconditions/invariants: `safe` and `age_appropriate` are False.
  - Side effects: None.

Add/Modify Types / Classes / Constants
- None.

I/O Contracts
Inputs
- Types/schemas: JSON strings.
- Validation rules: N/A.
- Default behaviors: N/A.

Outputs
- Types/schemas: Assertions on `JudgeResult`.
- Invariants: No API calls.
- Serialization (if applicable): N/A.

Side Effects
- File I/O: None.
- Network: None.
- Storage: None.
- Logging/metrics: None.

Error Handling & Edge Cases
- Expected exceptions (type + when raised): None (tests assert no exceptions).
- Retry behavior (if any): N/A.
- Edge cases to explicitly handle: Extra text, missing braces.

Dependencies & Integration Points
- Imports from: `src.judge`, `src.schemas`.
- Calls into: `parse_judge_json`.
- External services/libraries: pytest.
- Configuration/env vars: None.

Definition of Done (DoD)
- [ ] Implementation complete and type-checked
- [ ] Unit tests added and passing (pytest)
- [ ] Public APIs documented (docstrings)
- [ ] Error handling implemented per contract
- [ ] No unresolved TODOs in scoped areas
- [ ] Lint/style consistent with repo conventions

Tests (pytest)
New/Updated test files
- tests/test_judge_parser.py

Test cases
- Case 1: Valid JSON returns hard pass.
- Case 2: Mixed text parses correctly.
- Failure cases: Invalid JSON returns failing result.

Notes
- Assumptions: Parsing functions are deterministic.
- Follow-ups: None.

### [TICKET-15] Controller Tests
Target: tests/test_controller.py (new)
Owner Responsibilities: Ensure controller loop is deterministic and safe.

Scope
- In scope: Max rounds, acceptance, fallback behaviors.
- Out of scope: Real LLM calls.

Changes
Add/Modify Functions
- def test_controller_stopping_condition_max_rounds() -> None:
  - Behavior: Stops at MAX_ROUNDS with low scores.
  - Preconditions/validation: Mock judge results.
  - Postconditions/invariants: Max rounds honored.
  - Side effects: None.
- def test_controller_accepts_immediately_when_pass_and_high_score() -> None:
  - Behavior: Accepts on first pass.
  - Preconditions/validation: Mock judge returns high score.
  - Postconditions/invariants: Storyteller called once.
  - Side effects: None.
- def test_controller_fallback_after_repeated_judge_failures() -> None:
  - Behavior: Returns safe fallback after repeated parse failures.
  - Preconditions/validation: Mock judge failures.
  - Postconditions/invariants: Fallback returned.
  - Side effects: None.

Add/Modify Types / Classes / Constants
- None.

I/O Contracts
Inputs
- Types/schemas: Mocked outputs for storyteller and judge.
- Validation rules: None.
- Default behaviors: None.

Outputs
- Types/schemas: Assertions on final story output and call counts.
- Invariants: No API calls.
- Serialization (if applicable): N/A.

Side Effects
- File I/O: None.
- Network: None.
- Storage: None.
- Logging/metrics: None.

Error Handling & Edge Cases
- Expected exceptions (type + when raised): None.
- Retry behavior (if any): N/A.
- Edge cases to explicitly handle: All rounds fail hard-pass.

Dependencies & Integration Points
- Imports from: `src.controller`, `src.schemas`.
- Calls into: `run`.
- External services/libraries: pytest.
- Configuration/env vars: Override config values in tests.

Definition of Done (DoD)
- [ ] Implementation complete and type-checked
- [ ] Unit tests added and passing (pytest)
- [ ] Public APIs documented (docstrings)
- [ ] Error handling implemented per contract
- [ ] No unresolved TODOs in scoped areas
- [ ] Lint/style consistent with repo conventions

Tests (pytest)
New/Updated test files
- tests/test_controller.py

Test cases
- Case 1: Max rounds stop condition.
- Case 2: Immediate acceptance path.
- Failure cases: Repeated failures trigger fallback.

Notes
- Assumptions: Use monkeypatch or fixtures for config and mocks.
- Follow-ups: None.

### [TICKET-16] System Block Diagram (Mermaid)
Target: diagrams/system_block_diagram.mmd (new)
Owner Responsibilities: Provide machine-readable system flow diagram.

Scope
- In scope: Mermaid flowchart of control loop.
- Out of scope: Diagram styling beyond clarity.

Changes
Add/Modify Functions
- None.

Add/Modify Types / Classes / Constants
- None.

I/O Contracts
Inputs
- Types/schemas: Mermaid syntax.
- Validation rules: Must render without syntax errors.
- Default behaviors: N/A.

Outputs
- Types/schemas: `.mmd` file.
- Invariants: Shows user, controller, storyteller, judge, loop, and output.
- Serialization (if applicable): N/A.

Side Effects
- File I/O: Diagram file created.
- Network: None.
- Storage: None.
- Logging/metrics: None.

Error Handling & Edge Cases
- Expected exceptions (type + when raised): N/A.
- Retry behavior (if any): N/A.
- Edge cases to explicitly handle: N/A.

Dependencies & Integration Points
- Imports from: None.
- Calls into: None.
- External services/libraries: Mermaid renderer (optional).
- Configuration/env vars: None.

Definition of Done (DoD)
- [ ] Implementation complete and type-checked
- [ ] Unit tests added and passing (pytest)
- [ ] Public APIs documented (docstrings)
- [ ] Error handling implemented per contract
- [ ] No unresolved TODOs in scoped areas
- [ ] Lint/style consistent with repo conventions

Tests (pytest)
New/Updated test files
- tests/diagrams/test_system_block_diagram.py

Test cases
- Case 1: Mermaid text includes all nodes and edges.
- Case 2: Loop edge present.
- Failure cases: Missing node names.

Notes
- Assumptions: Optional tests for diagram content.
- Follow-ups: None.

### [TICKET-17] System Block Diagram (Markdown)
Target: diagrams/system_block_diagram.md (new)
Owner Responsibilities: Provide markdown wrapper and explanation for the diagram.

Scope
- In scope: Diagram embed or link and brief caption.
- Out of scope: Extended design docs.

Changes
Add/Modify Functions
- None.

Add/Modify Types / Classes / Constants
- None.

I/O Contracts
Inputs
- Types/schemas: Markdown text.
- Validation rules: Must reference `.mmd` file.
- Default behaviors: N/A.

Outputs
- Types/schemas: Markdown file.
- Invariants: Includes link or embed of diagram.
- Serialization (if applicable): N/A.

Side Effects
- File I/O: Markdown file created.
- Network: None.
- Storage: None.
- Logging/metrics: None.

Error Handling & Edge Cases
- Expected exceptions (type + when raised): N/A.
- Retry behavior (if any): N/A.
- Edge cases to explicitly handle: N/A.

Dependencies & Integration Points
- Imports from: None.
- Calls into: None.
- External services/libraries: None.
- Configuration/env vars: None.

Definition of Done (DoD)
- [ ] Implementation complete and type-checked
- [ ] Unit tests added and passing (pytest)
- [ ] Public APIs documented (docstrings)
- [ ] Error handling implemented per contract
- [ ] No unresolved TODOs in scoped areas
- [ ] Lint/style consistent with repo conventions

Tests (pytest)
New/Updated test files
- tests/diagrams/test_system_block_diagram_md.py

Test cases
- Case 1: References `system_block_diagram.mmd`.
- Case 2: Includes brief description.
- Failure cases: Missing link.

Notes
- Assumptions: Optional tests for docs.
- Follow-ups: None.

### [TICKET-18] Example 01: Gentle Animal Friendship
Target: examples/example_01_gentle_animal_friendship.md (new)
Owner Responsibilities: Document Example 1 input and expected behavior.

Scope
- In scope: Example prompt and description of expected output.
- Out of scope: Generated story content.

Changes
Add/Modify Functions
- None.

Add/Modify Types / Classes / Constants
- None.

I/O Contracts
Inputs
- Types/schemas: Markdown text with input and notes.
- Validation rules: Must match Example 1 intent.
- Default behaviors: N/A.

Outputs
- Types/schemas: Markdown file.
- Invariants: Contains input prompt and notes.
- Serialization (if applicable): N/A.

Side Effects
- File I/O: Example file created.
- Network: None.
- Storage: None.
- Logging/metrics: None.

Error Handling & Edge Cases
- Expected exceptions (type + when raised): N/A.
- Retry behavior (if any): N/A.
- Edge cases to explicitly handle: N/A.

Dependencies & Integration Points
- Imports from: None.
- Calls into: None.
- External services/libraries: None.
- Configuration/env vars: None.

Definition of Done (DoD)
- [ ] Implementation complete and type-checked
- [ ] Unit tests added and passing (pytest)
- [ ] Public APIs documented (docstrings)
- [ ] Error handling implemented per contract
- [ ] No unresolved TODOs in scoped areas
- [ ] Lint/style consistent with repo conventions

Tests (pytest)
New/Updated test files
- tests/examples/test_example_01.py

Test cases
- Case 1: File includes input prompt.
- Case 2: Notes match expected behavior.
- Failure cases: Missing sections.

Notes
- Assumptions: Example content is illustrative.
- Follow-ups: None.

### [TICKET-19] Example 02: Emotional Comfort
Target: examples/example_02_emotional_comfort.md (new)
Owner Responsibilities: Document Example 2 input and expected behavior.

Scope
- In scope: Example prompt and expected behavior notes.
- Out of scope: Generated story content.

Changes
Add/Modify Functions
- None.

Add/Modify Types / Classes / Constants
- None.

I/O Contracts
Inputs
- Types/schemas: Markdown text.
- Validation rules: Must match Example 2 intent.
- Default behaviors: N/A.

Outputs
- Types/schemas: Markdown file.
- Invariants: Contains input prompt and notes.
- Serialization (if applicable): N/A.

Side Effects
- File I/O: Example file created.
- Network: None.
- Storage: None.
- Logging/metrics: None.

Error Handling & Edge Cases
- Expected exceptions (type + when raised): N/A.
- Retry behavior (if any): N/A.
- Edge cases to explicitly handle: N/A.

Dependencies & Integration Points
- Imports from: None.
- Calls into: None.
- External services/libraries: None.
- Configuration/env vars: None.

Definition of Done (DoD)
- [ ] Implementation complete and type-checked
- [ ] Unit tests added and passing (pytest)
- [ ] Public APIs documented (docstrings)
- [ ] Error handling implemented per contract
- [ ] No unresolved TODOs in scoped areas
- [ ] Lint/style consistent with repo conventions

Tests (pytest)
New/Updated test files
- tests/examples/test_example_02.py

Test cases
- Case 1: File includes input prompt.
- Case 2: Notes match expected behavior.
- Failure cases: Missing sections.

Notes
- Assumptions: Example content is illustrative.
- Follow-ups: None.

### [TICKET-20] Example 03: Humor Within Safety
Target: examples/example_03_humor_safe_dinosaur.md (new)
Owner Responsibilities: Document Example 3 input and expected behavior.

Scope
- In scope: Example prompt and expected behavior notes.
- Out of scope: Generated story content.

Changes
Add/Modify Functions
- None.

Add/Modify Types / Classes / Constants
- None.

I/O Contracts
Inputs
- Types/schemas: Markdown text.
- Validation rules: Must match Example 3 intent.
- Default behaviors: N/A.

Outputs
- Types/schemas: Markdown file.
- Invariants: Contains input prompt and notes.
- Serialization (if applicable): N/A.

Side Effects
- File I/O: Example file created.
- Network: None.
- Storage: None.
- Logging/metrics: None.

Error Handling & Edge Cases
- Expected exceptions (type + when raised): N/A.
- Retry behavior (if any): N/A.
- Edge cases to explicitly handle: N/A.

Dependencies & Integration Points
- Imports from: None.
- Calls into: None.
- External services/libraries: None.
- Configuration/env vars: None.

Definition of Done (DoD)
- [ ] Implementation complete and type-checked
- [ ] Unit tests added and passing (pytest)
- [ ] Public APIs documented (docstrings)
- [ ] Error handling implemented per contract
- [ ] No unresolved TODOs in scoped areas
- [ ] Lint/style consistent with repo conventions

Tests (pytest)
New/Updated test files
- tests/examples/test_example_03.py

Test cases
- Case 1: File includes input prompt.
- Case 2: Notes match expected behavior.
- Failure cases: Missing sections.

Notes
- Assumptions: Example content is illustrative.
- Follow-ups: None.

### [TICKET-21] Example 04: Adventure Without Violence
Target: examples/example_04_adventure_no_violence.md (new)
Owner Responsibilities: Document Example 4 input and expected behavior.

Scope
- In scope: Example prompt and expected behavior notes.
- Out of scope: Generated story content.

Changes
Add/Modify Functions
- None.

Add/Modify Types / Classes / Constants
- None.

I/O Contracts
Inputs
- Types/schemas: Markdown text.
- Validation rules: Must match Example 4 intent.
- Default behaviors: N/A.

Outputs
- Types/schemas: Markdown file.
- Invariants: Contains input prompt and notes.
- Serialization (if applicable): N/A.

Side Effects
- File I/O: Example file created.
- Network: None.
- Storage: None.
- Logging/metrics: None.

Error Handling & Edge Cases
- Expected exceptions (type + when raised): N/A.
- Retry behavior (if any): N/A.
- Edge cases to explicitly handle: N/A.

Dependencies & Integration Points
- Imports from: None.
- Calls into: None.
- External services/libraries: None.
- Configuration/env vars: None.

Definition of Done (DoD)
- [ ] Implementation complete and type-checked
- [ ] Unit tests added and passing (pytest)
- [ ] Public APIs documented (docstrings)
- [ ] Error handling implemented per contract
- [ ] No unresolved TODOs in scoped areas
- [ ] Lint/style consistent with repo conventions

Tests (pytest)
New/Updated test files
- tests/examples/test_example_04.py

Test cases
- Case 1: File includes input prompt.
- Case 2: Notes match expected behavior.
- Failure cases: Missing sections.

Notes
- Assumptions: Example content is illustrative.
- Follow-ups: None.

### [TICKET-22] Example 05: Prompt Injection Attempt
Target: examples/example_05_prompt_injection.md (new)
Owner Responsibilities: Document Example 5 input and expected behavior.

Scope
- In scope: Example prompt and expected safe behavior notes.
- Out of scope: Generated story content.

Changes
Add/Modify Functions
- None.

Add/Modify Types / Classes / Constants
- None.

I/O Contracts
Inputs
- Types/schemas: Markdown text.
- Validation rules: Must match Example 5 intent.
- Default behaviors: N/A.

Outputs
- Types/schemas: Markdown file.
- Invariants: Contains input prompt and refusal/redirect expectations.
- Serialization (if applicable): N/A.

Side Effects
- File I/O: Example file created.
- Network: None.
- Storage: None.
- Logging/metrics: None.

Error Handling & Edge Cases
- Expected exceptions (type + when raised): N/A.
- Retry behavior (if any): N/A.
- Edge cases to explicitly handle: N/A.

Dependencies & Integration Points
- Imports from: None.
- Calls into: None.
- External services/libraries: None.
- Configuration/env vars: None.

Definition of Done (DoD)
- [ ] Implementation complete and type-checked
- [ ] Unit tests added and passing (pytest)
- [ ] Public APIs documented (docstrings)
- [ ] Error handling implemented per contract
- [ ] No unresolved TODOs in scoped areas
- [ ] Lint/style consistent with repo conventions

Tests (pytest)
New/Updated test files
- tests/examples/test_example_05.py

Test cases
- Case 1: File includes injection prompt.
- Case 2: Notes specify safe fallback behavior.
- Failure cases: Missing expected behavior notes.

Notes
- Assumptions: Example content is illustrative.
- Follow-ups: None.

### [TICKET-23] Example 06: Revision Loop
Target: examples/example_06_revision_loop.md (new)
Owner Responsibilities: Document Example 6 input and expected revision behavior.

Scope
- In scope: Example prompt and expected revision notes.
- Out of scope: Generated story content.

Changes
Add/Modify Functions
- None.

Add/Modify Types / Classes / Constants
- None.

I/O Contracts
Inputs
- Types/schemas: Markdown text.
- Validation rules: Must match Example 6 intent.
- Default behaviors: N/A.

Outputs
- Types/schemas: Markdown file.
- Invariants: Contains input prompt and judge-driven revision notes.
- Serialization (if applicable): N/A.

Side Effects
- File I/O: Example file created.
- Network: None.
- Storage: None.
- Logging/metrics: None.

Error Handling & Edge Cases
- Expected exceptions (type + when raised): N/A.
- Retry behavior (if any): N/A.
- Edge cases to explicitly handle: N/A.

Dependencies & Integration Points
- Imports from: None.
- Calls into: None.
- External services/libraries: None.
- Configuration/env vars: None.

Definition of Done (DoD)
- [ ] Implementation complete and type-checked
- [ ] Unit tests added and passing (pytest)
- [ ] Public APIs documented (docstrings)
- [ ] Error handling implemented per contract
- [ ] No unresolved TODOs in scoped areas
- [ ] Lint/style consistent with repo conventions

Tests (pytest)
New/Updated test files
- tests/examples/test_example_06.py

Test cases
- Case 1: File includes prompt and revision expectations.
- Case 2: Notes describe judge issues and fixes.
- Failure cases: Missing revision description.

Notes
- Assumptions: Example content is illustrative.
- Follow-ups: None.

### [TICKET-24] README Documentation
Target: README.md (existing)
Owner Responsibilities: Provide full project documentation per spec.

Scope
- In scope: Overview, setup, diagram, rubric, trade-offs, examples, future work.
- Out of scope: API reference.

Changes
Add/Modify Functions
- None.

Add/Modify Types / Classes / Constants
- None.

I/O Contracts
Inputs
- Types/schemas: Markdown text.
- Validation rules: Must include required sections.
- Default behaviors: N/A.

Outputs
- Types/schemas: README content.
- Invariants: Mentions fixed model and safety constraints.
- Serialization (if applicable): N/A.

Side Effects
- File I/O: README updated.
- Network: None.
- Storage: None.
- Logging/metrics: None.

Error Handling & Edge Cases
- Expected exceptions (type + when raised): N/A.
- Retry behavior (if any): N/A.
- Edge cases to explicitly handle: N/A.

Dependencies & Integration Points
- Imports from: None.
- Calls into: None.
- External services/libraries: None.
- Configuration/env vars: None.

Definition of Done (DoD)
- [ ] Implementation complete and type-checked
- [ ] Unit tests added and passing (pytest)
- [ ] Public APIs documented (docstrings)
- [ ] Error handling implemented per contract
- [ ] No unresolved TODOs in scoped areas
- [ ] Lint/style consistent with repo conventions

Tests (pytest)
New/Updated test files
- tests/docs/test_readme.py

Test cases
- Case 1: README includes required sections.
- Case 2: Diagram referenced.
- Failure cases: Missing “what I’d do with 2 more hours”.

Notes
- Assumptions: Optional to test README content.
- Follow-ups: None.

### [TICKET-25] Request Classifier
Target: src/classifier.py (new), src/prompts.py (existing), src/schemas.py (existing)
Owner Responsibilities: Classify the request and select a category template.

Scope
- In scope: LLM-based classification with JSON-only output and allowlist validation.
- Out of scope: Any routing that changes the model or safety rules.

Changes
Add/Modify Functions
- def classify_request(user_request: str) -> ClassificationResult:
  - Behavior: Call LLM classifier, validate category, fall back to default on failure.
  - Preconditions/validation: Non-empty input.
  - Postconditions/invariants: Category is always in allowlist.
  - Side effects: None.

Add/Modify Types / Classes / Constants
- ClassificationResult dataclass with `category`, `reason`.
- Category allowlist and default category constant.
  - Allowlist: `gentle_bedtime`, `comfort`, `adventure`, `humor`, `educational`.

I/O Contracts
Inputs
- Types/schemas: user request string.
- Validation rules: Non-empty.
- Default behaviors: Default category on parse/validation failure.

Outputs
- Types/schemas: ClassificationResult.
- Invariants: `category` is in allowlist.
- Serialization (if applicable): JSON-only from classifier LLM.

Side Effects
- File I/O: None.
- Network: LLM call via llm_client.
- Storage: None.
- Logging/metrics: Log parse/validation failures (no secrets).

Error Handling & Edge Cases
- Expected exceptions (type + when raised): ValueError on empty input.
- Retry behavior (if any): None.
- Edge cases to explicitly handle: Invalid JSON, unknown category.

Dependencies & Integration Points
- Imports from: `logging`, `src.llm_client`, `src.prompts`, `src.schemas`.
- Calls into: `call_chat_completion`.
- External services/libraries: OpenAI SDK.
- Configuration/env vars: None.

Definition of Done (DoD)
- [ ] Implementation complete and type-checked
- [ ] Unit tests added and passing (pytest)
- [ ] Public APIs documented (docstrings)
- [ ] Error handling implemented per contract
- [ ] No unresolved TODOs in scoped areas
- [ ] Lint/style consistent with repo conventions

Tests (pytest)
New/Updated test files
- tests/test_classifier.py

Test cases
- Case 1: Valid JSON yields a known category.
- Case 2: Invalid JSON uses default category.
- Failure cases: Empty input raises ValueError.

Notes
- Assumptions: Classifier categories map to prompt templates.
- Follow-ups: None.

### [TICKET-26] Story Session and Feedback Loop
Target: src/session.py (new), src/controller.py (existing)
Owner Responsibilities: Support session state and user feedback revisions.

Scope
- In scope: StorySession data container and controller support for revision instructions.
- Out of scope: Persistence beyond the current process.

Changes
Add/Modify Functions
- def run(user_request: str, session: StorySession | None = None, verbose: bool = False) -> str:
  - Behavior: Use session fields when provided, update revision instructions per feedback.
  - Preconditions/validation: Non-empty input.
  - Postconditions/invariants: Session updated with last story and revision instructions.
  - Side effects: None.

Add/Modify Types / Classes / Constants
- StorySession dataclass with `user_request`, `category`, `blueprint`,
  `revision_instructions`, and `last_story`.

I/O Contracts
Inputs
- Types/schemas: user request string and optional StorySession.
- Validation rules: Non-empty user_request.
- Default behaviors: Create a new session when none provided.

Outputs
- Types/schemas: Story string.
- Invariants: Session always reflects the latest story.
- Serialization (if applicable): N/A.

Side Effects
- File I/O: None.
- Network: LLM calls via storyteller/judge/classifier.
- Storage: None.
- Logging/metrics: Optional verbose stage logs.

Error Handling & Edge Cases
- Expected exceptions (type + when raised): ValueError for empty input.
- Retry behavior (if any): None.
- Edge cases to explicitly handle: Feedback with no prior story, missing session fields.

Dependencies & Integration Points
- Imports from: `dataclasses`, `src.schemas`, `src.classifier`, `src.storyteller`, `src.judge`, `src.config`.
- Calls into: `classify_request`, `generate_blueprint`, `write_story`, `judge_story`.
- External services/libraries: None directly.
- Configuration/env vars: `MAX_ROUNDS`, `QUALITY_THRESHOLD`.

Definition of Done (DoD)
- [ ] Implementation complete and type-checked
- [ ] Unit tests added and passing (pytest)
- [ ] Public APIs documented (docstrings)
- [ ] Error handling implemented per contract
- [ ] No unresolved TODOs in scoped areas
- [ ] Lint/style consistent with repo conventions

Tests (pytest)
New/Updated test files
- tests/test_main.py

Test cases
- Case 1: Interactive feedback updates revision instructions.
- Case 2: Session preserves category and blueprint across revisions.
- Failure cases: Feedback-only input without prior story handled gracefully.

Notes
- Assumptions: Session lives only for the current CLI run.
- Follow-ups: None.

### [TICKET-27] Verbose Process Logging
Target: src/controller.py (existing)
Owner Responsibilities: Emit stage transitions and stop reasons on demand.

Scope
- In scope: Structured log messages for classifier, storyteller, judge, and controller decisions.
- Out of scope: Chain-of-thought output.

Changes
Add/Modify Functions
- def run(user_request: str, session: StorySession | None = None, verbose: bool = False) -> str:
  - Behavior: When verbose, log stage start/end, judge summary, suggestions, and stop reason.
  - Preconditions/validation: N/A.
  - Postconditions/invariants: Story output unchanged by verbose mode.
  - Side effects: Logging to stderr.

Add/Modify Types / Classes / Constants
- Stop reason constants (e.g., threshold_met, max_rounds, fallback).

I/O Contracts
Inputs
- Types/schemas: boolean verbose flag.
- Validation rules: N/A.
- Default behaviors: verbose is off.

Outputs
- Types/schemas: Same story output.
- Invariants: Logs contain no secrets or user content beyond necessary summaries.
- Serialization (if applicable): N/A.

Side Effects
- File I/O: None.
- Network: None directly.
- Storage: None.
- Logging/metrics: Verbose logs when enabled.

Error Handling & Edge Cases
- Expected exceptions (type + when raised): None specific.
- Retry behavior (if any): None.
- Edge cases to explicitly handle: Repeated judge parse failures.

Dependencies & Integration Points
- Imports from: `logging`, `src.schemas`.
- Calls into: None.
- External services/libraries: None.
- Configuration/env vars: None.

Definition of Done (DoD)
- [ ] Implementation complete and type-checked
- [ ] Unit tests added and passing (pytest)
- [ ] Public APIs documented (docstrings)
- [ ] Error handling implemented per contract
- [ ] No unresolved TODOs in scoped areas
- [ ] Lint/style consistent with repo conventions

Tests (pytest)
New/Updated test files
- tests/test_main.py

Test cases
- Case 1: Verbose flag emits stage logs.
- Failure cases: Logging does not raise exceptions.

Notes
- Assumptions: Logging via stdlib logger.
- Follow-ups: None.

### [TICKET-28] Example 07: User Feedback Revision
Target: examples/example_07_user_feedback_revision.md (new)
Owner Responsibilities: Document Example 7 input and expected feedback behavior.

Scope
- In scope: Example prompt, follow-up feedback, and expected revision notes.
- Out of scope: Generated story content.

Changes
Add/Modify Functions
- None.

Add/Modify Types / Classes / Constants
- None.

I/O Contracts
Inputs
- Types/schemas: Markdown text.
- Validation rules: Must match Example 7 intent.
- Default behaviors: N/A.

Outputs
- Types/schemas: Markdown file.
- Invariants: Contains input prompt, feedback, and expected revision behavior.
- Serialization (if applicable): N/A.

Side Effects
- File I/O: Example file created.
- Network: None.
- Storage: None.
- Logging/metrics: None.

Error Handling & Edge Cases
- Expected exceptions (type + when raised): N/A.
- Retry behavior (if any): N/A.
- Edge cases to explicitly handle: N/A.

Dependencies & Integration Points
- Imports from: None.
- Calls into: None.
- External services/libraries: None.
- Configuration/env vars: None.

Definition of Done (DoD)
- [ ] Implementation complete and type-checked
- [ ] Unit tests added and passing (pytest)
- [ ] Public APIs documented (docstrings)
- [ ] Error handling implemented per contract
- [ ] No unresolved TODOs in scoped areas
- [ ] Lint/style consistent with repo conventions

Tests (pytest)
New/Updated test files
- tests/examples/test_example_07.py

Test cases
- Case 1: File includes prompt and feedback.
- Case 2: Notes specify revision expectations.
- Failure cases: Missing feedback description.

Notes
- Assumptions: Example content is illustrative.
- Follow-ups: None.
