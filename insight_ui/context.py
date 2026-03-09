from typing import Any

from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.translation import gettext as _

from insight_ui import config
from insight_ui.component_details.components import Component, ComponentCategory
from insight_ui.component_details.demo_context import get_component_demo_context
from insight_ui.component_details.parameter_context import ParameterDetails


def get_main_page_links() -> list[dict[str, Any]]:
    """Serve a list of links to the main pages."""
    return [
        {
            "text": _("Home"),
            "view_name": "index_view",
            "icon": {"name": "home", "size": "small"},
            "active": False,
            "need_auth": False,
            "staff_only": False,
        },
        {
            "text": _("Installation"),
            "view_name": "installation_view",
            "icon": {"name": "download", "size": "small"},
            "active": False,
            "need_auth": False,
            "staff_only": False,
        },
        {
            "text": _("Base Template"),
            "view_name": "base_template_view",
            "icon": {"name": "blueprint", "size": "small"},
            "active": False,
            "need_auth": False,
            "staff_only": False,
        },
        {
            "text": _("Customization"),
            "view_name": "customization_view",
            "icon": {"name": "settings", "size": "small"},
            "active": False,
            "need_auth": False,
            "staff_only": False,
        },
        {
            "text": _("Icons"),
            "view_name": "icon_view",
            "icon": {"name": "sparkles", "size": "small"},
            "active": False,
            "need_auth": False,
            "staff_only": False,
        },
    ]


def get_navbar_context(current_view: str = "index_view") -> dict:
    """Serve data for main navbar."""
    links = get_main_page_links()
    links.append(
        {
            "text": _("Components"),
            "open_dropdown": "components-menu",
            "icon": {"name": "cards", "size": "small"},
            "items": [
                {
                    "text": category.formatted_name,
                    "view_name": "storybook_view",
                    "view_arg": category.value,
                    "htmx": {"target": "#content"},
                }
                for category in ComponentCategory
            ],
            "chevron": {"name": "chevron_down", "size": "small"},
            "active": False,
            "need_auth": False,
            "staff_only": False,
        }
    )

    for link in links:
        if link.get("view_name") is not None:
            if link["view_name"] == current_view:
                link["active"] = True
                break
        else:
            for item in link["items"]:
                if item["view_name"] == current_view:
                    link["active"] = True
                    break

    return {
        "nav_config": {
            "brand": {
                "title": "Insight UI",
                "view_name": "index_view",
                "gap": "0.5rem",
                "logo": {
                    "url": "insight_ui/svg/ai-logo.svg",
                    "url_dark": "insight_ui/svg/ai-logo.svg",
                    "alt": "Insight UI Logo",
                    "height": "2rem",
                },
            },
            "links": links,
            "searchbar_request_view": "index_view",
            "show_usermenu": False,
            "show_language_selector": True,
            "show_theme_toggle": True,
        }
    }


def get_sidebar_context() -> dict:
    """Serve data for the main sidebar."""
    categories = [{"caption": category.formatted_name, "items": []} for category in ComponentCategory]

    for component in Component:
        for category in categories:
            if category["caption"] == component.group.formatted_name:
                category["items"].append(
                    {
                        "text": component.formatted_name,
                        "url": reverse("component_detail_page_view", kwargs={"component_name": component.value}),
                        "htmx": {"target": "#content"},
                    }
                )
                break

    return {"left_sidebar": {"title": _("Components"), "categories": categories}}


def get_footer_context() -> dict:
    """Server data for main footer."""
    links = get_main_page_links()

    return {
        "footer_data": {
            "description": {
                "title": "Insight UI",
                "text": "A modern, accessible, and responsive UI library for Django projects.",
            },
            "links": links,
            "contact": {
                "mail_url": "support@alpininsight.com",
                "imprint": "https://alpininsight.com/imprint/",
                "privacy": "https://alpininsight.com/privacy/",
            },
            "copyright": {"year": 2026, "app_name": "Insight UI"},
        }
    }


def get_base_context(current_view: str = "index_view") -> dict:
    """Serve basic context data, like navbar, footer and settings."""
    return config.get_config() | get_navbar_context(current_view) | get_footer_context()


def get_icon_context() -> dict:
    """Serve context for the icon detailpage."""
    main_params = [
        ParameterDetails("name", "str", "Name des Icons (siehe Tabelle unten).", "question-mark"),
        ParameterDetails(
            "size", "str", "Größe des Icons. Mögliche Werte sind: 'big', 'medium', 'small' und 'xs'", "default"
        ),
    ]

    table_rows = [
        [
            render_to_string("insight_ui/components/icons.html", {"name": "home"}),
            "home",
            "Typisch für Verlinkungen auf die Startseite.",
            "Heroicons - home",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "office"}),
            "office",
            "Themen mit Bezug zum Büro oder der Arbeit.",
            "Heroicons - building-office",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "globe"}),
            "globe",
            "Elemente zur Sprachauswahl.",
            "Heroicons - globe-alt",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "gear"}),
            "gear",
            "Generelle Einstellungen.",
            "Heroicons - cog-6-tooth",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "leave"}),
            "leave",
            "Als Abmeldebutton oder verlassen eines Bereichs.",
            "Heroicons - arrow-left-start-on-rectangle",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "cards"}),
            "cards",
            "Karten basierte Dashboards, Rasteransichten, etc..",
            "Flowbite - grid",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "list"}),
            "list",
            "Listenansichten jeder Art.",
            "Heroicons - list-bullet",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "carousel"}),
            "carousel",
            "Speziell für unsere Karussell-Komponenten. <b>(Das Icon soll demnächst ausgetauscht werden!)</b>",
            "Heroicons - square-3-stack-3d",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "chevron_down"}),
            "chevron_down",
            "Klassiker für Dropdowns, Accordion, eben alles was sich aufklappen lässt.",
            "Heroicons - chevron-down",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "chevron_up"}),
            "chevron_up",
            "Klassiker für Dropdowns, Accordion, eben alles was sich zuklappen lässt.",
            "Heroicons - chevron-up",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "chevron_both"}),
            "chevron_both",
            "Klassiker für die Andeutung einer Möglichkeit zum sortieren.",
            "Heroicons - chevron-up-down",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "chevron_left"}),
            "chevron_left",
            "Karussells, Pagination oder Elemente zum ausklappen wie z.b.: ein Drawer.",
            "Heroicons - chevron-left",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "chevron_right"}),
            "chevron_right",
            "Karussells, Pagination oder Elemente zum ausklappen wie z.b.: ein Drawer.",
            "Heroicons - chevron-right",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "tick"}),
            "tick",
            "Checklisten.",
            "Heroicons - check",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "x-mark"}),
            "x-mark",
            "Klassisch für Buttons zum schließen von Dialogen, Alerts, etc..",
            "Heroicons - x-mark",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "question-mark"}),
            "question-mark",
            "Indikator für weitere Informationen oder FAQs.",
            "Heroicons - question-mark-circle",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "sparkles"}),
            "sparkles",
            "Für spezielle Fälle, wo es um etwas besonderes geht, oder einfach kein anderes Icon passt :).",
            "Heroicons - sparkles",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "tools"}),
            "tools",
            "Einstellungen oder als Wartungssymbol.",
            "Heroicons - wrench-screwdriver",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "search"}),
            "search",
            "Klassiker für jede Suchleiste.",
            "Heroicons - magnifying-glass",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "rectangles"}),
            "rectangles",
            "Gruppen von unterschiedlichen Objekten, zum Beispiel Komponenten oder Dashboards.",
            "Heroicons - rectangle-group",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "app"}),
            "app",
            "Indikator für Anwendungen, Programme oder Dialogfenster.",
            "Heroicons - window",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "doc"}),
            "doc",
            "Klassisch für Dokumente.",
            "Heroicons - document-text",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "clipboard"}),
            "clipboard",
            "Klassisch für Copy and Paste.",
            "Heroicons - clipboard-document-check",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "cursor-click"}),
            "cursor-click",
            "Indikator für ein klickbares Element.",
            "Heroicons - cursor-arrow-rays",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "link"}),
            "link",
            "Klassisch für Anhänge bzw. Links zu Dokumenten.",
            "Heroicons - link",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "open-link"}),
            "open-link",
            "Klassisch für Links zu anderen, oft externen Seiten oder zum öffnen eines Dialogfensters.",
            "Heroicons - arrow-top-right-on-square",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "smartphone"}),
            "smartphone",
            "Hinweis auf Smartphone-Nutzung.",
            "Heroicons - device-phone-mobile",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "tablet"}),
            "tablet",
            "Hinweis auf Table-Nutzung.",
            "Heroicons - device-tablet",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "desktop"}),
            "desktop",
            "Hinweis auf Desktop-PC Nutzung.",
            "Heroicons - computer-desktop",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "sun"}),
            "sun",
            "Klassisch für Hell/Dunkel Switches.",
            "Heroicons - sun",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "moon"}),
            "moon",
            "Klassisch für Hell/Dunkel Switches.",
            "Heroicons - moon",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "git"}),
            "git",
            "Verlinkungen zu GitHub.",
            "Flowbite - github",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "user"}),
            "user",
            "Typisches Benutzericon, Benutzerprofil, Einstellungen, etc..",
            "Heroicons - user",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "clock"}),
            "clock",
            "Alles zum Thema Uhrzeit.",
            "Heroicons - clock",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "calendar"}),
            "calendar",
            "Datumsangaben, Deadlines, Termine.",
            "Heroicons - calendar-days",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "bell"}),
            "bell",
            "Typisch für Benachrichtigungen.",
            "Heroicons - bell",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "chat-bubble"}),
            "chat-bubble",
            "Interaktive Chats.",
            "Heroicons - chat-bubble-bottom-center-text",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "rocket"}),
            "rocket",
            "Besondere Dinge oder als Indikator für 'Jetzt geht`s los!'.",
            "Heroicons - rocket-launch",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "terminal"}),
            "terminal",
            "Indikator für die Verwendung des Terminals bzw. der Commandline.",
            "Heroicons - command-line",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "code"}),
            "code",
            "Hinweis auf Quellcode.",
            "Heroicons - code-bracket",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "download"}),
            "download",
            "Klassisch für Downloads.",
            "Heroicons - arrow-down-tray",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "settings"}),
            "settings",
            "Anpassungen, Einstellungen, eher für feingranulare Einstellungen.",
            "Heroicons - adjustments-horizontal",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "blueprint"}),
            "blueprint",
            "Anpassungen, Einstellungen, eher für feingranulare Einstellungen.",
            "Heroicons - cube-transparent",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "info"}),
            "info",
            "Informationen und Anmerkungen.",
            "Heroicons - information-circle",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "warning"}),
            "warning",
            "Warnhinweise, Probleme, kleinere Fehler.",
            "Heroicons - exclamation-triangle",
        ],
        [
            render_to_string("insight_ui/components/icons.html", {"name": "danger"}),
            "danger",
            "Große Fehler, kritische Probleme oder gefährliche Aktionen.",
            "Heroicons - exclamation-circle",
        ],
    ]

    icon_table = {
        "caption": "",
        "empty_msg": "",
        "headers": ["Icon", "Name", "Verwendungsbeispiele", "Quelle"],
        "rows": table_rows,
    }

    size_table = {
        "caption": "",
        "empty_msg": "",
        "headers": ["xs", "small", "default", "medium", "big"],
        "rows": [
            [
                render_to_string("insight_ui/components/icons.html", {"name": "home", "size": "xs"}),
                render_to_string("insight_ui/components/icons.html", {"name": "home", "size": "small"}),
                render_to_string("insight_ui/components/icons.html", {"name": "home", "size": ""}),
                render_to_string("insight_ui/components/icons.html", {"name": "home", "size": "medium"}),
                render_to_string("insight_ui/components/icons.html", {"name": "home", "size": "big"}),
            ]
        ],
    }

    return {"main_params": main_params, "icon_table": icon_table, "size_table": size_table}


def get_demo_container_context() -> dict:
    """Serve data of the device switch, etc. for component demos."""
    return {
        "device_radio_config": {
            "items": [
                {"tag_id": "mobile", "value": "mobile", "icon": {"name": "smartphone"}, "disabled": False},
                {"tag_id": "tablet", "value": "tablet", "icon": {"name": "tablet"}, "disabled": False},
                {"tag_id": "desktop", "value": "desktop", "icon": {"name": "desktop"}, "disabled": False},
            ]
        },
        "dir_toggle": {"label": _("RTL")},
        "theme_toggle": {"icon": {"name": "moon"}},
    }


def get_storybook_context(storybook: ComponentCategory) -> dict:
    """Serve the base context and the context for each component in the list."""
    context = get_base_context("storybook_view") | get_sidebar_context()
    components = []
    for component in Component:
        if component.group.value == storybook.value:
            context |= get_component_demo_context(component)
            components.append(component)

    context["components"] = components

    return context
