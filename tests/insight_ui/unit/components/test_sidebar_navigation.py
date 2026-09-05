"""Tests for sidebar navigation markup."""

import pytest
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
