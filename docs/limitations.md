# Limitations

- Output quality depends on the model, prompt, available Jira context, MCP tool behavior, and correctness of local team configuration.
- SprintPilot is not a Jira server, Jira client SDK, or MCP server and does not install or configure those services.
- It does not independently enforce Jira authorization. MCP permissions determine which operations are available.
- The local approval check confirms the supplied approver string matches the configured team map; it is not an identity provider or an external approval workflow.
- Jira issue descriptions and other fetched content are untrusted input. Prompt guidance cannot replace service-level permissions.
- Scheduling, GUI and analytics storage are not included. Automated tests cover the validator and the offline demo; the live agent/MCP path is not covered by automated tests.
- The PowerShell runner targets Windows PowerShell; CI exercises the offline demo on Windows PowerShell 5.1, PowerShell 7 and Linux, but the live runner is only verified on Windows.
