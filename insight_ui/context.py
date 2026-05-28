from typing import Any

from core.context_processor import get_app_version
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext as _

from insight_ui import config
from insight_ui.component_details.components import Component, ComponentCategory
from insight_ui.component_details.demo_context import get_component_demo_context
from insight_ui.component_details.parameter_context import ParameterDetails
from insight_ui.configs import (
    CopyrightNoticeConfig,
    FooterConfig,
    FooterContactConfig,
    FooterDescriptionConfig,
    IconConfig,
    LogoConfig,
    NavbarBrandConfig,
    NavbarConfig,
    NavbarLinkConfig,
    RadioItemConfig,
    SidebarItemConfig,
    TableConfig,
)
from insight_ui.configs.base import HtmxConfig
from insight_ui.configs.input import DropdownConfig, DropdownItemConfig


def get_main_page_links() -> list[dict[str, Any]]:
    """Serve a list of links to the main pages."""
    return [
        NavbarLinkConfig(_("Home"), reverse("index_view"), IconConfig("home", "s")),
        NavbarLinkConfig(_("Installation"), reverse("installation_view"), IconConfig("download", "s")),
        NavbarLinkConfig(_("Base Template"), reverse("base_template_view"), IconConfig("blueprint", "s")),
        NavbarLinkConfig(_("Customization"), reverse("customization_view"), IconConfig("settings", "s")),
        NavbarLinkConfig(_("Icons"), reverse("icon_view"), IconConfig("sparkles", "s")),
    ]


def get_navbar_context() -> dict:
    """Serve data for main navbar."""
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
            NavbarBrandConfig(
                "Insight UI",
                "/",
                LogoConfig(
                    url="insight_ui/svg/ai-logo.svg",
                    url_dark="insight_ui/svg/ai-logo.svg",
                    alt="Insight UI Logo",
                    height="2rem",
                ),
                "0.5rem",
            ),
            links,
            "/",
            show_language_selector=True,
            show_theme_toggle=True,
        ),
        "navbar_fixed": True,
        "white_bg": True,
        "default_padding": True,
        "use_default_loading_indicator": False,
    }


def get_sidebar_context() -> dict:
    """Serve data for the main sidebar."""
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
    """Server data for main footer."""
    links = get_main_page_links()

    return {
        "footer_config": FooterConfig(
            FooterDescriptionConfig(
                "Insight UI", _("A modern, accessible, and responsive UI library for Django projects.")
            ),
            links,
            FooterContactConfig(
                "support@alpininsight.com", "https://alpininsight.com/imprint/", "https://alpininsight.com/privacy/"
            ),
            CopyrightNoticeConfig(
                2026,
                "Alpin Insight Solutions GmbH & Co. KG",
                "Open Source",
                "AGPL-3.0",
                reverse_lazy("license_view"),
            ),
            get_app_version(),
        )
    }


def get_base_context() -> dict:
    """Serve basic context data, like navbar, footer and settings."""
    return config.get_config() | get_navbar_context() | get_footer_context()


def get_icon_context() -> dict:
    """Serve context for the icon detailpage."""
    main_params = [
        ParameterDetails("name", "str", _("Name of the icon (see table below)."), "question-mark"),
        ParameterDetails("size", "str", _("Size of the icon. Possible values are: 'xl', 'l', 'm', 's' and 'xs'."), "m"),
    ]

    table_rows = [
        [
            render_to_string("insight_ui/components/icons.html", {"name": "home"}),
            "home",
            _("Typically used for links to the home page."),
            "Heroicons - home",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "office"}),
            "office",
            _("Topics related to the office or work."),
            "Heroicons - building-office",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "globe"}),
            "globe",
            _("Language selection elements."),
            "Heroicons - globe-alt",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "gear"}),
            "gear",
            _("General settings."),
            "Heroicons - cog-6-tooth",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "leave"}),
            "leave",
            _("As a logout button or for leaving a section."),
            "Heroicons - arrow-left-start-on-rectangle",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "cards"}),
            "cards",
            _("Card-based dashboards, grid views, etc."),
            "Flowbite - grid",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "list"}),
            "list",
            _("List views of all kinds."),
            "Heroicons - list-bullet",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "carousel"}),
            "carousel",
            _("Specifically for our carousel components. <b>(This icon is to be replaced soon!)</b>"),
            "Heroicons - square-3-stack-3d",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "chevron_down"}),
            "chevron_down",
            _("Classic for dropdowns, accordions, and everything that can be expanded."),
            "Heroicons - chevron-down",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "chevron_up"}),
            "chevron_up",
            _("Classic for dropdowns, accordions, and everything that can be collapsed."),
            "Heroicons - chevron-up",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "chevron_both"}),
            "chevron_both",
            _("Classic for indicating a sorting option."),
            "Heroicons - chevron-up-down",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "chevron_left"}),
            "chevron_left",
            _("Carousels, pagination or expandable elements such as a drawer."),
            "Heroicons - chevron-left",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "chevron_right"}),
            "chevron_right",
            _("Carousels, pagination or expandable elements such as a drawer."),
            "Heroicons - chevron-right",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "tick"}),
            "tick",
            _("Checklists."),
            "Heroicons - check",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "x-mark"}),
            "x-mark",
            _("Classic for buttons to close dialogs, alerts, etc."),
            "Heroicons - x-mark",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "question-mark"}),
            "question-mark",
            _("Indicator for additional information or FAQs."),
            "Heroicons - question-mark-circle",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "sparkles"}),
            "sparkles",
            _("For special cases where something unique is needed, or simply no other icon fits :)."),
            "Heroicons - sparkles",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "tools"}),
            "tools",
            _("Settings or as a maintenance symbol."),
            "Heroicons - wrench-screwdriver",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "search"}),
            "search",
            _("Classic for any search bar."),
            "Heroicons - magnifying-glass",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "rectangles"}),
            "rectangles",
            _("Groups of different objects, for example components or dashboards."),
            "Heroicons - rectangle-group",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "app"}),
            "app",
            _("Indicator for applications, programs or dialog windows."),
            "Heroicons - window",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "doc"}),
            "doc",
            _("Classic for documents."),
            "Heroicons - document-text",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "clipboard"}),
            "clipboard",
            _("Classic for copy and paste."),
            "Heroicons - clipboard-document-check",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "cursor-click"}),
            "cursor-click",
            _("Indicator for a clickable element."),
            "Heroicons - cursor-arrow-rays",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "link"}),
            "link",
            _("Classic for attachments or links to documents."),
            "Heroicons - link",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "open-link"}),
            "open-link",
            _("Classic for links to other, often external pages or for opening a dialog window."),
            "Heroicons - arrow-top-right-on-square",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "share"}),
            "share",
            _("Classic for sharing content."),
            "Heroicons - share",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "smartphone"}),
            "smartphone",
            _("Indicates smartphone usage."),
            "Heroicons - device-phone-mobile",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "tablet"}),
            "tablet",
            _("Indicates tablet usage."),
            "Heroicons - device-tablet",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "desktop"}),
            "desktop",
            _("Indicates desktop PC usage."),
            "Heroicons - computer-desktop",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "sun"}),
            "sun",
            _("Classic for light/dark mode switches."),
            "Heroicons - sun",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "moon"}),
            "moon",
            _("Classic for light/dark mode switches."),
            "Heroicons - moon",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "git"}),
            "git",
            _("Links to GitHub."),
            "Flowbite - github",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "user"}),
            "user",
            _("Typical user icon, user profile, settings, etc."),
            "Heroicons - user",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "clock"}),
            "clock",
            _("Everything related to time."),
            "Heroicons - clock",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "calendar"}),
            "calendar",
            _("Dates, deadlines, appointments."),
            "Heroicons - calendar-days",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "bell"}),
            "bell",
            _("Typical for notifications."),
            "Heroicons - bell",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "chat-bubble"}),
            "chat-bubble",
            _("Interactive chats."),
            "Heroicons - chat-bubble-bottom-center-text",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "rocket"}),
            "rocket",
            _("Special things or as an indicator for 'Let's get started!'."),
            "Heroicons - rocket-launch",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "terminal"}),
            "terminal",
            _("Indicator for the use of the terminal or command line."),
            "Heroicons - command-line",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "code"}),
            "code",
            _("Indicates source code."),
            "Heroicons - code-bracket",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "download"}),
            "download",
            _("Classic for downloads."),
            "Heroicons - arrow-down-tray",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "settings"}),
            "settings",
            _("Customizations, settings, more for fine-grained settings."),
            "Heroicons - adjustments-horizontal",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "blueprint"}),
            "blueprint",
            _("Customizations, settings, more for fine-grained settings."),
            "Heroicons - cube-transparent",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "info"}),
            "info",
            _("Information and notes."),
            "Heroicons - information-circle",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "warning"}),
            "warning",
            _("Warnings, issues, minor errors."),
            "Heroicons - exclamation-triangle",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "danger"}),
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
                render_to_string("insight_ui/components/icons.html", {"name": "home", "size": "xs"}),
                render_to_string("insight_ui/components/icons.html", {"name": "home", "size": "s"}),
                render_to_string("insight_ui/components/icons.html", {"name": "home", "size": "m"}),
                render_to_string("insight_ui/components/icons.html", {"name": "home", "size": "l"}),
                render_to_string("insight_ui/components/icons.html", {"name": "home", "size": "xl"}),
            ]
        ],
    )

    return {"main_params": main_params, "icon_table": icon_table, "size_table": size_table}


def get_demo_container_context() -> dict:
    """Serve data of the device switch, etc. for component demos."""
    return {
        "device_radio_items": [
            RadioItemConfig("mobile", "mobile", icon=IconConfig("smartphone")),
            RadioItemConfig("tablet", "tablet", icon=IconConfig("tablet")),
            RadioItemConfig("desktop", "desktop", icon=IconConfig("desktop")),
        ],
        "theme_toggle_icon": IconConfig("moon"),
    }


def get_storybook_context(storybook: ComponentCategory) -> dict:  # noqa: C901
    """Serve the base context and the context for each component in the list."""
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
