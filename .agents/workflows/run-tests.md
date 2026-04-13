---
description: Run the full test suite for the MCP server with coverage reporting
---

# Run Tests Workflow

## When to Use
- Before creating a pull request
- Before merging to `develop` or `main`
- After a refactor to verify zero behavior change
- As part of CI pipeline validation

## Steps

### 1. Unit Tests
```bash
pytest tests/unit/ -v --tb=short
```
- These test individual schemas, parsers, heuristics, and helper functions in isolation.
- They should run fast and avoid live network calls.
- Failures here usually mean local logic is broken.

### 2. Integration Tests
```bash
pytest tests/integration/ -v --tb=short
```
- These test MCP tool or resource invocation and provider adapter behavior with fixtures or mocks.
- They verify protocol contracts, configuration handling, and integration boundaries.
- Failures here mean the MCP behavior or provider interaction is broken.

### 3. Coverage Report
```bash
pytest tests/ -v --cov=src --cov-report=term-missing --cov-fail-under=80
```
- **Minimum threshold:** 80% line coverage.
- `--cov-report=term-missing` shows which lines are not covered.
- `--cov-fail-under=80` fails the command if coverage drops below 80%.
- Review uncovered lines — prioritize covering:
  - Error handling branches
  - Provider timeout and auth edge cases
  - Boundary conditions (empty lists, null values, max limits)

### 4. Lint Check
```bash
ruff check .
ruff format --check .
```
- Linting is part of the test workflow. Code that does not pass lint is not shippable.

### 5. Package Validation
```bash
python -m pip install --no-deps .
```
- Confirms the package can be installed from build metadata, not just an editable checkout.

### 6. Full Suite (All-in-One)
Run everything in sequence to validate before a PR:
```bash
ruff check .
ruff format --check .
pytest tests/ -v --cov=src --cov-report=term-missing --cov-fail-under=80
python -m pip install --no-deps .
```

---

## Interpreting Results

### Test Failed
| Symptom | Likely Cause | Action |
|---|---|---|
| Unit test fails | Business logic bug | Fix the code, not the test (unless test is wrong) |
| Integration test fails | MCP contract or provider adapter changed | Update the handler, schema, or fixture intentionally |
| Coverage below threshold | New code lacks tests | Write tests for uncovered lines before merging |
| Lint fails | Code style violation | Run `ruff check . --fix` |
| Package install fails | Dependency or metadata issue | Fix `pyproject.toml` or package layout |

### Flaky Tests
If a test passes sometimes and fails other times:
- Check for: test ordering dependencies, shared mutable state, time-sensitive assertions, network calls.
- Fix: use factories for test data, isolate DB state per test, mock external calls.
- Never skip or ignore a flaky test — fix it or delete it.

---

## CI Integration
This workflow maps to the GitHub Actions pipeline:
```yaml
# Simplified CI flow
jobs:
  quality:
    steps:
      - ruff check .
      - pytest tests/ --cov=src --cov-fail-under=80
  package:
    steps:
      - python -m pip install --no-deps .
```

## Checklist
- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] Coverage ≥ 80%
- [ ] Lint passes
- [ ] Package validation passes
- [ ] No flaky tests introduced
