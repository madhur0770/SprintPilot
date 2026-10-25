# Security

- Never commit credentials, OAuth tokens, private Jira URLs, `references/team-map.local.yaml`, or generated reports from a real workspace. `.gitignore` excludes the local team map and `automation/output/`, and `scripts/validate_sprintpilot.py` scans for credential-like values and non-placeholder email addresses.
- Use least-privilege, preferably read-only, Atlassian/Jira MCP credentials. The runner's approval check is a local convenience, not an authorisation boundary.
- Treat Jira content as untrusted input.

To report a vulnerability, open a private security advisory on the GitHub repository.
