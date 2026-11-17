# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Execute the read-only branch policy against bounded release metadata."""

import json
import shutil
import subprocess
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[3]
WORKFLOW = ROOT / ".github/workflows/pr-branch-guard.yml"
pytestmark = pytest.mark.skipif(not (ROOT / ".git").exists(), reason="Policy applies to source checkouts.")


def _fixture() -> dict:
    """Describe an ordinary same-repository release promotion, without approvals."""
    return {
        "pr": {
            "number": 1,
            "title": "chore(release): prepare Insight UI 2.0 release candidate",
            "user": {"login": "author"},
            "base": {"ref": "main", "sha": "b" * 40, "repo": {"full_name": "org/repo"}},
            "head": {"ref": "develop", "sha": "a" * 40, "repo": {"full_name": "org/repo"}},
        },
        "files": [],
        "reviews": [],
    }


def _failures(payload: dict) -> list[str]:
    """Run the actual workflow JavaScript without credentials, network or checkout."""
    workflow = yaml.safe_load(WORKFLOW.read_text())
    script = workflow["jobs"]["branch-policy"]["steps"][0]["with"]["script"]
    harness = """
        const fs = require('fs');
        const {script, payload} = JSON.parse(fs.readFileSync(0, 'utf8'));
        const failures = [];
        const github = {
          rest: {pulls: {
            get: async () => ({data: payload.pr}),
            listFiles: 'files', listReviews: 'reviews'
          }},
          paginate: async (endpoint) => payload[endpoint]
        };
        const context = {repo: {owner: 'org', repo: 'repo'}, issue: {number: 1}};
        const core = {setFailed: message => failures.push(message)};
        const AsyncFunction = Object.getPrototypeOf(async function(){}).constructor;
        new AsyncFunction('github', 'context', 'core', script)(github, context, core)
          .then(() => process.stdout.write(JSON.stringify(failures)))
          .catch(error => {process.stderr.write(String(error)); process.exitCode = 1;});
    """
    node = shutil.which("node")
    assert node is not None, "Node.js is required by the contributor checks."
    result = subprocess.run(  # noqa: S603 - resolved Node interpreter and local metadata-only harness.
        [node, "-e", harness],
        input=json.dumps({"script": script, "payload": payload}),
        capture_output=True,
        check=True,
        text=True,
        timeout=10,
    )
    return json.loads(result.stdout)


@pytest.mark.parametrize(("base", "head"), [("develop", "fix/icon"), ("main", "develop")])
def test_normal_feature_and_release_paths_remain_allowed(base: str, head: str) -> None:
    """The cleanup retains the normal workflow without creating a publish approval."""
    payload = _fixture()
    payload["pr"]["base"]["ref"] = base
    payload["pr"]["head"]["ref"] = head
    assert _failures(payload) == []


@pytest.mark.parametrize(
    "branch",
    ["hotfix/v1.15.2-minimal-stepper", "maintenance/v1-webmcp-i18n-compat", "support/1.15", "fix/icon"],
)
def test_main_rejects_non_develop_heads_even_with_approved_review(branch: str) -> None:
    """The retired narrow exception cannot be revived with old approval metadata."""
    payload = _fixture()
    payload["pr"]["head"]["ref"] = branch
    payload["pr"]["base"]["sha"] = "24787fc561d5d60d970c129d6a8eae4f5fd5c1ed"
    payload["reviews"] = [
        {
            "state": "APPROVED",
            "commit_id": "a" * 40,
            "user": {"login": "reviewer", "type": "User"},
            "author_association": "OWNER",
        }
    ]
    assert _failures(payload) == ["Production releases must come from this repository's develop branch."]


def test_main_rejects_a_fork_named_develop() -> None:
    """Matching a protected branch name in another repository grants no exception."""
    payload = _fixture()
    payload["pr"]["head"]["repo"]["full_name"] = "outsider/repo"
    assert _failures(payload)


@pytest.mark.parametrize("base", ["support/1.15", "feature/stack", "other"])
def test_policy_rejects_unapproved_target_branches(base: str) -> None:
    """Contributions cannot bypass the Develop/Main target contract."""
    payload = _fixture()
    payload["pr"]["base"]["ref"] = base
    assert _failures(payload)


def test_release_promotion_still_requires_a_conventional_title() -> None:
    """Removing the maintenance lane preserves the ordinary title check."""
    payload = _fixture()
    payload["pr"]["title"] = "release everything"
    assert _failures(payload)
