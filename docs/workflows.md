# The nine workflows

| Mode | Purpose | Can change Jira with `-Apply` |
|---|---|:---:|
| `shape-sprint` | Propose sprint scope from the backlog or board, favouring ready and owned work. | Yes |
| `triage-queue` | Classify backlog items: ready, unclear, blocked, duplicate, owner-needed, sprint-candidate. | Yes |
| `suggest-owner` | Recommend an assignee per issue, scored by ownership signals, load, capacity, history and risk. | Yes |
| `balance-load` | Find overloaded people and propose safe reassignments. | Yes |
| `inspect-sprint` | Review sprint health: blocked, stale, unassigned, overdue, review- and test-stuck work. | No |
| `surface-risk` | List only delivery threats, with impact, likely cause, owner and next action. | No |
| `progress-pulse` | Short status snapshot with movement since the previous snapshot. | No |
| `standup-brief` | Daily summary: moved work, blockers, stale tickets, decisions needed. | No |
| `retro-notes` | Retrospective inputs from sprint patterns. | No |

Assignee-changing modes always require `-ApprovedBy` matching a configured assigning authority; unapproved recommendations are listed under *Assignment Approval Items* as `PENDING APPROVAL`. Prompt templates live in [`automation/prompts/`](../automation/prompts).
