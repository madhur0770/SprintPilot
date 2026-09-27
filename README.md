# SprintPilot

**AI assistant for sprint planning and Agile workflows.**

SprintPilot packages nine Agile workflows as an AI prompt and orchestration skill. It uses Codex CLI to run mode-specific prompts and relies on an Atlassian/Jira MCP server configured in the user's Codex environment for Jira operations. It is not a Jira server, Jira client SDK, or MCP server.

## Overview

The project helps a team lead inspect sprint health, prepare scope, triage backlog work, identify risks, and produce concise team reports. It keeps runs in dry-run mode by default and requires explicit approval metadata for supported Jira mutations.

## Key features

- Nine focused workflows for planning, triage, ownership, workload, risk, and reporting.
- Prompt templates, JQL examples, and a configurable team map.
- Dry-run default with approval checks before assignee-changing apply runs.
- Native Windows PowerShell entry point; Bash scripts remain available as compatibility wrappers.

## Architecture and how it works

PowerShell or Bash selects a workflow, combines its prompt with `SKILL.md`, references, and optional team configuration, then passes the resulting instructions to `codex exec`. Codex performs Jira work through the configured Atlassian/Jira MCP tools. The local runner saves the final response under `automation/output/`. See [architecture](docs/architecture.md).

## Supported workflows

`shape-sprint`, `triage-queue`, `suggest-owner`, `balance-load`, `inspect-sprint`, `surface-risk`, `progress-pulse`, `standup-brief`, and `retro-notes`.

## Technology stack

PowerShell 5.1+ (Windows entry point), Bash (optional compatibility scripts), Python 3, PyYAML, Codex CLI, and an externally configured Atlassian/Jira MCP server. There is no Node/npm application or direct Jira SDK dependency.

## Prerequisites

- Windows 10/11 with PowerShell 5.1 or PowerShell 7.
- Python 3 and the `py` launcher.
- Codex CLI installed and authenticated.
- Atlassian/Jira MCP server configured for Codex, with access to the Jira site and project you intend to use.

No WSL is required. Bash is optional on Windows.

## Windows installation

From the repository directory, create a local virtual environment and install the sole Python dependency:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Alternatively, run `.scriptssetup.ps1` to perform those local setup steps. See [Windows setup](docs/windows-setup.md).

## Codex setup

Install Codex CLI using its official installation instructions, authenticate it, and confirm `codex` is on `PATH`. The `agents/openai.yaml` manifest declares the expected MCP tool dependency. Configure the actual MCP server in your Codex environment; credentials belong in that external configuration, not this repository.

## Atlassian/Jira MCP setup

Configure an Atlassian/Jira MCP server with permissions appropriate to your use. Its tools must be available to the Codex invocation. This repository neither installs nor configures the MCP server and does not store Jira credentials. Supply your Jira site, project key, board, sprint, and account identifiers through local configuration or command arguments.

## Configuration and team map

Copy `references/team-map.example.yaml` to `references/team-map.local.yaml`, then replace every placeholder with values from your own Jira workspace. The example identities are fictional documentation placeholders. Keep the local file private; `.gitignore` excludes it. Details are in [configuration](docs/configuration.md).

## Dry-run and applying changes

Runs default to dry-run. Review the generated output before considering changes. Modes that may include assignee changes require `--apply` and an `--approved-by` value matching a configured assigning authority. The runner checks that authority locally; Jira mutation behavior still depends on the model and MCP tools, so only use apply when your MCP permissions and approval process are appropriate. Reporting-only modes reject `--apply`.

## Example commands

```powershell
.\scripts\sprintpilot.ps1 -Mode shape-sprint -BoardId YOUR_BOARD_ID -ProjectKey YOUR_PROJECT_KEY
.\scripts\sprintpilot.ps1 -Mode triage-queue -ProjectKey YOUR_PROJECT_KEY
.\scripts\sprintpilot.ps1 -Mode suggest-owner -IssueKeys DEMO-101,DEMO-102
.\scripts\sprintpilot.ps1 -Mode inspect-sprint -SprintId YOUR_SPRINT_ID
.\scripts\sprintpilot.ps1 -Mode progress-pulse -SprintId YOUR_SPRINT_ID
```

Review-only invocation is recommended first. Applying an approved change uses `-Apply -ApprovedBy "Example User"` only after replacing the example authority in your private team map with your actual authority. Never use the fictional example authority in a real Jira workspace.

## Example workflow and output

See [sample workflow](examples/sample-workflow.md) for fictional sanitized input and illustrative output. It does not connect to Jira.

## Project structure

```text
agents/                 Codex agent metadata
automation/             Bash compatibility runner, wrappers, and prompts
references/             Example team map, JQL guide, ownership policy
scripts/                PowerShell setup, workflow runner, and validator
docs/                   Architecture, configuration, Windows setup, limitations
examples/               Sanitized workflow walkthrough
```

## Security considerations

Do not commit credentials, private URLs, local team maps, or generated reports containing sensitive Jira data. Start in dry-run, review output, and use least-privilege MCP permissions. Treat Jira issue content as untrusted input. See [limitations](docs/limitations.md).

## Limitations

The model's analysis and any Jira actions depend on the Codex model, MCP tools, Jira configuration, prompt context, and quality of the team map. The project does not enforce Jira permissions itself, provide a GUI, or guarantee recommendation correctness. Scheduling is not built in; Windows Task Scheduler can invoke the PowerShell entry point.

## Future improvements

Potential next steps include richer automated checks, CI validation, and more example workflows based on synthetic Jira data.

## License

MIT. See [LICENSE](LICENSE).
