# Quality Assurance (QA) Rules

## 1. Test Framework
- **Framework:** `pytest`.
- Add `pytest-asyncio` when async handlers or provider clients require it.
- Never make live network calls to GitHub, Jenkins, or any production system in automated tests.
- Use fixtures and recorded payloads to keep tests deterministic.

## 2. Test Layout
- Organize tests to mirror the package structure:
  ```
  tests/
  ├── fixtures/        # Sample logs, workflow payloads, build metadata
  ├── unit/            # Schema validation, parsers, heuristics, small pure functions
  └── integration/     # MCP tool/resource invocation and provider adapter behavior
  ```
- Put reusable sample CI logs and provider responses under `tests/fixtures/`.

## 3. MCP-Focused Test Strategy
- Unit test schema validation, normalization, parsing, truncation, and heuristic classification.
- Integration test tool invocation through the server or SDK harness, not just helper functions in isolation.
- Verify error behavior for missing credentials, provider timeouts, malformed payloads, empty logs, and oversized inputs.
- Prefer golden inputs and assertions on structured outputs over brittle prose-only assertions.

## 4. Coverage Requirements
- **Minimum coverage:** 80% line coverage for Python code.
- Cover edge cases and null or empty inputs, not just the happy path.
- Critical paths such as tool registration, parsing, redaction, and provider error handling should have strong branch coverage.
- Coverage reports must be generated in CI and fail the pipeline if below threshold.

## 5. Test Naming Convention
- Use descriptive names: `test_<unit>_<scenario>_<expected_result>`.
- Examples:
  - `test_fetch_gha_run_logs_with_missing_token_raises_configuration_error`
  - `test_analyze_pipeline_failure_detects_out_of_memory_signature`

## 6. Regression Discipline
- Reproduce bugs with a failing test before implementing the fix whenever practical.
- Keep fixtures minimal but realistic. Trim secrets and irrelevant noise from captured logs.
- Do not snapshot entire unbounded logs when a smaller representative excerpt covers the behavior.

## 7. CI Integration
- Tests run on **every pull request**. A failing test blocks merge.
- Preferred execution order: lint → unit → integration → package validation.
- Use parallel test execution where it helps without hiding order dependencies or flaky behavior.

## 8. Code Review Checklist (QA Perspective)
- [ ] Are there tests for the new or changed tool, resource, or integration?
- [ ] Do tests cover error cases, truncation behavior, and boundary conditions?
- [ ] Are fixtures realistic and scrubbed of secrets?
- [ ] Do integration tests validate protocol behavior rather than only helper internals?
- [ ] Is the test suite deterministic and independent of live provider state?
