# Security Rules

## 1. Threat Model
- Evaluate changes against common risks for MCP servers and CI/CD integrations:
  1. Secret exposure
  2. Over-scoped provider tokens
  3. SSRF and unsafe outbound requests
  4. Log-based data leakage
  5. Dependency compromise
  6. Unsafe parsing of untrusted pipeline output
  7. Overly permissive tool capabilities
  8. Inadequate auditability of failures

## 2. Credentials and Authorization
- Never store plaintext tokens, API keys, or secrets in code, fixtures, examples, or committed docs.
- Use least-privilege credentials for GitHub and Jenkins. Read-only tokens are preferred for debugging workflows.
- Validate required credentials early and fail with clear, sanitized errors.
- Do not build write-capable provider actions unless the requirement is explicit and approved.

## 3. Input Validation
- Validate all protocol-facing inputs before making network calls.
- Constrain user-controlled fields such as URLs, regexes, file paths, page sizes, and timeouts.
- Treat logs and workflow metadata as untrusted input.
- Never interpolate user input into shell commands or unsafe subprocess calls.

## 4. Outbound HTTP Safety
- Use HTTPS by default and keep certificate verification enabled.
- Allowlist provider hosts where practical. Do not permit arbitrary outbound URLs without an ADR.
- Set explicit timeouts, redirect limits, and payload size limits on all outbound clients.
- Defend against SSRF when accepting URLs or instance identifiers from callers.

## 5. Dependency Scanning
- Run `pip-audit` in CI to detect known vulnerabilities in Python packages.
- Use Dependabot or Renovate for automated dependency update PRs where possible.
- Review changelogs and privilege implications before merging dependency updates.

## 6. Secrets Management
- Use `.env` files only for local development and keep them out of version control.
- In CI, use encrypted secrets.
- In deployed environments, use a secrets manager or equivalent secure configuration channel.
- Rotate secrets on a defined schedule and immediately after suspected exposure.

## 7. Logging and Redaction
- **Never log:** tokens, authorization headers, cookies, full provider URLs with embedded credentials, or sensitive pipeline variables.
- Redact known secret patterns in logs before returning tool output to clients when feasible.
- Keep log excerpts bounded and purposeful. Prefer summaries over dumping entire sensitive payloads.
- Record enough context to debug failures without exposing confidential build data.

## 8. Incident Response
- Define an incident response runbook: detect → contain → eradicate → recover → post-mortem.
- If a token or secret may have leaked, revoke it first and investigate second.
- If an outbound integration is behaving unsafely, disable the affected tool path until the issue is understood.
