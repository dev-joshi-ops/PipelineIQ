---
description: Emergency production hotfix workflow with fast-track process
---

# Hotfix Workflow

## When to Use
A **critical bug in production** that cannot wait for the next release cycle. Examples:
- Users cannot log in
- Data is being corrupted
- Security vulnerability is actively exploited
- Payment processing is broken

> If the bug is not critical, use the regular `fix-bug.md` workflow instead.

## Steps

### 1. Assess Severity
Before starting the hotfix, confirm:
- [ ] The issue is happening in **production** (not staging or dev)
- [ ] The issue is **critical** (data loss, security, core flow broken)
- [ ] The issue cannot wait for the next regular release
- Notify the team lead / on-call engineer

### 2. Branch from Main
Hotfixes branch from `main` (production), not `develop`:
```bash
git checkout main
git pull origin main
git checkout -b hotfix/<ticket-id>-<short-description>
```

### 3. Reproduce and Fix
- Reproduce the issue locally against production-equivalent data.
- Apply the **minimal fix** — do not refactor, do not fix adjacent issues.
- Write a regression test that captures the bug.

### 4. Test Locally
```bash
# Run the specific test
pytest tests/ -k "test_<regression_test_name>" -v

# Run full suite to check for side effects
pytest tests/ -v
```

### 5. Fast-Track Code Review
- Create PR targeting `main`.
- **Title:** `hotfix(<scope>): <critical issue description>`
- **Labels:** `hotfix`, `critical`
- Tag the reviewer directly — hotfix reviews are top priority.
- Reviewer focuses on: correctness, no side effects, regression test exists.

### 6. Merge and Deploy
```bash
# After approval
git checkout main
git merge hotfix/<ticket-id>-<short-description> --no-ff
git tag -a v<major>.<minor>.<patch+1> -m "Hotfix: <description>"
git push origin main --tags
```
- CI/CD deploys to production.
- Monitor the deployment closely.

### 7. Verify in Production
- [ ] The bug is fixed in production
- [ ] No new errors in logs or monitoring
- [ ] Health check returns 200
- [ ] Affected user flow works correctly

### 8. Backport to Develop
This is **critical** — if you skip this, the next release will reintroduce the bug:
```bash
git checkout develop
git pull origin develop
git merge main --no-ff
git push origin develop
```

### 9. Cleanup
```bash
git branch -d hotfix/<ticket-id>-<short-description>
git push origin --delete hotfix/<ticket-id>-<short-description>
```

### 10. Post-Mortem
For every hotfix, document:
- **What happened?** (timeline of events)
- **What was the root cause?**
- **How was it detected?** (monitoring, user report, etc.)
- **How was it fixed?**
- **What will prevent it from happening again?** (better tests, monitoring, validation)

Store post-mortems in `docs/post-mortems/<date>-<title>.md`.

---

## Hotfix Checklist
- [ ] Severity confirmed: production + critical
- [ ] Team notified
- [ ] Branched from `main` (not `develop`)
- [ ] Minimal fix only — no refactoring
- [ ] Regression test written
- [ ] Full test suite passes
- [ ] Fast-track review completed
- [ ] Deployed to production and verified
- [ ] Backported to `develop`
- [ ] Post-mortem documented
