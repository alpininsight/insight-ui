# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for the card component."""

from tests.insight_ui.unit.components.test_template_tags import TemplateTagsTestCase


class TestCard(TemplateTagsTestCase):
    """Test suite for the card component."""

    def test_card_basic(self) -> None:
        """Test für grundlegende card Funktionalität."""
        template_string = """
        {% load insight_tags %}
        {% card title="Test Card" content="Test Card Content" %}
        """
        rendered = self.render_template(template_string)
        assert "Test Card" in rendered

    def test_card_content_allows_html(self) -> None:
        """Card content can render developer-provided HTML fragments."""
        rendered = self.render_template(
            '{% load insight_tags %}{% card title="Formatted" content="<strong>Important</strong><br>Line 2" %}'
        )
        assert "<strong>Important</strong>" in rendered
        assert "<br>Line 2" in rendered
