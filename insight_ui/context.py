"""Context utilities for Insight UI templates."""

import re
from pathlib import Path
from typing import Any

from core.context_processor import get_app_version
from django.template.loader import get_template, render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext as _

from insight_ui import config
from insight_ui.brand import get_footer_description_defaults, get_navbar_brand_defaults
from insight_ui.component_details.components import Component, ComponentCategory
from insight_ui.component_details.demo_context import get_component_demo_context
from insight_ui.component_details.parameter_context import ParameterDetails
from insight_ui.configs import (
    BadgeConfig,
    DropdownConfig,
    DropdownItemConfig,
    FooterConfig,
    FooterContactConfig,
    HtmxConfig,
    IconConfig,
    LegalNoticeConfig,
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
        NavbarLinkConfig(_("Installation"), reverse("installation_view"), IconConfig("arrow-down-tray", "s")),
        NavbarLinkConfig(_("Base Template"), reverse("base_template_view"), IconConfig("cube-transparent", "s")),
        NavbarLinkConfig(_("Customization"), reverse("customization_view"), IconConfig("adjustments-horizontal", "s")),
        NavbarLinkConfig(_("Icons"), reverse("icon_view"), IconConfig("sparkles", "s")),
        NavbarLinkConfig(_("Types"), reverse("types_view"), IconConfig("code-bracket", "s")),
        NavbarLinkConfig(_("Configs"), reverse("config_reference_view"), IconConfig("cube", "s")),
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
            icon=IconConfig("squares-2x2", "s"),
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
            enable_doc_search=True,
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
                # Determine badge: New > Beta > None
                badge = None
                if component.is_new:
                    badge = BadgeConfig(label=_("New"), type="primary", size="xs")
                elif component.in_development:
                    badge = BadgeConfig(label="Beta", type="warning", size="xs")

                category["items"].append(
                    SidebarItemConfig(
                        component.formatted_name,
                        reverse("component_detail_page_view", kwargs={"component_name": component.value}),
                        IconConfig("wrench-screwdriver", "s") if component.in_development else None,
                        HtmxConfig(target="#content"),
                        badge,
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
            LegalNoticeConfig(
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
    return config.get_config() | get_navbar_context() | get_footer_context() | {"use_default_loading_indicator": False}


def get_icon_context() -> dict:
    """Serve context for the icon detailpage.

    Returns:
        Context dict with icon parameters, icons list, and size table.

    """
    main_params = [
        ParameterDetails("name", "str", _("Name of the icon (see grid below)."), "question-mark"),
        ParameterDetails("size", "str", _("Size of the icon. Possible values are: 'xl', 'l', 'm', 's' and 'xs'."), "m"),
    ]

    # Extract icon names from icons.html template
    template = get_template("insight_ui/components/icons.html")
    template_path = Path(template.origin.name)
    template_content = template_path.read_text(encoding="utf-8")

    # Match icon names from: icon_config.name == "name"
    icon_names = re.findall(r'icon_config\.name == "([^"]+)"', template_content)

    # Generate icon list
    icons = [
        {
            "name": name,
            "svg": render_to_string("insight_ui/components/icons.html", {"icon_config": IconConfig(name)}),
        }
        for name in sorted(set(icon_names))
    ]

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

    return {"main_params": main_params, "icons": icons, "size_table": size_table}


def get_demo_container_context() -> dict:
    """Serve data of the device switch, etc. for component demos.

    Returns:
        Context dict with device radio items and theme toggle icon.

    """
    return {
        "device_radio_items": [
            RadioItemConfig("mobile", "mobile", icon=IconConfig("device-phone-mobile")),
            RadioItemConfig("tablet", "tablet", icon=IconConfig("device-tablet")),
            RadioItemConfig("desktop", "desktop", icon=IconConfig("computer-desktop")),
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
