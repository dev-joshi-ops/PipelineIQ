# DevOps & SRE Rules

## 1. Build and Packaging
- Treat the repository as a Python package first. Keep packaging metadata in `pyproject.toml`.
- CI must validate installability from a clean checkout.
- Build immutable artifacts for releases: at minimum an sdist and wheel. Add a container image only when deployment requires one.
- If a container is used, pin the base image version and run as a non-root user.

## 2. Local Development
- Prefer a simple local workflow: virtual environment, editable install, and direct server execution.
- Document one command path for linting, one for tests, and one for launching the MCP server locally.
- Introduce Docker only when it materially improves reproducibility or deployment parity.

## 3. Environment Strategy
| Environment | Branch | Purpose |
|---|---|---|
| `local` | any | Developer workstation and fixture-driven testing |
| `dev` | `develop` or feature branches | Shared validation of packaging, configuration, and integrations |
| `staging` | `release/*` | Pre-production verification with representative credentials and provider access |
| `production` | `main` | Published package or deployed runtime |

- Environment-specific config lives in `.env.<environment>` files or a secrets manager. Commit only `.env.example`.

## 4. CI/CD Automation
- **On Pull Request:** `ruff` → `pytest` → package build → security scan.
- **On Merge to `develop`:** All PR checks plus optional publish to an internal test environment.
- **On Merge to `main`:** All checks plus release packaging and any gated production deployment.
- Fail fast on lint failures, test failures, packaging failures, or critical vulnerabilities.
- Cache Python dependencies carefully, but never let stale caches hide missing dependency declarations.

## 5. Secrets Management
- Never store secrets in code, package metadata, workflow files, or test fixtures.
- Use GitHub Actions secrets for CI and a runtime secrets manager for deployed environments.
- Use least-privilege tokens for GitHub and Jenkins integrations.
- Rotate secrets on a defined schedule and revoke them immediately after suspected exposure.

## 6. Monitoring and Alerting
- Capture structured logs for server startup, tool failures, and outbound provider errors.
- Track basic SLOs such as server startup success, tool latency p95, provider error rate, and timeout rate.
- Alert on sustained authentication failures, repeated provider throttling, and sudden spikes in log-analysis failures.
- Every production incident should produce a blameless post-mortem.

## 7. Rollback Strategy
- Keep the previous few release artifacts available for quick rollback.
- Make rollback steps explicit for both package releases and any deployed runtime.
- If configuration changes accompany a release, version them and roll them back with the code.

## 8. Infrastructure as Code (IaC)
- Use IaC for any persistent deployment infrastructure.
- Review infrastructure changes in pull requests before apply.
- Keep runtime configuration, secrets references, and networking rules out of ad hoc manual steps.
