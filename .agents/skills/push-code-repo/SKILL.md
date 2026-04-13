---
name: push-code-repo
description: Push committed code to the remote repository safely, including branch checks, remote verification, secret-awareness, and upstream setup. Use when an agent needs to publish local commits to `origin`, push a feature or fix branch, or confirm the correct git push command before opening a pull request.
---

# Push Code to Repo

Follow these steps while consulting `.agents/rules/devops.md` and the git conventions in `agents.md`.

## 1. Verify the Local State
- Run `git status --short` and confirm the working tree is in the expected state.
- Run `git branch --show-current` and confirm the branch name follows repo conventions such as `feature/<ticket>-<description>`, `fix/<ticket>-<description>`, or `chore/<description>`.
- Run `git remote -v` and confirm the correct remote exists.

## 2. Check Push Safety
- Confirm the branch is not an unintended direct push to `main` or `develop` unless the task explicitly requires it.
- Confirm secrets, tokens, and `.env` files are not being pushed.
- If the push is tied to a feature or fix, make sure the relevant linting or tests have been run when practical.

## 3. Confirm Commits
- Run `git log --oneline -n 5` to verify the commits that will be published.
- If changes are not committed yet, stop and commit first using the repo's Conventional Commit rules.

## 4. Push the Branch
- If the branch has no upstream yet, use:

```bash
git push -u origin <current-branch>
```

- If the upstream already exists, use:

```bash
git push
```

## 5. Verify the Result
- Confirm the push completed without rejected updates.
- If the push was rejected because the remote moved ahead, fetch and reconcile before pushing again.
- If the branch is intended for review, capture the branch name so a pull request can be opened next.

## 6. Common Guardrails
- Do not force-push unless the user explicitly asks for it.
- Do not push unfinished or unrelated work on the same branch.
- Do not push generated secrets, local config, or temporary files.
- Prefer pushing the current feature branch rather than a detached HEAD state.

## 7. Quick Checklist
- [ ] Correct branch selected
- [ ] Remote verified
- [ ] Intended commits reviewed
- [ ] No secrets or local-only files included
- [ ] Upstream set if needed
- [ ] Push completed successfully
