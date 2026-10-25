"""Tests for the SprintPilot validator and the offline demo.

Run from the repository root with:  python -m unittest discover -s tests -v

The demo tests need PowerShell (``pwsh`` or Windows ``powershell``). Set
SPRINTPILOT_TEST_PWSH to point at a specific executable. They are skipped, not
failed, when no PowerShell is available.
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_sprintpilot.py"
PWSH = os.environ.get("SPRINTPILOT_TEST_PWSH") or shutil.which("pwsh") or shutil.which("powershell")
IGNORE = shutil.ignore_patterns(".git", ".venv", "__pycache__", "output")


def copy_repo(dest: Path) -> Path:
    target = dest / "repo"
    shutil.copytree(ROOT, target, ignore=IGNORE)
    (target / "automation" / "output").mkdir(parents=True, exist_ok=True)
    return target


def run_validator(repo: Path) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(VALIDATOR), str(repo)], capture_output=True, text=True)


def run_demo(repo: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [PWSH, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(repo / "scripts" / "demo-sprintpilot.ps1")],
        capture_output=True, text=True,
    )


def read_report(repo: Path) -> str:
    return (repo / "automation" / "output" / "offline-demo-report.md").read_text(encoding="utf-8")


class ValidatorTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.repo = copy_repo(Path(self._tmp.name))

    def test_repository_passes(self):
        result = run_validator(self.repo)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("validation passed", result.stdout)

    def test_detects_missing_prompt(self):
        (self.repo / "automation" / "prompts" / "retro-notes.md").unlink()
        result = run_validator(self.repo)
        self.assertEqual(result.returncode, 1)
        self.assertIn("Missing prompt", result.stdout)

    def test_detects_credential_like_value(self):
        fake = "sk-" + "A1b2C3d4" * 4  # assembled at runtime so this file is not itself a finding
        (self.repo / "docs" / "leak.md").write_text(f"api_key: {fake}\n", encoding="utf-8")
        result = run_validator(self.repo)
        self.assertEqual(result.returncode, 1)
        self.assertIn("Possible credential", result.stdout)
        self.assertNotIn(fake, result.stdout, "validator must withhold the matched value")

    def test_detects_real_looking_email(self):
        (self.repo / "docs" / "contact.md").write_text("Write to " + "someone@" + "gmail.com\n", encoding="utf-8")
        result = run_validator(self.repo)
        self.assertEqual(result.returncode, 1)
        self.assertIn("Non-placeholder email", result.stdout)

    def test_detects_broken_doc_link(self):
        (self.repo / "docs" / "links.md").write_text("[gone](does-not-exist.md)\n", encoding="utf-8")
        result = run_validator(self.repo)
        self.assertEqual(result.returncode, 1)
        self.assertIn("Broken documentation link", result.stdout)

    def test_rejects_demo_fixture_without_synthetic_marker(self):
        fixture = self.repo / "examples" / "demo-sprint.yaml"
        data = yaml.safe_load(fixture.read_text(encoding="utf-8"))
        data["data_notice"] = "real customer data"
        fixture.write_text(yaml.safe_dump(data), encoding="utf-8")
        result = run_validator(self.repo)
        self.assertEqual(result.returncode, 1)
        self.assertIn("synthetic", result.stdout)

    def test_team_map_example_defaults_to_dry_run(self):
        data = yaml.safe_load((ROOT / "references" / "team-map.example.yaml").read_text(encoding="utf-8"))
        self.assertIs(data["defaults"]["dry_run"], True)
        self.assertIs(data["approval"]["allow_apply_without_approval"], False)


@unittest.skipUnless(PWSH, "PowerShell is not available")
class OfflineDemoTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.repo = copy_repo(Path(self._tmp.name))

    def test_report_matches_committed_sample(self):
        result = run_demo(self.repo)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        expected = (ROOT / "examples" / "sample-report.md").read_text(encoding="utf-8")
        self.assertEqual(read_report(self.repo).replace("\r\n", "\n"), expected.replace("\r\n", "\n"))

    def test_totals_agree_with_fixture(self):
        self.assertEqual(run_demo(self.repo).returncode, 0)
        data = yaml.safe_load((ROOT / "examples" / "demo-sprint.yaml").read_text(encoding="utf-8"))
        total = sum(issue["estimate"] for issue in data["issues"])
        report = read_report(self.repo)
        self.assertIn(f"{total} points across {len(data['issues'])} issues", report)
        self.assertIn(f"capacity is {data['sprint']['capacity_points']} points", report)
        for issue in data["issues"]:
            self.assertIn(issue["key"], report)

    def test_over_capacity_is_reported(self):
        fixture = self.repo / "examples" / "demo-sprint.yaml"
        text = fixture.read_text(encoding="utf-8")
        fixture.write_text(re.sub(r"capacity_points: \d+", "capacity_points: 10", text), encoding="utf-8")
        self.assertEqual(run_demo(self.repo).returncode, 0)
        self.assertIn("exceeds capacity by 11 points", read_report(self.repo))

    def test_fails_without_fixture(self):
        (self.repo / "examples" / "demo-sprint.yaml").unlink()
        result = run_demo(self.repo)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("fixture was not found", result.stdout + result.stderr)

    def test_refuses_fixture_without_synthetic_marker(self):
        fixture = self.repo / "examples" / "demo-sprint.yaml"
        text = re.sub(r'data_notice: ".*"', 'data_notice: "customer export"', fixture.read_text(encoding="utf-8"))
        fixture.write_text(text, encoding="utf-8")
        result = run_demo(self.repo)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("synthetic marker", result.stdout + result.stderr)

    def test_rejects_unsupported_yaml(self):
        fixture = self.repo / "examples" / "demo-sprint.yaml"
        fixture.write_text(fixture.read_text(encoding="utf-8") + "\n  nested:\n      too: deep\n", encoding="utf-8")
        result = run_demo(self.repo)
        self.assertNotEqual(result.returncode, 0)

    def test_makes_no_network_or_agent_calls(self):
        script = (ROOT / "scripts" / "demo-sprintpilot.ps1").read_text(encoding="utf-8")
        for token in ("Invoke-WebRequest", "Invoke-RestMethod", "curl", "codex"):
            self.assertNotIn(token, script)


if __name__ == "__main__":
    unittest.main()
