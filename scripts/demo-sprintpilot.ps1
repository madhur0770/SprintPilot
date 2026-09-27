[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$fixturePath = Join-Path $root 'examples/demo-sprint.yaml'
$outputDirectory = Join-Path $root 'automation/output'
$reportPath = Join-Path $outputDirectory 'offline-demo-report.md'

function ConvertFrom-DemoScalar {
    param([string]$Text)

    $value = $Text.Trim()
    if ($value.Length -ge 2 -and $value.StartsWith('"') -and $value.EndsWith('"')) {
        return $value.Substring(1, $value.Length - 2)
    }
    if ($value.Length -ge 2 -and $value.StartsWith("'") -and $value.EndsWith("'")) {
        return $value.Substring(1, $value.Length - 2).Replace("''", "'")
    }
    if ($value -match '^(?i:true|false)$') { return [bool]::Parse($value) }
    if ($value -match '^-?\d+$') { return [int]$value }
    if ($value -match '^(?i:null|~)$') { return $null }
    return $value
}

if (-not (Test-Path -LiteralPath $fixturePath -PathType Leaf)) {
    throw "Offline demo fixture was not found: $fixturePath"
}

# Parse the fixture's intentionally small YAML subset using PowerShell only.
# This keeps the recruiter demo independent of Python and third-party modules.
$demo = @{ sprint = @{}; issues = (New-Object 'System.Collections.Generic.List[object]') }
$section = ''
$currentIssue = $null
foreach ($line in (Get-Content -LiteralPath $fixturePath -Encoding UTF8)) {
    if ($line -match '^\s*(#.*)?$') { continue }
    if ($line -match '^(sprint|issues):\s*$') {
        $section = $Matches[1]
        $currentIssue = $null
        continue
    }
    if ($line -match '^([a-z_]+):\s*(.*)$') {
        $demo[$Matches[1]] = ConvertFrom-DemoScalar $Matches[2]
        $section = ''
        continue
    }
    if ($section -eq 'sprint' -and $line -match '^  ([a-z_]+):\s*(.*)$') {
        $demo.sprint[$Matches[1]] = ConvertFrom-DemoScalar $Matches[2]
        continue
    }
    if ($section -eq 'issues' -and $line -match '^  - ([a-z_]+):\s*(.*)$') {
        $currentIssue = @{}
        $currentIssue[$Matches[1]] = ConvertFrom-DemoScalar $Matches[2]
        [void]$demo.issues.Add($currentIssue)
        continue
    }
    if ($section -eq 'issues' -and $null -ne $currentIssue -and $line -match '^    ([a-z_]+):\s*(.*)$') {
        $currentIssue[$Matches[1]] = ConvertFrom-DemoScalar $Matches[2]
        continue
    }
    throw "Unsupported YAML structure in offline demo fixture: $line"
}

if (-not $demo.data_notice -or $demo.data_notice -notmatch '(?i)synthetic|fictional' -or
    -not $demo.sprint.name -or $demo.issues.Count -eq 0) {
    throw 'Offline demo fixture is missing its synthetic marker, sprint metadata, or issues.'
}

$totalPoints = 0
foreach ($issue in $demo.issues) {
    $totalPoints += [int]$issue['estimate']
}
$riskIssues = @($demo.issues | Where-Object { $_.blocker -and $_.blocker -ne 'none' })
$blockedIssues = @($demo.issues | Where-Object { $_.status -eq 'Blocked' })
$notReadyIssues = @($demo.issues | Where-Object { -not $_.ready })
$report = @(
    '# SprintPilot Offline Sprint Demo'
    ''
    '> **Offline demo using fictional data.** All people, issues, and sprint details below are synthetic. This report was generated locally and does not connect to Jira.'
    ''
    '## Sprint snapshot'
    ''
    "- **Sprint:** $($demo.sprint.name)"
    "- **Project:** $($demo.sprint.project) (fictional)"
    "- **Goal:** $($demo.sprint.goal)"
    "- **Dates:** $($demo.sprint.start_date) to $($demo.sprint.end_date)"
    "- **Planned estimate:** $totalPoints points across $($demo.issues.Count) issues; stated capacity is $($demo.sprint.capacity_points) points."
    ''
    '## Issue review'
    ''
    '| Issue | Status | Fictional owner | Estimate | Ready | Summary |'
    '|---|---|---|---:|:---:|---|'
)
foreach ($issue in $demo.issues) {
    $readyText = if ($issue.ready) { 'Yes' } else { 'No' }
    $report += "| $($issue.key) - $($issue.title) | $($issue.status) | $($issue.owner) | $($issue.estimate) | $readyText | $($issue.detail) |"
}
$report += @('', '## Risks and blockers', '')
if ($riskIssues.Count -eq 0) {
    $report += '- No explicit blockers are present in the synthetic fixture.'
} else {
    foreach ($issue in $riskIssues) {
        $report += "- **$($issue.key):** $($issue.blocker)"
    }
}
$report += @('', '## Recommended next steps', '')
if ($blockedIssues.Count -gt 0) {
    foreach ($issue in $blockedIssues) {
        $report += "- Resolve the dependency for **$($issue.key)** and confirm the signup flow in the fictional email sandbox."
    }
}
foreach ($issue in $notReadyIssues) {
    $report += "- Confirm the missing product decision for **$($issue.key)** before treating it as ready for sprint delivery."
}
$report += @(
    "- Keep the sprint commitment within the stated $($demo.sprint.capacity_points)-point capacity and revisit scope if estimates change."
    '- Recheck blocked and not-ready work during the next team sync.'
    ''
    '## Execution details'
    ''
    '- **Mode:** deterministic offline demo'
    '- **Input:** `examples/demo-sprint.yaml`'
    '- **Data:** fictional and synthetic; no Jira records are used.'
    '- **Connections:** none; this script does not invoke Codex, Jira, Atlassian MCP, credentials, or network resources.'
    '- **Changes applied:** none; this is a local report only.'
    ''
)

New-Item -ItemType Directory -Path $outputDirectory -Force | Out-Null
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($reportPath, ($report -join "`r`n"), $utf8NoBom)
Write-Output "Report: $reportPath"
