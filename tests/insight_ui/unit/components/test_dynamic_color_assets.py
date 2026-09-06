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
    classes = BeautifulSoup(rendered, "html.parser").div["class"]
    if not color:
        assert not any(name.startswith("text-insight-") for name in classes)
        return
    class_name = f"text-insight-{color}"
    assert class_name in classes
    assert_color_rule(built_css, class_name, "color", f"insight-{color}")


@pytest.mark.parametrize("color", COLOR_TYPE_VALUES)
@pytest.mark.parametrize("foreground_color", ["", *COLOR_TYPE_VALUES])
@pytest.mark.parametrize("request_url", ["", "/beta/"])
def test_corner_ribbon_colors_have_built_css(
    color: str, foreground_color: str, request_url: str, built_css: str
) -> None:
    """Cover all background/foreground pairs in passive and linked ribbons."""
    rendered = Template(
        "{% load insight_tags %}"
        "{% corner_ribbon text='Beta' color=color foreground_color=foreground_color request_url=request_url %}"
    ).render(Context({"color": color, "foreground_color": foreground_color, "request_url": request_url}))
    soup = BeautifulSoup(rendered, "html.parser")
    ribbon = soup.find("a") if request_url else soup.select_one("[role='status'] div")
    classes = ribbon["class"]
    background_variable = "insight-bg-raised" if color == "neutral" else f"insight-{color}"
    if foreground_color == "neutral" or (not foreground_color and color == "neutral"):
        foreground_variable = "insight-text-body"
    else:
        foreground_variable = f"insight-{foreground_color}" if foreground_color else "white"

    assert f"bg-{background_variable}" in classes
    assert f"text-{foreground_variable}" in classes
    assert "bg-insight-neutral" not in classes
    assert "text-insight-neutral" not in classes
    assert_color_rule(built_css, f"bg-{background_variable}", "background-color", background_variable)
    assert_color_rule(built_css, f"text-{foreground_variable}", "color", foreground_variable)
