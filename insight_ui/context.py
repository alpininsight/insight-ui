from typing import Any

from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.translation import gettext as _

from insight_ui import config
from insight_ui.component_details.demo_context import get_component_demo_context
from insight_ui.demo_utils import generate_payload, map_payload_to_cards


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
                {"text": "Layout", "view_name": "storybook_view", "view_arg": "layout", "htmx": {"target": "#content"}},
                {
                    "text": "Main / Navigation",
                    "view_name": "storybook_view",
                    "view_arg": "main",
                    "htmx": {"target": "#content"},
                },
                {
                    "text": "Input Elements",
                    "view_name": "storybook_view",
                    "view_arg": "input",
                    "htmx": {"target": "#content"},
                },
                {"text": "Popups", "view_name": "storybook_view", "view_arg": "popup", "htmx": {"target": "#content"}},
                {"text": "Utils", "view_name": "storybook_view", "view_arg": "util", "htmx": {"target": "#content"}},
                {
                    "text": "List & Tables",
                    "view_name": "storybook_view",
                    "view_arg": "table",
                    "htmx": {"target": "#content"},
                },
                {"text": "Cards", "view_name": "storybook_view", "view_arg": "card", "htmx": {"target": "#content"}},
                {"text": "Forms", "view_name": "storybook_view", "view_arg": "form", "htmx": {"target": "#content"}},
                {
                    "text": "Search & Filters",
                    "view_name": "storybook_view",
                    "view_arg": "filter",
                    "htmx": {"target": "#content"},
                },
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
    return {
        "left_sidebar": {
            "title": _("Components"),
            "categories": [
                {
                    "caption": _("Layout"),
                    "items": [
                        {
                            "text": _("Page Header"),
                            "url": reverse("component_detail_page_view", kwargs={"component_name": "page_header"}),
                            "htmx": {"target": "#content"},
                        },
                        {
                            "text": _("Article"),
                            "url": reverse("component_detail_page_view", kwargs={"component_name": "article"}),
                            "htmx": {"target": "#content"},
                        },
                        {
                            "text": _("Hero Section"),
                            "url": reverse("component_detail_page_view", kwargs={"component_name": "hero"}),
                            "htmx": {"target": "#content"},
                        },
                    ],
                },
                {
                    "caption": _("Navigation / Main"),
                    "items": [
                        {
                            "text": _("Navbar"),
                            "url": reverse("component_detail_page_view", kwargs={"component_name": "navbar"}),
                            "htmx": {"target": "#content"},
                        },
                        {
                            "text": _("Sidebar"),
                            "url": reverse("component_detail_page_view", kwargs={"component_name": "sidebar"}),
                            "htmx": {"target": "#content"},
                        },
                        {
                            "text": _("Footer"),
                            "url": reverse("component_detail_page_view", kwargs={"component_name": "footer"}),
                            "htmx": {"target": "#content"},
                        },
                        {
                            "text": _("Breadcrumb Navigation"),
                            "url": reverse("component_detail_page_view", kwargs={"component_name": "breadcrumbs"}),
                            "htmx": {"target": "#content"},
                        },
                        {
                            "text": _("Step Bar"),
                            "url": reverse("component_detail_page_view", kwargs={"component_name": "step_bar"}),
                            "htmx": {"target": "#content"},
                        },
                        {
                            "text": _("Minimal Step Bar"),
                            "url": reverse("component_detail_page_view", kwargs={"component_name": "minimal_step_bar"}),
                            "htmx": {"target": "#content"},
                        },
                        {
                            "text": _("Bullet Point List"),
                            "url": reverse(
                                "component_detail_page_view", kwargs={"component_name": "bullet_point_list"}
                            ),
                            "htmx": {"target": "#content"},
                        },
                        {
                            "text": _("Accordion"),
                            "url": reverse("component_detail_page_view", kwargs={"component_name": "accordion"}),
                            "htmx": {"target": "#content"},
                        },
                        {
                            "text": _("Tabs"),
                            "url": reverse("component_detail_page_view", kwargs={"component_name": "tabs"}),
                            "htmx": {"target": "#content"},
                        },
                    ],
                },
                {
                    "caption": _("Input Elements"),
                    "items": [
                        {
                            "text": _("Buttons"),
                            "url": reverse("component_detail_page_view", kwargs={"component_name": "button"}),
                            "htmx": {"target": "#content"},
                        },
                        {
                            "text": _("Input Fields"),
                            "url": reverse("component_detail_page_view", kwargs={"component_name": "input_field"}),
                            "htmx": {"target": "#content"},
                        },
                        {
                            "text": _("Checkboxes"),
                            "url": reverse("component_detail_page_view", kwargs={"component_name": "checkbox"}),
                            "htmx": {"target": "#content"},
                        },
                        {
                            "text": _("Checkbox-Group"),
                            "url": reverse("component_detail_page_view", kwargs={"component_name": "checkbox_group"}),
                            "htmx": {"target": "#content"},
                        },
                        {
                            "text": _("Dropdown"),
                            "url": reverse("component_detail_page_view", kwargs={"component_name": "dropdown"}),
                            "htmx": {"target": "#content"},
                        },
                        {
                            "text": _("Radio-Group"),
                            "url": reverse("component_detail_page_view", kwargs={"component_name": "radio_group"}),
                            "htmx": {"target": "#content"},
                        },
                        {
                            "text": _("Range Slider"),
                            "url": reverse("component_detail_page_view", kwargs={"component_name": "range_slider"}),
                            "htmx": {"target": "#content"},
                        },
                        {
                            "text": _("Toggle-Buttons"),
                            "url": reverse("component_detail_page_view", kwargs={"component_name": "toggle"}),
                            "htmx": {"target": "#content"},
                        },
                        {
                            "text": _("Select"),
                            "url": reverse("component_detail_page_view", kwargs={"component_name": "select"}),
                            "htmx": {"target": "#content"},
                        },
                        {
                            "text": _("Multiselect"),
                            "url": reverse("component_detail_page_view", kwargs={"component_name": "multiselect"}),
                            "htmx": {"target": "#content"},
                        },
                        {
                            "text": _("Chat"),
                            "url": reverse("component_detail_page_view", kwargs={"component_name": "chat"}),
                            "htmx": {"target": "#content"},
                        },
                    ],
                },
                {
                    "caption": _("Popups"),
                    "items": [
                        {
                            "text": _("Alerts"),
                            "url": reverse("component_detail_page_view", kwargs={"component_name": "alert"}),
                            "htmx": {"target": "#content"},
                        },
                        {
                            "text": _("Modals"),
                            "url": reverse("component_detail_page_view", kwargs={"component_name": "modal"}),
                            "htmx": {"target": "#content"},
                        },
                        {
                            "text": _("Popovers"),
                            "url": reverse("component_detail_page_view", kwargs={"component_name": "popover"}),
                            "htmx": {"target": "#content"},
                        },
                        {
                            "text": _("Tooltips"),
                            "url": reverse("component_detail_page_view", kwargs={"component_name": "tooltip"}),
                            "htmx": {"target": "#content"},
                        },
                    ],
                },
                {
                    "caption": _("Utils"),
                    "items": [
                        {
                            "text": _("Code Blocks"),
                            "url": reverse("component_detail_page_view", kwargs={"component_name": "code_block"}),
                            "htmx": {"target": "#content"},
                        },
                        {
                            "text": _("Differentiator"),
                            "url": reverse("component_detail_page_view", kwargs={"component_name": "differentiator"}),
                            "htmx": {"target": "#content"},
                        },
                        {
                            "text": _("Progress Bar"),
                            "icon": {"name": "tools", "size": "xs"},
                            "url": reverse("component_detail_page_view", kwargs={"component_name": "progress_bar"}),
                            "htmx": {"target": "#content"},
                        },
                        {
                            "text": _("Geo-Maps"),
                            "url": reverse("component_detail_page_view", kwargs={"component_name": "geo_map"}),
                            "htmx": {"target": "#content"},
                        },
                        {
                            "text": _("Charts"),
                            "url": reverse("component_detail_page_view", kwargs={"component_name": "chart"}),
                            "htmx": {"target": "#content"},
                        },
                        {
                            "text": _("Live-Content (Pull)"),
                            "url": reverse("component_detail_page_view", kwargs={"component_name": "live_content"}),
                            "htmx": {"target": "#content"},
                        },
                        {
                            "text": _("Web-Sockets (Push)"),
                            "icon": {"name": "tools", "size": "xs"},
                            "url": reverse("component_detail_page_view", kwargs={"component_name": "web_socket"}),
                            "htmx": {"target": "#content"},
                        },
                    ],
                },
                {
                    "caption": _("Lists & Tables"),
                    "items": [
                        {
                            "text": _("Infinite Scroll"),
                            "url": reverse("component_detail_page_view", kwargs={"component_name": "infinite_scroll"}),
                            "htmx": {"target": "#content"},
                        },
                        {
                            "text": _("Pagination"),
                            "url": reverse("component_detail_page_view", kwargs={"component_name": "pagination"}),
                            "htmx": {"target": "#content"},
                        },
                        {
                            "text": _("Tables"),
                            "url": reverse("component_detail_page_view", kwargs={"component_name": "table"}),
                            "htmx": {"target": "#content"},
                        },
                    ],
                },
                {
                    "caption": _("Search & Filters"),
                    "items": [
                        {
                            "text": _("Generic Filter"),
                            "url": reverse("component_detail_page_view", kwargs={"component_name": "generic_filter"}),
                            "htmx": {"target": "#content"},
                        },
                        {
                            "text": _("Search Bar"),
                            "url": reverse("component_detail_page_view", kwargs={"component_name": "search_bar"}),
                            "htmx": {"target": "#content"},
                        },
                        {
                            "text": _("Query-Builder"),
                            "url": reverse("component_detail_page_view", kwargs={"component_name": "query_builder"}),
                            "htmx": {"target": "#content"},
                        },
                    ],
                },
                {
                    "caption": _("Cards"),
                    "items": [
                        {
                            "text": _("Cards"),
                            "url": reverse("component_detail_page_view", kwargs={"component_name": "card"}),
                            "htmx": {"target": "#content"},
                        },
                        {
                            "text": _("Card Carousel"),
                            "url": reverse("component_detail_page_view", kwargs={"component_name": "card_carousel"}),
                            "htmx": {"target": "#content"},
                        },
                        {
                            "text": _("Image Carousel"),
                            "url": reverse("component_detail_page_view", kwargs={"component_name": "image_carousel"}),
                            "htmx": {"target": "#content"},
                        },
                        {
                            "text": _("3D Carousel"),
                            "url": reverse("component_detail_page_view", kwargs={"component_name": "3d_carousel"}),
                            "htmx": {"target": "#content"},
                        },
                        {
                            "text": _("Toggle-View"),
                            "url": reverse("component_detail_page_view", kwargs={"component_name": "toggle_view"}),
                            "htmx": {"target": "#content"},
                        },
                    ],
                },
                {
                    "caption": _("Forms"),
                    "items": [
                        {
                            "text": _("Forms"),
                            "url": reverse("component_detail_page_view", kwargs={"component_name": "form"}),
                            "htmx": {"target": "#content"},
                        }
                    ],
                },
            ],
        }
    }


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
        ["name", "str", "Name des Icons (siehe Tabelle unten).", "question-mark"],
        ["size", "str", "Größe des Icons. Mögliche Werte sind: 'big', 'medium', 'small' und 'xs'", "default"],
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
            "settings",
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
            render_to_string("insight_ui/components/icons.html", {"name": "cog"}),
            "cog",
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


def get_storybook_context(components: list[str]) -> dict:
    """Serve the base context and the context for each component in the list."""
    context = get_base_context("storybook_view") | get_sidebar_context()
    for component in components:
        context |= get_component_demo_context(component)

    return context


def get_layout_storybook_context() -> dict:
    """Serve data for layout storybook."""
    return get_storybook_context([])


def get_main_storybook_context() -> dict:
    """Serve data for main storybook."""
    return get_storybook_context(
        ["sidebar", "breadcrumbs", "step_bar", "minimal_step_bar", "bullet_point_list", "accordion", "tabs"]
    )


def get_inputs_storybook_context() -> dict:
    """Serve data for input elements storybook."""
    return get_storybook_context(
        ["checkbox", "radio_group", "toggle_button", "range_slider", "dropdown", "select", "multiselect"]
    )


def get_popup_storybook_context() -> dict:
    """Serve data for popup storybook."""
    return get_storybook_context(["alert", "modal"])


def get_utils_storybook_context() -> dict:
    """Serve data for utils storybook."""
    return get_storybook_context(["differentiator", "geo_map"])


def get_table_storybook_context() -> dict:
    """Serve data for table examples."""
    return get_storybook_context(["table", "pagination", "infinite_scroll"])


def get_card_storybook_context() -> dict:
    """Serve data for card examples."""
    return get_storybook_context(["card", "image_carousel", "toggle_view", "3d_carousel"]) | {
        "carousel_items": map_payload_to_cards(generate_payload())
    }


def get_form_storybook_context() -> dict:
    """Serve data for form examples."""
    return get_storybook_context(["form"])


def get_filter_storybook_context() -> dict:
    """Serve data for filter example."""
    return get_storybook_context(["generic_filter", "query_builder"])
