# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for sidebar navigation markup."""

import re

import pytest
from bs4 import BeautifulSoup
from django.template import Context, Template
from insight_ui.configs import SidebarCategoryConfig, SidebarDataConfig, SidebarItemConfig

from tests.insight_ui.unit.components.test_template_tags import TemplateTagsTestCase


class TestSidebarNavigation(TemplateTagsTestCase):
    """Ensure sidebar navigation only exposes usable links."""

    def test_items_without_a_request_url_are_not_rendered_as_empty_links(self) -> None:
        """Keep invalid sidebar configuration from creating unnamed empty targets."""
        with pytest.warns(UserWarning, match="has no request_url set"):
            sidebar_data = SidebarDataConfig(
                links=[
                    SidebarItemConfig(text="Hidden top-level item"),
                    SidebarItemConfig(text="Visible top-level item", request_url="/top-level/"),
                ],
                categories=[
                    SidebarCategoryConfig(
                        caption="Navigation",
                        items=[
                            SidebarItemConfig(text="Hidden category item"),
                            SidebarItemConfig(text="Visible category item", request_url="/category/"),
                        ],
                    )
                ],
            )

        rendered = self.render_template(
            '{% include "insight_ui/components/sidebar_nav.html" with sidebar_data=sidebar_data %}',
            {"sidebar_data": sidebar_data},
        )

        assert 'href=""' not in rendered
        assert 'href="/top-level/"' in rendered
        assert 'href="/category/"' in rendered
        assert "Hidden top-level item" not in rendered
        assert "Hidden category item" not in rendered


def _render_sidebar(sidebar_data: SidebarDataConfig) -> BeautifulSoup:
    """Render the sidebar navigation partial."""
    html = Template('{% include "insight_ui/components/sidebar_nav.html" with sidebar_data=sidebar_data %}').render(
        Context({"sidebar_data": sidebar_data})
    )
    return BeautifulSoup(html, "html.parser")


def _headings(soup: BeautifulSoup) -> list[tuple[str, str]]:
    """Return (hook, tag name) of every heading in document order."""
    return [(h["data-sidebar-heading"], h.name) for h in soup.find_all(re.compile(r"^h[1-6]$"))]


CATEGORY = SidebarCategoryConfig(caption="Components", items=[SidebarItemConfig(text="Button", request_url="/button/")])


@pytest.mark.parametrize(
    ("title", "categories_title", "expected"),
    [
        pytest.param(
            "Docs",
            "Reference",
            [("title", "h2"), ("categories-title", "h3"), ("category", "h4")],
            id="title-and-categories-title",
        ),
        pytest.param("Docs", "", [("title", "h2"), ("category", "h3")], id="title-only"),
        pytest.param("", "Reference", [("categories-title", "h2"), ("category", "h3")], id="categories-title-only"),
        pytest.param("", "", [("category", "h2")], id="no-titles"),
    ],
)
def test_heading_levels_never_skip_a_level(title: str, categories_title: str, expected: list) -> None:
    """Each heading sits exactly one level below the previous rendered one (axe heading-order)."""
    soup = _render_sidebar(SidebarDataConfig(title=title, categories_title=categories_title, categories=[CATEGORY]))

    assert _headings(soup) == expected


def test_heading_look_does_not_depend_on_the_level() -> None:
    """A category heading keeps its classes whether it renders as h2, h3 or h4."""
    variants = [
        SidebarDataConfig(title="Docs", categories_title="Reference", categories=[CATEGORY]),
        SidebarDataConfig(categories=[CATEGORY]),
    ]

    classes = {tuple(_render_sidebar(v).find(attrs={"data-sidebar-heading": "category"})["class"]) for v in variants}

    assert len(classes) == 1
