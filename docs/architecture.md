# Architecture

SprintPilot is a local prompt assembly and orchestration layer. Its PowerShell entry point (`scripts/sprintpilot.ps1`) is the primary Windows interface. The Bash runner in `automation/` remains available for compatible shells.

Each invocation selects one of nine Markdown prompt templates. The runner adds `SKILL.md`, the Jira query guide, ownership policy, optional local team map, previous progress snapshot, and operator context, then sends the assembled text to `codex exec`. Codex is expected to use an Atlassian/Jira MCP server configured outside this repository. The runner writes the final assistant response to `automation/output/`.

The repository contains no Jira HTTP client, SDK, MCP server implementation, or credentials. Approval-authority validation parses the local team map with PyYAML before supported apply runs.
