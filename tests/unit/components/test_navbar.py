"""Tests for the navbar component."""

import warnings

import pytest
from bs4 import BeautifulSoup
from insight_ui.configs.base import IconConfig
from insight_ui.configs.filter import SearchBarConfig
from insight_ui.configs.navigation import (
    NavbarBrandConfig,
    NavbarConfig,
    NavbarLinkConfig,
    UserMenuConfig,
    UserMenuLinkConfig,
)
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
                        "insight_ui/svg/insight-ui-logo.svg",
                        "insight_ui/svg/insight-ui-logo.svg",
                        "Insight UI Logo",
                        height="2rem",
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
            search_bar=SearchBarConfig(placeholder="Search..."),
            show_language_selector=True,
            show_theme_toggle=True,
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

    def test_navbar_passes_host_owned_search_index_url(self) -> None:
        """Navbar search keeps a host-owned static URL unchanged."""
        nav_config = NavbarConfig(
            brand=NavbarBrandConfig(request_url="/", mark=BrandMarkConfig(primary_text="Insight UI")),
            search_bar=SearchBarConfig(
                enable_search=True,
                search_index_url="/static/host-search/search-index-en.json",
            ),
        )

        rendered = self.render_template(
            "{% load insight_tags %}{% navbar config=nav_config %}", context={"nav_config": nav_config}
        )
        search_container = BeautifulSoup(rendered, "html.parser").select_one("[data-insight-search]")

        assert search_container is not None
        assert search_container["data-search-index"] == "/static/host-search/search-index-en.json"

    def test_navbar_keeps_existing_positional_arguments(self) -> None:
        """Keyword arguments work as expected."""
        usermenu = UserMenuConfig()
        search_bar = SearchBarConfig(placeholder="Search...")
        nav_config = NavbarConfig(
            brand=None,
            links=[],
            search_bar=search_bar,
            usermenu=usermenu,
            hide_login=True,
            show_language_selector=True,
            show_theme_toggle=True,
        )

        assert nav_config.search_bar is search_bar
        assert nav_config.usermenu is usermenu
        assert nav_config.hide_login is True
        assert nav_config.show_language_selector is True
        assert nav_config.show_theme_toggle is True

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

    def test_navbar_user_menu_renders_string_icon(self) -> None:
        """User menu icon names render through the documented string contract."""
        nav_config = NavbarConfig(
            NavbarBrandConfig(request_url="/", mark=BrandMarkConfig(primary_text="Insight UI")),
            usermenu=UserMenuConfig(
                links=[UserMenuLinkConfig(text="Profile", request_url="/profile", icon="user")],
            ),
        )

        rendered = self.render_template(
            "{% load insight_tags %}{% navbar config=nav_config %}",
            context={"nav_config": nav_config, "user": self.user},
        )
        menu_link = BeautifulSoup(rendered, "html.parser").select_one('#user-menu a[href="/profile"]')

        assert menu_link is not None
        assert menu_link.find("svg") is not None

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
                        "insight_ui/svg/insight-ui-logo.svg",
                        "insight_ui/svg/insight-ui-logo.svg",
                        "Insight UI Logo",
                        height="2rem",
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

    def test_navbar_link_config_warns_without_request_url_modal_or_dropdown(self) -> None:
        """A NavbarLinkConfig with no request_url, modal, or dropdown would render invisibly."""
        with pytest.warns(UserWarning, match="has no request_url, modal, or dropdown"):
            NavbarLinkConfig(text="Home")

    def test_navbar_link_config_no_warning_with_request_url(self) -> None:
        """A NavbarLinkConfig with request_url set does not warn."""
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            NavbarLinkConfig(text="Home", request_url="/")
        assert len(caught) == 0
