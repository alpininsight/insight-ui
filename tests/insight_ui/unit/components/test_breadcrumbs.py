# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for the breadcrumbs component."""

from types import ModuleType

import pytest
from bs4 import BeautifulSoup
from django.http import HttpResponse
from django.template import Context, Template
from django.test import override_settings
from django.urls import clear_url_caches, path, reverse_lazy
from django.utils.functional import lazy
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


def test_trail_can_be_configured_before_urlconf_population() -> None:
    """A class-level trail may use reverse_lazy before the application URLs are loaded."""
    urlconf = ModuleType("breadcrumb_lazy_urls")
    urlconf.urlpatterns = []
    with override_settings(ROOT_URLCONF=urlconf):
        config = BreadcrumbsConfig(
            items=[
                BreadcrumbItemConfig(text="Home", request_url=reverse_lazy("home")),
                BreadcrumbItemConfig(text="Now"),
            ]
        )
        urlconf.urlpatterns = [path("home/", lambda _request: HttpResponse("home"), name="home")]
        clear_url_caches()
        rendered = Template("{% load insight_tags %}{% breadcrumbs config=config %}").render(
            Context({"config": config})
        )
        assert BeautifulSoup(rendered, "html.parser").find("a")["href"] == "/home/"
    clear_url_caches()


@pytest.mark.parametrize("url", ["", "javascript:alert(1)"])
def test_lazy_link_url_is_validated_before_rendering(url: str) -> None:
    """Deferring a URL does not permit an empty or unsafe link in the rendered trail."""
    config = BreadcrumbsConfig(
        items=[
            BreadcrumbItemConfig(text="Home", request_url=lazy(lambda: url, str)()),
            BreadcrumbItemConfig(text="Now"),
        ]
    )
    with pytest.raises(ValueError, match=r"needs a request_url|is not allowed"):
        Template("{% load insight_tags %}{% breadcrumbs config=config %}").render(Context({"config": config}))
