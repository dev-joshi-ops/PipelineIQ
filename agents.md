# Global AI Agent Directives

## 0. Instruction Hierarchy

When instruction sources conflict, the following precedence order applies (highest -> lowest):

1. **`agents.md`** - Global directives. Always wins.
2. **Persona rules** (`.agents/rules/*`) - Domain-specific constraints.
3. **Skills & workflows** (`.agents/skills/*/SKILL.md`, `.agents/workflows/*`) - Reusable execution guides.
4. **README examples** (`README.md`, `.agents/README.md`) - Illustrative only; never normative.

If a workflow or skill contradicts `agents.md` or a persona rule, follow the higher-authority source and flag the inconsistency to the developer.

## 1. Core Operating Procedure
- This repository utilizes a **Multi-Agent Persona Architecture**.
- Depending on the task requested, you **must** route work to the appropriate agent handle defined below. Each agent must follow its mapped rule file in `.agents/rules/` before generating a response or writing code.
- Consult `.agents/README.md` for a full index of available personas, skills, and workflows.

### Persona Routing
Use the following agent handles as the canonical routing layer. `@orchestrator` is the entrypoint and delegates work to the specialized subagents below.

## @orchestrator
- **Role:** Lead Solutions Architect and delegation coordinator following `.agents/rules/orchestrator.md`. Reads the request, inspects the repository structure, selects the right specialist agents, and reconciles outputs across domains.
- **Tools:** [`read_file`, `list_directory`]
- **Model:** `gemini-3.1-pro`
- **Default Skills:** []

## @mcp-builder
- **Role:** MCP server developer following `.agents/rules/mcp-builder.md`. Expert in FastMCP (mcp) library, tool/resource/prompt schemas, stdio/SSE communication patterns, and server-side resource management.
- **Tools:** [`read_file`, `edit_file`]
- **Model:** `gemini-3.1-pro`
- **Default Skills:** []

## @cicd-expert
- **Role:** CI/CD automation specialist following `.agents/rules/cicd-expert.md`. Expert in Jenkins Pipeline syntax, GitHub Actions YAML, log pattern matching (regex), and diagnosing infrastructure failures (OOM, timeouts).
- **Tools:** [`read_file`, `edit_file`, `run_terminal_command`]
- **Model:** `gemini-3.1-pro`
- **Default Skills:** []

## @architect
- **Role:** Systems architect following `.agents/rules/architect.md` for boundaries, ADR-worthy decisions, performance trade-offs, and cross-cutting design choices.
- **Tools:** [`read_file`, `edit_file`]
- **Model:** `gemini-3-flash`
- **Default Skills:** [`.agents/skills/performance-profiler/SKILL.md`]

## @security
- **Role:** Security engineer following `.agents/rules/security.md` for auth, vulnerability analysis, hardening, dependency risk, and least-privilege review.
- **Tools:** [`read_file`, `edit_file`]
- **Model:** `gemini-3-flash`
- **Default Skills:** [`.agents/skills/security-scanner/SKILL.md`]

## @devops
- **Role:** DevOps and SRE specialist following `.agents/rules/devops.md` for Docker, CI/CD, infrastructure, deployment, and operational readiness.
- **Tools:** [`read_file`, `edit_file`, `run_terminal_command`]
- **Model:** `gemini-3-flash`
- **Default Skills:** [`.agents/skills/push-code-repo/SKILL.md`, `.agents/skills/performance-profiler/SKILL.md`]


## @qa
- **Role:** QA engineer following `.agents/rules/qa.md` for coverage strategy, regression prevention, test authoring, and release-quality verification.
- **Tools:** [`read_file`, `edit_file`, `run_terminal_command`]
- **Model:** `gemini-3-flash`
- **Default Skills:** [`.agents/skills/pr-reviewer/SKILL.md`]

## @ba
- **Role:** Business analyst following `.agents/rules/ba.md` for requirements, user stories, acceptance criteria, API contract review, and scope clarity.
- **Tools:** [`read_file`, `edit_file`]
- **Model:** `gemini-3-flash`
- **Default Skills:** []

## @pm
- **Role:** Project manager following `.agents/rules/pm.md` for task decomposition, delivery planning, release readiness, and risk tracking.
- **Tools:** [`read_file`, `edit_file`]
- **Model:** `gemini-3-flash`
- **Default Skills:** []

> When a task spans multiple domains (e.g., "add a new feature end-to-end"), consult **all** relevant agents and reconcile their guidance.

### Mandatory Co-Consultation Matrix

The agent routing definitions above select the **primary** agent. The matrix below lists additional rule domains that **must also** be consulted for specific change types, regardless of how the task is phrased:

| Change Type | Always Co-Consult |
|---|---|
| Auth / permissions / login | `@security` + `@qa` + `@architect` |
| MCP Tool / Resource schema | `@mcp-builder` + `@architect` + `@qa` |
| MCP transport / server bootstrap | `@mcp-builder` + `@architect` + `@security` |
| CI/CD Pipeline logic | `@cicd-expert` + `@devops` + `@qa` |
| External / third-party API integration | `@security` + `@devops` + `@architect` + `@cicd-expert` |
| Dependency add / upgrade | `@security` + `@devops` |

### Supported Version Matrix

Do **not** use phrases like "latest stable" or "v6+" when referring to dependencies. Use the pinned versions below. Upgrades require an ADR (see `architect.md` §3).

| Dependency | Supported Version | Upgrade Policy |
|---|---|---|
| Python | 3.11.x, 3.12.x | Adopt new minor within 90 days of release |
| mcp (FastMCP) | 1.2.x | Pin minor; track SDK updates |
| httpx | 0.27.x | Pin minor |
| pydantic | 2.x | Pin major |
| pydantic-settings | 2.7.x | Pin minor |
| pytest | 8.x | Pin major |

> Update this matrix in `agents.md` whenever a version is upgraded. The matrix is the single source of truth for supported versions.

## 1.1 MCP-First Constraints
- This repository builds an MCP server using the **FastMCP** (mcp) library. It is not a FastAPI/React application scaffold.
- Use the `@mcp.tool()`, `@mcp.resource()`, and `@mcp.prompt()` decorators for registration. Avoid manual JSON-RPC transport handling.
- Default transport is `stdio`. Add SSE only when a client requirement explicitly calls for remote transport.
- Define protocol-facing tool and resource inputs using typed Python parameters. FastMCP automatically handles Pydantic validation for these.
- Outputs exposed through MCP must be deterministic and return FastMCP-compliant content objects (e.g., `TextContent`).
- Keep schema models in `src/pipeline_iq/schemas/`, tool handlers in `src/pipeline_iq/tools/`, resource handlers in `src/pipeline_iq/resources/`, and external service adapters in `src/pipeline_iq/integrations/`.
- Do **not** introduce React, Redux, FastAPI, OpenAPI, Alembic, SQLAlchemy, browser E2E frameworks, or REST route conventions unless an ADR explicitly approves them.

## 2. General Code Guidelines
- **No Dead Code:** Never leave commented-out code blocks or `print()`/`console.log()` statements in committed code.
- **Environment Variables:** Never hardcode secrets, API keys, or connection strings. Use `.env` files locally and a secrets manager in production.
- **Root Cleanliness:** Keep application code under `src/pipeline_iq/`, tests under `tests/`, and architecture records under `docs/adrs/`. Do not create `backend/` or `frontend/` trees unless an ADR explicitly introduces them.
- **Formatting:** All Python code must pass `ruff` linting and formatting. Do not add TypeScript or JavaScript scaffolding to this repository unless the task explicitly requires a separate client package.
- **Naming Conventions:**
  - Python: `snake_case` for variables, functions, modules. `PascalCase` for classes.
  - MCP tool and resource IDs: descriptive `snake_case`.
  - Environment variables: upper snake case (for example, `GITHUB_TOKEN`, `JENKINS_URL`).

### 2.1 Documentation Standards
- **Python:** Every public function, class, and module must have a docstring (Google style).
  ```python
  def analyze_pipeline_failure(log_text: str) -> dict[str, str]:
      """Analyze a CI log and return a probable failure classification.

      Args:
          log_text: Normalized CI log content.

      Returns:
          A structured diagnostic summary.

      Raises:
          ValueError: If the log payload is empty.
      """
  ```
- **MCP Contracts:** Document each exported tool and resource with a short purpose statement, input contract summary, output shape, and failure behavior.
- **Comments:** Explain **why**, never **what**. The code shows what it does; comments explain non-obvious reasoning.
- **README updates:** When adding a new feature that changes setup, configuration, or environment variables, update the relevant section in `README.md` in the same PR.

## 3. Canonical Folder Structure

```
/
├── agents.md
├── README.md
├── CHANGELOG.md
├── pyproject.toml
├── .gitignore
├── .agentignore
├── .agents/
│   ├── README.md
│   ├── rules/
│   ├── skills/
│   └── workflows/
├── docs/
│   └── adrs/
├── src/
│   └── pipeline_iq/
│       ├── __init__.py
│       ├── server.py
│       ├── config.py
│       ├── integrations/
│       ├── schemas/
│       ├── tools/
│       └── resources/
└── tests/
    ├── fixtures/
    ├── unit/
    └── integration/
```

## 4. Git Conventions
- **Branch naming:** `feature/<ticket-id>-short-description`, `fix/<ticket-id>-short-description`, `chore/<description>`.
- **Commit messages:** Use Conventional Commits (`feat:`, `fix:`, `docs:`, `chore:`, `test:`, `refactor:`).
- **Pull requests:** Must reference the originating ticket. Require at least one approval before merge.

### 4.1 Granular Atomic Commits
- Each commit must represent **one logical change**. Never bundle unrelated changes.
- Preferred commit sequence for a new feature:
  ```
  feat(schemas): add Jenkins build log request and response models
  feat(integrations): add Jenkins API client with typed parsing
  feat(tools): add analyze pipeline failure tool
  feat(resources): add workflow metadata resource
  test: add server and tool invocation coverage
  docs: update CHANGELOG for CI debugger capability
  ```
- If a commit cannot be described without using the word "and", it should be split.
- Tests and code must be in the same PR but may be in separate commits.

### 4.2 Changelog
- Maintain a `CHANGELOG.md` in the project root following [Keep a Changelog](https://keepachangelog.com/) format.
- Every user-facing change **must** have a changelog entry in the same PR that introduces it.
- Group entries under: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`.
- Format:
  ```markdown
  ## [Unreleased]
  ### Added
  - Jenkins build log retrieval tool (#42)
  - GitHub Actions failure analysis heuristics (#43)

  ### Fixed
  - Log truncation bug for very large CI job output (#38)
  ```
- On release, move `[Unreleased]` entries under the version heading with the release date.

### 4.3 Pull Request Description
- Every PR must include:
  ```markdown
  ## Summary
  Brief description of what this PR does and why.

  ## Changes
  - Bullet list of specific changes made.

  ## Related Ticket
  Closes #<ticket-id>

  ## Testing
  Describe how this was tested (automated + manual).

  ## Example Invocations (if protocol change)
  Include sample MCP tool/resource calls or transcript snippets.

  ## Checklist
  - [ ] Tests pass locally
  - [ ] Linting passes
  - [ ] CHANGELOG updated
  - [ ] Documentation updated (if applicable)
  ```
