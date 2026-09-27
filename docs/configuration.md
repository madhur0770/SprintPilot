# Configuration

Copy `references/team-map.example.yaml` to `references/team-map.local.yaml` and replace placeholders with identifiers and workflow settings from your own Jira workspace. Do not commit the local file; it is ignored by Git.

Configure board ID, project keys, JQL, workflow statuses, team capacity and WIP limits, and assigning authorities. Example names and emails are fictional documentation placeholders. The runner accepts workflow scope through options and `SPRINT_ASSIGNER_*` environment variables; inspect `scripts/sprintpilot.ps1` and `automation/run-sprintpilot.sh` for the supported names.

Configure Codex CLI authentication and the Atlassian/Jira MCP server separately in your own environment. Do not place passwords, tokens, or private Jira URLs in this repository. See [Windows setup](windows-setup.md) for local Python setup.
