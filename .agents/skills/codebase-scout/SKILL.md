---
name: codebase-scout
description: Deeply map and understand a new MCP codebase from scratch. Identify the package layout, core architecture flows, entry points, tool and resource contracts, and release process. Use when first entering a repository or exploring an unfamiliar feature area.
---

# Codebase Scout Skill

Use this skill to build a "zero-to-one" mental model of any repository. Always consult `.agents/rules/orchestrator.md` and `.agents/rules/architect.md` during discovery.

## 1. Technology Stack Audit
Identify the core technologies and pinned versions. For this repository:

| Layer | Technology | Version | Key Configuration |
|---|---|---|---|
| **Runtime** | Python | See `agents.md` | `pyproject.toml` |
| **MCP SDK** | `antigravity` | See `agents.md` | `pyproject.toml` |
| **HTTP Client** | `httpx` | See `agents.md` | `pyproject.toml` |
| **Testing** | `pytest` | See `agents.md` | `pyproject.toml` |
| **Package Layout** | `src/` layout | N/A | `src/pipeline_iq/` |

## 2. Core Architecture Flow
Trace a tool call from the MCP client to the provider integration.

### 2.1 The "Tool Invocation Life Cycle"
1. **MCP Client:** A desktop app, IDE, or orchestrator issues a tool or resource request.
2. **Server Bootstrap:** `src/pipeline_iq/server.py` configures and starts the Antigravity server.
3. **Schema Validation:** Input models in `src/pipeline_iq/schemas/` validate and normalize arguments.
4. **Handler Execution:** Tool or resource handlers in `src/pipeline_iq/tools/` or `src/pipeline_iq/resources/` orchestrate the request.
5. **Provider Adapter:** Integrations in `src/pipeline_iq/integrations/` call Jenkins, GitHub Actions, or other services.
6. **Structured Result:** The server returns deterministic JSON-serializable output to the client.

## 3. Key Files & Directories
| Path | Purpose |
|---|---|
| `src/pipeline_iq/server.py` | MCP server bootstrap and registration entry point. |
| `src/pipeline_iq/tools/` | Tool handlers exposed to MCP clients. |
| `src/pipeline_iq/resources/` | Resource handlers and static/dynamic resource definitions. |
| `src/pipeline_iq/integrations/` | External service adapters such as Jenkins and GitHub Actions clients. |
| `src/pipeline_iq/schemas/` | Typed protocol-facing input and output models. |
| `tests/fixtures/` | Recorded CI logs, provider payloads, and regression artifacts. |
| `agents.md` | Global AI directive and persona routing. |
| `.agents/rules/` | Persona-specific rule files. |

## 4. Local Development Guide
Follow these unified steps to get productive:
1. **Environment:** create a virtual environment and install the package in editable mode.
2. **Server:** run the MCP server entry point from `src/pipeline_iq/server.py`.
3. **Testing:** run `pytest` for unit and integration coverage.
4. **Validation:** smoke-test a representative tool invocation against local fixtures.

## 5. Deployment & Release Process
1. **Release Strategy:** Feature branches -> `develop` -> `release/*` -> `main`.
2. **Artifacts:** Build a wheel or other immutable artifact from CI.
3. **Validation:** smoke-test the released server against representative credentials or fixtures.
4. **Rollback:** reinstall the previous release artifact or redeploy the previous runtime image.

## 6. Discovery Checklist
When scouting a new module or feature:
- [ ] List all exposed tools, resources, or prompts.
- [ ] Identify the protocol models that define their contracts.
- [ ] Locate the provider adapter or parsing logic.
- [ ] Check for existing unit and integration tests.
- [ ] Audit for credential handling, redaction, and timeout behavior.
