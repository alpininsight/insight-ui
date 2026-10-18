# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for the infinite_scroll component."""

import pytest
from bs4 import BeautifulSoup
from insight_ui.configs import InfiniteScrollConfig

from tests.insight_ui.unit.components.test_template_tags import TemplateTagsTestCase


class TestInfiniteScroll(TemplateTagsTestCase):
    """Test suite for the infinite_scroll component."""

    def test_infinite_scroll_basic(self) -> None:
        """Test für grundlegende infinite_scroll Funktionalität."""
        template_string = """
        {% load insight_tags %}
        {% infinite_scroll request_url="/api/more-items/" %}
        """
        rendered = self.render_template(template_string)
        assert "/api/more-items/" in rendered

    def test_infinite_scroll_config_requires_request_url(self) -> None:
        """InfiniteScrollConfig requires request_url."""
        with pytest.raises(TypeError):
            InfiniteScrollConfig()  # type: ignore[call-arg]

    def test_infinite_scroll_renders_feed_items_as_direct_articles(self) -> None:
        """A feed exposes its entries with the child role required by ARIA."""
        config = InfiniteScrollConfig(
            request_url="/api/more-items/",
            items=[{"title": "First", "content": "Content"}],
        )

        rendered = self.render_template("{% load insight_tags %}{% infinite_scroll config %}", {"config": config})
        soup = BeautifulSoup(rendered, "html.parser")

        feed = soup.find("div", {"role": "feed"})
        articles = feed.find_all("article", recursive=False)
        assert len(articles) == 1
        assert articles[0].get_text(strip=True) == "FirstContent"

    def test_auto_fetch_shows_only_its_own_loading_indicator(self) -> None:
        """Automatic loading reveals the indicator inside the feed, not every indicator on the page."""
        config = InfiniteScrollConfig(request_url="/api/more-items/", auto_fetch=True)
        rendered = self.render_template("{% load insight_tags %}{% infinite_scroll config %}", {"config": config})
        feed = BeautifulSoup(rendered, "html.parser").find("div", {"role": "feed"})

        assert feed["hx-indicator"] == "find .htmx-indicator"
        assert feed.select_one(".htmx-indicator") is not None

    def test_load_more_button_shows_the_feed_indicator(self) -> None:
        """The button targets the indicator that follows it in the feed."""
        config = InfiniteScrollConfig(request_url="/api/more-items/", auto_fetch=False)
        rendered = self.render_template("{% load insight_tags %}{% infinite_scroll config %}", {"config": config})
        feed = BeautifulSoup(rendered, "html.parser").find("div", {"role": "feed"})
        button = feed.find("button")

        assert button["hx-indicator"] == "next .htmx-indicator"
        assert "htmx-indicator" in button.find_next(class_="htmx-indicator")["class"]
