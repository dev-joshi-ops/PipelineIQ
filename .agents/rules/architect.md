# Systems Architect Rules

## 1. Design Principles
- Keep the MCP transport layer thin. Put protocol bootstrap in `server.py`, handler logic in `tools/` or `resources/`, and provider-specific I/O in `integrations/`.
- Prefer small, composable tools over one tool with many optional branches.
- Design for deterministic outputs. The same inputs should produce materially equivalent structured results.
- Follow twelve-factor principles for configuration, packaging, and process management.

## 2. Contract Design
- Treat MCP tool and resource schemas as first-class contracts.
- Define typed request and response models before writing handler logic.
- Use explicit field names, enums, bounds, and descriptions for any protocol-facing shape.
- Keep backward compatibility in mind for tool names, resource URIs, and response fields once they are published to clients.

## 3. Architecture Decision Records (ADRs)
- Any significant architectural decision **must** be documented as an ADR.
- Store ADRs in `docs/adrs/` using the format: `NNNN-title.md`.
- ADR format:
  - **Status:** Proposed / Accepted / Deprecated / Superseded
  - **Context:** Why is this decision needed?
  - **Decision:** What was decided?
  - **Consequences:** What are the trade-offs?

## 4. Transport and Integration Boundaries
- Default to `stdio` unless a client requires remote transport.
- Add SSE only when explicitly justified by deployment or client interoperability needs.
- Do not hand-roll raw JSON-RPC behavior if the pinned `antigravity` SDK already supports the needed pattern.
- Keep Jenkins and GitHub Actions adapters isolated from protocol concerns.

## 5. Resilience and Large Payload Strategy
- CI logs are unbounded inputs. Design truncation, chunking, pagination, and summarization intentionally.
- Apply strict timeouts, retries, and failure classification around outbound HTTP calls.
- Prefer graceful degradation: if one provider is unavailable, unaffected tools should still function.
- Document provider limits such as pagination, artifact size, rate limits, and retention windows.

## 6. Observability
- Use structured logs at provider and protocol boundaries.
- Include correlation fields where available, such as workflow run ID, job ID, build number, and request ID.
- Emit enough context to diagnose failures without logging secrets or full sensitive payloads.
- Define health and smoke-test strategy for the runtime, even if the primary transport is `stdio`.

## 7. Documentation
- Maintain a living architecture overview for the MCP server and provider integrations.
- Update diagrams or sequence notes when adding a new transport, provider, or major tool family.
- Include example invocation transcripts when a tool contract changes in a non-obvious way.
