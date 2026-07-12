"""Tests for the navbar component."""

# ruff: noqa: E501

from bs4 import BeautifulSoup
from insight_ui.configs.base import IconConfig
from insight_ui.configs.navigation import NavbarBrandConfig, NavbarConfig, NavbarLinkConfig
from insight_ui.configs.popup import ModalConfig
from insight_ui.configs.utils import BrandMarkConfig, LogoConfig

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
        assert "insight-user-dropdown-menu" in menu.get("class", [])
        assert "shadow-lg" not in menu.get("class", [])
        assert "bg-neutral-100" not in menu.get("class", [])
        assert "dark:bg-gray-700" not in menu.get("class", [])

    def test_navbar_mobile_toggle_uses_semantic_icon_button_class(self) -> None:
        """The mobile navbar toggle uses the semantic nav icon button class."""
        nav_config = NavbarConfig(NavbarBrandConfig("Insight UI", "/"))

        rendered = self.render_template(
            "{% load insight_tags %}{% navbar config=nav_config %}", context={"nav_config": nav_config}
        )
        soup = BeautifulSoup(rendered, "html.parser")

        trigger = soup.select_one('button[data-insight-collapsible="navigation-menu"]')

        assert trigger is not None
        assert trigger.get("class") == ["insight-nav-icon-button"]
        assert "hover:bg-gray-100" not in rendered
        assert "focus:ring-blue-500" not in rendered

    def test_navbar_user_menu_renders_avatar_image_when_configured(self) -> None:
        """Host apps can provide a user avatar URL without replacing the dropdown."""
        nav_config = NavbarConfig(NavbarBrandConfig("Insight UI", "/"), show_usermenu=True)

        template_string = """
        {% load insight_tags %}
        {% navbar config=nav_config user_dropdown_links=user_dropdown_links user_avatar_url=user_avatar_url user_avatar_alt=user_avatar_alt %}
        """

        rendered = self.render_template(
            template_string,
            context={
                "nav_config": nav_config,
                "user_dropdown_links": [],
                "user": self.user,
                "user_avatar_url": "/media/avatars/demo.webp",
                "user_avatar_alt": "Demo user avatar",
            },
        )
        soup = BeautifulSoup(rendered, "html.parser")

        trigger = soup.select_one('button[data-insight-dropdown="user-menu"]')
        avatar = trigger.find("img") if trigger else None

        assert trigger is not None
        assert trigger.get("aria-label") == "Demo user avatar"
        assert avatar is not None
        assert avatar.get("src") == "/media/avatars/demo.webp"
        assert avatar.get("alt") == "Demo user avatar"
        assert "object-cover" in avatar.get("class", [])

    def test_navbar_user_menu_keeps_initials_fallback_without_avatar(self) -> None:
        """Existing initials fallback remains the default user menu trigger."""
        nav_config = NavbarConfig(NavbarBrandConfig("Insight UI", "/"), show_usermenu=True)

        rendered = self.render_template(
            "{% load insight_tags %}{% navbar config=nav_config user_dropdown_links=user_dropdown_links %}",
            context={"nav_config": nav_config, "user_dropdown_links": [], "user": self.user},
        )
        soup = BeautifulSoup(rendered, "html.parser")

        trigger = soup.select_one('button[data-insight-dropdown="user-menu"]')

        assert trigger is not None
        assert trigger.find("img") is None
        assert trigger.get_text(strip=True) == self.user.get_username()[:1].upper()

    def test_navbar_renders_brand_mark_when_configured(self) -> None:
        """Navbar can render a controlled brand mark instead of logo plus title."""
        nav_config = NavbarConfig(
            NavbarBrandConfig(
                "Insight UI",
                "/",
                aria_label="Insight UI Indexpage",
                mark=BrandMarkConfig(
                    "Insight",
                    "UI",
                    LogoConfig(
                        "insight_ui/svg/ai-logo.svg", "insight_ui/svg/ai-logo.svg", "Insight UI Logo", height="2rem"
                    ),
                ),
            )
        )

        rendered = self.render_template(
            "{% load insight_tags %}{% navbar config=nav_config %}", context={"nav_config": nav_config}
        )
        soup = BeautifulSoup(rendered, "html.parser")

        brand_link = soup.find("a", attrs={"aria-label": "Insight UI Indexpage"})
        assert brand_link is not None
        assert "Insight" in brand_link.get_text(" ", strip=True)
        assert "UI" in brand_link.get_text(" ", strip=True)
        assert brand_link.find("img") is not None
        assert brand_link.find("svg") is None

    def test_navbar_keeps_logo_title_fallback_without_mark(self) -> None:
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
