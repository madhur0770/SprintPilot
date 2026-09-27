"""Portable local checks for SprintPilot repository content."""
from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is required. Run scripts/setup.ps1 first.")
    raise SystemExit(2)

root = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]).resolve()
errors: list[str] = []
required = ["README.md", "LICENSE", ".gitignore", "requirements.txt", "SKILL.md", "agents/openai.yaml", "references/team-map.example.yaml", "scripts/setup.ps1", "scripts/sprintpilot.ps1", "scripts/validate-sprintpilot.ps1", "docs/architecture.md", "docs/configuration.md", "docs/windows-setup.md", "docs/limitations.md", "examples/sample-workflow.md"]
for item in required:
    if not (root / item).is_file():
        errors.append(f"Missing required file: {item}")

modes = ("shape-sprint", "triage-queue", "suggest-owner", "balance-load", "inspect-sprint", "surface-risk", "progress-pulse", "standup-brief", "retro-notes")
for mode in modes:
    if not (root / "automation" / "prompts" / f"{mode}.md").is_file():
        errors.append(f"Missing prompt: automation/prompts/{mode}.md")

yaml_files = [p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in {".yaml", ".yml"}]
for yaml_path in yaml_files:
    rel = yaml_path.relative_to(root).as_posix()
    try:
        data = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            errors.append(f"YAML root must be a mapping: {rel}")
        if rel == "agents/openai.yaml" and not (data.get("interface") or {}).get("display_name"):
            errors.append("Agent metadata is missing interface.display_name")
        if rel.endswith("team-map.example.yaml"):
            if not isinstance(data.get("approval"), dict) or not isinstance(data.get("board"), dict):
                errors.append("Team-map example is missing board or approval metadata")
            if not isinstance(data.get("team"), list) or not data.get("team"):
                errors.append("Team-map example must define at least one team member")
            if not (data.get("defaults") or {}).get("dry_run", False):
                errors.append("Team-map example must default to dry-run")
    except Exception as exc:
        errors.append(f"Invalid YAML in {rel}: {exc}")

excluded = {".git", ".venv", "__pycache__"}
files = [p for p in root.rglob("*") if p.is_file() and not any(part in excluded for part in p.relative_to(root).parts)]
brand_fragments = ("codin" + "zhub", "coder " + "coder")
secret_patterns = [re.compile(r"(?i)\bsk-[A-Za-z0-9_-]{20,}\b"), re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"), re.compile(r"\bAKIA[0-9A-Z]{16}\b"), re.compile(r"-----BEGIN (?:RSA|OPENSSH|EC) PRIVATE KEY-----"), re.compile(r"(?i)(?:api[_-]?key|access[_-]?token|password|client[_-]?secret)\s*[:=]\s*[\"']?(?!YOUR_|CHANGE_ME|REPLACE_ME)[A-Za-z0-9_./+=-]{8,}")]
email_pattern = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
for path in files:
    try:
        content = path.read_text(encoding="utf-8")
    except (UnicodeError, OSError):
        continue
    rel = path.relative_to(root).as_posix()
    lowered = content.casefold()
    for fragment in brand_fragments:
        if fragment in lowered:
            errors.append(f"Competition branding remains in {rel}")
            break
    for pattern in secret_patterns:
        if pattern.search(content):
            errors.append(f"Possible credential in {rel} (value withheld)")
            break
    if any(not address.lower().endswith("@example.com") for address in email_pattern.findall(content)):
        errors.append(f"Non-placeholder email address in {rel} (value withheld)")

runner = root / "automation" / "run-sprintpilot.sh"
if runner.exists():
    text = runner.read_text(encoding="utf-8")
    for mode in modes:
        if not (root / "automation" / "prompts" / f"{mode}.md").exists() or mode not in text:
            errors.append(f"Runner mode/prompt reference missing: {mode}")
for path in (root / "automation").glob("*.sh"):
    if path.name == runner.name:
        continue
    text = path.read_text(encoding="utf-8")
    for target in re.findall(r'\$SCRIPT_DIR/([^\s"\']+)', text):
        if not (path.parent / target).is_file():
            errors.append(f"Broken script reference in {path.relative_to(root)}: {target}")

for path in files:
    if path.suffix.lower() not in {".md", ".yaml", ".yml"}:
        continue
    text = path.read_text(encoding="utf-8", errors="ignore")
    for target in re.findall(r'\]\(([^)#]+)', text):
        if "://" in target or target.startswith("#"):
            continue
        if not (path.parent / target).exists():
            errors.append(f"Broken documentation link in {path.relative_to(root)}: {target}")

if errors:
    print("SprintPilot validation failed:")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)
print(f"SprintPilot validation passed ({len(required)} required files, {len(modes)} prompts, YAML and content checks).")
