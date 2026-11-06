# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Public dynamic color variants must have rules in the built package CSS."""

import re
from pathlib import Path

import pytest
from bs4 import BeautifulSoup
from django.template import Context, Template
from insight_ui.configs import COLOR_TYPE_VALUES, ICON_COLOR_VALUES

import insight_ui


@pytest.fixture(scope="module")
def built_css() -> str:
    """Read the same compiled stylesheet shipped in the package wheel."""
    return (Path(insight_ui.__file__).parent / "static/insight_ui/css/tailwind.css").read_text()


def assert_color_rule(css: str, class_name: str, property_name: str, token: str) -> None:
    """Require a real declaration, not merely a token or class name mention."""
    pattern = rf"\.{re.escape(class_name)}\s*\{{[^}}]*\b{property_name}:\s*var\(--color-{token}\)"
    assert re.search(pattern, css), f"Missing built CSS rule for {class_name}"


@pytest.mark.parametrize("color", ICON_COLOR_VALUES)
def test_icon_colors_have_built_css(color: str, built_css: str) -> None:
    """Cover every public icon color, including inheritance and text roles."""
    rendered = Template("{% load insight_tags %}{% icon name='check' color=color %}").render(Context({"color": color}))
    classes = BeautifulSoup(rendered, "html.parser").span["class"]
    if not color:
        assert not any(name.startswith("text-insight-") for name in classes)
        return
    # Text roles keep their token; color families use their -text token, which is readable in both themes.
    token = f"insight-{color}" if color.startswith("text-") else f"insight-{color}-text"
    class_name = f"text-{token}"
    assert class_name in classes
    assert_color_rule(built_css, class_name, "color", token)


@pytest.mark.parametrize("color", COLOR_TYPE_VALUES)
@pytest.mark.parametrize("request_url", ["", "/beta/"])
def test_corner_ribbon_colors_have_built_css(color: str, request_url: str, built_css: str) -> None:
    """Every ribbon color fills like a solid button and takes the text color made for that fill."""
    rendered = Template(
        "{% load insight_tags %}{% corner_ribbon text='Beta' color=color request_url=request_url %}"
    ).render(Context({"color": color, "request_url": request_url}))
    soup = BeautifulSoup(rendered, "html.parser")
    ribbon = soup.find("a") if request_url else soup.select_one("[role='status'] div")

    assert f"control-{color}" in ribbon["class"]
    tone = re.search(rf"\.control-{color}\b[^{{]*{{([^}}]*)}}", built_css)
    assert tone, f"Missing built CSS rule for .control-{color}"
    assert "--tone-fill:" in tone.group(1)
    assert "--tone-on-action:" in tone.group(1)
