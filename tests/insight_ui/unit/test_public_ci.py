# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Keep contributor checks independent of private infrastructure and credentials."""

import re
import tomllib
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[3]
WORKFLOWS = ROOT / ".github/workflows"
ARTIFACT_RETENTION_DAYS = 7
pytestmark = pytest.mark.skipif(not (ROOT / ".git").exists(), reason="Workflow policy applies to source checkouts.")


def _workflows() -> dict[str, dict]:
    """Read safe YAML and normalize the YAML 1.1 interpretation of 'on'."""
    workflows = {}
    for path in WORKFLOWS.glob("*.yml"):
        workflow = yaml.safe_load(path.read_text())
        if True in workflow:
            workflow["on"] = workflow.pop(True)
        workflows[path.name] = workflow
    return workflows


def test_pull_request_workflows_have_no_private_access() -> None:
    """Fork contributions must run without private reusable workflows or secrets."""
    pull_requests = {
        name: workflow
        for name, workflow in _workflows().items()
        if any(event.startswith("pull_request") for event in workflow.get("on", {}))
    }
    assert set(pull_requests) == {"feature-ci.yml", "pr-branch-guard.yml"}
    for name, workflow in pull_requests.items():
        source = (WORKFLOWS / name).read_text()
        assert "pull_request_target" not in workflow["on"]
        assert ".github-private/" not in source
        assert "secrets." not in source
        assert "secrets:" not in source
        assert "write" not in workflow["permissions"].values()
        for job in workflow["jobs"].values():
            assert job["runs-on"] == "ubuntu-latest"
            assert "uses" not in job
            assert "write" not in job.get("permissions", {}).values()
            for step in job.get("steps", []):
                if "uses" in step:
                    assert re.fullmatch(r"(?:actions|astral-sh)/[a-z-]+@[a-f0-9]{40}", step["uses"])
                if step.get("uses", "").startswith("actions/checkout@"):
                    assert step["with"]["persist-credentials"] is False


def test_quality_gate_preserves_required_checks() -> None:
    """Every executed check gates the PR without renaming protected statuses."""
    workflow = _workflows()["feature-ci.yml"]
    # Retargeting a PR to develop must start its required checks without a new push.
    assert "edited" in workflow["on"]["pull_request"]["types"]
    jobs = workflow["jobs"]
    quality = jobs["quality"]
    assert quality["strategy"]["matrix"]["python"] == ["3.12", "3.13", "3.14"]
    assert quality["name"] == "Python/Django Quality / Quality (Python ${{ matrix.python }})"
    assert jobs["quality_gate"]["name"] == "Python/Django Quality / Quality Gate"
    assert set(jobs["quality_gate"]["needs"]) == set(jobs) - {"quality_gate"}
    assert "always() && !cancelled()" in jobs["quality_gate"]["if"]
    assert 'all(.[]; .result == "success")' in jobs["quality_gate"]["steps"][0]["run"]
    for job in jobs.values():
        assert job.get("continue-on-error", False) is False
        assert all(step.get("continue-on-error", False) is False for step in job["steps"])
    policy = _workflows()["pr-branch-guard.yml"]["jobs"]["branch-policy"]
    assert policy["name"] == "branch-policy / Repository Policy"


def test_artifacts_are_uploaded_only_after_installation_smoke() -> None:
    """Package evidence must be tested, short-lived, and never implicitly published."""
    steps = _workflows()["feature-ci.yml"]["jobs"]["distribution"]["steps"]
    smoke = next(index for index, step in enumerate(steps) if "scripts/smoke_distribution.py" in step.get("run", ""))
    upload = next(
        index for index, step in enumerate(steps) if step.get("uses", "").startswith("actions/upload-artifact@")
    )
    assert smoke < upload
    assert steps[upload]["with"]["retention-days"] == ARTIFACT_RETENTION_DAYS
    assert steps[upload]["with"]["if-no-files-found"] == "error"
    assert "publish" not in "\n".join(step.get("run", "") for step in steps)


def test_locked_dependencies_require_only_public_indexes() -> None:
    """Contributor setup must not start depending on a private Git or package host."""
    project = tomllib.loads((ROOT / "pyproject.toml").read_text())
    assert not project.get("tool", {}).get("uv", {}).get("sources")
    lock = tomllib.loads((ROOT / "uv.lock").read_text())
    for package in lock["package"]:
        assert package["source"] in ({"registry": "https://pypi.org/simple"}, {"editable": "."})
