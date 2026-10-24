# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for the sidebar layout tag."""

import pytest
from bs4 import BeautifulSoup
from django.template import Context, Template
from django.template.loader import render_to_string
from insight_ui.config import get_config

from tests.insight_ui.unit.components.test_template_tags import TemplateTagsTestCase


class TestSidebarLayoutTag(TemplateTagsTestCase):
    """Test suite for the sidebar layout tag."""

    def test_sidebar_basic(self) -> None:
        """Test basic sidebar rendering with default side (right)."""
        template_string = """
        {% load layout_tags %}
        {% sidebar %}
            <nav>Navigation content</nav>
        {% endsidebar %}
        """
        rendered = self.render_template(template_string)
        assert "Navigation content" in rendered
        assert 'data-insight-sidebar="right"' in rendered

    def test_sidebar_right_side(self) -> None:
        """Test sidebar on the right side."""
        template_string = """
        {% load layout_tags %}
        {% sidebar %}
            <div>TOC content</div>
        {% endsidebar %}
        """
        rendered = self.render_template(template_string)
        assert "TOC content" in rendered
        assert 'data-insight-sidebar="right"' in rendered

    def test_sidebar_width_narrow(self) -> None:
        """Test narrow sidebar width."""
        template_string = """
        {% load layout_tags %}
        {% sidebar width="narrow" %}
            Content
        {% endsidebar %}
        """
        rendered = self.render_template(template_string)
        assert "w-56" in rendered

    def test_sidebar_width_wide(self) -> None:
        """Test wide sidebar width."""
        template_string = """
        {% load layout_tags %}
        {% sidebar width="wide" %}
            Content
        {% endsidebar %}
        """
        rendered = self.render_template(template_string)
        assert "w-96" in rendered

    def test_sidebar_drawer_mode(self) -> None:
        """Test non-static (drawer) sidebar."""
        template_string = """
        {% load layout_tags %}
        {% sidebar static=False %}
            Drawer content
        {% endsidebar %}
        """
        rendered = self.render_template(template_string)
        assert "Drawer content" in rendered
        assert 'data-static="false"' in rendered

    def test_sidebar_mobile_drawer(self) -> None:
        """Test mobile drawer behavior for static sidebars."""
        template_string = """
        {% load layout_tags %}
        {% sidebar mobile_behavior="drawer" %}
            Content
        {% endsidebar %}
        """
        rendered = self.render_template(template_string)
        assert 'data-mobile-behavior="drawer"' in rendered
        # Should have mobile toggle button
        assert 'data-sidebar-toggle="right"' in rendered

    def test_sidebar_with_content(self) -> None:
        """Test sidebar with custom content."""
        template_string = """
        {% load layout_tags %}
        {% sidebar side="left" %}
            <h2>Navigation</h2>
            <nav>
                <ul>
                    <li><a href="/button">Button</a></li>
                </ul>
            </nav>
        {% endsidebar %}
        """
        rendered = self.render_template(template_string)
        assert "Navigation" in rendered
        assert "Button" in rendered
        assert 'href="/button"' in rendered

    def test_sidebar_auto_side_from_context(self) -> None:
        """Test that sidebar infers side from _sidebar_side context variable."""
        template_string = """
        {% load layout_tags %}
        {% sidebar %}
            Content
        {% endsidebar %}
        """
        # Without context variable, defaults to "right"
        rendered = self.render_template(template_string)
        assert 'data-insight-sidebar="right"' in rendered

        # With _sidebar_side="left" in context (as set by base.html sidebar blocks)
        rendered = self.render_template(template_string, {"_sidebar_side": "left"})
        assert 'data-insight-sidebar="left"' in rendered

        # With _sidebar_side="right" in context
        rendered = self.render_template(template_string, {"_sidebar_side": "right"})
        assert 'data-insight-sidebar="right"' in rendered

    def test_sidebar_explicit_side_overrides_context(self) -> None:
        """Test that explicit side parameter overrides context variable."""
        template_string = """
        {% load layout_tags %}
        {% sidebar side="right" %}
            Content
        {% endsidebar %}
        """
        # Even with _sidebar_side="left", explicit side="right" wins
        rendered = self.render_template(template_string, {"_sidebar_side": "left"})
        assert 'data-insight-sidebar="right"' in rendered


def render_sidebar(arguments: str) -> str:
    """Render a sidebar with the given tag arguments."""
    return Template("{% load layout_tags %}{% sidebar " + arguments + " %}Content{% endsidebar %}").render(Context())


def test_fit_width_follows_the_content_up_to_wide_by_default() -> None:
    """width="fit" sizes the sidebar to its content, capped at the wide width."""
    aside = BeautifulSoup(render_sidebar('width="fit"'), "html.parser").find("aside")

    assert {"w-fit", "max-w-96"} <= set(aside["class"])
    assert not any(cls.startswith("min-w-") for cls in aside["class"])


def test_fit_width_takes_lower_and_upper_limits() -> None:
    """min_width and max_width use the named sidebar widths."""
    aside = BeautifulSoup(render_sidebar('width="fit" min_width="narrow" max_width="normal"'), "html.parser").aside

    assert {"w-fit", "min-w-56", "max-w-72"} <= set(aside["class"])


@pytest.mark.parametrize(
    ("arguments", "message"),
    [
        pytest.param('width="normal" max_width="wide"', 'only apply to width="fit"', id="limit-without-fit"),
        pytest.param('min_width="narrow"', 'only apply to width="fit"', id="limit-with-default-width"),
        pytest.param('width="fit" min_width="wide" max_width="narrow"', "wider than max_width", id="min-above-max"),
        pytest.param('width="fit" max_width="300px"', "Invalid max_width", id="free-css-value"),
    ],
)
def test_invalid_width_limits_fail_clearly(arguments: str, message: str) -> None:
    """Limits that would be ignored or contradict each other raise instead."""
    with pytest.raises(ValueError, match=message):
        render_sidebar(arguments)


def test_content_column_fills_the_sidebar_height() -> None:
    """The content column is at least as tall as the sidebar, so mt-auto pushes content to the bottom."""
    soup = BeautifulSoup(render_sidebar('mobile_behavior="drawer"'), "html.parser")

    assert all("min-h-full" in aside.find("div")["class"] for aside in soup.find_all("aside"))


def test_base_aside_columns_do_not_shrink_fit_width_sidebars() -> None:
    """The base layout preserves the intrinsic width selected by a sidebar."""
    soup = BeautifulSoup(render_to_string("insight_ui/base.html", get_config()), "html.parser")

    assert "shrink-0" in soup.find(id="left-aside")["class"]
    assert "shrink-0" in soup.find(id="right-aside")["class"]
