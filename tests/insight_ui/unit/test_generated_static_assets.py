# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Keep generated minified CSS and JavaScript out of the package repository."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
requires_git = pytest.mark.skipif(not (ROOT / ".git").exists(), reason="Git index checks apply to source checkouts.")
MINIFIED_SUFFIXES = (".min.css", ".min.js")
IGNORED_MINIFIED_PATHS = (
    "insight_ui/static/insight_ui/css/tailwind.min.css",
    "insight_ui/static/insight_ui/css/vendor/tailwind.min.css",
    "insight_ui/static/insight_ui/js/insight-ui-init.min.js",
    "insight_ui/static/insight_ui/js/vendor/insight-ui-init.min.js",
    "devtools/example.min.js",
    "example.min.css",
)
READABLE_ASSET_PATHS = (
    "insight_ui/static/insight_ui/css/tailwind.css",
    "insight_ui/static/insight_ui/js/insight-ui-init.js",
)


def _git(*args: str) -> subprocess.CompletedProcess[str]:
    """Run git against this source checkout."""
    return subprocess.run(  # noqa: S603
        ["git", *args],  # noqa: S607 - git is required by the repository contract
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )


def test_verify_static_build_includes_minified_asset_check() -> None:
    """The static verify flow rejects tracked minified assets before it minifies."""
    scripts = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))["scripts"]
    verify = scripts["verify:static-build"]

    assert scripts["check:generated-assets"] == "node scripts/check-generated-static-assets.mjs"
    assert verify.startswith("npm run check:generated-assets &&")
    assert "npm run check:tailwind-sync" in verify
    assert verify.endswith("npm run build:static")
    assert scripts["check:static-build"] == "npm run verify:static-build"
    assert "tailwind build" not in scripts["check:generated-assets"]


@requires_git
def test_repository_does_not_track_minified_assets() -> None:
    """Force-added minified files must not already be in the index."""
    result = _git("ls-files", "-z")

    assert result.returncode == 0, result.stderr
    tracked = [path for path in result.stdout.split("\0") if path.endswith(MINIFIED_SUFFIXES)]
    assert tracked == []


@requires_git
def test_gitignore_covers_nested_minified_assets() -> None:
    """Ignore minified CSS and JavaScript in nested directories, not only one folder level."""
    ignored = _git("check-ignore", "-v", "--", *IGNORED_MINIFIED_PATHS)
    ignored_paths = {line.split("\t", 1)[1] for line in ignored.stdout.splitlines() if "\t" in line}
    readable = _git("check-ignore", "-v", "--", *READABLE_ASSET_PATHS)

    assert ignored_paths == set(IGNORED_MINIFIED_PATHS)
    assert readable.stdout == ""
