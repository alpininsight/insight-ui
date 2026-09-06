# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for the tabs component."""

import pytest
from insight_ui.configs import TabConfig

from tests.insight_ui.unit.components.test_template_tags import TemplateTagsTestCase

# TODO: Implement tests for Tabs component  # noqa: TD002, TD003


class TestTabs(TemplateTagsTestCase):
    """Test suite for the tabs component."""

    def test_tab_config_requires_request_url(self) -> None:
        """TabConfig requires request_url (config mode is HTMX-only)."""
        with pytest.raises(TypeError):
            TabConfig(tag_id="general", title="General")  # type: ignore[call-arg]
