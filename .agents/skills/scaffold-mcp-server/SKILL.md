---
name: scaffold-mcp-server
description: Create or extend an MCP server using the Python antigravity SDK, including typed schemas, stdio-first transport, provider adapters, and tests. Use when adding or updating MCP tools, resources, prompts, server bootstrap, or CI/CD debugging integrations.
---

# Scaffold MCP Server

Follow these steps while consulting `.agents/rules/mcp-builder.md`, `.agents/rules/cicd-expert.md`, `.agents/rules/security.md`, and `.agents/rules/qa.md`.

## 1. Model the Contract
- Create typed input and output models in `src/pipeline_iq/schemas/`.
- Constrain large or risky inputs such as log length, page size, regex patterns, and timeouts.
- Prefer explicit model names that map cleanly to tool intent.

## 2. Implement the Server
- Register tools, resources, or prompts using the current Antigravity SDK API for the pinned version.
- Keep server bootstrap in `src/pipeline_iq/server.py`.
- Default to `stdio`; add SSE only when explicitly requested.

## 3. Isolate Integrations
- Put Jenkins and GitHub Actions clients in `src/pipeline_iq/integrations/`.
- Keep handlers thin and deterministic.
- Normalize provider payloads before exposing them through MCP-facing contracts.

## 4. Add Tests
- Unit: schema validation, parsing, heuristics, truncation, and redaction.
- Integration: tool or resource invocation through the MCP server or SDK harness.
- Fixtures: sample Jenkins and GitHub Actions payloads under `tests/fixtures/`.

## 5. Checklist
- [ ] Typed schemas added for all new protocol-facing inputs and outputs
- [ ] Tool, resource, or prompt registered through the SDK
- [ ] `stdio` remains the default transport unless a different requirement was explicit
- [ ] Provider integration isolated from protocol bootstrap
- [ ] Unit and integration tests added with realistic scrubbed fixtures
