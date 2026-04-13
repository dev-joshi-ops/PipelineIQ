---
description: Structured workflow for debugging and fixing bugs with regression test coverage
---

# Fix Bug Workflow

## Prerequisites
- Bug ticket with reproduction steps
- Local environment is running (see `setup-local.md`)

## Steps

### 1. Create a Fix Branch
```bash
git checkout develop
git pull origin develop
git checkout -b fix/<ticket-id>-<short-description>
```

### 2. Reproduce the Bug
Before touching any code, **reproduce the bug locally**:
- Follow the exact reproduction steps from the ticket.
- Confirm you see the expected failure (error message, wrong behavior, crash).
- If you cannot reproduce it, add a comment to the ticket and stop. Do not guess-fix.

### 3. Isolate the Problem
Narrow down the root cause:
- **Server:** Check startup and tool invocation logs.
- **Provider Integration:** Compare expected versus actual Jenkins or GitHub responses.
- **Parsing / Heuristics:** Reduce the failing case to the smallest representative fixture.

Ask yourself:
- When did this last work? (`git log` / `git bisect` can help)
- What changed since then? (`git diff develop..main`)
- Is this a data issue, a code issue, or an environment issue?

### 4. Write a Failing Test First
Before writing the fix, write a test that **reproduces the bug**:
```python
def test_analyze_pipeline_failure_detects_timeout_signature():
    """Regression test for BUG-123: timeout logs were misclassified as generic failure."""
    log_text = "Job exceeded the maximum execution time limit"
    result = analyze_pipeline_failure(log_text)
    assert result["category"] == "timeout"
```
Run the test — it **should fail**. This confirms you've captured the bug.

### 5. Implement the Fix
- Make the **minimal change** needed to fix the bug. Resist the urge to refactor adjacent code.
- If the fix requires a broader refactor, create a separate ticket for that.
- Follow the relevant persona rules (`mcp-builder.md`, `cicd-expert.md`, and companions as needed).

### 6. Verify the Fix
```bash
# Run the specific regression test
pytest tests/ -k "test_analyze_pipeline_failure_detects_timeout_signature" -v

# Run the full test suite to check for regressions
pytest tests/ -v
```

### 7. Commit and Push
```bash
git add -A
git commit -m "fix(<scope>): <short description>

- Root cause: <what was actually wrong>
- Fix: <what you changed and why>
- Added regression test

Closes #<ticket-id>"
git push origin fix/<ticket-id>-<short-description>
```

### 8. Create PR
- **Title:** `fix(<scope>): <short description>`
- **Description:** Include:
  - Link to bug ticket
  - Root cause analysis (1–2 sentences)
  - What the fix does
  - How to verify
- **Labels:** `bug`

### 9. Post-Fix Checklist
- [ ] Bug is reproducible before the fix
- [ ] Regression test fails before the fix, passes after
- [ ] Full test suite passes
- [ ] No unrelated changes included
- [ ] PR description includes root cause analysis
