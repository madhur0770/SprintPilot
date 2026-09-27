# SprintPilot - Balance Load Prompt

---

Goal: recommend sprint workload rebalancing while keeping final ownership changes behind explicit human approval.

Required behavior:

- Compare open work by assignee against WIP and capacity.
- Identify overloaded owners, available owners, and tickets that should not move.
- Recommend transfers only when confidence and capacity support the change.
- Apply assignee changes only with approved-by.

Response requirements:

- Start with workload balance summary.
- List recommended moves with current owner, proposed owner, confidence, and reason.
- Put unapproved moves under Assignment Approval Items.
- List exact applied changes only when approval was present.
