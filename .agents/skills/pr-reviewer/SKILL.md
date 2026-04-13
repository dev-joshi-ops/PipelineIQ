---
name: pr-reviewer
description: Review pull requests and local code changes against the repository's MCP architecture, CI/CD domain rules, security constraints, testing standards, and protocol correctness. Use before approving a PR, when auditing a diff, or when preparing structured review feedback for changed files.
---

# PR Reviewer

## Steps

### 1. Understand the Change
- Read the PR title, description, and linked ticket.
- Understand what changed and why before looking at code.
- Ask whether the PR does one thing or mixes concerns.

### 2. Architecture and Design Review
Consult `.agents/rules/architect.md`:
- [ ] Does the change follow the existing project structure?
- [ ] Are new files in the correct directories per the canonical folder structure?
- [ ] Are protocol bootstrap, handlers, and external integrations kept in separate layers?
- [ ] Are new dependencies justified?
- [ ] Does the change introduce tight coupling between protocol code and provider-specific logic?

### 3. MCP Builder Review
Consult `.agents/rules/mcp-builder.md`:
- [ ] Are tool and resource inputs strongly typed?
- [ ] Are outputs JSON-serializable and deterministic?
- [ ] Does the implementation use the SDK's native patterns rather than ad hoc JSON-RPC code?
- [ ] Is `stdio` still the default unless a remote transport is explicitly required?
- [ ] Are large logs or payloads bounded, paginated, truncated, or summarized intentionally?

### 4. CI/CD Domain Review
Consult `.agents/rules/cicd-expert.md`:
- [ ] Are Jenkins and GitHub Actions concepts modeled correctly?
- [ ] Are failure classifications tied to observable evidence in logs or metadata?
- [ ] Are confidence levels or caveats included when diagnosis is heuristic?
- [ ] Are line references, step names, or job identifiers preserved where useful?

### 5. Security Review
Consult `.agents/rules/security.md`:
- [ ] Are there no hardcoded secrets, tokens, or API keys?
- [ ] Are provider tokens scoped and handled with least privilege?
- [ ] Are outbound requests constrained with safe hosts, TLS verification, and timeouts?
- [ ] Is sensitive data excluded from logs and tool outputs?
- [ ] Are potentially dangerous capabilities avoided unless explicitly required?

### 6. Testing Review
Consult `.agents/rules/qa.md`:
- [ ] Does new code have corresponding tests?
- [ ] Do tests cover error cases and edge conditions, not just happy paths?
- [ ] Are fixtures realistic and scrubbed of secrets?
- [ ] Do integration tests exercise MCP behavior rather than only helper internals?
- [ ] Are tests independent of execution order and live provider state?

### 7. Code Quality
- [ ] Is dead code removed, including commented-out blocks and unused imports?
- [ ] Are `console.log()` and `print()` statements absent?
- [ ] Are TODO or FIXME notes linked to a ticket?
- [ ] Are names descriptive?
- [ ] Do comments explain why rather than what?

### 8. Provide Feedback
Categorize comments as:
- `Blocker`: Must fix before merge.
- `Suggestion`: Should fix, but not a merge blocker.
- `Nit`: Optional stylistic preference. Prefix with `nit:`.
- `Question`: Clarification request rather than change request.

### 9. Final Decision
- Approve when blockers are resolved and the change meets the repo standards.
- Request changes when blockers remain.
- Comment when more context is needed before deciding.
