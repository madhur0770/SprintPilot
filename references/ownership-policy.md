# Ownership Policy

Use this file when a mode produces Jira owner recommendations, changes sprint scope, balances workload, or reviews delivery risk.

## Owner Score

Score each possible owner and show the best candidate plus close alternatives. This score is a recommendation signal, not approval to change Jira.

Positive signals:

- `+4` component ownership
- `+3` label or feature-area ownership
- `+3` skill match
- `+2` recent similar work
- `+2` existing watcher, reviewer, commit, branch, or PR activity
- `+1` backup owner

Negative signals:

- `-5` not in assignment allowlist
- `-4` unavailable in the sprint window
- `-4` at or above WIP limit
- `-3` above sprint capacity
- `-3` move outside the configured ownership map without a routing rule
- `-2` blocked issue where proposed owner cannot clear the blocker
- `-2` weak issue description or missing acceptance criteria

Confidence:

- `high`: score `6+` and no hard blocker
- `medium`: score `3-5` or one soft risk
- `low`: score below `3`, missing routing data, or several close candidates

## Sprint Readiness Score

Positive signals:

- `+4` high priority or release-critical
- `+3` clear owner with medium or high confidence
- `+2` defined acceptance criteria
- `+2` dependencies are clear or unblocked
- `+1` stale but still relevant customer or release need

Negative signals:

- `-5` blocked
- `-4` no safe owner
- `-3` missing description or acceptance criteria
- `-3` unclear dependency
- `-2` too large for remaining capacity

## Approval Checkpoint

Owner recommendations are allowed in dry-run. Assignee changes require explicit human approval.

- Without `approved-by`, owner recommendations that would change Jira are always `PENDING APPROVAL`.
- With `approved-by`, apply only medium or high confidence changes with no hard blocker.
- Low-confidence, outside-map, or capacity-breaking changes need explicit issue-to-owner approval.
- Record applied approvals in the automation output and approval log when the runner supplies approval metadata.

## Approval Item

Use this shape for pending items:

```text
PENDING APPROVAL: ISSUE-123
Current owner: Example User (fictional)
Proposed owner: Example Teammate (fictional)
Confidence: medium
Reason: component match, matching skill, capacity available
Risk: acceptance criteria needs cleanup
Authority needed: configured assigning authority
```

Use this shape after approval:

```text
APPROVED: ISSUE-123
Approved by: Example Authority (fictional)
Applied: assignee changed to Example Teammate (fictional)
Reason: strong component ownership and available WIP
```
