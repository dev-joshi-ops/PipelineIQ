---
description: Safe refactoring workflow with test-guarded verification to prevent behavior changes
---

# Refactor Workflow

## When to Use
When improving code structure, readability, or performance **without changing external behavior**. If the refactor also changes behavior, treat it as a feature (see `create-feature.md`).

## Steps

### 1. Create a Refactor Branch
```bash
git checkout develop
git pull origin develop
git checkout -b refactor/<short-description>
```

### 2. Define the Refactor Scope
Before writing any code, document:
- **What** you are refactoring (specific files, functions, handlers, schemas, or integrations).
- **Why** (performance, readability, removing duplication, reducing coupling).
- **What you are NOT changing** (behavior, MCP contracts, provider semantics).

### 3. Ensure Full Test Coverage FIRST
Run the existing test suite and confirm everything passes:
```bash
pytest tests/ -v --cov=src --cov-report=term-missing
```
If the code you're refactoring has **insufficient test coverage**, write tests for the existing behavior **before** refactoring:
- This is critical. Without tests, you can't verify the refactor didn't break anything.
- Commit these tests in a separate commit: `test: add coverage for <module> before refactor`.

### 4. Refactor in Small Steps
- Make **one logical change** per commit.
- Run tests after **every change**:
```bash
pytest tests/ -v
```
- If tests fail, the last change broke something. Fix or revert immediately.
- Do **not** batch multiple refactoring changes into one large commit.

### 5. Common Refactoring Patterns

#### MCP Server
| Pattern | Before | After |
|---|---|---|
| Extract integration | HTTP logic in handler | Provider logic in `integrations/<provider>.py` |
| Extract schema | Inline dict validation | Typed models in `schemas/` |
| Split handler | One oversized tool | Smaller focused tools |
| Config cleanup | Scattered `os.getenv()` | Centralized `config.py` |

### 6. Verify No Behavior Changed
After all refactoring is complete:
```bash
pytest tests/ -v --cov=src
ruff check .
ruff format --check .
```
**All tests must pass. Coverage must not decrease.**

### 7. Commit and Push
```bash
git add -A
git commit -m "refactor(<scope>): <short description>

- <what was refactored and why>
- No behavior changes
- All existing tests pass"
git push origin refactor/<short-description>
```

### 8. Create PR
- **Title:** `refactor(<scope>): <short description>`
- **Description:**
  - What was refactored and why.
  - Explicitly state: "No behavior changes. All existing tests pass."
  - Before/after comparison if it improves clarity.
- **Labels:** `refactor`, `tech-debt`

### 9. Refactor Checklist
- [ ] Scope defined before starting
- [ ] Existing tests pass before refactoring
- [ ] Tests added for uncovered code (committed separately)
- [ ] Each change is a small, testable step
- [ ] Tests pass after every step
- [ ] No behavior changes introduced
- [ ] Coverage did not decrease
- [ ] Linting passes
