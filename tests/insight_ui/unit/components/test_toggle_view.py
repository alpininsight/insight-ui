# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for the toggle_view component."""

from pathlib import Path

import pytest
from bs4 import BeautifulSoup
from django.conf import settings
from django.template import Context, Template
from django.test import override_settings
from insight_ui.configs import CardConfig, HtmxConfig, RadioBlockConfig, RadioItemConfig, TableConfig, ToggleViewConfig

from tests.insight_ui.unit.components.test_template_tags import TemplateTagsTestCase


def switch(*views: str, current: str = "", **options: object) -> RadioBlockConfig:
    """Build a view switch that offers the given views."""
    return RadioBlockConfig(
        name="view", items=[RadioItemConfig(value=view) for view in views], current_value=current, **options
    )


def render(config: ToggleViewConfig, **context: object) -> BeautifulSoup:
    """Render a toggle view with the given config and page context."""
    html = Template("{% load insight_tags %}{% toggle_view config %}").render(Context({"config": config, **context}))
    return BeautifulSoup(html, "html.parser")


TABLE = TableConfig(headers=["Name"], rows=[["Lamp"]])
CARDS = [CardConfig(title="Lamp", content="Brass", heading_level=4), CardConfig(title="Chair", content="Oak")]


class TestToggleView(TemplateTagsTestCase):
    """The view switch reloads the whole component through HTMX."""

    def render_view(self, **switch_options: object) -> BeautifulSoup:
        """Render a toggle view whose view switch gets the given options."""
        config = ToggleViewConfig(
            tag_id="products", table=TABLE, view_switch=switch("grid", "table", current="table", **switch_options)
        )
        return render(config)

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


def test_grid_renders_cards_with_all_their_fields() -> None:
    """The default item template renders each CardConfig as a full card, heading level included."""
    soup = render(ToggleViewConfig(tag_id="products", items=CARDS, view_switch=switch("grid", "table"), table=TABLE))

    assert [heading.get_text(strip=True) for heading in soup.find_all("h4")] == ["Lamp"]
    assert soup.find("h3").get_text(strip=True) == "Chair"
    assert soup.find("table") is None


def test_grid_renders_own_items_with_the_item_template(tmp_path: Path) -> None:
    """Any objects work as items; the item template sees the item and the page context."""
    (tmp_path / "product_tile.html").write_text("{{ item.name }} for {{ customer }}", encoding="utf-8")
    templates = [{**settings.TEMPLATES[0], "DIRS": [tmp_path, *settings.TEMPLATES[0].get("DIRS", [])]}]
    config = ToggleViewConfig(
        tag_id="products",
        items=[{"name": "Lamp"}, {"name": "Chair"}],
        item_template="product_tile.html",
        view_switch=switch("grid"),
    )
    with override_settings(TEMPLATES=templates):
        soup = render(config, customer="Ada")

    assert soup.find(attrs={"data-toggle-view-content": True}).get_text(" ", strip=True) == "Lamp for Ada Chair for Ada"


def test_grid_uses_the_minimum_item_width() -> None:
    """min_item_width sets how narrow an item may get before the grid drops a column."""
    config = ToggleViewConfig(tag_id="products", items=CARDS, view_switch=switch("grid"), min_item_width="12rem")

    grid = render(config).find(attrs={"data-toggle-view-content": True}).find("div")
    assert grid["style"] == "--item-min-width: 12rem"


def test_selected_table_view_renders_the_table() -> None:
    """The view switch's current value picks the view."""
    soup = render(
        ToggleViewConfig(
            tag_id="products", items=CARDS, table=TABLE, view_switch=switch("grid", "table", current="table")
        )
    )

    assert soup.find("table") is not None
    assert soup.find("article") is None


def test_carousel_view_shows_the_items_in_a_carousel() -> None:
    """The carousel gets the same items and item template as the grid."""
    soup = render(ToggleViewConfig(tag_id="products", items=CARDS, view_switch=switch("carousel", "grid")))

    carousel = soup.find(attrs={"data-insight-carousel": True})
    assert carousel is not None
    assert [heading.get_text(strip=True) for heading in carousel.find_all(["h3", "h4"])] == ["Lamp", "Chair"]


def test_first_view_is_shown_when_nothing_is_selected() -> None:
    """Without a current value the first view of the switch is active."""
    soup = render(ToggleViewConfig(tag_id="products", items=CARDS, table=TABLE, view_switch=switch("table", "grid")))

    assert soup.find("table") is not None


@pytest.mark.parametrize("view", ["card", "list", ""])
def test_unknown_view_in_the_switch_is_rejected(view: str) -> None:
    """Each switch value must be one of the views; a typo would otherwise fall back to the table silently."""
    with pytest.raises(ValueError, match="view_switch item value"):
        ToggleViewConfig(tag_id="products", table=TABLE, view_switch=switch("grid", view))


def test_table_view_needs_a_table() -> None:
    """Offering the table view without a table would render an empty table."""
    with pytest.raises(ValueError, match="has no table"):
        ToggleViewConfig(tag_id="products", items=CARDS, view_switch=switch("grid", "table"))


def test_view_switch_is_required() -> None:
    """The switch picks the view, so the component cannot render without it."""
    with pytest.raises(ValueError, match="view_switch"):
        Template('{% load insight_tags %}{% toggle_view tag_id="products" %}').render(Context())
