# .agents - AI Agent Suite

This directory contains the AI persona rules, specialized skills, and workflows that govern how AI assistants interact with this codebase.

> **Start here:** Read `../agents.md` for the global agent routing definitions that determine which Antigravity handle and rule file to use for each task.

## Personas (`rules/`)

| File | Role | When to Use |
|---|---|---|
| `orchestrator.md` | Lead Orchestrator | Triaging incoming work, selecting specialist agents, reconciling cross-domain guidance |
| `mcp-builder.md` | MCP Server Developer | Building or extending MCP tools, resources, prompts, transports, and typed protocol contracts |
| `cicd-expert.md` | CI/CD Debugging Specialist | Analyzing Jenkins or GitHub Actions behavior, logs, workflow failures, and remediation paths |
| `architect.md` | Systems Architect | Making architectural decisions, designing system boundaries, ADRs |
| `security.md` | Security Engineer | Token handling, dependency risk, outbound request hardening, secret redaction, least privilege |
| `devops.md` | DevOps / SRE | Packaging, CI automation, release discipline, runtime operations, observability |
| `qa.md` | QA Engineer | Unit and integration testing for MCP tools, fixtures, protocol correctness, regression prevention |
| `ba.md` | Business Analyst | Defining tool contracts, acceptance criteria, supported scenarios, and failure expectations |
| `pm.md` | Project Manager | Task breakdown, release readiness, dependency tracking, and delivery risk management |

## Skills (`skills/`)

| Capability | Purpose |
|---|---|
| `security-scanner` | Audit dependency risk, secret handling, outbound HTTP safety, token scope, and log redaction |
| `performance-profiler` | Profile MCP startup, tool latency, provider calls, and large-log handling with actionable findings |
| `pr-reviewer` | Review MCP server changes against architecture, protocol correctness, CI/CD domain rules, and tests |
| `scaffold-mcp-server` | Generate or extend an Antigravity-based MCP server with typed schemas, handlers, integrations, and tests |
| `push-code-repo` | Push committed code to the correct remote branch with git safety checks |
| `codebase-scout` | Build a clean mental model of the package layout, entrypoints, contracts, and release shape |

Agents that do not auto-discover skills should read `.agents/skills/registry.yaml` to map tasks to the correct skill file.

## Workflows (`workflows/`)

### Development
| File | Purpose |
|---|---|
| `setup-local.md` | Bootstrap the local Python environment and run the MCP server locally |
| `create-feature.md` | End-to-end MCP feature development from branch creation to PR merge |
| `fix-bug.md` | Structured debugging with reproduce-first approach and regression tests |
| `refactor.md` | Safe refactoring with test-guarded verification |
| `add-third-party-api.md` | Integrate Jenkins, GitHub, or other external APIs with retries, timeouts, redaction, and tests |
| `write-adr.md` | Document Architecture Decision Records for significant technical choices |
| `run-tests.md` | Run linting, unit tests, integration tests, and package validation for the MCP server |

### Operations
| File | Purpose |
|---|---|
| `deploy-production.md` | Step-by-step package or runtime deployment with smoke validation and rollback planning |
| `hotfix.md` | Emergency production hotfix with fast-track review process |

### Team
| File | Purpose |
|---|---|
| `onboard-developer.md` | New team member onboarding from clone to first merged PR for this Python package |

## How to Use

1. **AI assistants** automatically consult the agent routing definitions in `agents.md` to select the right Antigravity handle and governing rule file.
2. **Skills** define self-contained capabilities for the AI (for example, "Run the `security-scanner` skill" or "Use `scaffold-mcp-server`").
3. **Workflows** provide step-by-step guides for common processes - useful for onboarding and consistency.
