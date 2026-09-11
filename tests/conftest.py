# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Pytest configuration and fixtures for Insight UI tests."""

import tomllib
from email.message import EmailMessage
from pathlib import Path

import pytest
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


@pytest.fixture
def distribution_metadata() -> EmailMessage:
    """Create package metadata for the small archive fixtures from the source contract."""
    project = tomllib.loads((Path(__file__).resolve().parents[1] / "pyproject.toml").read_text())["project"]
    metadata = EmailMessage()
    metadata["Metadata-Version"] = "2.4"
    metadata["Name"] = project["name"]
    metadata["Version"] = "1.0.0"
    metadata["Requires-Python"] = project["requires-python"]
    for classifier in project["classifiers"]:
        metadata["Classifier"] = classifier
    for name, url in project["urls"].items():
        metadata["Project-URL"] = f"{name}, {url}"
    return metadata


@pytest.fixture(scope="session")
def live_server_class() -> type[StaticLiveServerTestCase]:
    """Use Django's StaticLiveServerTestCase for serving static files."""
    return StaticLiveServerTestCase


@pytest.fixture
def live_server_url(live_server) -> None:  # noqa: ANN001
    """Fixture für Live-Server-URL."""
    return live_server.url
