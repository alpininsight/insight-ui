from django.templatetags.static import static
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext as _

from insight_ui import config
from insight_ui.demo_utils import generate_payload, map_payload_to_cards, map_payload_to_table
from insight_ui.utils.pagination import get_page

# Some example filters for the filter example
issuedate_filters = {
    _("All"): "all",
    _("Today & Yesterday"): "newest",
    _("Last 7 days"): "7days",
    _("Last 14 days"): "14days",
    _("Last 30 days"): "30days",
    _("Last 60 days"): "60days",
    _("Without release date"): "missing",
    "-----": "-",  # no actual value, used as a divider
    "2020": "2020",
    "2021": "2021",
    "2022": "2022",
    "2023": "2023",
    "2024": "2024",
    "2025": "2025",
}
expiration_filters = {
    _("All"): "all",
    _("Expires today"): "today",
    _("Expires in 7 days at the earliest"): "7days",
    _("Expires in 14 days at the earliest"): "14days",
    _("Expires in 30 days at the earliest"): "30days",
    _("Expires in 60 days at the earliest"): "60days",
    _("Expires in 120 days at the earliest"): "120days",
    _("Without deadline"): "missing",
    "-----": "-",  # no actual value, used as a divider
    "2020": "2020",
    "2021": "2021",
    "2022": "2022",
    "2023": "2023",
    "2024": "2024",
    "2025": "2025",
}
reward_filters = {
    _("All"): "all",
    "> 200.000€": "gt_200",
    "> 100.000€": "gt_100",
    "> 50.000€": "gt_50",
    "<= 1,0€": "lt_one",
}

# Some example data for the query builder filter
DEMO_FIELDS = [
    {
        "field": "title",
        "name": _("Title"),
        "type": "text",
        "operations": {
            "iexact": _("is exact"),
            "icontains": _("contains"),
            "contains": _("contains (case sensitive)"),
            "istartswith": _("starts with"),
            "iendswith": _("ends with"),
        },
        "values": {},
    },
    {
        "field": "description",
        "name": _("Description"),
        "type": "text",
        "operations": {"icontains": _("contains"), "contains": _("contains (case sensitive)")},
        "values": {},
    },
    {
        "field": "short_description",
        "name": _("Short Description"),
        "type": "text",
        "operations": {"icontains": _("contains"), "contains": _("contains (case sensitive)")},
        "values": {},
    },
    {
        "field": "release_date",
        "name": _("Release Date"),
        "type": "date",
        "operations": {"date": _("is exact"), "date__gte": _("is not before"), "date__lte": _("is not after")},
        "values": {},
    },
    {
        "field": "deadline",
        "name": _("Deadline"),
        "type": "date",
        "operations": {"date": _("is exact"), "date__gte": _("is not before"), "date__lte": _("is not after")},
        "values": {},
    },
    {
        "field": "client__name",
        "name": _("Client"),
        "type": "text",
        "operations": {
            "iexact": _("is exact"),
            "icontains": _("contains"),
            "istartswith": _("starts with"),
            "iendswith": _("ends with"),
        },
        "values": {},
    },
]


def get_nav_and_footer_context() -> dict:
    """Serve content for navigation and footer."""
    return config.get_config() | {
        "nav_config": {
            "brand": {
                "title": "Django Insight UI NavBar",
                "view_name": "storybook_view",
                "logo_url": "insight_ui/svg/ai-logo.svg",
                "logo_alt": "Insight UI Logo",
            },
            "links": [
                {
                    "text": _("Startseite"),
                    "icon": {"name": "home", "size": "small"},
                    "view_name": "storybook_view",
                    "active": True,
                    "need_auth": False,
                    "staff_only": False,
                },
                {
                    "text": _("Komponenten"),
                    "open_dropdown": "components-menu",
                    "items": [
                        {"text": "Tabellen", "view_name": "table_storybook_view"},
                        {"text": "Kacheln", "view_name": "card_storybook_view"},
                        {"text": "Formulare", "view_name": "form_storybook_view"},
                        {"text": "Filter", "view_name": "filter_storybook_view"},
                    ],
                    "chevron": {"name": "chevron_down", "size": "small"},
                    "active": False,
                    "need_auth": False,
                    "staff_only": False,
                },
                {
                    "text": _("Über"),
                    "open_modal": "about-modal",
                    "active": False,
                    "need_auth": False,
                    "staff_only": False,
                },
                {
                    "text": _("Test"),
                    "view_name": "storybook_view",
                    "active": False,
                    "need_auth": True,
                    "staff_only": False,
                },
                {
                    "text": _("Test2"),
                    "view_name": "storybook_view",
                    "active": False,
                    "need_auth": True,
                    "staff_only": True,
                },
            ],
            "searchbar_request_view": "storybook_view",
            "show_usermenu": True,
            "show_language_selector": True,
            "show_theme_toggle": True,
        },
        "user_dropdown_links": [
            {
                "text": _("Einstellungen"),
                "view_name": "storybook_view",
                "staff_only": False,
                "icon": {"name": "cog", "size": "small"},
            },
            {
                "text": _("Administration"),
                "view_name": "admin:index",
                "staff_only": True,
                "icon": {"name": "home", "size": "small"},
            },
            {
                "text": _("Übersetzung"),
                "view_name": "storybook_view",
                "staff_only": True,
                "icon": {"name": "globe", "size": "small"},
            },
        ],
        "footer_data": {
            "description": {
                "title": "Django Insight UI",
                "text": "Eine moderne UI-Bibliothek für Django-Anwendungen mit Fokus auf Barrierefreiheit und Benutzerfreundlichkeit.",  # noqa: E501
            },
            "links": [
                {"text": _("Startseite"), "icon": {"name": "home", "size": "small"}, "view_name": "storybook_view"},
                {"text": _("Storybook"), "view_name": "storybook_view"},
                {"text": _("Dokumentation"), "view_name": "storybook_view"},
            ],
        },
    }


def get_table_storybook_data() -> dict:
    """Serve data for table examples."""
    # Generate data for pagination example
    page_obj, surrounding_pages = get_page(generate_payload(100))

    return get_nav_and_footer_context() | {
        "table": {
            "caption": _("Ein Beispiel einer Tabellen-Komponente."),
            "empty_msg": _("Keine Daten vorhanden!"),
            "headers": [_("Name"), _("E-Mail"), _("Status"), _("Aktionen")],
            "rows": [
                [
                    "Max Mustermann",
                    "max@example.com",
                    _("Aktiv"),
                    format_html(
                        '<button class="bg-insight-primary border-insight-primary border-2 rounded-sm text-white px-6 py-2 hover:bg-insight-primary-hover active:bg-insight-primary-active hover:border-insight-primary-hover active:border-insight-primary-active transition">Bearbeiten</button>'  # noqa: E501
                    ),
                ],
                [
                    "Anna Schmidt",
                    "anna@example.com",
                    _("Inaktiv"),
                    format_html(
                        '<button class="bg-insight-primary border-insight-primary border-2 rounded-sm text-white px-6 py-2 hover:bg-insight-primary-hover active:bg-insight-primary-active hover:border-insight-primary-hover active:border-insight-primary-active transition">Bearbeiten</button>'  # noqa: E501
                    ),
                ],
                [
                    "Tom Weber",
                    "tom@example.com",
                    _("Aktiv"),
                    format_html(
                        '<button class="bg-insight-primary border-insight-primary border-2 rounded-sm text-white px-6 py-2 hover:bg-insight-primary-hover active:bg-insight-primary-active hover:border-insight-primary-hover active:border-insight-primary-active transition">Bearbeiten</button>'  # noqa: E501
                    ),
                ],
            ],
        },
        "start_page": {"page_obj": page_obj, "surrounding_pages": surrounding_pages},
        "scroll_items": [{"title": f"Element {i}", "content": f"Inhalt für Element {i}"} for i in range(1, 11)],
    }


def get_card_storybook_data() -> dict:
    """Serve data for card examples."""
    # Generate data for examples
    payload = generate_payload()
    headers, rows = map_payload_to_table(payload)

    return get_nav_and_footer_context() | {
        "cards": [
            {
                "title": "Beispiel-Karte",
                "subtitle": "Untertitel",
                "content": "Dies ist der Inhalt einer Karte.",
                "actions": [
                    {"text": _("Mehr erfahren"), "url": "#", "type": "secondary"},
                    {"text": _("Teilen"), "url": "#", "type": "primary"},
                ],
            },
            {
                "title": "Karte mit Aktionen",
                "content": "Diese Karte hat Aktions-Buttons.",
                "actions": [
                    {"text": _("Mehr erfahren"), "url": "#", "type": "secondary"},
                    {"text": _("Teilen"), "url": "#", "type": "primary"},
                ],
            },
        ],
        "horizontale_cards": [
            {
                "title": "Horizontale Karte",
                "content": "Eine Karte dessen Inhalt horizontal angeordnet ist.",
                "image": {"url": static("insight_ui/img/thumbnail.png"), "alt": "Card-Image"},
                "tags": ["Test", "Test2", "Test3"],
                "actions": [
                    {"text": _("Mehr erfahren"), "url": "#", "type": "secondary"},
                    {"text": _("Teilen"), "url": "#", "type": "primary"},
                ],
            }
        ],
        "flip_cards": [
            {
                "title": "Flip Karte",
                "content": "Eine Karte die sich um 180° dreht und weiteren Inhalt auf der Rückseite bereit hält.",
                "image": {"url": static("insight_ui/img/thumbnail.png"), "alt": "Card-Image"},
                "tags": ["Test", "Test2", "Test3"],
                "actions": [
                    {"text": _("Mehr erfahren"), "url": "#", "type": "secondary"},
                    {"text": _("Teilen"), "url": "#", "type": "primary"},
                ],
            }
        ],
        "carousel_items": map_payload_to_cards(generate_payload()),
        "image_carousel_items": [
            {"description": "Test Bild 1", "url": static("insight_ui/img/text-services-main.png"), "alt": "Image 1"},
            {
                "description": "Test Bild 2",
                "url": static("insight_ui/img/text-services-response.png"),
                "alt": "Image 2",
            },
            {
                "description": "Test Bild 3",
                "url": static("insight_ui/img/text-services-response2.png"),
                "alt": "Image 3",
            },
        ],
        "range_total_slides": range(3),
        "toggle_table": {"empty_msg": "Keine Daten vorhanden!", "headers": headers, "rows": rows},
        "toggle_start_view": "table",
        "view_options": {
            "name": "view-options",
            "param_name": "view",
            "options": [
                {"id": "card-view", "value": "card", "icon": {"name": "card"}},
                {"id": "table-view", "value": "table", "icon": {"name": "list"}},
                {"id": "carousel-view", "value": "carousel", "icon": {"name": "carousel"}},
            ],
        },
    }


def get_form_storybook_data() -> dict:
    """Serve data for form examples."""
    return get_nav_and_footer_context() | {
        "form_fields": [
            {
                "type": "text",
                "name": "name",
                "label": _("Name"),
                "placeholder": _("Ihr vollständiger Name"),
                "required": True,
            },
            {
                "type": "email",
                "name": "email",
                "label": _("E-Mail"),
                "placeholder": _("ihre.email@example.com"),
                "required": True,
            },
            {
                "type": "textarea",
                "name": "message",
                "label": _("Nachricht"),
                "placeholder": _("Ihre Nachricht..."),
                "rows": 4,
            },
        ],
        "form_actions": [
            {"text": _("Absenden"), "type": "submit", "style": "primary"},
            {"text": _("Zurücksetzen"), "type": "reset", "style": "secondary"},
        ],
    }


def get_filter_storybook_data() -> dict:
    """Serve data for filter example."""
    return get_nav_and_footer_context() | {
        "filters": [
            {
                "text": _("Issue Date"),
                "icon": {"name": "home", "size": "small"},
                "name": "issuedate_filter",
                "values": issuedate_filters,
                "explanation": _("To filter by the issue date."),
            },
            {
                "text": _("Deadline"),
                "icon": {"name": "home", "size": "small"},
                "name": "expiration_filter",
                "values": expiration_filters,
                "explanation": _("To filter by the deadline."),
            },
            {
                "text": _("Reward in €"),
                "icon": {"name": "home", "size": "small"},
                "name": "reward_filter",
                "values": reward_filters,
                "explanation": _("To filter by the reward."),
            },
        ],
        "view_name": "filter_storybook_view",
        "model_fields": DEMO_FIELDS,
    }


def get_storybook_context() -> dict:
    """Serve data for main storybook."""
    return get_nav_and_footer_context() | {
        "breadcrumb_items": [
            {"text": _("Startseite"), "view_name": "storybook_view", "icon": {"name": "home", "size": "small"}},
            {"text": _("Demo"), "view_name": "storybook_view", "query_params": "?test=123"},
            {"text": _("Komponenten")},
        ],
        "single_breadcrumb_item": [{"text": _("Startseite"), "icon": {"name": "home", "size": "small"}}],
        "confirm_modal_actions": [
            {"text": _("Ja, fortfahren"), "type": "primary", "onclick": 'alert("Aktion bestätigt!")'},
            {"text": _("Abbrechen"), "type": "cancel", "dismiss": True},
        ],
        "right_sidebar_items": [
            {
                "text": _("Benachrichtigungen"),
                "icon": {"name": "home", "size": "small"},
                "url": reverse("storybook_view"),
            },
            {"text": _("Nachrichten"), "icon": {"name": "home", "size": "small"}, "url": reverse("storybook_view")},
            {"text": _("Aufgaben"), "icon": {"name": "home", "size": "small"}, "url": reverse("storybook_view")},
            {"text": _("Kalender"), "icon": {"name": "home", "size": "small"}, "url": reverse("storybook_view")},
            {"text": _("Profil"), "icon": {"name": "home", "size": "small"}, "url": reverse("storybook_view")},
        ],
        "left_sidebar_items": [
            {"text": _("Dashboard"), "icon": {"name": "home", "size": "small"}, "url": reverse("storybook_view")},
            {"text": _("Benutzer"), "icon": {"name": "home", "size": "small"}, "url": reverse("storybook_view")},
            {"text": _("Einstellungen"), "icon": {"name": "home", "size": "small"}, "url": reverse("storybook_view")},
            {"text": _("Hilfe"), "icon": {"name": "home", "size": "small"}, "url": reverse("storybook_view")},
        ],
        "htmx_config": {"url": "/api/form-submit/", "method": "post", "target": "#htmx-form", "swap": "innerHTML"},
        "textA": "The cat is sleeping on the red sofa.",
        "textB": "This is a completely different sentence!",
        "progress_bar_items": [
            {"title": "Test", "description": "Test", "completed": True},
            {"title": "Test 2", "description": "Test 2", "completed": False, "current": True},
            {"title": "Test 3", "description": "Test 3", "completed": False},
        ],
    }
