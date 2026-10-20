# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for button colors, variants and states and the matching badge options."""

import pytest
from bs4 import BeautifulSoup
from django.template import Context, Template
from insight_ui.configs import BUTTON_COLOR_VALUES, BadgeConfig, HtmxConfig, RadioBlockConfig, RadioItemConfig


def render(template: str, context: dict | None = None) -> BeautifulSoup:
    """Render a template snippet with insight_tags loaded."""
    html = Template("{% load insight_tags %}" + template).render(Context(context or {}))
    return BeautifulSoup(html, "html.parser")


def button_classes(arguments: str) -> list[str]:
    """Render a button and return the classes of the button or link element."""
    soup = render(f'{{% button label="Save" {arguments} %}}')
    return (soup.find("button") or soup.find("a"))["class"]


@pytest.mark.parametrize("color", BUTTON_COLOR_VALUES)
@pytest.mark.parametrize("variant", ["outline", "subtle"])
def test_colored_variants_combine_a_variant_and_a_color_class(color: str, variant: str) -> None:
    """The variant class builds the look from the color class."""
    classes = button_classes(f'color="{color}" variant="{variant}"')

    assert {"btn", f"btn-{variant}", f"btn-{color}"} <= set(classes)


@pytest.mark.parametrize("color", BUTTON_COLOR_VALUES)
def test_solid_needs_no_variant_class(color: str) -> None:
    """Solid is the default look of .btn, so only the color class is rendered."""
    classes = button_classes(f'color="{color}" variant="solid"')

    assert {"btn", f"btn-{color}"} <= set(classes)
    assert not [c for c in classes if c in {"btn-solid", "btn-outline", "btn-subtle", "btn-link", "btn-plain"}]


def test_solid_primary_is_the_default() -> None:
    """Without color and variant a button is a filled primary button."""
    classes = button_classes("")

    assert "btn-primary" in classes
    assert "btn-solid" not in classes


@pytest.mark.parametrize("variant", ["link", "plain"])
def test_link_and_plain_ignore_the_color(variant: str) -> None:
    """Link and plain use the link or text color, so no color class is rendered."""
    classes = button_classes(f'color="danger" variant="{variant}"')

    assert f"btn-{variant}" in classes
    assert not [c for c in classes if c in {f"btn-{color}" for color in BUTTON_COLOR_VALUES}]


def test_disabled_button_keeps_its_color_and_uses_the_attribute() -> None:
    """The disabled look comes from the attribute, so a script can enable the button again."""
    soup = render('{% button label="Delete" color="danger" disabled=True disabled_reason="" %}')
    button = soup.find("button")

    assert button.has_attr("disabled")
    assert "btn-danger" in button["class"]
    assert "btn-disabled" not in button["class"]


def test_disabled_link_is_aria_disabled_without_href_or_requests() -> None:
    """Browsers do not block clicks on links, so a disabled link drops href and hx attributes."""
    soup = render('{% button label="Docs" request_url="/docs/" hx_get="/docs/" disabled=True disabled_reason="" %}')
    link = soup.find("a")

    assert link["aria-disabled"] == "true"
    assert not link.has_attr("href")
    assert not link.has_attr("hx-get")


def test_aria_and_hx_arguments_keep_their_prefix() -> None:
    """aria_* and hx_* arguments render as aria-* and hx-* attributes."""
    button = render('{% button label="Menu" aria_expanded="false" hx_get="/menu/" %}').find("button")

    assert button["aria-expanded"] == "false"
    assert button["hx-get"] == "/menu/"


def test_data_attributes_reject_other_prefixes() -> None:
    """Only data, aria and hx attributes can be rendered from DataAttrConfig lists."""
    with pytest.raises(ValueError, match="Invalid attribute prefix 'on'"):
        render('{% data_attributes attrs prefix="on" %}', {"attrs": []})


def test_alert_close_button_uses_the_plain_variant() -> None:
    """The close icon takes the text color, so it stays visible on every alert color."""
    button = render('{% alert message="Saved" severity="success" %}').find("button", attrs={"aria-label": "Close"})

    assert "btn-plain" in button["class"]


# --- Badges ------------------------------------------------------------------


def test_badge_renders_its_color_class() -> None:
    """The badge color is a class of its own."""
    badge = render('{% badge label="New" color="success" %}').find(class_="badge")

    assert "badge-success" in badge["class"]
    assert "badge-disabled" not in badge["class"]


def test_disabled_badge_is_dimmed_and_disables_its_remove_button() -> None:
    """A disabled badge cannot be removed."""
    config = BadgeConfig(label="Draft", disabled=True, remove_htmx=HtmxConfig("/filters/", target="#list"))
    soup = render("{% badge config=config %}", {"config": config})

    assert "badge-disabled" in soup.find(class_="badge")["class"]
    assert soup.find("button").has_attr("disabled")


@pytest.mark.parametrize(("color", "button_class"), [("neutral", "btn-plain"), ("danger", "btn-danger")])
def test_remove_button_follows_the_badge_color(color: str, button_class: str) -> None:
    """The remove icon matches the badge; neutral has no button color and uses the text color."""
    config = BadgeConfig(label="Tag", color=color, remove_htmx=HtmxConfig("/filters/", target="#list"))
    button = render("{% badge config=config %}", {"config": config}).find("button")

    assert button_class in button["class"]


# --- Button-styled form controls ----------------------------------------------


def test_disabled_radio_block_option_uses_the_disabled_state_class() -> None:
    """Labels cannot be disabled natively, so they carry the state class."""
    config = RadioBlockConfig(
        name="view",
        items=[
            RadioItemConfig(value="a", label="A"),
            RadioItemConfig(value="b", label="B", disabled=True, disabled_reason=""),
        ],
    )
    labels = render("{% radio_block config=config %}", {"config": config}).find_all("label")

    assert "btn-disabled" not in labels[0]["class"]
    assert "btn-disabled" in labels[1]["class"]


def test_disabled_toggle_button_uses_the_disabled_state_class() -> None:
    """The button-styled toggle looks disabled when its checkbox is disabled."""
    soup = render('{% toggle tag_id="t" name="t" label="Bold" disabled=True disabled_reason="" %}')

    assert "btn-disabled" in soup.find("label")["class"]
