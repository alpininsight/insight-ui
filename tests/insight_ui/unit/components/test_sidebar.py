# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for the sidebar layout tag."""

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
        assert "w-156" in rendered

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
