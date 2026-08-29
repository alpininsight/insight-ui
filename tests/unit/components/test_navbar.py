"""Tests for the navbar component."""

from bs4 import BeautifulSoup
from insight_ui.configs.base import IconConfig
from insight_ui.configs.navigation import NavbarBrandConfig, NavbarConfig, NavbarLinkConfig, UserMenuConfig
from insight_ui.configs.popup import ModalConfig
from insight_ui.configs.utils import BrandMarkConfig, LogoConfig

from tests.unit.components.test_template_tags import TemplateTagsTestCase


class TestNavbar(TemplateTagsTestCase):
    """Test suite for the navbar component."""

    def test_navbar(self) -> None:
        """Test für grundlegende navbar Funktionalität."""
        nav_config = NavbarConfig(
            NavbarBrandConfig(
                request_url="/",
                mark=BrandMarkConfig(
                    primary_text="Insight UI",
                    logo=LogoConfig(
                        "insight_ui/svg/ai-logo.svg", "insight_ui/svg/ai-logo.svg", "Insight UI Logo", height="2rem"
                    ),
                ),
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
        """Authenticated user menus are hidden by default."""
        nav_config = NavbarConfig(
            NavbarBrandConfig(
                request_url="/",
                mark=BrandMarkConfig(primary_text="Insight UI"),
            ),
            show_language_selector=True,
            show_theme_toggle=True,
        )

        template_string = """
        {% load insight_tags %}
        {% navbar config=nav_config %}
        """

        rendered = self.render_template(template_string, context={"nav_config": nav_config, "user": self.user})
        soup = BeautifulSoup(rendered, "html.parser")

        trigger = soup.select_one('button[data-insight-dropdown="user-menu"]')
        menu = soup.select_one("#user-menu")

        assert trigger is not None
        assert menu is not None
        # State class: menu must be hidden initially (JS toggles this)
        assert "hidden" in menu.get("class", [])

    def test_navbar_passes_documentation_search_index_url(self) -> None:
        """Navbar documentation search keeps the host-owned static URL."""
        nav_config = NavbarConfig(
            brand=NavbarBrandConfig(request_url="/", mark=BrandMarkConfig(primary_text="Insight UI")),
            enable_doc_search=True,
            search_index_url="/static/documentation/data/search-index-en.json",
        )

        rendered = self.render_template(
            "{% load insight_tags %}{% navbar config=nav_config %}", context={"nav_config": nav_config}
        )
        search_container = BeautifulSoup(rendered, "html.parser").select_one("[data-insight-search]")

        assert search_container is not None
        assert search_container["data-search-index"] == "/static/documentation/data/search-index-en.json"

    def test_navbar_keeps_existing_positional_arguments(self) -> None:
        """Appending search_index_url must not change the public positional API."""
        usermenu = UserMenuConfig()
        nav_config = NavbarConfig(None, [], "/search/", True, usermenu, True, True, True)

        assert nav_config.usermenu is usermenu
        assert nav_config.hide_login is True
        assert nav_config.show_language_selector is True
        assert nav_config.show_theme_toggle is True
        assert nav_config.search_index_url == ""

    def test_navbar_user_menu_renders_avatar_image_when_configured(self) -> None:
        """Host apps can provide a user avatar URL via UserMenuConfig."""
        nav_config = NavbarConfig(
            NavbarBrandConfig(
                request_url="/",
                mark=BrandMarkConfig(primary_text="Insight UI"),
            ),
            usermenu=UserMenuConfig(
                avatar_url="/media/avatars/demo.webp",
                avatar_alt="Demo user avatar",
            ),
        )

        template_string = """
        {% load insight_tags %}
        {% navbar config=nav_config %}
        """

        rendered = self.render_template(
            template_string,
            context={
                "nav_config": nav_config,
                "user": self.user,
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

    def test_navbar_user_menu_keeps_initials_fallback_without_avatar(self) -> None:
        """Existing initials fallback remains the default user menu trigger."""
        nav_config = NavbarConfig(
            NavbarBrandConfig(
                request_url="/",
                mark=BrandMarkConfig(primary_text="Insight UI"),
            ),
        )

        rendered = self.render_template(
            "{% load insight_tags %}{% navbar config=nav_config %}",
            context={"nav_config": nav_config, "user": self.user},
        )
        soup = BeautifulSoup(rendered, "html.parser")

        trigger = soup.select_one('button[data-insight-dropdown="user-menu"]')

        assert trigger is not None
        assert trigger.find("img") is None
        assert trigger.get_text(strip=True) == self.user.get_username()[:1].upper()

    def test_navbar_renders_brand_mark_when_configured(self) -> None:
        """Navbar can render a controlled brand mark."""
        nav_config = NavbarConfig(
            NavbarBrandConfig(
                request_url="/",
                aria_label="Insight UI Indexpage",
                mark=BrandMarkConfig(
                    primary_text="Insight",
                    secondary_text="UI",
                    logo=LogoConfig(
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
