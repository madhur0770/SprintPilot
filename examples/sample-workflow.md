# Offline demo workflow (fictional)

This runnable example uses sanitized, synthetic sprint data only. Every project, issue, person, and work item in `demo-sprint.yaml` is fictional. It does not connect to Jira.

Run the native Windows PowerShell demo from the repository directory:

```powershell
.\scripts\demo-sprintpilot.ps1
```

No team map, account, credentials, installation, Codex, Jira, MCP, Python, or network access is needed. The script reads `examples/demo-sprint.yaml` and writes the deterministic Markdown report to `automation/output/offline-demo-report.md`.

The report shows the sprint snapshot, issue readiness and status, a meaningful dependency blocker, and suggested next steps. It is a local demonstration only; no Jira changes are made.
