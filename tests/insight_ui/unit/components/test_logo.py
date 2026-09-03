"""Tests for the logo component."""

from bs4 import BeautifulSoup
from insight_ui.configs.base import IconConfig
from insight_ui.configs.utils import LogoConfig

from tests.insight_ui.unit.components.test_template_tags import TemplateTagsTestCase


class TestLogo(TemplateTagsTestCase):
    """Test suite for the logo component."""

    def test_logo_renders_svg_asset(self) -> None:
        """SVG logo assets should render as static image tags."""
        template_string = """
        {% load insight_tags %}
        {% logo url="insight_ui/svg/insight-ui-logo.svg" alt="Insight UI Logo" height="3rem" %}
        """
        rendered = self.render_template(template_string)
        soup = BeautifulSoup(rendered, "html.parser")

        logo = soup.find("img")
        assert logo is not None
        assert logo.name == "img"
        assert logo.get("src") == "/static/insight_ui/svg/insight-ui-logo.svg"
        assert logo.get("alt") == "Insight UI Logo"
        assert "height: 3rem" in logo.get("style")

    def test_logo_renders_dark_variant(self) -> None:
        """Dark logo variants should render two images with theme-switching classes."""
        config = LogoConfig("light.png", "dark.png", "Insight UI Logo")
        template_string = """
        {% load insight_tags %}
        {% logo config=config %}
        """
        rendered = self.render_template(template_string, context={"config": config})
        soup = BeautifulSoup(rendered, "html.parser")

        logos = soup.find_all("img")
        assert len(logos) == 2  # noqa: PLR2004
        assert logos[0].get("src") == "/static/light.png"
        assert logos[1].get("src") == "/static/dark.png"
        # Theme-switching requires these Tailwind classes to show/hide variants
        assert "dark:hidden" in logos[0].get("class", [])
        assert "dark:inline-block" in logos[1].get("class", [])

    def test_logo_renders_icon(self) -> None:
        """Icon logos should use the existing Insight UI icon set."""
        config = LogoConfig(icon=IconConfig("sparkles", "xl"), alt="Decorative product icon")
        template_string = """
        {% load insight_tags %}
        {% logo config=config %}
        """
        rendered = self.render_template(template_string, context={"config": config})
        soup = BeautifulSoup(rendered, "html.parser")

        wrapper = soup.find("span", attrs={"role": "img", "aria-label": "Decorative product icon"})
        assert wrapper is not None
        assert wrapper.find("svg") is not None
