# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for the breadcrumbs component."""

import pytest
from bs4 import BeautifulSoup
from insight_ui.configs import BreadcrumbItemConfig, BreadcrumbsConfig

from tests.insight_ui.unit.components.test_template_tags import TemplateTagsTestCase


class TestBreadcrumbs(TemplateTagsTestCase):
    """Test suite for the breadcrumbs component."""

    def render_trail(self) -> BeautifulSoup:
        """Render a three-level trail."""
        config = BreadcrumbsConfig(
            items=[
                BreadcrumbItemConfig(text="Home", request_url="/"),
                BreadcrumbItemConfig(text="Products", request_url="/products/"),
                BreadcrumbItemConfig(text="Laptops"),
            ]
        )
        rendered = self.render_template("{% load insight_tags %}{% breadcrumbs config=c %}", {"c": config})
        return BeautifulSoup(rendered, "html.parser")

    def test_trail_is_an_ordered_list_in_a_labelled_navigation(self) -> None:
        """The trail is an ordered list inside a nav landmark named Breadcrumb."""
        soup = self.render_trail()

        nav = soup.find("nav")
        assert nav["aria-label"] == "Breadcrumb"
        assert not nav.has_attr("role")
        assert [li.get_text(strip=True) for li in nav.find("ol").find_all("li")] == ["Home", "Products", "Laptops"]
        assert nav.find("ul") is None

    def test_only_the_last_item_is_the_current_page(self) -> None:
        """Earlier items link to their pages; the last one is marked as current page and is no link."""
        soup = self.render_trail()

        assert [(a.get_text(strip=True), a["href"]) for a in soup.find_all("a")] == [
            ("Home", "/"),
            ("Products", "/products/"),
        ]
        current = soup.find_all(attrs={"aria-current": True})
        assert [element.get_text(strip=True) for element in current] == ["Laptops"]
        assert current[0]["aria-current"] == "page"

    def test_separators_are_hidden_from_assistive_technology(self) -> None:
        """The chevrons between items are decorative."""
        svgs = self.render_trail().find_all("svg")

        assert len(svgs) == 2  # noqa: PLR2004
        assert all(svg["aria-hidden"] == "true" for svg in svgs)


def test_items_before_the_last_need_a_url() -> None:
    """Only the current page may omit its URL; a gap in the trail is rejected."""
    with pytest.raises(ValueError, match="'Products'"):
        BreadcrumbsConfig(items=[BreadcrumbItemConfig(text="Products"), BreadcrumbItemConfig(text="Laptops")])

    BreadcrumbsConfig(items=[BreadcrumbItemConfig(text="Home", request_url="/"), BreadcrumbItemConfig(text="Now")])
    BreadcrumbsConfig(items=[BreadcrumbItemConfig(text="Home")])


def test_items_need_a_label() -> None:
    """An item without text would be an unnamed link."""
    with pytest.raises(ValueError, match="text"):
        BreadcrumbItemConfig(text="", request_url="/")
