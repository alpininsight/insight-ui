# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for the carousel component."""

import pytest
from bs4 import BeautifulSoup
from django.test import override_settings
from insight_ui.configs import CardConfig, CarouselConfig, CarouselImageConfig

from tests.insight_ui.unit.components.test_template_tags import TemplateTagsTestCase

CUSTOM_ITEM_TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "OPTIONS": {
            "loaders": [
                (
                    "django.template.loaders.locmem.Loader",
                    {"shop/product_slide.html": "<p class='product'>{{ item.name }} for {{ customer }}</p>"},
                ),
                "django.template.loaders.app_directories.Loader",
            ],
        },
    }
]


class TestCarousel(TemplateTagsTestCase):
    """Test suite for the carousel component."""

    def render_carousel(self, config: CarouselConfig, **context: object) -> BeautifulSoup:
        """Render the carousel tag with the config and return the parsed HTML."""
        rendered = self.render_template("{% load insight_tags %}{% carousel config %}", {"config": config, **context})
        return BeautifulSoup(rendered, "html.parser")

    def test_cards_are_the_default_items(self) -> None:
        """Without an item template, each item is rendered as a card."""
        config = CarouselConfig(items=[CardConfig(title="First", content=""), CardConfig(title="Second", content="")])
        items = self.render_carousel(config).select(".carousel-item")

        assert [item.get_text(" ", strip=True) for item in items] == ["First", "Second"]

    @override_settings(TEMPLATES=CUSTOM_ITEM_TEMPLATES)
    def test_custom_item_template_gets_item_and_page_context(self) -> None:
        """Own content is rendered with the item template, which also sees the variables of the page."""
        config = CarouselConfig(items=[{"name": "Lamp"}], item_template="shop/product_slide.html")
        product = self.render_carousel(config, customer="Ada").select_one(".carousel-item .product")

        assert product.get_text() == "Lamp for Ada"

    def test_image_template_shows_caption_below_the_image(self) -> None:
        """The caption is a figcaption of the image, not text laid over it."""
        config = CarouselConfig(
            items=[CarouselImageConfig(url="/img/lake.jpg", alt="Lake at dawn", caption="Lake Constance")],
            item_template="insight_ui/components/items/image_item.html",
        )
        figure = self.render_carousel(config).select_one(".carousel-item figure")

        assert figure.img["src"] == "/img/lake.jpg"
        assert figure.img["alt"] == "Lake at dawn"
        assert figure.figcaption.get_text(strip=True) == "Lake Constance"

    def test_image_without_caption_has_no_figcaption(self) -> None:
        """An image without caption renders no empty caption."""
        config = CarouselConfig(
            items=[CarouselImageConfig(url="/img/lake.jpg", alt="")],
            item_template="insight_ui/components/items/image_item.html",
        )

        assert self.render_carousel(config).figcaption is None

    def test_carousel_and_items_are_labelled(self) -> None:
        """The carousel is a named region and every item names its position."""
        config = CarouselConfig(
            items=[CardConfig(title="A", content=""), CardConfig(title="B", content="")], label="Products"
        )
        soup = self.render_carousel(config)
        region = soup.select_one("[data-insight-carousel]")

        assert region["role"] == "region"
        assert region["aria-label"] == "Products"
        assert [item["aria-label"] for item in soup.select("[aria-roledescription='slide']")] == ["1 of 2", "2 of 2"]

    def test_unlabelled_carousel_gets_a_default_name(self) -> None:
        """A carousel without label still has an accessible name."""
        region = self.render_carousel(CarouselConfig(items=[])).select_one("[data-insight-carousel]")

        assert region["aria-label"] == "Content carousel"

    def test_page_options_are_passed_to_the_script(self) -> None:
        """The script reads the maximum per page and the minimum item width from data attributes."""
        config = CarouselConfig(items=[], items_per_slide=3, min_item_width="16rem", autoplay=True)
        region = self.render_carousel(config).select_one("[data-insight-carousel]")

        assert region["data-items-per-slide"] == "3"
        assert region["data-min-item-width"] == "16rem"
        assert region["data-autoplay"] == "true"

    def test_dots_and_index_follow_their_switches(self) -> None:
        """Dots are only rendered when switched on; the page number is visible when switched on."""
        soup = self.render_carousel(CarouselConfig(items=[], show_dots=False, show_index=True))

        assert soup.select_one(".carousel-dots") is None
        assert not soup.select_one(".carousel-index-text").has_attr("hidden")

    def test_page_number_waits_hidden_for_dots_that_do_not_fit(self) -> None:
        """Without show_index the page number is hidden; the script shows it when the dots do not fit."""
        soup = self.render_carousel(CarouselConfig(items=[]))

        assert soup.select_one(".carousel-index-text").has_attr("hidden")

    def test_caption_starts_at_the_text_edge_unless_centered(self) -> None:
        """Long captions read better aligned to the start; short ones can be centered."""
        config = CarouselConfig(
            items=[
                CarouselImageConfig(url="/img/a.jpg", alt="", caption="A long caption"),
                CarouselImageConfig(url="/img/b.jpg", alt="", caption="Short", center_caption=True),
            ],
            item_template="insight_ui/components/items/image_item.html",
        )
        start, centered = self.render_carousel(config).select("figcaption")

        assert "text-start" in start["class"]
        assert "text-center" in centered["class"]

    def test_items_can_be_passed_as_tag_argument(self) -> None:
        """Items can be passed directly to the tag without a config."""
        rendered = self.render_template(
            "{% load insight_tags %}{% carousel items=cards %}", {"cards": [CardConfig(title="Solo", content="")]}
        )

        assert BeautifulSoup(rendered, "html.parser").select_one(".carousel-item").get_text(strip=True) == "Solo"


def test_item_template_must_not_be_empty() -> None:
    """Without a template the items could not be rendered."""
    with pytest.raises(ValueError, match="requires a non-empty item_template"):
        CarouselConfig(items=[], item_template="")


def test_at_least_one_item_per_page() -> None:
    """A page shows at least one item."""
    with pytest.raises(ValueError, match="items_per_slide"):
        CarouselConfig(items=[], items_per_slide=0)
