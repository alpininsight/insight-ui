# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for the standalone theme toggle tag."""

from bs4 import BeautifulSoup

from tests.insight_ui.unit.components.test_template_tags import TemplateTagsTestCase


class TestThemeToggle(TemplateTagsTestCase):
    """Test suite for the theme toggle tag."""

    def test_theme_toggle_tag_renders_toggle_button(self) -> None:
        """The tag renders the same toggle button as the navbar."""
        rendered = self.render_template("{% load insight_tags %}{% theme_toggle %}")
        button = BeautifulSoup(rendered, "html.parser").find("button")
        assert button is not None
        assert button.has_attr("data-insight-theme-toggle")
        assert button.get("aria-label")
