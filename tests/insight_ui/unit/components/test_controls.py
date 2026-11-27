# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for the color, selection state and icon-only option of toggle, switch, radio block, slider and dropdown."""

import pytest
from bs4 import BeautifulSoup, Tag
from django.template import Context, Template
from insight_ui.configs import (
    BUTTON_COLOR_VALUES,
    CONTROL_VARIANT_VALUES,
    DropdownConfig,
    IconConfig,
    RadioBlockConfig,
    RadioItemConfig,
    SliderConfig,
    ToggleConfig,
)


def render(template: str, context: dict | None = None) -> BeautifulSoup:
    """Render a template snippet with insight_tags loaded."""
    html = Template("{% load insight_tags %}" + template).render(Context(context or {}))
    return BeautifulSoup(html, "html.parser")


ITEMS = [RadioItemConfig(value="a", label="A"), RadioItemConfig(value="b", label="B")]

# Tag call without color, for each control that takes one.
CONTROLS = [
    pytest.param('{% toggle tag_id="t" name="t" label="Bold"', id="toggle"),
    pytest.param('{% toggle tag_id="t" name="t" label="Bold" switch=True', id="switch"),
    pytest.param('{% radio_block name="view" items=items', id="radio_block"),
    pytest.param('{% slider tag_id="s" name="s" label="Volume"', id="slider"),
]


@pytest.mark.parametrize("tag", CONTROLS)
@pytest.mark.parametrize("color", BUTTON_COLOR_VALUES)
def test_color_selects_the_control_color_class(tag: str, color: str) -> None:
    """The color parameter maps to the control color class that the fill, track and thumb use."""
    soup = render(f'{tag} color="{color}" %}}', {"items": ITEMS})

    assert soup.select_one(f".control-{color}") is not None


@pytest.mark.parametrize("tag", CONTROLS)
def test_controls_default_to_primary(tag: str) -> None:
    """Without a color the controls keep the primary look."""
    assert render(tag + " %}", {"items": ITEMS}).select_one(".control-primary") is not None


@pytest.mark.parametrize(
    "config",
    [
        lambda: ToggleConfig(name="t", color="neutral"),
        lambda: RadioBlockConfig(name="v", items=ITEMS, color="neutral"),
        lambda: SliderConfig(name="s", color="neutral"),
        lambda: DropdownConfig(tag_id="d", title="Menu", color="neutral"),
    ],
)
def test_unknown_colors_are_rejected(config: object) -> None:
    """The controls accept the button colors only."""
    with pytest.raises(ValueError, match="neutral"):
        config()  # type: ignore[operator]


def control_and_label(soup: BeautifulSoup, input_id: str) -> tuple[Tag, Tag]:
    """Return an input and the element right after it, which shows its state."""
    control = soup.find(id=input_id)
    return control, control.find_next_sibling()


def test_toggle_state_comes_from_its_checkbox() -> None:
    """The visible option follows its checkbox, so checked and disabled states reach it."""
    soup = render('{% toggle tag_id="bold" name="bold" label="Bold" checked=True disabled=True disabled_reason="" %}')
    control, label = control_and_label(soup, "bold")

    assert control.has_attr("checked")
    assert control.has_attr("disabled")
    assert "choice" in label["class"]
    assert label.get_text(strip=True) == "Bold"


def test_radio_block_options_follow_their_inputs() -> None:
    """Each option label follows its radio input; a disabled option is a disabled input."""
    items = [
        RadioItemConfig(value="a", label="A"),
        RadioItemConfig(value="b", label="B", disabled=True, disabled_reason=""),
    ]
    soup = render('{% radio_block name="view" items=items current_value="a" %}', {"items": items})

    for value, checked, disabled in (("a", True, False), ("b", False, True)):
        control, label = control_and_label(soup, f"view-{value}")
        assert control.has_attr("checked") is checked
        assert control.has_attr("disabled") is disabled
        assert "choice" in label["class"]


def test_switch_track_follows_its_checkbox_and_is_hidden() -> None:
    """The track is decoration; the checkbox inside the label carries name and state."""
    soup = render('{% toggle tag_id="dark" name="dark" label="Dark mode" switch=True checked=True %}')
    control, track = control_and_label(soup, "dark")

    assert control.find_parent("label").get_text(strip=True) == "Dark mode"
    assert "switch-track" in track["class"]
    assert track["aria-hidden"] == "true"


ICON = IconConfig(name="bold")


def test_icon_only_toggle_names_the_checkbox_with_its_label() -> None:
    """The label stays the accessible name as hidden text and shows as tooltip on hover and focus."""
    soup = render('{% toggle tag_id="bold" name="bold" label="Bold" icon=icon icon_only=True %}', {"icon": ICON})
    control, label = control_and_label(soup, "bold")

    assert label["for"] == "bold"
    assert label.select_one(".sr-only").get_text(strip=True) == "Bold"
    assert control["data-insight-tooltip"] == "Bold"
    assert label.find("svg") is not None


def test_toggle_with_text_has_no_tooltip() -> None:
    """A visible label needs no tooltip."""
    control = render('{% toggle tag_id="bold" name="bold" label="Bold" %}').find(id="bold")

    assert not control.has_attr("data-insight-tooltip")


@pytest.mark.parametrize(
    ("arguments", "message"),
    [
        ({"label": "Bold"}, "needs an icon and a label"),
        ({"icon": ICON}, "needs an icon and a label"),
        ({"label": "Bold", "icon": ICON, "switch": True}, "not to switches"),
    ],
)
def test_icon_only_toggle_needs_an_icon_and_a_label(arguments: dict, message: str) -> None:
    """Without an icon nothing is visible, without a label the toggle has no name."""
    with pytest.raises(ValueError, match=message):
        ToggleConfig(name="bold", icon_only=True, **arguments)


def test_dropdown_passes_color_and_variant_to_its_button() -> None:
    """The trigger is a regular button in the configured look."""
    config = DropdownConfig(tag_id="actions", title="Actions", color="danger", variant="outline")
    button = render("{% dropdown config %}", {"config": config}).find("button")

    assert {"btn-outline", "btn-danger"} <= set(button["class"])


def test_dropdown_rejects_unknown_variants() -> None:
    """Variants are the button variants."""
    with pytest.raises(ValueError, match="variant"):
        DropdownConfig(tag_id="actions", title="Actions", variant="ghost")  # type: ignore[arg-type]


# Tag call of each control that has a variant, and the element that carries the choice classes.
VARIANT_CONTROLS = [
    pytest.param('{% toggle tag_id="t" name="t" label="Bold"', "label", id="toggle"),
    pytest.param('{% radio_block name="view" items=items', "label", id="radio_block"),
]


@pytest.mark.parametrize(("tag", "selector"), VARIANT_CONTROLS)
@pytest.mark.parametrize("variant", CONTROL_VARIANT_VALUES)
def test_variant_selects_the_choice_class(tag: str, selector: str, variant: str) -> None:
    """The variant parameter maps to the choice class that builds the look."""
    soup = render(f'{tag} variant="{variant}" %}}', {"items": ITEMS})

    assert f"choice-{variant}" in soup.select_one(selector)["class"]


@pytest.mark.parametrize(("tag", "selector"), VARIANT_CONTROLS)
def test_controls_default_to_the_neutral_variant(tag: str, selector: str) -> None:
    """Without a variant toggle buttons and radio blocks are neutral."""
    assert "choice-neutral" in render(tag + " %}", {"items": ITEMS}).select_one(selector)["class"]


@pytest.mark.parametrize("variant", CONTROL_VARIANT_VALUES)
def test_radio_block_variant_selects_the_group_class(variant: str) -> None:
    """The options of a radio block share a track (neutral, subtle) or their borders (outline)."""
    soup = render(f'{{% radio_block name="view" items=items variant="{variant}" %}}', {"items": ITEMS})

    assert soup.select_one(f".choice-group-{variant}") is not None


@pytest.mark.parametrize(
    "config",
    [
        lambda: ToggleConfig(name="t", variant="solid"),
        lambda: RadioBlockConfig(name="v", items=ITEMS, variant="solid"),
    ],
)
def test_unknown_variants_are_rejected(config: object) -> None:
    """Toggle buttons and radio blocks accept the control variants only."""
    with pytest.raises(ValueError, match="solid"):
        config()  # type: ignore[operator]


def test_radio_block_option_text_is_read_once() -> None:
    """The semibold width is reserved from an attribute, so the label text is not duplicated."""
    label = render('{% radio_block name="view" items=items %}', {"items": ITEMS}).find("label")

    assert label.get_text(strip=True) == "A"


def test_toggle_text_is_read_once() -> None:
    """The toggle reserves its semibold width the same way."""
    label = render('{% toggle tag_id="t" name="t" label="Bold" %}').find("label")

    assert label.get_text(strip=True) == "Bold"
