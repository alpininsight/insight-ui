# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Pytest configuration and fixtures for Insight UI tests."""

import pytest
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


@pytest.fixture(scope="session")
def live_server_class() -> type[StaticLiveServerTestCase]:
    """Use Django's StaticLiveServerTestCase for serving static files."""
    return StaticLiveServerTestCase


@pytest.fixture
def live_server_url(live_server) -> None:  # noqa: ANN001
    """Fixture für Live-Server-URL."""
    return live_server.url
