---
description: End-to-end workflow for developing a new feature from branch to PR
---

# Create Feature Workflow

## Prerequisites
- Local environment is running (see `setup-local.md`)
- You have a ticket/issue number for the feature

## Steps

### 1. Create a Feature Branch
```bash
git checkout develop
git pull origin develop
git checkout -b feature/<ticket-id>-<short-description>
```

### 2. Define Requirements
- Review the ticket's user story and acceptance criteria.
- Consult `.agents/rules/ba.md` for requirements standards.
- Clarify any ambiguities **before** writing code.

### 3. Implement the MCP Feature
Use the skill: `.agents/skills/scaffold-mcp-server/SKILL.md`
- Schema -> Integration -> Tool/Resource -> Registration -> Tests

### 4. Run Linting
```bash
ruff check . --fix
ruff format .
```

### 5. Run Tests
```bash
pytest tests/ -v --cov=src --cov-report=term-missing
```

### 6. Commit Changes (Atomic Commits)
Per `agents.md` Section 4.1, each commit must represent **one logical change**. Never bundle unrelated layers into a single commit. Use the following sequence:

```bash
git add src/pipeline_iq/schemas/
git commit -m "feat(schemas): add <ToolName> request and response models"

git add src/pipeline_iq/integrations/
git commit -m "feat(integrations): add <Provider> adapter for <ToolName>"

git add src/pipeline_iq/tools/ src/pipeline_iq/resources/ src/pipeline_iq/server.py
git commit -m "feat(mcp): add <ToolName> registration and handler"

git add tests/
git commit -m "test: add <ToolName> unit and integration coverage"

# Docs
git add CHANGELOG.md
git commit -m "docs: update CHANGELOG for <ToolName> feature (Closes #<ticket-id>)"
```

> **Rule of thumb:** If a commit message needs the word "and" to describe unrelated layers, split it.


### 7. Push and Create PR
```bash
git push origin feature/<ticket-id>-<short-description>
```
Create a Pull Request:
- **Title:** `feat(<scope>): <short description>`
- **Description:** Link to ticket, summary of changes, example MCP invocations if the contract changed
- **Reviewers:** Assign at least one peer reviewer
- **Labels:** `mcp`, `cicd`, `security`, or `devops` as appropriate

### 8. Address Review Feedback
- Respond to all comments.
- Push fixes as additional commits (do not force-push during review).
- Re-request review once all feedback is addressed.

### 9. Merge
- Squash merge into `develop` after approval.
- Delete the feature branch after merge.
- Verify the shared validation or packaging workflow succeeds.
