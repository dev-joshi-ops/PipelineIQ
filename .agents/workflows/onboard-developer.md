---
description: New team member onboarding guide from clone to first merged PR
---

# Onboard Developer Workflow

## Purpose
Get a new team member productive in **one day**. By the end of this workflow, they will have:
- A working local environment
- An understanding of the project architecture
- A merged PR (even a small one)

## Steps

### 1. Access Setup (Before Day 1)
The team lead should ensure:
- [ ] GitHub repo access granted
- [ ] CI/CD platform access (GitHub Actions - view permissions at minimum)
- [ ] Communication channels joined (Slack/Teams)
- [ ] Ticket board access (Jira/Linear/GitHub Issues)
- [ ] Cloud dashboard access (if applicable)
- [ ] `.env` values shared securely (password manager, not email/chat)

### 2. Local Environment Setup
Follow the `.agents/workflows/setup-local.md` workflow:
```bash
git clone <repository-url>
cd <project-name>
# Follow all steps in setup-local.md
```
**Checkpoint:** The package installs locally, the MCP server starts, and at least one test passes.

### 3. Understand the Architecture
Read these files in order:
1. **`README.md`** — Project overview, tech stack, folder structure.
2. **`agents.md`** — How AI personas work, code conventions, git workflow.
3. **`.agents/README.md`** — Index of all personas, skills, and workflows.

Then explore the codebase:
- Start with `src/pipeline_iq/server.py` -> trace a single tool or resource from registration -> schema -> handler -> integration.
- Review `tests/fixtures/` and `tests/integration/` to understand how behavior is validated.

### 4. Understand the Persona System
Read at least these two rule files:
- `.agents/rules/mcp-builder.md`
- `.agents/rules/cicd-expert.md`

Try asking your AI assistant: *"Explain the folder structure of this project based on agents.md"*. This validates the AI is reading the rules correctly.

### 5. Run the Test Suite
```bash
pytest tests/ -v
```
**Checkpoint:** All tests pass. If they don't, fix the environment (not the tests).

### 6. Make a Practice PR
Pick a small, low-risk task:
- Fix a typo in documentation
- Add a missing test for an existing function
- Improve an error message
- Improve a tool description or schema field docstring

Follow the `create-feature.md` workflow:
```bash
git checkout develop
git pull origin develop
git checkout -b feature/onboarding-<your-name>
# Make your change
git add -A
git commit -m "chore: <your small change>"
git push origin feature/onboarding-<your-name>
```
Create a PR and request review from your onboarding buddy.

### 7. Review Process Walkthrough
- Your buddy reviews using the `pr-reviewer` skill.
- Address any feedback.
- Merge your first PR.

### 8. Deep Dives (Day 2+)
Based on your role, dive deeper:

#### MCP Builder
- Read `mcp-builder.md` fully
- Try the `scaffold-mcp-server` skill to add or extend a small tool
- Trace one feature from MCP registration to provider integration and tests

#### CI/CD Specialist
- Read `cicd-expert.md` fully
- Study one Jenkins and one GitHub Actions fixture
- Review how failure classifications are represented in code and tests

### 9. Onboarding Checklist
Share this with the new developer:
- [ ] Local environment running
- [ ] Can access: repo, CI/CD, ticket board, chat
- [ ] Read: README, agents.md, .agents/README.md
- [ ] Read: relevant persona rules (MCP and CI/CD)
- [ ] All tests pass locally
- [ ] First PR created, reviewed, and merged
- [ ] Knows how to use the repo skills (`scaffold-mcp-server`, `pr-reviewer`)
- [ ] Knows the git workflow (feature branches, conventional commits)
- [ ] Assigned first real ticket
