---
description: Document an Architecture Decision Record (ADR) for significant technical decisions
---

# Write ADR Workflow

## When to Use
Document a decision when:
- Choosing between multiple technical approaches
- Introducing a new dependency, tool, or service
- Changing a fundamental design pattern
- Making a trade-off that future developers need to understand

> **Rule of thumb:** If someone might later ask "why did we do it this way?", write an ADR.

## Steps

### 1. Create the ADR File
```bash
mkdir -p docs/adrs
```
Naming convention: `NNNN-<short-title>.md` (zero-padded number + kebab-case title).
```
docs/adrs/
├── 0001-use-antigravity-sdk-for-mcp-server.md
├── 0002-default-to-stdio-transport.md
└── 0003-use-read-only-provider-tokens.md
```

### 2. Fill in the Template
```markdown
# ADR-NNNN: <Title>

## Status
<!-- One of: Proposed | Accepted | Deprecated | Superseded by ADR-XXXX -->
Proposed

## Date
YYYY-MM-DD

## Context
<!-- What is the issue? Why does this decision need to be made?
     Include relevant constraints, requirements, and forces at play. -->


## Options Considered

### Option A: <Name>
- **Pros:** ...
- **Cons:** ...

### Option B: <Name>
- **Pros:** ...
- **Cons:** ...

### Option C: <Name> (if applicable)
- **Pros:** ...
- **Cons:** ...

## Decision
<!-- Which option was chosen and why?
     Be specific about the reasoning. -->


## Consequences

### Positive
- ...

### Negative
- ...

### Risks
- ...

## References
- [Link to relevant documentation]
- [Link to spike/prototype if applicable]
- [Link to team discussion thread]
```

### 3. Review Process
- Share the ADR with the team for review.
- For **Proposed** ADRs: collect feedback, update, then change status to **Accepted**.
- ADRs are **immutable** once accepted. If a decision is reversed, create a new ADR that **supersedes** the old one.

### 4. Keep the Index Updated
Maintain a summary in `docs/adrs/README.md`:
```markdown
# Architecture Decision Records

| ADR | Title | Status | Date |
|---|---|---|---|
| 0001 | Use Antigravity SDK for MCP server | Accepted | 2026-03-15 |
| 0002 | Default to stdio transport | Accepted | 2026-03-20 |
| 0003 | Use read-only provider tokens by default | Proposed | 2026-04-01 |
```

### 5. ADR Quality Checklist
- [ ] Title clearly describes the decision (not the problem)
- [ ] Context explains **why** the decision was needed
- [ ] At least 2 options were considered with pros/cons
- [ ] Decision clearly states **what** was chosen and **why**
- [ ] Consequences include both positive and negative impacts
- [ ] References link to supporting materials
- [ ] Status is set correctly
- [ ] ADR index is updated

---

## Examples of Good ADR Titles
- ✅ "Use Antigravity SDK instead of handwritten JSON-RPC plumbing"
- ✅ "Default to stdio transport for local and desktop MCP clients"
- ✅ "Use read-only GitHub and Jenkins credentials by default"
- ❌ "Database decision" (too vague)
- ❌ "We need to pick a queue" (describes the problem, not the decision)
