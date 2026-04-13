---
name: security-scanner
description: Audit dependencies, secrets handling, token scope, outbound request safety, log redaction, and operational security controls for an MCP server. Use before releases, after provider-integration changes, or when investigating elevated security risk.
---

# Security Scanner

## Steps

### 1. Dependency Vulnerability Scan

```bash
pip install pip-audit
pip-audit --desc
```

- Fix critical and high severity findings immediately.
- Create tickets for medium and low severity findings.

### 2. Secrets Scan
Check for accidentally committed secrets:

```bash
trufflehog git file://. --only-verified
# or
gitleaks detect --source . --verbose
```

- [ ] No API keys, tokens, or passwords in source code
- [ ] No secrets in CI config, examples, or fixtures
- [ ] `.env` files are listed in `.gitignore`
- [ ] `.env.example` files contain only placeholder values

### 3. Credential and Authorization Review
Consult `.agents/rules/security.md`:
- [ ] Provider tokens are read-only unless write access is required
- [ ] Tokens are scoped to the minimum set of repositories, jobs, or endpoints needed
- [ ] Missing credentials fail fast with sanitized errors
- [ ] No provider credential is echoed in logs or returned tool output
- [ ] Configuration docs do not encourage over-privileged tokens

### 4. Input Validation Review
- [ ] Tool inputs are validated before outbound requests are made
- [ ] URL, host, timeout, regex, and paging inputs are constrained
- [ ] User input is not used directly in shell commands or unsafe subprocess calls
- [ ] Large log payloads have explicit size handling
- [ ] Malformed provider payloads fail safely

### 5. Outbound HTTP Safety Review
- [ ] TLS verification is enabled
- [ ] Safe host allowlists or equivalent controls exist where practical
- [ ] Redirect behavior is constrained
- [ ] Timeouts are explicit
- [ ] Provider retries will not create uncontrolled retry storms

### 6. Logging and Monitoring Review
- [ ] Sensitive tokens and headers are redacted
- [ ] Returned log excerpts are bounded
- [ ] Sensitive data is excluded from logs
- [ ] Logs include request IDs
- [ ] Alerting exists for provider auth failures and suspicious error spikes

### 7. Document Findings
Create a security audit report:

```markdown
## Security Audit - <Date>

### Summary
- Dependencies: X critical, Y high, Z medium
- Secrets scan: clean/found issues
- Credential review: pass/found issues

### Findings
| # | Severity | Category | Finding | Remediation | Status |
|---|---|---|---|---|---|
| 1 | Critical | Dependencies | Vulnerable package version | Upgrade package | Open |
| 2 | High | Token Scope | GitHub token has broader access than required | Reduce scopes to read-only | Open |

### Action Items
- [ ] Fix all critical findings before release
- [ ] Create tickets for high and medium findings
- [ ] Schedule a re-audit after fixes ship
```

### 8. Incident Response Reminder
If a vulnerability is actively exploited:
1. Contain the issue by disabling the affected path or revoking credentials.
2. Notify the team lead and security owner.
3. Apply the hotfix.
4. Recover data or service integrity if needed.
5. Document the post-mortem and prevention steps.
