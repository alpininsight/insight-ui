# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for the textarea component."""

from bs4 import BeautifulSoup

from tests.insight_ui.unit.components.test_template_tags import TemplateTagsTestCase

# TODO: Implement tests for Textarea component  # noqa: TD002, TD003


class TestTextarea(TemplateTagsTestCase):
    """Test suite for the textarea component."""

    def test_textarea_shows_explanation_as_tooltip(self) -> None:
        """The explanation is rendered as a tooltip next to the label."""
        rendered = self.render_template(
            "{% load insight_tags %}{% textarea name='message' label='Message' explanation='Max. 500 characters.' %}"
        )
        soup = BeautifulSoup(rendered, "html.parser")

        tooltip = soup.select_one("label [data-insight-tooltip]")
        assert tooltip is not None
        assert tooltip["data-insight-tooltip"] == "Max. 500 characters."
