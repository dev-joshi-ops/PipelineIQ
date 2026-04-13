# Business Analyst (BA) Rules

## 1. User Stories
- Format: **"As a [role], I want to [action], so that [value]."**
- Each story must be **independent, negotiable, valuable, estimable, small, and testable** (INVEST criteria).
- Include sample MCP invocations or transcript snippets when that clarifies the request.

## 2. Acceptance Criteria
- Define criteria using **BDD format** (Given / When / Then):
  ```
  Given the user is logged in
  When they submit an order with a valid payment method
  Then the order status is set to "confirmed"
  And a confirmation email is sent
  ```
- Include criteria for **error states**, not just the success path.
- Each acceptance criterion must be independently verifiable.

## 3. Requirements Template
Every feature document must include:
1. **Summary** — one-paragraph problem statement.
2. **User Stories** — all stories for the feature.
3. **Acceptance Criteria** — BDD for each story.
4. **Non-Functional Requirements** — performance, security, observability, determinism.
5. **Data Requirements** — provider fields, log artifacts, fixture needs, retention or truncation concerns.
6. **Tool / Resource Contract** — MCP tool names or resource URIs, input shape, output shape, error conditions.
7. **Out of Scope** — explicitly state what this feature does NOT cover.

## 4. Non-Functional Requirements (NFR) Checklist
For every feature, explicitly address:
- [ ] **Performance:** Expected response time? Expected concurrent users?
- [ ] **Security:** Does this handle PII? Auth required? Role-based access?
- [ ] **Accessibility:** WCAG 2.1 AA compliance needed?
- [ ] **Scalability:** Will data volume grow significantly?
- [ ] **Localization:** Multi-language or multi-timezone support?

## 5. API Contract Review
- Before development begins, BA must review the proposed MCP contract.
- Validate that field names, tool names, and resource identifiers match the domain language.
- Confirm request and response shapes satisfy the intended client workflows.

## 6. Edge Cases & Constraints
- Define constraints **before** development starts. Examples:
  - Maximum string lengths for each input field.
  - Allowed characters / regex patterns for validated fields.
  - Rate limits for public-facing endpoints.
  - Concurrency scenarios (e.g., two users editing the same resource).

## 7. Sign-Off Process
- BA signs off on **requirements completeness** before sprint starts.
- BA signs off on **acceptance criteria met** during QA review.
- Disputed behavior: the acceptance criteria in the ticket are the source of truth.
