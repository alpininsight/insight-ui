# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for the radio_block component."""

import pytest
from bs4 import BeautifulSoup
from insight_ui.configs import HtmxConfig, RadioBlockConfig, RadioItemConfig

from tests.insight_ui.unit.components.test_template_tags import TemplateTagsTestCase


class TestRadioBlock(TemplateTagsTestCase):
    """Test suite for the radio_block component."""

    def test_radio_block(self) -> None:
        """Test the {% radio_block %} tag with HTMX attributes."""
        # Create a test config with HTMX attributes (not using demo context)
        config = RadioBlockConfig(
            "size",
            "Select size:",
            items=[
                RadioItemConfig("small", "small-size", "s"),
                RadioItemConfig("medium", "medium-size", "m"),
                RadioItemConfig("large", "large-size", "l", disabled=True),
            ],
            as_row=True,
            request_url="/api/size/",
            htmx=HtmxConfig(target="#size-target", swap_method="outerHTML"),
            method="onSizeChange",
        )

        template_string = """
        {% load insight_tags %}
        {% radio_block config %}
        """

        rendered = self.render_template(template_string, {"config": config})
        soup = BeautifulSoup(rendered, "html.parser")

        wrapper = soup.find("fieldset")

        # Check label (legend element for accessibility)
        legend = wrapper.find("legend")
        assert legend.text.strip() == "Select size:"

        form = wrapper.find("form", id="size")
        assert form is not None

        # Check count of radios
        inputs = form.find_all("input", type="radio")
        labels = form.find_all("label")
        assert len(inputs) == 3  # noqa: PLR2004

        # First radio
        assert inputs[0]["id"] == "size-small-size"
        assert inputs[0]["name"] == "size"
        assert inputs[0]["value"] == "small"
        assert inputs[0].has_attr("checked")
        assert not inputs[0].has_attr("disabled")
        assert inputs[0]["hx-get"] == "/api/size/"
        assert inputs[0]["hx-target"] == "#size-target"
        assert inputs[0]["hx-swap"] == "outerHTML"
        assert inputs[0].has_attr("data-radio-callback")
        assert labels[0]["for"] == "size-small-size"
        assert labels[0].get_text().strip() == "s"

        # Second radio
        assert inputs[1]["id"] == "size-medium-size"
        assert inputs[1]["name"] == "size"
        assert inputs[1]["value"] == "medium"
        assert not inputs[1].has_attr("checked")
        assert not inputs[1].has_attr("disabled")
        assert labels[1]["for"] == "size-medium-size"
        assert labels[1].get_text().strip() == "m"

        # Third radio
        assert inputs[2]["id"] == "size-large-size"
        assert inputs[2]["name"] == "size"
        assert inputs[2]["value"] == "large"
        assert not inputs[2].has_attr("checked")
        assert inputs[2].has_attr("disabled")
        assert labels[2]["for"] == "size-large-size"
        assert labels[2].get_text().strip() == "l"

    def test_radio_block_config_rejects_current_value_not_matching_items(self) -> None:
        """RadioBlockConfig raises ValueError when current_value matches no item."""
        with pytest.raises(ValueError, match="current_value"):
            RadioBlockConfig(
                name="view",
                items=[RadioItemConfig(value="card")],
                current_value="table",
            )

    def test_radio_block_uses_value_as_accessible_name_for_icon_only_items(self) -> None:
        """Icon-only controls retain a stable label and input ID."""
        config = RadioBlockConfig(name="view", items=[RadioItemConfig(value="card")])

        rendered = self.render_template("{% load insight_tags %}{% radio_block config %}", {"config": config})
        soup = BeautifulSoup(rendered, "html.parser")

        radio = soup.find("input", {"type": "radio"})
        label = soup.find("label")
        assert radio["id"] == "view-card"
        assert radio["aria-label"] == "card"
        assert label["for"] == "view-card"

    def test_radio_block_without_htmx_sends_no_request(self) -> None:
        """HTMX is opt-in: without an HtmxConfig the options only change the value."""
        config = RadioBlockConfig(name="view", items=[RadioItemConfig(value="card")], request_url="/products/")

        rendered = self.render_template("{% load insight_tags %}{% radio_block config %}", {"config": config})

        assert "hx-" not in rendered

    def test_radio_block_htmx_options_reach_the_options(self) -> None:
        """Shared request options of the HtmxConfig are rendered on every option."""
        config = RadioBlockConfig(
            name="view",
            items=[RadioItemConfig(value="card"), RadioItemConfig(value="table")],
            request_url="/products/",
            htmx=HtmxConfig(target="#products", push_url=True, loading_indicator_id="#spinner"),
        )

        rendered = self.render_template("{% load insight_tags %}{% radio_block config %}", {"config": config})
        radios = BeautifulSoup(rendered, "html.parser").find_all("input", type="radio")

        for radio in radios:
            assert radio["hx-get"] == "/products/"
            assert radio["hx-target"] == "#products"
            assert radio["hx-swap"] == "innerHTML"
            assert radio["hx-push-url"] == "true"
            assert radio["hx-indicator"] == "#spinner"

    def test_radio_block_htmx_can_bring_its_own_url(self) -> None:
        """htmx.request_url is used when the block has no request_url."""
        config = RadioBlockConfig(
            name="view", items=[RadioItemConfig(value="card")], htmx=HtmxConfig("/products/", target="#products")
        )

        rendered = self.render_template("{% load insight_tags %}{% radio_block config %}", {"config": config})

        assert BeautifulSoup(rendered, "html.parser").find("input", type="radio")["hx-get"] == "/products/"


@pytest.mark.parametrize(
    ("options", "message"),
    [
        pytest.param(
            {"request_url": "/products/", "htmx": HtmxConfig(target="#products"), "integrated": True},
            "integrated",
            id="integrated",
        ),
        pytest.param({"htmx": HtmxConfig(target="#products")}, "request_url", id="no-url"),
        pytest.param({"request_url": "/products/", "htmx": HtmxConfig()}, "htmx.target", id="no-target"),
    ],
)
def test_radio_block_rejects_htmx_that_would_not_work(options: dict, message: str) -> None:
    """An integrated block, a missing URL or a missing target would make the request a no-op or swap the radio."""
    with pytest.raises(ValueError, match=message):
        RadioBlockConfig(name="view", items=[RadioItemConfig(value="card")], **options)
