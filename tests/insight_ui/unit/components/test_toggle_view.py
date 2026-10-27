# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for the toggle_view component."""

from bs4 import BeautifulSoup
from insight_ui.configs import HtmxConfig, RadioBlockConfig, RadioItemConfig, TableConfig, ToggleViewConfig

from tests.insight_ui.unit.components.test_template_tags import TemplateTagsTestCase


class TestToggleView(TemplateTagsTestCase):
    """Test suite for the toggle_view component."""

    def render_view(self, **switch_options: object) -> BeautifulSoup:
        """Render a toggle view whose view switch gets the given options."""
        config = ToggleViewConfig(
            tag_id="products",
            table=TableConfig(headers=["Name"], rows=[["Lamp"]]),
            view_switch=RadioBlockConfig(
                name="view",
                items=[RadioItemConfig(value="card"), RadioItemConfig(value="table")],
                current_value="table",
                **switch_options,
            ),
        )
        rendered = self.render_template("{% load insight_tags %}{% toggle_view config %}", {"config": config})
        return BeautifulSoup(rendered, "html.parser")

    def test_switching_the_view_replaces_the_whole_component(self) -> None:
        """With a request_url the view switch reloads and replaces the toggle view itself."""
        radios = self.render_view(request_url="/products/").find_all("input", type="radio")

        for radio in radios:
            assert radio["hx-get"] == "/products/"
            assert radio["hx-target"] == "#products"
            assert radio["hx-swap"] == "outerHTML"

    def test_shared_htmx_options_of_the_view_switch_are_kept(self) -> None:
        """Target and swap are fixed by the toggle view; other options of the switch's HtmxConfig stay."""
        soup = self.render_view(
            request_url="/products/", htmx=HtmxConfig(target="#elsewhere", swap_method="innerHTML", push_url=True)
        )
        radio = soup.find("input", type="radio")

        assert radio["hx-target"] == "#products"
        assert radio["hx-swap"] == "outerHTML"
        assert radio["hx-push-url"] == "true"

    def test_without_request_url_no_request_is_sent(self) -> None:
        """Without a URL there is nothing to load, so the switch renders no HTMX attributes."""
        soup = self.render_view()

        assert not soup.find(attrs={"hx-get": True})
