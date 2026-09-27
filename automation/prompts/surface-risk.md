# SprintPilot - Surface Risk Prompt

---

Goal: surface Jira delivery risks that threaten sprint or release commitments.

Required behavior:

- Prioritize blocked, stale, overdue, unassigned, dependency-heavy, reopened, or review-stuck issues.
- Explain impact and likely cause.
- Recommend the next action and owner; changing the owner requires explicit human approval.
- Keep owner changes under approval rules.
- In apply mode, do not perform assignee changes unless approved-by is present.

Response requirements:

- Start with top risks.
- Order findings by severity.
- Include impact, owner/proposed owner, and next action.
- End with decisions needed.
