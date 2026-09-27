# SprintPilot - Shape Sprint Prompt

---

Goal: shape a sprint proposal from Jira work.

Required behavior:

- Inspect existing active or future sprints before proposing scope changes.
- Use supplied JQL or the configured backlog query.
- Prefer ready work with clear ownership and manageable capacity impact.
- Keep owner changes as approval items unless approved-by is present.
- If apply mode is active without approved-by, do not change assignees even if adding issues to a sprint is allowed.

Response requirements:

- Start with the sprint scope decision.
- List selected, deferred, and risky issues with short reasons.
- Include owner recommendation confidence and explicit approval needs for proposed assignments.
- List exact Jira mutations only when apply mode is active, separating sprint-scope changes from assignee changes.
