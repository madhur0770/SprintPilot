# SprintPilot - Inspect Sprint Prompt

---

Goal: inspect sprint health and find issues that need intervention.

Required behavior:

- Focus on blocked, stale, unassigned, overdue, review-stuck, testing-stuck, and near-sprint-end work.
- Pull history or development info only for risky issues.
- Recommend next actions and likely owners, but keep reassignment under explicit human approval rules.
- In apply mode, do not perform assignee changes unless approved-by is present.

Response requirements:

- Start with findings ordered by severity.
- Include issue key, status, owner, risk, and next action.
- Include Assignment Approval Items for ownership changes.
- End with manager/team lead actions.
