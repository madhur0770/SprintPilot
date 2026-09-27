# Sample workflow (fictional)

This example is illustrative only and does not connect to Jira. The project key, issues, names, and work items are fictional.

1. Configure a private team map with a fictional project key such as `DEMO`, sample issues such as `DEMO-101` and `DEMO-102`, and dry-run settings.
2. Run `scripts/sprintpilot.ps1 -Mode triage-queue -ProjectKey DEMO` from PowerShell.
3. Review the generated Markdown report under `automation/output/`.
4. Use the report to clarify acceptance criteria and identify sprint candidates. Keep Jira changes in dry-run until reviewed and explicitly approved.

Illustrative output:

```text
Summary: 2 fictional backlog items reviewed; 1 appears ready and 1 needs clarification.

DEMO-101 — Sprint candidate
Reason: acceptance criteria and ownership are clear in this fictional example.

DEMO-102 — Needs clarification
Reason: dependency and acceptance criteria are unspecified.

Recommended next action: clarify DEMO-102 before sprint commitment.
Mutation mode: dry-run; no Jira changes applied.
```
