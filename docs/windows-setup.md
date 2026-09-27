# Windows setup

Requirements: Windows 10/11, PowerShell 5.1 or PowerShell 7, Python 3 with the `py` launcher, Codex CLI, and a separately configured Atlassian/Jira MCP server. WSL is not required; Git Bash is optional if using the Bash compatibility scripts.

From the repository root:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Or run `scripts/setup.ps1` from the repository root. It creates the project-local environment and installs only the declared dependency into it. Configure Codex CLI and Jira MCP in your environment, copy the example team map to `references/team-map.local.yaml`, then run `scripts/validate-sprintpilot.ps1`.

Run workflows as `scripts/sprintpilot.ps1 -Mode triage-queue`. Use `Get-Help .\scripts\sprintpilot.ps1 -Detailed` for the PowerShell parameters. Windows Task Scheduler can run the entry point for scheduled jobs.

Generated Markdown reports are UTF-8. In Windows PowerShell 5.1, display a report with `Get-Content -Raw -Encoding UTF8 automation/output/<report-name>.md` to avoid legacy console decoding.
