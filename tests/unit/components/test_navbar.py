"""Tests for the navbar component."""

# ruff: noqa: E501

from bs4 import BeautifulSoup
from insight_ui.configs.base import IconConfig
from insight_ui.configs.navigation import (
    NavbarBrandConfig,
    NavbarConfig,
    NavbarLinkConfig,
    NavbarNotificationItemConfig,
    NavbarNotificationsConfig,
)
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

    def test_navbar_notifications_renders_badge_and_items(self) -> None:
        """The standalone notification dropdown renders unread count and list items."""
        notifications_config = NavbarNotificationsConfig(
            items=[
                NavbarNotificationItemConfig(
                    "Pipeline finished",
                    "The develop image is ready.",
                    "Now",
                    icon=IconConfig("rocket", "s"),
                    priority="success",
                    unread=True,
                ),
                NavbarNotificationItemConfig(
                    "Review requested",
                    "A reviewer left a comment.",
                    "5 min ago",
                    icon=IconConfig("chat-bubble", "s"),
                    unread=True,
                ),
            ],
            all_notifications_url="/notifications/",
        )

        rendered = self.render_template(
            "{% load insight_tags %}{% navbar_notifications config=notifications_config %}",
            context={"notifications_config": notifications_config},
        )
        soup = BeautifulSoup(rendered, "html.parser")

        trigger = soup.select_one('button[data-insight-dropdown="navbar-notifications-menu"]')
        menu = soup.select_one("#navbar-notifications-menu")

        assert trigger is not None
        assert trigger.get("aria-label") == "Open notifications"
        assert trigger.get_text(" ", strip=True) == "2"
        assert menu is not None
        assert menu.get("role") == "menu"
        assert "Pipeline finished" in menu.get_text(" ", strip=True)
        assert "Review requested" in menu.get_text(" ", strip=True)
        assert menu.find("a", href="/notifications/") is not None

    def test_navbar_notifications_empty_state(self) -> None:
        """Empty notification dropdowns should render an explanatory empty state."""
        notifications_config = NavbarNotificationsConfig(items=[])

        rendered = self.render_template(
            "{% load insight_tags %}{% navbar_notifications config=notifications_config %}",
            context={"notifications_config": notifications_config},
        )
        soup = BeautifulSoup(rendered, "html.parser")

        assert "No notifications." in soup.get_text(" ", strip=True)
        assert soup.select_one('button[data-insight-dropdown="navbar-notifications-menu"]') is not None

    def test_navbar_embeds_notifications_when_configured(self) -> None:
        """Navbar renders the notification control when NavbarConfig includes it."""
        nav_config = NavbarConfig(
            NavbarBrandConfig("Insight UI", "/"),
            notifications=NavbarNotificationsConfig(
                items=[NavbarNotificationItemConfig("Deployment", "Ready", unread=True)]
            ),
        )

        rendered = self.render_template(
            "{% load insight_tags %}{% navbar config=nav_config %}",
            context={"nav_config": nav_config, "user": self.user},
        )
        soup = BeautifulSoup(rendered, "html.parser")

        assert soup.select_one("[data-insight-navbar-notifications]") is not None
        assert soup.select_one('button[data-insight-dropdown="navbar-notifications-menu"]') is not None
