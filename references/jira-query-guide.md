# Jira Query Guide

These generic JQL examples use `YOUR_PROJECT_KEY`; replace it with a project key from your Jira workspace.

Active sprint:

```text
project in (YOUR_PROJECT_KEY) AND sprint in openSprints() ORDER BY Rank ASC
```

Future sprint candidates:

```text
project in (YOUR_PROJECT_KEY) AND statusCategory != Done AND sprint is EMPTY ORDER BY priority DESC, created ASC
```

Backlog triage:

```text
project in (YOUR_PROJECT_KEY) AND statusCategory != Done AND sprint is EMPTY ORDER BY priority DESC, updated ASC
```

Unassigned work:

```text
project in (YOUR_PROJECT_KEY) AND assignee is EMPTY AND statusCategory != Done ORDER BY priority DESC, updated ASC
```

Stale work:

```text
project in (YOUR_PROJECT_KEY) AND statusCategory != Done AND updated <= -3d ORDER BY updated ASC
```

Delivery risk:

```text
project in (YOUR_PROJECT_KEY) AND statusCategory != Done AND (assignee is EMPTY OR updated <= -3d OR status in ("Blocked", "On Hold", "In Review", "Testing")) ORDER BY priority DESC, updated ASC
```

Workload balance:

```text
project in (YOUR_PROJECT_KEY) AND sprint in openSprints() AND statusCategory != Done ORDER BY assignee ASC, priority DESC
```

Daily pulse:

```text
project in (YOUR_PROJECT_KEY) AND sprint in openSprints() AND updated >= -1d ORDER BY updated DESC
```

Retro review:

```text
project in (YOUR_PROJECT_KEY) AND sprint in closedSprints() ORDER BY updated DESC
```

Suggested fields:

```text
summary,status,assignee,priority,components,labels,updated,created,duedate
```

Use `*all` only when a custom field is required and the field ID is unknown.
