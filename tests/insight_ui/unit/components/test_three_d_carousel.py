# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for the three_d_carousel component."""

import pytest
from bs4 import BeautifulSoup
from django.test import override_settings
from insight_ui.configs import CardConfig, ThreeDCarouselConfig

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


def cards(*titles: str) -> list[CardConfig]:
    """Return a card per title."""
    return [CardConfig(title=title, content="") for title in titles]


class TestThreeDCarousel(TemplateTagsTestCase):
    """Test suite for the three_d_carousel component."""

    def render_carousel(self, config: ThreeDCarouselConfig, **context: object) -> BeautifulSoup:
        """Render the tag with the config and return the parsed HTML."""
        rendered = self.render_template(
            "{% load insight_tags %}{% three_d_carousel config %}", {"config": config, **context}
        )
        return BeautifulSoup(rendered, "html.parser")

    def test_cards_are_the_default_items(self) -> None:
        """Without an item template, each item is rendered as a card."""
        config = ThreeDCarouselConfig(tag_id="ring", items=cards("First", "Second"))
        fronts = self.render_carousel(config).select(".three-d-carousel-front")

        assert [front.get_text(" ", strip=True) for front in fronts] == ["First", "Second"]

    @override_settings(TEMPLATES=CUSTOM_ITEM_TEMPLATES)
    def test_custom_item_template_gets_item_and_page_context(self) -> None:
        """Own content is rendered with the item template, which also sees the variables of the page."""
        config = ThreeDCarouselConfig(tag_id="ring", items=[{"name": "Lamp"}], item_template="shop/product_slide.html")
        product = self.render_carousel(config, customer="Ada").select_one(".three-d-carousel-front .product")

        assert product.get_text() == "Lamp for Ada"

    def test_carousel_and_items_are_labelled(self) -> None:
        """The carousel is a named region and every item names its position."""
        config = ThreeDCarouselConfig(tag_id="ring", items=cards("A", "B"), label="Products")
        soup = self.render_carousel(config)
        region = soup.select_one("[data-insight-3D-carousel]")

        assert region["id"] == "ring"
        assert region["role"] == "region"
        assert region["aria-label"] == "Products"
        assert [item["aria-label"] for item in soup.select("[aria-roledescription='slide']")] == ["1 of 2", "2 of 2"]

    def test_unlabelled_carousel_gets_a_default_name(self) -> None:
        """A carousel without label still has an accessible name."""
        region = self.render_carousel(ThreeDCarouselConfig(tag_id="ring")).select_one("[data-insight-3D-carousel]")

        assert region["aria-label"] == "3D carousel"

    def test_back_of_an_item_is_hidden_from_screen_readers(self) -> None:
        """The solid back is decoration only."""
        back = self.render_carousel(ThreeDCarouselConfig(tag_id="ring", items=cards("A"))).select_one(
            ".three-d-carousel-back"
        )

        assert back["aria-hidden"] == "true"

    def test_ring_options_are_passed_to_the_script(self) -> None:
        """The script reads tilt and camera mode from data attributes; the duration drives the transitions."""
        config = ThreeDCarouselConfig(tag_id="ring", items=cards("A"), tilt=15, face_camera=True, duration=800)
        region = self.render_carousel(config).select_one("[data-insight-3D-carousel]")

        assert region["data-tilt"] == "15"
        assert region["data-face-camera"] == "true"
        assert "--insight-3d-carousel-duration: 800ms" in region["style"]

    def test_controls_need_more_than_one_item(self) -> None:
        """A single item cannot turn, so the controls and the position are left out."""
        single = self.render_carousel(ThreeDCarouselConfig(tag_id="ring", items=cards("A")))
        several = self.render_carousel(ThreeDCarouselConfig(tag_id="ring", items=cards("A", "B")))

        assert single.select_one(".three-d-carousel-next") is None
        assert several.select_one(".three-d-carousel-next") is not None
        assert several.select_one(".three-d-carousel-status")["aria-live"] == "polite"

    def test_items_can_be_passed_as_tag_argument(self) -> None:
        """Items can be passed directly to the tag without a config."""
        rendered = self.render_template(
            '{% load insight_tags %}{% three_d_carousel tag_id="ring" items=cards %}', {"cards": cards("Solo")}
        )
        front = BeautifulSoup(rendered, "html.parser").select_one(".three-d-carousel-front")

        assert front.get_text(strip=True) == "Solo"


def test_item_template_must_not_be_empty() -> None:
    """Without a template the items could not be rendered."""
    with pytest.raises(ValueError, match="requires a non-empty item_template"):
        ThreeDCarouselConfig(tag_id="ring", item_template="")


def test_duration_must_not_be_negative() -> None:
    """A turn cannot take less than no time."""
    with pytest.raises(ValueError, match="duration"):
        ThreeDCarouselConfig(tag_id="ring", duration=-1)
