# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for the navbar component."""

import warnings

import pytest
from bs4 import BeautifulSoup
from django.contrib.auth.models import AnonymousUser, User
from django.test import override_settings
from insight_ui.configs.base import IconConfig
from insight_ui.configs.filter import SearchBarConfig
from insight_ui.configs.input import DropdownConfig, DropdownItemConfig
from insight_ui.configs.navigation import (
    NavbarBrandConfig,
    NavbarConfig,
    NavbarLinkConfig,
    UserMenuConfig,
    UserMenuLinkConfig,
)
from insight_ui.configs.utils import BrandMarkConfig, LogoConfig

from tests.insight_ui.unit.components.test_template_tags import TemplateTagsTestCase


class TestNavbar(TemplateTagsTestCase):
    """Test suite for the navbar component."""

    def test_navbar(self) -> None:
        """Test für grundlegende navbar Funktionalität."""
        nav_config = NavbarConfig(
            brand=NavbarBrandConfig(
                request_url="/",
                mark=BrandMarkConfig(
                    primary_text="Insight UI",
                    logo=LogoConfig(
                        url="insight_ui/svg/insight-ui-logo.svg",
                        url_dark="insight_ui/svg/insight-ui-logo.svg",
                        alt="Insight UI Logo",
                        height="2rem",
                    ),
                ),
            ),
            links=[
                NavbarLinkConfig(text="Startpage", request_url="/", icon=IconConfig(name="home", size="s")),
                NavbarLinkConfig(text="About", modal_id="about-modal"),
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
            brand=NavbarBrandConfig(
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

    def test_navbar_language_form_preserves_return_url(self) -> None:
        """The nested language form receives the host's canonical GET URL."""
        return_url = '/cases/42/?queue=mine&page=2&q="quoted"#conversation'
        rendered = self.render_template(
            "{% load insight_tags %}{% navbar config=nav_config %}",
            context={"nav_config": NavbarConfig(show_language_selector=True), "redirect_to": return_url},
        )
        next_input = BeautifulSoup(rendered, "html.parser").select_one('form input[name="next"]')

        assert next_input is not None
        assert next_input["value"] == return_url
        assert "&amp;page=2" in rendered
        assert "&quot;quoted&quot;" in rendered

    def test_navbar_language_form_without_return_url_keeps_empty_default(self) -> None:
        """Hosts without an explicit return URL retain Django's fallback behavior."""
        rendered = self.render_template(
            "{% load insight_tags %}{% navbar config=nav_config %}",
            context={"nav_config": NavbarConfig(show_language_selector=True)},
        )
        next_input = BeautifulSoup(rendered, "html.parser").select_one('form input[name="next"]')

        assert next_input is not None
        assert next_input["value"] == ""

    def test_navbar_passes_documentation_search_index_url(self) -> None:
        """Navbar documentation search keeps the host-owned static URL."""
        nav_config = NavbarConfig(
            brand=NavbarBrandConfig(request_url="/", mark=BrandMarkConfig(primary_text="Insight UI")),
            search_bar=SearchBarConfig(
                enable_search=True,
                search_index_url="/static/documentation/data/search-index-en.json",
            ),
        )

        rendered = self.render_template(
            "{% load insight_tags %}{% navbar config=nav_config %}", context={"nav_config": nav_config}
        )
        search_container = BeautifulSoup(rendered, "html.parser").select_one("[data-insight-search]")

        assert search_container is not None
        assert search_container["data-search-index"] == "/static/documentation/data/search-index-en.json"

    def test_navbar_keeps_keyword_arguments(self) -> None:
        """Each keyword argument lands in its own field."""
        user_menu = UserMenuConfig()
        search_bar = SearchBarConfig(placeholder="Search...")
        nav_config = NavbarConfig(
            brand=None,
            links=[],
            search_bar=search_bar,
            user_menu=user_menu,
            hide_login=True,
            show_language_selector=True,
            show_theme_toggle=True,
        )

        assert nav_config.search_bar is search_bar
        assert nav_config.user_menu is user_menu
        assert nav_config.hide_login is True
        assert nav_config.show_language_selector is True
        assert nav_config.show_theme_toggle is True

    def test_navbar_user_menu_renders_avatar_image_when_configured(self) -> None:
        """Host apps can provide a user avatar URL via UserMenuConfig."""
        nav_config = NavbarConfig(
            brand=NavbarBrandConfig(
                request_url="/",
                mark=BrandMarkConfig(primary_text="Insight UI"),
            ),
            user_menu=UserMenuConfig(
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
            brand=NavbarBrandConfig(
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
            brand=NavbarBrandConfig(request_url="/", mark=BrandMarkConfig(primary_text="Insight UI")),
            user_menu=UserMenuConfig(
                links=[UserMenuLinkConfig(text="Profile", request_url="/profile", icon=IconConfig(name="user"))],
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
        """The brand link is named by the wordmark it shows; the logo beside it is decorative."""
        nav_config = NavbarConfig(
            brand=NavbarBrandConfig(
                request_url="/",
                mark=BrandMarkConfig(
                    primary_text="Insight",
                    secondary_text="UI",
                    logo=LogoConfig(
                        url="insight_ui/svg/insight-ui-logo.svg",
                        url_dark="insight_ui/svg/insight-ui-logo.svg",
                        alt="Insight UI Logo",
                        height="2rem",
                    ),
                ),
            )
        )

        rendered = self.render_template(
            "{% load insight_tags %}{% navbar config=nav_config %}", context={"nav_config": nav_config}
        )
        soup = BeautifulSoup(rendered, "html.parser")

        brand_link = soup.find("a", href="/")
        assert not brand_link.has_attr("aria-label")
        assert brand_link.get_text(" ", strip=True) == "Insight UI"
        assert brand_link.find("img")["alt"] == ""
        assert brand_link.find("svg") is None

    def test_navbar_link_config_warns_without_request_url_modal_id_or_dropdown(self) -> None:
        """A NavbarLinkConfig with no request_url, modal_id, or dropdown would render invisibly."""
        with pytest.warns(UserWarning, match="has no request_url, modal_id, or dropdown"):
            NavbarLinkConfig(text="Home")

    def test_navbar_link_config_no_warning_with_request_url(self) -> None:
        """A NavbarLinkConfig with request_url set does not warn."""
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            NavbarLinkConfig(text="Home", request_url="/")
        assert len(caught) == 0

    @override_settings(INSIGHT_UI={"brand": {"mark": BrandMarkConfig(primary_text="Acme", secondary_text="Prototype")}})
    def test_navbar_without_config_uses_brand_defaults(self) -> None:
        """Without a Config the navbar shows the configured brand."""
        rendered = self.render_template("{% load insight_tags %}{% navbar %}")
        soup = BeautifulSoup(rendered, "html.parser")
        assert soup.find("nav") is not None
        assert "Acme" in soup.get_text()
        assert "Prototype" in soup.get_text()

    def test_navbar_renders_explicit_config(self) -> None:
        """An explicit NavbarConfig is rendered as supplied."""
        rendered = self.render_template(
            "{% load insight_tags %}{% navbar config=navbar_config %}",
            {"navbar_config": NavbarConfig(show_theme_toggle=True)},
        )
        assert "data-insight-theme-toggle" in rendered


def render_navbar(config: NavbarConfig, user: User | AnonymousUser | None = None) -> BeautifulSoup:
    """Render a navbar with the given config, optionally for a user."""
    from django.template import Context, Template  # noqa: PLC0415

    html = Template("{% load insight_tags %}{% navbar config=config %}").render(
        Context({"config": config, "user": user})
    )
    return BeautifulSoup(html, "html.parser")


def packages_dropdown(*, show_arrow: bool = True) -> NavbarLinkConfig:
    """Navbar entry that opens a dropdown menu."""
    return NavbarLinkConfig(
        text="Packages",
        dropdown=DropdownConfig(
            tag_id="packages-menu",
            title="Packages",
            show_arrow=show_arrow,
            items=[DropdownItemConfig(text="Insight UI User", request_url="/user/")],
        ),
    )


@pytest.mark.parametrize(("show_arrow", "expected"), [(True, True), (False, False)])
def test_navbar_dropdown_trigger_shows_the_arrow_from_its_config(show_arrow: bool, expected: bool) -> None:
    """The dropdown trigger shows an arrow exactly when DropdownConfig.show_arrow asks for it."""
    soup = render_navbar(NavbarConfig(links=[packages_dropdown(show_arrow=show_arrow)]))

    trigger = soup.select_one('button[data-insight-dropdown="packages-menu"]')
    assert trigger is not None
    assert (trigger.find("svg") is not None) is expected


def test_navbar_dropdown_trigger_announces_its_collapsed_menu() -> None:
    """Before the first click the trigger already tells assistive technology that it controls a closed menu."""
    soup = render_navbar(NavbarConfig(links=[packages_dropdown()]))

    trigger = soup.select_one('button[data-insight-dropdown="packages-menu"]')
    assert trigger is not None
    assert trigger.get("type") == "button"
    assert trigger.get("aria-expanded") == "false"
    assert trigger.get("aria-controls") == "packages-menu"
    assert soup.find(id="packages-menu") is not None


VISITOR = AnonymousUser()
MEMBER = User(username="member")
ADMIN = User(username="admin", is_staff=True)


@pytest.mark.parametrize(
    ("need_auth", "staff_only", "user", "visible"),
    [
        (False, False, VISITOR, True),
        (False, True, VISITOR, False),
        (True, False, VISITOR, False),
        (True, True, VISITOR, False),
        (False, False, MEMBER, True),
        (False, True, MEMBER, False),
        (True, False, MEMBER, True),
        (True, True, MEMBER, False),
        (False, False, ADMIN, True),
        (False, True, ADMIN, True),
        (True, False, ADMIN, True),
        (True, True, ADMIN, True),
    ],
    ids=lambda value: (value.username or "visitor") if isinstance(value, User | AnonymousUser) else None,
)
def test_navbar_link_visibility_follows_need_auth_and_staff_only(
    need_auth: bool,
    staff_only: bool,
    user: User | AnonymousUser,
    visible: bool,
) -> None:
    """need_auth limits a link to logged-in users and staff_only to administrators, each on its own."""
    link = NavbarLinkConfig(text="Reports", request_url="/reports/", need_auth=need_auth, staff_only=staff_only)
    soup = render_navbar(NavbarConfig(links=[link]), user=user)

    assert (soup.find("a", href="/reports/") is not None) is visible


def test_user_menu_leaves_no_empty_entry_for_a_hidden_staff_link() -> None:
    """A staff-only user menu link is left out together with its list item, so the list counts only visible links."""
    user_menu = UserMenuConfig(
        links=[
            UserMenuLinkConfig(text="Profile", request_url="/profile/"),
            UserMenuLinkConfig(text="Admin", request_url="/admin/", staff_only=True),
        ]
    )

    member_items = render_navbar(NavbarConfig(user_menu=user_menu), user=MEMBER).select("#user-menu li")
    admin_items = render_navbar(NavbarConfig(user_menu=user_menu), user=ADMIN).select("#user-menu li")

    assert [item.get_text(strip=True) for item in member_items] == ["Profile"]
    assert [item.get_text(strip=True) for item in admin_items] == ["Profile", "Admin"]


def test_external_navbar_link_tells_screen_readers_about_the_new_tab() -> None:
    """A navbar link that opens a new tab says so after its text; an internal one does not."""
    soup = render_navbar(
        NavbarConfig(
            links=[
                NavbarLinkConfig(text="Docs", request_url="https://example.com/", external=True),
                NavbarLinkConfig(text="Home", request_url="/"),
            ]
        )
    )

    assert soup.find("a", href="https://example.com/").get_text(" ", strip=True) == "Docs (opens in a new tab)"
    assert "Home" in [link.get_text(" ", strip=True) for link in soup.find_all("a", href="/")]


def test_external_navbar_link_needs_a_url() -> None:
    """A modal or dropdown entry has no URL to open in a new tab."""
    with pytest.raises(ValueError, match="external only applies together with request_url"):
        NavbarLinkConfig(text="About", modal_id="about", external=True)


def test_brand_logo_without_wordmark_keeps_its_name() -> None:
    """Without a wordmark the logo is the only content, so its alt text names the brand link."""
    mark = BrandMarkConfig(logo=LogoConfig(url="insight_ui/svg/insight-ui-logo.svg", alt="Insight UI"))
    soup = render_navbar(NavbarConfig(brand=NavbarBrandConfig(request_url="/home/", mark=mark)))

    assert soup.find("a", href="/home/").find("img")["alt"] == "Insight UI"
