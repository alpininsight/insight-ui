"""Tests for the navbar component."""

# ruff: noqa: E501

from bs4 import BeautifulSoup
from insight_ui.configs.base import IconConfig
from insight_ui.configs.navigation import NavbarBrandConfig, NavbarConfig, NavbarLinkConfig
from insight_ui.configs.popup import ModalConfig
from insight_ui.configs.utils import BrandLockupConfig, LogoConfig

from tests.unit.components.test_template_tags import TemplateTagsTestCase


class TestNavbar(TemplateTagsTestCase):
    """Test suite for the navbar component."""

    def test_navbar(self) -> None:
        """Test für grundlegende navbar Funktionalität."""
        nav_config = NavbarConfig(
            NavbarBrandConfig(
                "Insight UI",
                "/",
                LogoConfig(
                    "insight_ui/svg/ai-logo.svg", "insight_ui/svg/ai-logo.svg", "Insight UI Logo", height="2rem"
                ),
                "0.5rem",
            ),
            [
                NavbarLinkConfig("Startpage", "/", IconConfig("home", "s")),
                NavbarLinkConfig(
                    "About",
                    modal=ModalConfig(
                        "about-modal",
                        "About Insight-UI",
                        "A modern UI library for Django applications to get started quickly.",
                    ),
                ),
            ],
            "/",
            True,
            True,
            True,
        )

        template_string = """
        {% load insight_tags %}
        {% navbar config=nav_config %}
        """

        rendered = self.render_template(template_string, context={"nav_config": nav_config})
        assert "Insight UI" in rendered

    def test_navbar_user_menu_is_hidden_until_opened(self) -> None:
        """Authenticated user menus must not push navbar controls into a second row."""
        nav_config = NavbarConfig(
            NavbarBrandConfig(
                "Insight UI",
                "/",
                LogoConfig(
                    "insight_ui/svg/ai-logo.svg", "insight_ui/svg/ai-logo.svg", "Insight UI Logo", height="2rem"
                ),
                "0.5rem",
            ),
            show_usermenu=True,
            show_language_selector=True,
            show_theme_toggle=True,
        )

        template_string = """
        {% load insight_tags %}
        {% navbar config=nav_config user_dropdown_links=user_dropdown_links %}
        """

        rendered = self.render_template(
            template_string, context={"nav_config": nav_config, "user_dropdown_links": [], "user": self.user}
        )
        soup = BeautifulSoup(rendered, "html.parser")

        trigger = soup.select_one('button[data-insight-dropdown="user-menu"]')
        menu = soup.select_one("#user-menu")

        assert trigger is not None
        assert trigger.find_parent("div", class_="relative") is not None
        assert menu is not None
        assert "hidden" in menu.get("class", [])
        assert "absolute" in menu.get("class", [])
        assert "top-full" in menu.get("class", [])

    def test_navbar_renders_brand_lockup_when_configured(self) -> None:
        """Navbar can render a controlled brand lockup instead of logo plus title."""
        nav_config = NavbarConfig(
            NavbarBrandConfig(
                "Insight UI",
                "/",
                aria_label="Alpin Insight Develop Startseite",
                lockup=BrandLockupConfig("Alpin Insight", "Develop", height="2rem", variant="develop"),
            )
        )

        rendered = self.render_template(
            "{% load insight_tags %}{% navbar config=nav_config %}", context={"nav_config": nav_config}
        )
        soup = BeautifulSoup(rendered, "html.parser")

        brand_link = soup.find("a", attrs={"aria-label": "Alpin Insight Develop Startseite"})
        assert brand_link is not None
        assert "Alpin Insight" in brand_link.get_text(" ", strip=True)
        assert "Develop" in brand_link.get_text(" ", strip=True)
        assert brand_link.find("svg") is not None
        assert brand_link.find("img") is None

    def test_navbar_keeps_logo_title_fallback_without_lockup(self) -> None:
        """Existing logo plus title configuration remains the fallback mode."""
        nav_config = NavbarConfig(
            NavbarBrandConfig(
                "Insight UI",
                "/",
                LogoConfig(
                    "insight_ui/svg/ai-logo.svg", "insight_ui/svg/ai-logo.svg", "Insight UI Logo", height="2rem"
                ),
                "0.5rem",
            )
        )

        rendered = self.render_template(
            "{% load insight_tags %}{% navbar config=nav_config %}", context={"nav_config": nav_config}
        )
        soup = BeautifulSoup(rendered, "html.parser")

        brand_link = soup.find("a", attrs={"aria-label": "Insight UI"})
        assert brand_link is not None
        assert brand_link.find("span", string="Insight UI") is not None
        assert brand_link.find("img") is not None
