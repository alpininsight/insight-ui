# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Keep the Tailwind source build independent of moving release metadata."""

import json
import tomllib
from pathlib import Path

import pytest
from django.test import override_settings
from django_tailwind_cli import config as tailwind_config

from tests import tailwind_settings

ROOT = Path(__file__).resolve().parents[3]
TAILWIND_CLI_VERSION = "4.3.3"
DJANGO_TAILWIND_CLI_VERSION = "4.6.2"


def test_tailwind_dependency_and_build_settings_are_exactly_pinned() -> None:
    """The Python wrapper and its downloaded CLI must not resolve floating versions."""
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    lock = tomllib.loads((ROOT / "uv.lock").read_text(encoding="utf-8"))

    assert f"django-tailwind-cli=={DJANGO_TAILWIND_CLI_VERSION}" in project["dependency-groups"]["dev"]
    locked = next(package for package in lock["package"] if package["name"] == "django-tailwind-cli")
    assert locked["version"] == DJANGO_TAILWIND_CLI_VERSION

    assert tailwind_settings.TAILWIND_CLI_VERSION == TAILWIND_CLI_VERSION


def test_static_build_entrypoints_share_the_tailwind_compiler() -> None:
    """Only the documented compiler entrypoint may invoke Django Tailwind."""
    scripts = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))["scripts"]

    assert "django tailwind build" in scripts["build:tailwind"]
    assert scripts["build:tailwind"].startswith("DJANGO_SETTINGS_MODULE=tests.tailwind_settings")
    assert "build:tailwind" in scripts["build:static-all"]
    for name in ("build:js", "build:static", "verify:static-build", "check:static-build"):
        assert "tailwind build" not in scripts[name]


@override_settings(TAILWIND_CLI_VERSION=TAILWIND_CLI_VERSION)
def test_pinned_cli_version_skips_latest_network_resolution(monkeypatch: pytest.MonkeyPatch) -> None:
    """An explicit pin must not consult the mutable GitHub latest-release redirect."""
    monkeypatch.setattr(
        tailwind_config,
        "_load_cached_version",
        lambda _repo: pytest.fail("a pinned version must not read the latest-version cache"),
    )
    monkeypatch.setattr(
        tailwind_config.http,
        "fetch_redirect_location",
        lambda *_args, **_kwargs: pytest.fail("a pinned version must not resolve GitHub latest"),
    )

    version, parsed = tailwind_config.get_version()

    assert version == TAILWIND_CLI_VERSION
    assert str(parsed) == TAILWIND_CLI_VERSION


@override_settings(
    TAILWIND_CLI_VERSION=TAILWIND_CLI_VERSION,
    STATICFILES_DIRS=tailwind_settings.STATICFILES_DIRS,
    TAILWIND_CLI_SRC_CSS=tailwind_settings.TAILWIND_CLI_SRC_CSS,
    TAILWIND_CLI_DIST_CSS=tailwind_settings.TAILWIND_CLI_DIST_CSS,
)
def test_download_and_execution_keep_the_same_version(monkeypatch: pytest.MonkeyPatch) -> None:
    """Repeated config resolution must not download one version and execute another."""
    monkeypatch.setattr(
        tailwind_config.http,
        "fetch_redirect_location",
        lambda *_args, **_kwargs: pytest.fail("build configs must not resolve GitHub latest"),
    )
    download_config = tailwind_config.get_config()
    execution_config = tailwind_config.get_config()

    assert download_config.version_str == execution_config.version_str == TAILWIND_CLI_VERSION
    assert f"/v{TAILWIND_CLI_VERSION}/" in download_config.download_url
    assert f"-{TAILWIND_CLI_VERSION}" in download_config.cli_path.name
    assert download_config.cli_path == execution_config.cli_path
    assert execution_config.build_cmd[0] == str(download_config.cli_path)
