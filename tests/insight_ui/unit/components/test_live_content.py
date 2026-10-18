# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for the live_content component."""

import pytest
from bs4 import BeautifulSoup
from insight_ui.configs import LiveContentConfig

from tests.insight_ui.unit.components.test_template_tags import TemplateTagsTestCase


class TestLiveContent(TemplateTagsTestCase):
    """Test suite for the live_content component."""

    def test_live_content_basic(self) -> None:
        """Test für grundlegende live_content Funktionalität."""
        template_string = """
        {% load insight_tags %}
        {% live_content request_url="/api/live-data/" %}
        """
        rendered = self.render_template(template_string)
        assert "/api/live-data/" in rendered

    def test_live_content_config_requires_request_url(self) -> None:
        """LiveContentConfig requires request_url."""
        with pytest.raises(TypeError):
            LiveContentConfig()  # type: ignore[call-arg]

    def test_live_content_with_interval(self) -> None:
        """Test für live_content mit Intervall."""
        template_string = """
        {% load insight_tags %}
        {% live_content request_url="/api/live-data/" interval=5000 %}
        """
        rendered = self.render_template(template_string)
        assert "/api/live-data/" in rendered

    def test_live_content_shows_only_its_own_loading_indicator(self) -> None:
        """Polling must not reveal the indicators of forms or other components on the page."""
        rendered = self.render_template('{% load insight_tags %}{% live_content request_url="/api/live-data/" %}')
        container = BeautifulSoup(rendered, "html.parser").select_one("[hx-get]")

        assert container["hx-indicator"] == "find .htmx-indicator"
        assert container.select_one(".htmx-indicator") is not None
        # The inline script toggles aria-busy on elements with this class.
        assert "insight-live-content" in container["class"]

    def test_live_content_keeps_background_updates_out_of_global_loading_bar(self) -> None:
        """Polling does not flash the global loading bar unless switched on."""
        default = self.render_template('{% load insight_tags %}{% live_content request_url="/api/live-data/" %}')
        enabled = self.render_template(
            '{% load insight_tags %}{% live_content request_url="/api/live-data/" show_global_loading_indicator=True %}'
        )

        assert BeautifulSoup(default, "html.parser").select_one("[hx-get]")["data-insight-global-indicator"] == "false"
        assert (
            not BeautifulSoup(enabled, "html.parser").select_one("[hx-get]").has_attr("data-insight-global-indicator")
        )
