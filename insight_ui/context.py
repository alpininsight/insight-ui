"""Context utilities for Insight UI templates."""

from typing import Any

from core.context_processor import get_app_version
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext as _

from insight_ui import config
from insight_ui.brand import get_footer_description_defaults, get_navbar_brand_defaults
from insight_ui.component_details.components import Component, ComponentCategory
from insight_ui.component_details.demo_context import get_component_demo_context
from insight_ui.component_details.parameter_context import ParameterDetails
from insight_ui.configs import (
    CopyrightNoticeConfig,
    DropdownConfig,
    DropdownItemConfig,
    FooterConfig,
    FooterContactConfig,
    HtmxConfig,
    IconConfig,
    NavbarConfig,
    NavbarLinkConfig,
    RadioItemConfig,
    SidebarItemConfig,
    TableConfig,
)


def get_main_page_links() -> list[dict[str, Any]]:
    """Serve a list of links to the main pages.

    Returns:
        List of NavbarLinkConfig objects for main navigation.

    """
    return [
        NavbarLinkConfig(_("Home"), reverse("index_view"), IconConfig("home", "s")),
        NavbarLinkConfig(_("Installation"), reverse("installation_view"), IconConfig("download", "s")),
        NavbarLinkConfig(_("Base Template"), reverse("base_template_view"), IconConfig("blueprint", "s")),
        NavbarLinkConfig(_("Customization"), reverse("customization_view"), IconConfig("settings", "s")),
        NavbarLinkConfig(_("Icons"), reverse("icon_view"), IconConfig("sparkles", "s")),
    ]


def get_navbar_context() -> dict:
    """Serve data for main navbar.

    Returns:
        Context dict with navbar configuration and display options.

    """
    links = get_main_page_links()
    links.append(
        NavbarLinkConfig(
            _("Components"),
            icon=IconConfig("cards", "s"),
            dropdown=DropdownConfig(
                "components-menu",
                "",
                items=[
                    DropdownItemConfig(
                        category.formatted_name, reverse("storybook_view", kwargs={"storybook_name": category.value})
                    )
                    for category in ComponentCategory
                ],
            ),
        )
    )

    return {
        "nav_config": NavbarConfig(
            get_navbar_brand_defaults(),
            links,
            "/",
            show_language_selector=True,
            show_theme_toggle=True,
        ),
        "navbar_fixed": True,
    }


def get_sidebar_context() -> dict:
    """Serve data for the main sidebar.

    Returns:
        Context dict with sidebar categories and component items.

    """
    categories = [{"caption": category.formatted_name, "items": []} for category in ComponentCategory]

    for component in Component:
        for category in categories:
            if category["caption"] == component.group.formatted_name:
                category["items"].append(
                    SidebarItemConfig(
                        component.formatted_name,
                        reverse("component_detail_page_view", kwargs={"component_name": component.value}),
                        IconConfig("tools", "s") if component.in_development else None,
                        HtmxConfig(target="#content"),
                    )
                )
                break

    return {"left_sidebar": {"title": _("Components"), "categories": categories}}


def get_footer_context() -> dict:
    """Serve data for main footer.

    Returns:
        Context dict with footer configuration.

    """
    links = get_main_page_links()

    return {
        "footer_config": FooterConfig(
            get_footer_description_defaults(),
            links,
            FooterContactConfig(
                "support@alpininsight.com", "https://alpininsight.com/imprint/", "https://alpininsight.com/privacy/"
            ),
            CopyrightNoticeConfig(
                2026, "Alpin Insight Solutions GmbH & Co. KG", "Open Source", "AGPL-3.0", reverse_lazy("license_view")
            ),
            get_app_version(),
        )
    }


def get_base_context() -> dict:
    """Serve basic context data, like navbar, footer and settings.

    Returns:
        Combined context dict with config, navbar, and footer data.

    """
    return (
        config.get_config()
        | get_navbar_context()
        | get_footer_context()
        | {"white_bg": True, "default_padding": True, "use_default_loading_indicator": False}
    )


def get_icon_context() -> dict:
    """Serve context for the icon detailpage.

    Returns:
        Context dict with icon parameters, icon table, and size table.

    """
    main_params = [
        ParameterDetails("name", "str", _("Name of the icon (see table below)."), "question-mark"),
        ParameterDetails("size", "str", _("Size of the icon. Possible values are: 'xl', 'l', 'm', 's' and 'xs'."), "m"),
    ]

    table_rows = [
        [
            render_to_string("insight_ui/components/icons.html", {"icon_config": IconConfig("home")}),
            "home",
            _("Typically used for links to the home page."),
            "Heroicons - home",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"icon_config": IconConfig("office")}),
            "office",
            _("Topics related to the office or work."),
            "Heroicons - building-office",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"icon_config": IconConfig("globe")}),
            "globe",
            _("Language selection elements."),
            "Heroicons - globe-alt",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"icon_config": IconConfig("gear")}),
            "gear",
            _("General settings."),
            "Heroicons - cog-6-tooth",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"icon_config": IconConfig("leave")}),
            "leave",
            _("As a logout button or for leaving a section."),
            "Heroicons - arrow-left-start-on-rectangle",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"icon_config": IconConfig("cards")}),
            "cards",
            _("Card-based dashboards, grid views, etc."),
            "Flowbite - grid",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"icon_config": IconConfig("list")}),
            "list",
            _("List views of all kinds."),
            "Heroicons - list-bullet",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"icon_config": IconConfig("carousel")}),
            "carousel",
            _("Specifically for our carousel components. <b>(This icon is to be replaced soon!)</b>"),
            "Heroicons - square-3-stack-3d",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"icon_config": IconConfig("chevron_down")}),
            "chevron_down",
            _("Classic for dropdowns, accordions, and everything that can be expanded."),
            "Heroicons - chevron-down",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"icon_config": IconConfig("chevron_up")}),
            "chevron_up",
            _("Classic for dropdowns, accordions, and everything that can be collapsed."),
            "Heroicons - chevron-up",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"icon_config": IconConfig("chevron_both")}),
            "chevron_both",
            _("Classic for indicating a sorting option."),
            "Heroicons - chevron-up-down",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"icon_config": IconConfig("chevron_left")}),
            "chevron_left",
            _("Carousels, pagination or expandable elements such as a drawer."),
            "Heroicons - chevron-left",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"icon_config": IconConfig("chevron_right")}),
            "chevron_right",
            _("Carousels, pagination or expandable elements such as a drawer."),
            "Heroicons - chevron-right",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"icon_config": IconConfig("tick")}),
            "tick",
            _("Checklists."),
            "Heroicons - check",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"icon_config": IconConfig("x-mark")}),
            "x-mark",
            _("Classic for buttons to close dialogs, alerts, etc."),
            "Heroicons - x-mark",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"icon_config": IconConfig("question-mark")}),
            "question-mark",
            _("Indicator for additional information or FAQs."),
            "Heroicons - question-mark-circle",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"icon_config": IconConfig("sparkles")}),
            "sparkles",
            _("For special cases where something unique is needed, or simply no other icon fits :)."),
            "Heroicons - sparkles",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"icon_config": IconConfig("tools")}),
            "tools",
            _("Settings or as a maintenance symbol."),
            "Heroicons - wrench-screwdriver",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"icon_config": IconConfig("search")}),
            "search",
            _("Classic for any search bar."),
            "Heroicons - magnifying-glass",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"icon_config": IconConfig("rectangles")}),
            "rectangles",
            _("Groups of different objects, for example components or dashboards."),
            "Heroicons - rectangle-group",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"icon_config": IconConfig("app")}),
            "app",
            _("Indicator for applications, programs or dialog windows."),
            "Heroicons - window",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"icon_config": IconConfig("doc")}),
            "doc",
            _("Classic for documents."),
            "Heroicons - document-text",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"icon_config": IconConfig("clipboard")}),
            "clipboard",
            _("Classic for copy and paste."),
            "Heroicons - clipboard-document-check",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"icon_config": IconConfig("cursor-click")}),
            "cursor-click",
            _("Indicator for a clickable element."),
            "Heroicons - cursor-arrow-rays",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"icon_config": IconConfig("link")}),
            "link",
            _("Classic for attachments or links to documents."),
            "Heroicons - link",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"icon_config": IconConfig("open-link")}),
            "open-link",
            _("Classic for links to other, often external pages or for opening a dialog window."),
            "Heroicons - arrow-top-right-on-square",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"icon_config": IconConfig("share")}),
            "share",
            _("Classic for sharing content."),
            "Heroicons - share",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"icon_config": IconConfig("smartphone")}),
            "smartphone",
            _("Indicates smartphone usage."),
            "Heroicons - device-phone-mobile",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"icon_config": IconConfig("tablet")}),
            "tablet",
            _("Indicates tablet usage."),
            "Heroicons - device-tablet",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"icon_config": IconConfig("desktop")}),
            "desktop",
            _("Indicates desktop PC usage."),
            "Heroicons - computer-desktop",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"icon_config": IconConfig("sun")}),
            "sun",
            _("Classic for light/dark mode switches."),
            "Heroicons - sun",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"icon_config": IconConfig("moon")}),
            "moon",
            _("Classic for light/dark mode switches."),
            "Heroicons - moon",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"icon_config": IconConfig("git")}),
            "git",
            _("Links to GitHub."),
            "Flowbite - github",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"icon_config": IconConfig("user")}),
            "user",
            _("Typical user icon, user profile, settings, etc."),
            "Heroicons - user",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"icon_config": IconConfig("clock")}),
            "clock",
            _("Everything related to time."),
            "Heroicons - clock",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"icon_config": IconConfig("calendar")}),
            "calendar",
            _("Dates, deadlines, appointments."),
            "Heroicons - calendar-days",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"icon_config": IconConfig("bell")}),
            "bell",
            _("Typical for notifications."),
            "Heroicons - bell",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"icon_config": IconConfig("chat-bubble")}),
            "chat-bubble",
            _("Interactive chats."),
            "Heroicons - chat-bubble-bottom-center-text",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"icon_config": IconConfig("rocket")}),
            "rocket",
            _("Special things or as an indicator for 'Let's get started!'."),
            "Heroicons - rocket-launch",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"icon_config": IconConfig("terminal")}),
            "terminal",
            _("Indicator for the use of the terminal or command line."),
            "Heroicons - command-line",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"icon_config": IconConfig("code")}),
            "code",
            _("Indicates source code."),
            "Heroicons - code-bracket",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"icon_config": IconConfig("download")}),
            "download",
            _("Classic for downloads."),
            "Heroicons - arrow-down-tray",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"icon_config": IconConfig("settings")}),
            "settings",
            _("Customizations, settings, more for fine-grained settings."),
            "Heroicons - adjustments-horizontal",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"icon_config": IconConfig("blueprint")}),
            "blueprint",
            _("Customizations, settings, more for fine-grained settings."),
            "Heroicons - cube-transparent",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"icon_config": IconConfig("info")}),
            "info",
            _("Information and notes."),
            "Heroicons - information-circle",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"icon_config": IconConfig("warning")}),
            "warning",
            _("Warnings, issues, minor errors."),
            "Heroicons - exclamation-triangle",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"icon_config": IconConfig("danger")}),
            "danger",
            _("Major errors, critical issues or dangerous actions."),
            "Heroicons - exclamation-circle",
        ],
    ]

    icon_table = TableConfig([_("Icon"), _("Name"), _("Example usages"), _("Source")], table_rows)
    size_table = TableConfig(
        ["xs", "s", "m", "l", "xl"],
        [
            [
                render_to_string("insight_ui/components/icons.html", {"icon_config": IconConfig("home", "xs")}),
                render_to_string("insight_ui/components/icons.html", {"icon_config": IconConfig("home", "s")}),
                render_to_string("insight_ui/components/icons.html", {"icon_config": IconConfig("home", "m")}),
                render_to_string("insight_ui/components/icons.html", {"icon_config": IconConfig("home", "l")}),
                render_to_string("insight_ui/components/icons.html", {"icon_config": IconConfig("home", "xl")}),
            ]
        ],
    )

    return {"main_params": main_params, "icon_table": icon_table, "size_table": size_table}


def get_demo_container_context() -> dict:
    """Serve data of the device switch, etc. for component demos.

    Returns:
        Context dict with device radio items and theme toggle icon.

    """
    return {
        "device_radio_items": [
            RadioItemConfig("mobile", "mobile", icon=IconConfig("smartphone")),
            RadioItemConfig("tablet", "tablet", icon=IconConfig("tablet")),
            RadioItemConfig("desktop", "desktop", icon=IconConfig("desktop")),
        ],
        "theme_toggle_icon": IconConfig("moon"),
    }


def get_storybook_context(storybook: ComponentCategory) -> dict:  # noqa: C901
    """Serve the base context and the context for each component in the list.

    Args:
        storybook: The component category to display.

    Returns:
        Context dict with base context, components, and category description.

    """
    context = get_base_context() | get_sidebar_context()
    components = []
    for component in Component:
        if component.group.value == storybook.value:
            context |= get_component_demo_context(component)
            components.append(component)

    context["components"] = components

    match storybook:
        case ComponentCategory.LAYOUT:
            context["description"] = [_("Structural layout components.")]
        case ComponentCategory.NAVIGATION:
            context["description"] = [_("Main layout elements like navigation, footer and sidebars.")]
        case ComponentCategory.INPUT:
            context["description"] = [
                _("Standard input elements like Buttons, Radio-Buttons, Toggle-Buttons, Dropdown Menus and more.")
            ]
        case ComponentCategory.POPUP:
            context["description"] = [
                _("Popover, Tooltip, Modal and everything that pops up with additional information.")
            ]
        case ComponentCategory.UTIL:
            context["description"] = [_("Utility components.")]
        case ComponentCategory.LIST:
            context["description"] = [_("List and table components for big data.")]
        case ComponentCategory.FILTER:
            context["description"] = [_("Filter and search components for big data.")]
        case ComponentCategory.CARD:
            context["description"] = [_("Card components and different presentation types.")]
        case ComponentCategory.FORM:
            context["description"] = [_("Form components with various input fields and different request methods.")]

    return context
