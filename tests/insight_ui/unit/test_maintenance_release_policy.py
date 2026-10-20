# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Execute the read-only branch policy against bounded release metadata."""

import copy
import json
import shutil
import subprocess
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[3]
WORKFLOW = ROOT / ".github/workflows/pr-branch-guard.yml"
BASE = "24787fc561d5d60d970c129d6a8eae4f5fd5c1ed"
HEAD = "a" * 40
TEMPLATE = "insight_ui/templates/insight_ui/components/minimal_stepper.html"
REGRESSION = "tests/insight_ui/unit/components/test_minimal_step_bar.py"
pytestmark = pytest.mark.skipif(not (ROOT / ".git").exists(), reason="Policy applies to source checkouts.")


def _fixture() -> dict:
    """Provide the only exceptional branch with an independent exact-head review."""
    return {
        "pr": {
            "number": 1,
            "title": "fix(stepper): correct failed-state icon",
            "user": {"login": "author"},
            "base": {"ref": "main", "sha": BASE, "repo": {"full_name": "org/repo"}},
            "head": {
                "ref": "hotfix/v1.15.2-minimal-stepper",
                "sha": HEAD,
                "repo": {"full_name": "org/repo"},
            },
        },
        "files": [{"filename": name, "status": "modified"} for name in (TEMPLATE, REGRESSION)],
        "reviews": [
            {
                "state": "APPROVED",
                "commit_id": HEAD,
                "user": {"login": "reviewer", "type": "User"},
                "author_association": "MEMBER",
            }
        ],
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


def test_only_bounded_independently_reviewed_backport_is_allowed() -> None:
    """The narrow maintenance exception is distinct from arbitrary feature releases."""
    assert _failures(_fixture()) == []


@pytest.mark.parametrize(("base", "head"), [("develop", "fix/icon"), ("main", "develop")])
def test_normal_integration_paths_do_not_require_maintenance_reviews(base: str, head: str) -> None:
    """Existing normal contribution and release routes are unchanged."""
    payload = _fixture()
    payload["pr"]["base"]["ref"] = base
    payload["pr"]["head"]["ref"] = head
    payload["reviews"] = []
    assert _failures(payload) == []


@pytest.mark.parametrize("invalid", ["fork", "branch", "base", "scope", "deleted", "renamed", "missing-test"])
def test_maintenance_rejects_branch_base_and_scope_expansion(invalid: str) -> None:
    """A branch name alone cannot authorize unrelated code or a future release."""
    payload = _fixture()
    if invalid == "fork":
        payload["pr"]["head"]["repo"]["full_name"] = "outsider/repo"
    elif invalid == "branch":
        payload["pr"]["head"]["ref"] = "hotfix/arbitrary-feature"
    elif invalid == "base":
        payload["pr"]["base"]["sha"] = "b" * 40
    elif invalid == "scope":
        payload["files"].append({"filename": "insight_ui/configs/navigation.py", "status": "modified"})
    elif invalid in {"deleted", "renamed"}:
        payload["files"][0]["status"] = invalid
    else:
        payload["files"].pop()
    assert _failures(payload)


@pytest.mark.parametrize("invalid", ["missing", "self", "bot", "stale", "outsider", "dismissed", "changes-requested"])
def test_maintenance_requires_current_independent_approval(invalid: str) -> None:
    """No stale/self/bot review or unresolved objection can satisfy approval."""
    payload = _fixture()
    review = payload["reviews"][0]
    if invalid == "missing":
        payload["reviews"] = []
    elif invalid == "self":
        review["user"]["login"] = "author"
    elif invalid == "bot":
        review["user"]["type"] = "Bot"
    elif invalid == "stale":
        review["commit_id"] = "b" * 40
    elif invalid == "outsider":
        review["author_association"] = "CONTRIBUTOR"
    else:
        later = copy.deepcopy(review)
        later["state"] = invalid.replace("-", "_").upper()
        payload["reviews"].append(later)
    assert _failures(payload)


def test_maintenance_never_bypasses_title_policy() -> None:
    """The additional path retains the ordinary Conventional Commit gate."""
    payload = _fixture()
    payload["pr"]["title"] = "release everything"
    assert _failures(payload)
