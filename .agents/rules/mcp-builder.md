# MCP Builder Rules

## 1. Primary Responsibility
- Build MCP servers, tools, resources, and prompts using the Python `antigravity` SDK.
- Prefer SDK-native abstractions over handwritten JSON-RPC plumbing.

## 2. Project Shape
- Entry point: `src/pipeline_iq/server.py`.
- External clients: `src/pipeline_iq/integrations/`.
- Protocol-facing models: `src/pipeline_iq/schemas/`.
- Tool handlers: `src/pipeline_iq/tools/`.
- Resource handlers: `src/pipeline_iq/resources/`.

## 3. Tool and Resource Design
- Every tool input should be represented by a typed Python model.
- Every output must be deterministic and JSON-serializable.
- Use explicit field descriptions, enums, bounds, and patterns where supported.
- Prefer narrow, composable tools over one large multi-purpose tool.
- Treat large logs as bounded data: support truncation, windows, pagination, or summaries.

## 4. Transport
- Default to `stdio` for local development and desktop clients.
- Add SSE only when explicitly required by a client integration.
- Keep transport bootstrap isolated from business logic and integrations.

## 5. Protocol Correctness
- Preserve JSON-RPC 2.0 compatibility through the SDK.
- Do not invent ad hoc request or response envelopes outside the SDK conventions.
- Validate all incoming parameters before making network calls.
- Return structured, actionable errors.

## 6. Testing
- Add unit tests for schema validation and parsing logic.
- Add integration tests that exercise tool invocation through the server or SDK harness.
- Use recorded Jenkins and GitHub Actions fixtures. Never depend on live CI services in CI.
