"""Tests for the corner_ribbon component."""

from bs4 import BeautifulSoup
from insight_ui.configs.utils import CornerRibbonConfig

from tests.unit.components.test_template_tags import TemplateTagsTestCase


class TestCornerRibbon(TemplateTagsTestCase):
    """Test suite for the corner_ribbon component."""

    def test_default_ribbon_is_a_non_blocking_top_right_site_status(self) -> None:
        """Default ribbon crosses the right page edge without changing layout."""
        rendered = self.render_template('{% load insight_tags %}{% corner_ribbon text="This service is in beta." %}')
        soup = BeautifulSoup(rendered, "html.parser")

        status = soup.find(role="status")
        assert status is not None
        assert status.get("aria-live") == "polite"
        assert status.get("aria-atomic") == "true"
        assert "fixed" in status.get("class", [])
        assert "top-16" in status.get("class", [])
        assert "ltr:-right-24" in status.get("class", [])
        assert "pointer-events-none" in status.get("class", [])
        assert "This service is in beta." in status.get_text(strip=True)

        ribbon = status.find("div")
        assert ribbon is not None
        assert "ltr:transform-[rotate(45deg)]" in ribbon.get("class", [])
        assert "bg-insight-primary" in ribbon.get("class", [])

    def test_config_renders_the_requested_corner_and_semantic_color(self) -> None:
        """A config object preserves the supported corner and color variants."""
        rendered = self.render_template(
            "{% load insight_tags %}{% corner_ribbon config=config %}",
            context={
                "config": CornerRibbonConfig(
                    text="Maintenance window",
                    position="bottom-left",
                    color="warning",
                )
            },
        )
        soup = BeautifulSoup(rendered, "html.parser")

        status = soup.find(role="status")
        assert status is not None
        assert "bottom-16" in status.get("class", [])
        assert "ltr:-left-24" in status.get("class", [])

        ribbon = status.find("div")
        assert ribbon is not None
        assert "ltr:transform-[rotate(45deg)]" in ribbon.get("class", [])
        assert "bg-insight-warning" in ribbon.get("class", [])
        assert "Maintenance window" in ribbon.get_text(strip=True)
