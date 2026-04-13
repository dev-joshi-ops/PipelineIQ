# Project Manager (PM) Rules

## 1. Task Breakdown
- No task should exceed **2 days of effort**. If it does, decompose it further.
- Every task must be a vertical slice — deliverable and demo-able independently.
- Use sub-tasks for technical steps within a story (e.g., "create model", "create endpoint", "write tests").

## 2. Ticket Format
Every ticket must include:
| Field | Required | Description |
|---|---|---|
| Title | ✅ | Short, action-oriented (e.g., "Add Jenkins build log tool") |
| Priority | ✅ | Critical / High / Medium / Low |
| Story Points | ✅ | Fibonacci (1, 2, 3, 5, 8). Anything > 8 must be split. |
| Description | ✅ | Context, requirements, link to user story |
| Acceptance Criteria | ✅ | BDD or checklist format |
| Blockers | ✅ | List any dependencies or blockers (or "None") |
| Labels | ✅ | `mcp`, `cicd`, `security`, `devops`, `bug`, `tech-debt` |

## 3. Sprint Cadence
- **Sprint length:** 2 weeks.
- **Ceremonies:**
  - Sprint Planning (Day 1, 1 hour)
  - Daily Standup (15 min, async-friendly)
  - Sprint Review / Demo (Last day, 30 min)
  - Retrospective (Last day, 30 min)
- **No scope changes** after sprint planning without PM + Tech Lead approval.

## 4. Definition of Done (DoD)
A task is "Done" only when **all** of the following are true:
- [ ] Code is written and passes all linting rules.
- [ ] Unit and integration tests are written and passing.
- [ ] Code is reviewed and approved by at least one peer.
- [ ] Feature is validated in the intended local or shared runtime path.
- [ ] Acceptance criteria are verified by QA or BA.
- [ ] Documentation is updated (README, example invocations, ADRs if applicable).

## 5. Risk Register
- Maintain a living risk register in the project board or wiki.
- Each risk includes: **Description**, **Probability** (High/Med/Low), **Impact** (High/Med/Low), **Mitigation Plan**, **Owner**.
- Review risks at the start of each sprint.

## 6. Status Reporting
- **Weekly status update** to stakeholders:
  - What was completed this week?
  - What is planned for next week?
  - Are there any blockers or risks?
  - Burndown chart / velocity trend.

## 7. Release Checklist
Before every production release:
- [ ] All tickets in the release are in "Done" status.
- [ ] Staging environment passes full regression (automated + manual).
- [ ] Release notes are drafted with user-facing changes.
- [ ] Rollback plan is documented and tested.
- [ ] Stakeholders are notified of the release window.
- [ ] Database migrations are tested against a staging DB copy.
