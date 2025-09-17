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
                "title": "Insight UI NavBar",
                "view_name": "storybook_view",
                "logo_url": "insight_ui/svg/ai-logo.svg",
                "logo_alt": "Insight UI Logo",
            },
            "links": [
                {
                    "text": _("Startpage"),
                    "icon": {"name": "home", "size": "small"},
                    "view_name": "storybook_view",
                    "active": True,
                    "need_auth": False,
                    "staff_only": False,
                },
                {
                    "text": _("Components"),
                    "open_dropdown": "components-menu",
                    "items": [
                        {"text": "List & Tables", "view_name": "table_storybook_view"},
                        {"text": "Cards", "view_name": "card_storybook_view"},
                        {"text": "Forms", "view_name": "form_storybook_view"},
                        {"text": "Search & Filters", "view_name": "filter_storybook_view"},
                    ],
                    "chevron": {"name": "chevron_down", "size": "small"},
                    "active": False,
                    "need_auth": False,
                    "staff_only": False,
                },
                {
                    "text": _("About"),
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
                "text": _("Settings"),
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
                "text": _("Translation"),
                "view_name": "storybook_view",
                "staff_only": True,
                "icon": {"name": "globe", "size": "small"},
            },
        ],
        "footer_data": {
            "description": {
                "title": "Insight UI",
                "text": "A modern, accessible, and responsive UI library for Django projects.",
            },
            "links": [
                {"text": _("Startpage"), "icon": {"name": "home", "size": "xs"}, "view_name": "storybook_view"},
                {"text": _("Storybook"), "view_name": "storybook_view"},
                {"text": _("Documentation"), "view_name": "storybook_view"},
            ],
        },
    }


def get_sidebar_data() -> dict:
    """Serve data for the sidebars."""
    return {
        "right_sidebar": {
            "title": _("Secondary Sidebar"),
            "icon": {"name": "home", "size": "small"},
            "categories": [
                {
                    "caption": "Main",
                    "icon": {"name": "home", "size": "small"},
                    "items": [
                        {
                            "text": _("Notifications"),
                            "icon": {"name": "home", "size": "small"},
                            "url": reverse("storybook_view"),
                        },
                        {
                            "text": _("Messages"),
                            "icon": {"name": "home", "size": "small"},
                            "url": reverse("storybook_view"),
                        },
                        {
                            "text": _("Tasks"),
                            "icon": {"name": "home", "size": "small"},
                            "url": reverse("storybook_view"),
                        },
                        {
                            "text": _("Calender"),
                            "icon": {"name": "home", "size": "small"},
                            "url": reverse("storybook_view"),
                        },
                        {
                            "text": _("Profile"),
                            "icon": {"name": "home", "size": "small"},
                            "url": reverse("storybook_view"),
                        },
                    ],
                }
            ],
        },
        "left_sidebar": {
            "title": _("Insight UI Components"),
            "icon": {"name": "cards", "size": "small"},
            "categories": [
                {
                    "caption": _("Main"),
                    "icon": {"name": "sparks", "size": "small"},
                    "items": [
                        {
                            "text": _("Alerts"),
                            "url": reverse("component_detail_page_view", kwargs={"page_name": "alert"}),
                            "htmx": {"target": "#content"},
                        },
                        {
                            "text": _("Breadcrumb-Navigation"),
                            "url": reverse("component_detail_page_view", kwargs={"page_name": "breadcrumb"}),
                            "htmx": {"target": "#content"},
                        },
                        {
                            "text": _("Chat"),
                            "url": reverse("component_detail_page_view", kwargs={"page_name": "chat"}),
                            "htmx": {"target": "#content"},
                        },
                        {
                            "text": _("Code Blocks"),
                            "url": reverse("component_detail_page_view", kwargs={"page_name": "code_block"}),
                            "htmx": {"target": "#content"},
                        },
                        {
                            "text": _("Differentiator"),
                            "url": reverse("component_detail_page_view", kwargs={"page_name": "differentiator"}),
                            "htmx": {"target": "#content"},
                        },
                        {
                            "text": _("Geo-Maps"),
                            "url": reverse("component_detail_page_view", kwargs={"page_name": "geo_map"}),
                            "htmx": {"target": "#content"},
                        },
                        {
                            "text": _("Input Elements"),
                            "url": reverse("component_detail_page_view", kwargs={"page_name": "input_elements"}),
                            "htmx": {"target": "#content"},
                        },
                        {
                            "text": _("Live-Content (Pull)"),
                            "url": reverse("component_detail_page_view", kwargs={"page_name": "live_content"}),
                            "htmx": {"target": "#content"},
                        },
                        {
                            "text": _("Modals"),
                            "url": reverse("component_detail_page_view", kwargs={"page_name": "modal"}),
                            "htmx": {"target": "#content"},
                        },
                        {
                            "text": _("Popovers"),
                            "url": reverse("component_detail_page_view", kwargs={"page_name": "popover"}),
                            "htmx": {"target": "#content"},
                        },
                        {
                            "text": _("Step Bars"),
                            "url": reverse("component_detail_page_view", kwargs={"page_name": "step_bar"}),
                            "htmx": {"target": "#content"},
                        },
                        {
                            "text": _("Tooltips"),
                            "url": reverse("component_detail_page_view", kwargs={"page_name": "tooltip"}),
                            "htmx": {"target": "#content"},
                        },
                        {
                            "text": _("Web-Sockets (Push)"),
                            "url": reverse("component_detail_page_view", kwargs={"page_name": "web_socket"}),
                            "htmx": {"target": "#content"},
                        },
                    ],
                },
                {
                    "caption": _("Lists & Tables"),
                    "icon": {"name": "sparks", "size": "small"},
                    "items": [
                        {
                            "text": _("Infinite Scroll)"),
                            "url": reverse("component_detail_page_view", kwargs={"page_name": "infinite_scroll"}),
                            "htmx": {"target": "#content"},
                        },
                        {
                            "text": _("Pagination"),
                            "url": reverse("component_detail_page_view", kwargs={"page_name": "pagination"}),
                            "htmx": {"target": "#content"},
                        },
                        {
                            "text": _("Tables"),
                            "url": reverse("component_detail_page_view", kwargs={"page_name": "table"}),
                            "htmx": {"target": "#content"},
                        },
                    ],
                },
                {
                    "caption": _("Search & Filters"),
                    "icon": {"name": "sparks", "size": "small"},
                    "items": [
                        {
                            "text": _("Generic Filter"),
                            "url": reverse("component_detail_page_view", kwargs={"page_name": "generic_filter"}),
                            "htmx": {"target": "#content"},
                        },
                        {
                            "text": _("Search Bar"),
                            "url": reverse("component_detail_page_view", kwargs={"page_name": "search_bar"}),
                            "htmx": {"target": "#content"},
                        },
                        {
                            "text": _("SQL-Like Filter"),
                            "url": reverse("component_detail_page_view", kwargs={"page_name": "sql_like_filter"}),
                            "htmx": {"target": "#content"},
                        },
                    ],
                },
                {
                    "caption": _("Cards"),
                    "icon": {"name": "sparks", "size": "small"},
                    "items": [
                        {
                            "text": _("Cards"),
                            "url": reverse("component_detail_page_view", kwargs={"page_name": "card"}),
                            "htmx": {"target": "#content"},
                        },
                        {
                            "text": _("Card Carousel"),
                            "url": reverse("component_detail_page_view", kwargs={"page_name": "card_carousel"}),
                            "htmx": {"target": "#content"},
                        },
                        {
                            "text": _("Image Carousel"),
                            "url": reverse("component_detail_page_view", kwargs={"page_name": "image_carousel"}),
                            "htmx": {"target": "#content"},
                        },
                        {
                            "text": _("Toggle-View"),
                            "url": reverse("component_detail_page_view", kwargs={"page_name": "toggle_view"}),
                            "htmx": {"target": "#content"},
                        },
                    ],
                },
                {
                    "caption": _("Forms"),
                    "icon": {"name": "sparks", "size": "small"},
                    "items": [
                        {
                            "text": _("Forms"),
                            "url": reverse("component_detail_page_view", kwargs={"page_name": "form"}),
                            "htmx": {"target": "#content"},
                        }
                    ],
                },
            ],
        },
    }


def get_table_storybook_data() -> dict:
    """Serve data for table examples."""
    # Generate data for pagination example
    page_obj, surrounding_pages = get_page(generate_payload(100))

    return (
        get_nav_and_footer_context()
        | get_sidebar_data()
        | {
            "table": {
                "caption": _("Example of a table component."),
                "empty_msg": _("No data available!"),
                "headers": [_("Name"), _("E-Mail"), _("Status"), _("Actions")],
                "rows": [
                    [
                        "Max Mustermann",
                        "max@example.com",
                        _("Active"),
                        format_html(
                            '<button class="bg-insight-primary border-insight-primary border-2 rounded-sm text-white px-6 py-2 hover:bg-insight-primary-hover active:bg-insight-primary-active hover:border-insight-primary-hover active:border-insight-primary-active transition">Bearbeiten</button>'  # noqa: E501
                        ),
                    ],
                    [
                        "Anna Schmidt",
                        "anna@example.com",
                        _("Inactive"),
                        format_html(
                            '<button class="bg-insight-primary border-insight-primary border-2 rounded-sm text-white px-6 py-2 hover:bg-insight-primary-hover active:bg-insight-primary-active hover:border-insight-primary-hover active:border-insight-primary-active transition">Bearbeiten</button>'  # noqa: E501
                        ),
                    ],
                    [
                        "Tom Weber",
                        "tom@example.com",
                        _("Active"),
                        format_html(
                            '<button class="bg-insight-primary border-insight-primary border-2 rounded-sm text-white px-6 py-2 hover:bg-insight-primary-hover active:bg-insight-primary-active hover:border-insight-primary-hover active:border-insight-primary-active transition">Bearbeiten</button>'  # noqa: E501
                        ),
                    ],
                ],
            },
            "start_page": {"page_obj": page_obj, "surrounding_pages": surrounding_pages},
            "scroll_items": [{"title": f"Element {i}", "content": f"Inhalt für Element {i}"} for i in range(1, 11)],
        }
    )


def get_card_storybook_data() -> dict:
    """Serve data for card examples."""
    # Generate data for examples
    payload = generate_payload()
    headers, rows = map_payload_to_table(payload)

    return (
        get_nav_and_footer_context()
        | get_sidebar_data()
        | {
            "cards": [
                {
                    "title": _("Example Card"),
                    "subtitle": _("Subtitle"),
                    "content": _("This is the card content."),
                    "actions": [
                        {"text": _("Learn more"), "url": "#", "type": "secondary"},
                        {"text": _("Share"), "url": "#", "type": "primary"},
                    ],
                },
                {
                    "title": "Card with actions",
                    "content": "This card has some action buttons.",
                    "actions": [
                        {"text": _("Learn more"), "url": "#", "type": "secondary"},
                        {"text": _("Share"), "url": "#", "type": "primary"},
                    ],
                },
            ],
            "horizontale_cards": [
                {
                    "title": "Horizontale Cards",
                    "content": "A card with its content arranged horizontally.",
                    "image": {"url": static("insight_ui/img/thumbnail.png"), "alt": "Card-Image"},
                    "tags": ["Test", "Test2", "Test3"],
                    "actions": [
                        {"text": _("Learn more"), "url": "#", "type": "secondary"},
                        {"text": _("Share"), "url": "#", "type": "primary"},
                    ],
                }
            ],
            "flip_cards": [
                {
                    "title": "Flip Card",
                    "content": "A card that rotates 180° and has additional content on the back.",
                    "image": {"url": static("insight_ui/img/thumbnail.png"), "alt": "Card-Image"},
                    "tags": ["Test", "Test2", "Test3"],
                    "actions": [
                        {"text": _("Learn more"), "url": "#", "type": "secondary"},
                        {"text": _("Share"), "url": "#", "type": "primary"},
                    ],
                }
            ],
            "carousel_items": map_payload_to_cards(generate_payload()),
            "image_carousel_items": [
                {
                    "description": "The famous castle served as a model for many other buildings, including the castles at the Disneyland resorts in California and Paris.",  # noqa: E501
                    "url": static("insight_ui/img/neuschwanstein.jpg"),
                    "alt": "Neuschwanstein Castle in winter.",
                },
                {
                    "description": "Before Berlin became the capital of Germany, the city had already been the capital twice: of the Mark-Brandenburg and of Prussia.",  # noqa: E501
                    "url": static("insight_ui/img/berlin.jpg"),
                    "alt": "Berlin at night.",
                },
                {
                    "description": "The Free and Hanseatic City of Hamburg is the leading member of the Hanseatic League.",  # noqa: E501
                    "url": static("insight_ui/img/hamburg.jpg"),
                    "alt": "Hamburg and an arriving S-Bahn train.",
                },
            ],
            "range_total_slides": range(3),
            "toggle_table": {"empty_msg": "No data available!", "headers": headers, "rows": rows},
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
    )


def get_form_storybook_data() -> dict:
    """Serve data for form examples."""
    return (
        get_nav_and_footer_context()
        | get_sidebar_data()
        | {
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
    )


def get_filter_storybook_data() -> dict:
    """Serve data for filter example."""
    return (
        get_nav_and_footer_context()
        | get_sidebar_data()
        | {
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
    )


def get_storybook_context() -> dict:
    """Serve data for main storybook."""
    return (
        get_nav_and_footer_context()
        | get_sidebar_data()
        | {
            "htmx_config": {"url": "/api/form-submit/", "method": "post", "target": "#htmx-form", "swap": "innerHTML"},
            "bulletpoints": [
                {
                    "title": _("Kontaktdaten"),
                    "description": _("Informationen zur Person und Anschrift."),
                    "completed": True,
                },
                {"title": _("Zahlungsmethode"), "description": _("Art der Bezahlung auswählen."), "current": True},
                {"title": _("Überprüfen"), "description": _("Prüfen der Angaben und Bezahlen.")},
            ],
        }
    )


def get_alert_context() -> dict:
    """Serve data for alert detailpage."""
    return {
        "params": {
            "caption": _("Parameter of the alert component."),
            "empty_msg": _("No data available!"),
            "headers": [_("Parameter"), _("Type"), _("Default"), _("Description")],
            "rows": [
                ["message", "str", "''", _("Die Hauptnachricht der Benachrichtigung.")],
                ["type", "str", "info", _("Der Typ der Benachrichtigung ('info', 'success', 'warning', 'error')")],
                ["dismissible", "bool", "True", _("Ob die Benachrichtigung schließbar sein soll.")],
            ],
        }
    }


def get_breadcrumb_context() -> dict:
    """Serve data for breadcrumb detailpage."""
    return {
        "breadcrumb_items": [
            {"text": _("Startpage"), "view_name": "storybook_view", "icon": {"name": "home", "size": "small"}},
            {"text": _("Demo"), "view_name": "storybook_view", "query_params": "?test=123"},
            {"text": _("Components")},
        ],
        "single_breadcrumb_item": [{"text": _("Startpage"), "icon": {"name": "home", "size": "small"}}],
    }


def get_differentiator_context() -> dict:
    """Serve data for differentiator detailpage."""
    return {"textA": "The cat is sleeping on the red sofa.", "textB": "This is a completely different sentence!"}


def get_input_element_context() -> dict:
    """Serve data for input element detailpage."""
    return {
        "user_dropdown": {
            "tag_id": "DD_user",
            "title": _("User"),
            "show_arrow": True,
            "items": [
                {"text": _("Profile"), "view_name": "storybook_view", "icon": {"name": "user", "size": "small"}},
                {"text": _("Settings"), "view_name": "storybook_view", "icon": {"name": "cog", "size": "small"}},
                {"text": _("Logout"), "view_name": "storybook_view", "icon": {"name": "got-out", "size": "small"}},
            ],
        },
        "settings_dropdown": {
            "tag_id": "DD_settings",
            "title": _("Settings"),
            "show_arrow": False,
            "items": [
                {
                    "text": _("Personal Information"),
                    "view_name": "storybook_view",
                    "icon": {"name": "user", "size": "small"},
                },
                {"text": _("Appearance"), "view_name": "storybook_view", "icon": {"name": "cog", "size": "small"}},
            ],
        },
    }


def get_modal_context() -> dict:
    """Serve data for the modal detailpage."""
    return {
        "confirm_modal_actions": [
            {"text": _("Yes, confirm"), "type": "primary", "onclick": 'alert("Confirmed!")'},
            {"text": _("Abort"), "type": "cancel", "dismiss": True},
        ]
    }


def get_step_bar_context() -> dict:
    """Serve data for step bar detailpage."""
    return {
        "steps_bar_items": [
            {
                "title": _("Kontaktdaten"),
                "description": _("Informationen zur Person und Anschrift."),
                "completed": True,
            },
            {
                "title": _("Zahlungsmethode"),
                "description": _("Art der Bezahlung auswählen."),
                "completed": False,
                "current": True,
            },
            {"title": _("Überprüfen"), "description": _("Prüfen der Angaben und Bezahlen."), "completed": False},
        ]
    }


def get_empty_context() -> dict:
    """Serve an empty dictionary."""
    return {}
