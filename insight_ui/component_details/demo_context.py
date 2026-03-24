from django.templatetags.static import static
from django.urls import reverse
from django.utils.lorem_ipsum import paragraphs
from django.utils.translation import gettext as _

from insight_ui import config
from insight_ui.component_details.component_context import get_demo_context, register_demo_context
from insight_ui.component_details.components import Component
from insight_ui.demo_utils import generate_payload, map_payload_to_cards, map_payload_to_table
from insight_ui.utils.pagination import get_page

# Some example filters for the filter example
model_type_options = {
    "placeholder": "-- Select model --",
    "language": "Language Model",
    "vision": "Vision Model",
    "multimodal": "Multimodal Model",
    "audio": "Audio / Speech Processing",
    "recommendation": "Recommendation System",
    "generative": "Generative Model",
}
runtime_options = {
    "placeholder": "-- Select runtime --",
    "cloud": "Cloud (API-based)",
    "edge": "Edge / On-Device",
    "local": "Local (Self-hosted)",
    "hybrid": "Hybrid (Cloud + Local)",
    "serverless": "Serverless Deployment",
}
license_options = {
    "placeholder": "-- Select license --",
    "free": "Free / Open Source",
    "freemium": "Freemium",
    "subscription": "Subscription",
    "pay_per_use": "Pay per Use",
    "enterprise": "Enterprise License",
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


def get_component_demo_context(component: Component) -> dict:
    """Serve component demo context."""
    context_func = get_demo_context(component)

    if not context_func:
        context_func = get_empty_context()

    return context_func


def get_login_screen_context() -> dict:
    """Serve context data for the login screen."""
    return (
        config.get_config()
        | get_footer_context()
        | {
            "logo": {
                "url": "svg/ai-logo.svg",
                "url_dark": "svg/ai-logo.svg",
                "alt": _("Our Logo"),
                "height": "8rem",
                "position": "center",
            },
            "forgot_password": {"url": "#"},
            "alt_login": {"url": "#", "title": _("Login with OIDC")},
            "sign_up": {"url": "#"},
        }
    )


@register_demo_context(Component.NAVBAR)
def get_navbar_context() -> dict:
    """Serve data for navbar detailpage."""
    return {
        "demo_nav_config": {
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
            "links": [
                {
                    "text": _("Startpage"),
                    "icon": {"name": "home", "size": "small"},
                    "view_name": "index_view",
                    "active": True,
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
                {"text": _("Test"), "view_name": "index_view", "active": False, "need_auth": True, "staff_only": False},
                {"text": _("Test2"), "view_name": "index_view", "active": False, "need_auth": True, "staff_only": True},
            ],
            "searchbar_request_view": "index_view",
            "show_usermenu": True,
            "show_language_selector": True,
            "show_theme_toggle": True,
        },
        "user_dropdown_links": [
            {
                "text": _("Settings"),
                "view_name": "index_view",
                "staff_only": False,
                "icon": {"name": "gear", "size": "small"},
            },
            {
                "text": _("Administration"),
                "view_name": "admin:index",
                "staff_only": True,
                "icon": {"name": "home", "size": "small"},
            },
            {
                "text": _("Translation"),
                "view_name": "index_view",
                "staff_only": True,
                "icon": {"name": "globe", "size": "small"},
            },
        ],
    }


@register_demo_context(Component.SIDEBAR)
def get_drawer_context() -> dict:
    """Serve data for sidebar detailpage."""
    return {
        "demo_sidebar": {
            "title": _("Personal Settings"),
            "icon": {"name": "home", "size": "small"},
            "categories": [
                {
                    "caption": "Work",
                    "icon": {"name": "office", "size": "small"},
                    "items": [
                        {
                            "text": _("Notifications"),
                            "icon": {"name": "bell", "size": "small"},
                            "url": reverse("index_view"),
                        },
                        {
                            "text": _("Messages"),
                            "icon": {"name": "chat-bubble", "size": "small"},
                            "url": reverse("index_view"),
                        },
                        {
                            "text": _("Tasks"),
                            "icon": {"name": "checklist", "size": "small"},
                            "url": reverse("index_view"),
                        },
                    ],
                },
                {
                    "caption": "Management",
                    "icon": {"name": "gear", "size": "small"},
                    "items": [
                        {
                            "text": _("Calendar"),
                            "icon": {"name": "calendar", "size": "small"},
                            "url": reverse("index_view"),
                        },
                        {"text": _("Profile"), "icon": {"name": "user", "size": "small"}, "url": reverse("index_view")},
                    ],
                },
            ],
        }
    }


@register_demo_context(Component.FOOTER)
def get_footer_context() -> dict:
    """Server data for footer detailpage."""
    return {
        "footer_data": {
            "description": {
                "title": "Insight UI",
                "text": _("A modern, accessible, and responsive UI library for Django projects."),
                "image": {
                    "url": "img/thumbnail.png",
                    "url_dark": "img/thumbnail.png",
                    "alt": "Footer image",
                    "height": "6rem",
                },
            },
            "links": [
                {"text": _("Startpage"), "icon": {"name": "home", "size": "xs"}, "view_name": "index_view"},
                {"text": _("Storybook"), "view_name": "index_view"},
                {"text": _("Documentation"), "view_name": "index_view"},
            ],
            "contact": {
                "mail_url": "support@alpininsight.com",
                "imprint": "https://alpininsight.com/imprint/",
                "privacy": "https://alpininsight.com/privacy/",
            },
            "copyright": {"year": 2026, "app_name": "Insight UI"},
        }
    }


@register_demo_context(Component.ALERT)
def get_alert_context() -> dict:
    """Serve data for alert detailpage."""
    return {
        "params": {
            "caption": _("Parameter of the alert component."),
            "empty_msg": _("No data available!"),
            "headers": [_("Parameter"), _("Type"), _("Default"), _("Description")],
            "rows": [
                ["message", "str", "''", _("The main message of the notification.")],
                ["type", "str", "info", _("The type of the notification ('info', 'success', 'warning', 'error')")],
                ["dismissible", "bool", "True", _("Whether the notification should be dismissible.")],
            ],
        }
    }


@register_demo_context(Component.BREADCRUMBS)
def get_breadcrumb_context() -> dict:
    """Serve data for breadcrumbs detailpage."""
    return {
        "breadcrumb_items": [
            {"text": _("Startpage"), "view_name": "index_view", "icon": {"name": "home", "size": "small"}},
            {"text": _("Components"), "view_name": "index_view"},
            {"text": _("Breadcrumbs")},
        ],
        "single_breadcrumb_item": [{"text": _("Startpage"), "icon": {"name": "home", "size": "small"}}],
    }


@register_demo_context(Component.DIFFERENTIATOR)
def get_differentiator_context() -> dict:
    """Serve data for differentiator detailpage."""
    return {"textA": _("The cat is sleeping on the red sofa."), "textB": _("This is a completely different sentence!")}


@register_demo_context(Component.DROPDOWN)
def get_dropdown_context() -> dict:
    """Serve data for dropdown detailpage."""
    return {
        "user_dropdown": {
            "tag_id": "DD_user",
            "title": _("User"),
            "show_arrow": True,
            "items": [
                {"text": _("Profile"), "view_name": "index_view", "icon": {"name": "user", "size": "small"}},
                {"text": _("Settings"), "view_name": "index_view", "icon": {"name": "gear", "size": "small"}},
                {"text": _("Logout"), "view_name": "index_view", "icon": {"name": "leave", "size": "small"}},
            ],
        },
        "settings_dropdown": {
            "tag_id": "DD_settings",
            "title": _("Settings"),
            "show_arrow": False,
            "items": [
                {
                    "text": _("Personal Information"),
                    "view_name": "index_view",
                    "icon": {"name": "user", "size": "small"},
                },
                {"text": _("Appearance"), "view_name": "index_view", "icon": {"name": "gear", "size": "small"}},
            ],
        },
    }


@register_demo_context(Component.MODAL)
def get_modal_context() -> dict:
    """Serve data for the modal detailpage."""
    return {
        "confirm_modal_actions": [
            {"text": _("Yes, confirm"), "type": "primary", "onclick": 'alert("Confirmed!")'},
            {"text": _("Abort"), "type": "cancel", "dismiss": True},
        ]
    }


@register_demo_context(Component.STEP_BAR)
def get_step_bar_context() -> dict:
    """Serve data for step bar detailpage."""
    return {
        "step_bar_items": [
            {
                "title": _("Contact Details"),
                "description": _("Information about the person and address."),
                "success": True,
            },
            {"title": _("Payment Method"), "description": _("Select the payment method."), "current": True},
            {"title": _("Review"), "description": _("Review the data and pay.")},
        ],
        "step_bar_items_failed": [
            {
                "title": _("Contact Details"),
                "description": _("Information about the person and address."),
                "success": True,
            },
            {"title": _("Payment Method"), "description": _("Select the payment method."), "success": True},
            {"title": _("Review"), "description": _("Review the data and pay."), "failed": True},
        ],
    }


@register_demo_context(Component.MINIMAL_STEP_BAR)
def get_minimal_step_bar_context() -> dict:
    """Serve data for minimal step bar detailpage."""
    return {
        "min_step_bar": {"step_count": 5, "current_step": 3, "icon_size": "xs"},
        "min_step_bar_with_list": {"items": ["success", "success", "failed", "active", ""], "icon_size": "xs"},
    }


@register_demo_context(Component.CHECKBOX)
def get_checkbox_context() -> dict:
    """Serve data for checkbox detailpage."""
    return {
        "example_checkbox": {
            "tag_id": "accept-agbs",
            "name": "accept_agbs",
            "value": "AGB",
            "label": _("Accept GTC"),
            "disabled": False,
        }
    }


@register_demo_context(Component.CHECKBOX_GROUP)
def get_checkbox_group_context() -> dict:
    """Serve data for checkbox group detailpage."""
    return {
        "example_checkbox_group": {
            "name": "language_select",
            "label": "Choose languages: (max. 3)",
            "as_row": True,
            "minimum_checked": 1,
            "maximum_checked": 3,
            "items": [
                {"tag_id": "english", "value": "english", "label": _("English"), "disabled": False},
                {"tag_id": "german", "value": "german", "label": _("German"), "disabled": False},
                {"tag_id": "french", "value": "french", "label": _("French"), "disabled": False},
                {"tag_id": "spanish", "value": "spanish", "label": _("Spanish"), "disabled": False},
                {
                    "tag_id": "italian",
                    "value": "italian",
                    "label": _("Italian (currently not available)"),
                    "disabled": True,
                },
            ],
        }
    }


@register_demo_context(Component.RADIO_GROUP)
def get_radio_group_context() -> dict:
    """Serve data for radio group detailpage."""
    return get_radio_block_context() | {
        "example_radio": {
            "name": "radio-example1",
            "items": [
                {"tag_id": "model1", "value": "BERT", "label": _("BERT"), "disabled": False},
                {"tag_id": "model2", "value": "PaLM 2", "label": _("PaLM 2"), "disabled": False},
                {
                    "tag_id": "model3",
                    "value": "LLaMA 2",
                    "label": _("LLaMA 2 (currently not available)"),
                    "disabled": True,
                },
            ],
        }
    }


@register_demo_context(Component.RADIO_BLOCK)
def get_radio_block_context() -> dict:
    """Serve data for radio block detailpage."""
    return {
        "view_radio_config": {
            "name": "view",
            "param_name": "view",
            "items": [
                {"tag_id": "card-view", "value": "card", "icon": {"name": "cards"}},
                {"tag_id": "table-view", "value": "table", "icon": {"name": "list"}},
                {"tag_id": "carousel-view", "value": "carousel", "icon": {"name": "carousel"}},
            ],
        },
        "size_radio_config": {
            "name": "size",
            "param_name": "size",
            "items": [
                {"tag_id": "small-size", "value": "small", "label": "sm"},
                {"tag_id": "medium-size", "value": "medium", "label": "md"},
                {"tag_id": "large-size", "value": "large", "label": "lg"},
            ],
        },
    }


@register_demo_context(Component.TOGGLE)
def get_toggle_button_context() -> dict:
    """Serve data for toggle-button detailpage."""
    return {"example_toggle": {"tag_id": "toggle_button_example1", "label": _("Click me!"), "switch": True}}


@register_demo_context(Component.SELECT)
def get_select_context() -> dict:
    """Serve data for select detailpage."""
    return {
        "select_config": {"name": "capital", "label": _("Capitals:"), "options": [_("Berlin"), _("Rome"), _("London")]}
    }


@register_demo_context(Component.MULTISELECT)
def get_multiselect_context() -> dict:
    """Serve data for multiselect detailpage."""
    return {
        "multiselect_config": {
            "name": "capital",
            "label": _("Capitals:"),
            "maximum": 3,
            "show_buttons": False,
            "options": [_("Berlin"), _("Rome"), _("London"), _("Brussels"), _("Paris"), _("Warsaw")],
            "selected_options": [_("Rome"), _("Paris"), _("Berlin")],
        }
    }


@register_demo_context(Component.RANGE_SLIDER)
def get_range_slider_context() -> dict:
    """Serve data for range-slider detailpage."""
    return {
        "example_slider": {
            "tag_id": "range_slider_example",
            "name": "range_slider_example",
            "label": "Range Slider Title",
            "value": 1000,
            "minimum": 100,
            "maximum": 1500,
            "items": [_("100€ (minimum)"), "500€", "750€", "1000€", _("1500€ (maximum)")],
        }
    }


register_demo_context(Component.INFINITE_SCROLL)


def get_infinite_scroll_context() -> dict:
    """Serve data for infinite scroll detailpage."""
    return {
        "scroll_items": [
            {"title": f"{_('Element')} {i}", "content": f"{_('Content for element')} {i}"} for i in range(1, 11)
        ]
    }


@register_demo_context(Component.PAGINATION)
def get_pagination_context() -> dict:
    """Serve data for pagination detailpage."""
    page_obj, surrounding_pages = get_page(generate_payload(500))
    ipp_config = {"name": "ipp", "label": _("Items per page"), "options": [10, 20, 30]}

    return {"start_page": page_obj, "surrounding_pages": surrounding_pages, "ipp_config": ipp_config}


@register_demo_context(Component.TABLE)
def get_table_context() -> dict:
    """Serve data for table detailpage."""
    return {
        "table": {
            "caption": _("Example of a table component."),
            "empty_msg": _("No data available!"),
            "headers": [_("Name"), _("E-mail"), _("Status"), _("Actions")],
            "rows": [
                [
                    "Max Mustermann",
                    "max@example.com",
                    _("Active"),
                    '<button class="bg-insight-primary border-insight-primary border-2 rounded-sm text-white px-6 py-2 hover:bg-insight-primary-hover active:bg-insight-primary-active hover:border-insight-primary-hover active:border-insight-primary-active transition">Bearbeiten</button>',  # noqa: E501
                ],
                [
                    "Anna Schmidt",
                    "anna@example.com",
                    _("Inactive"),
                    '<button class="bg-insight-primary border-insight-primary border-2 rounded-sm text-white px-6 py-2 hover:bg-insight-primary-hover active:bg-insight-primary-active hover:border-insight-primary-hover active:border-insight-primary-active transition">Bearbeiten</button>',  # noqa: E501
                ],
                [
                    "Tom Weber",
                    "tom@example.com",
                    _("Active"),
                    '<button class="bg-insight-primary border-insight-primary border-2 rounded-sm text-white px-6 py-2 hover:bg-insight-primary-hover active:bg-insight-primary-active hover:border-insight-primary-hover active:border-insight-primary-active transition">Bearbeiten</button>',  # noqa: E501
                ],
            ],
        }
    }


@register_demo_context(Component.GENERIC_FILTER)
def get_generic_filter_context() -> dict:
    """Serve data for generic filter detailpage."""
    return {
        "filters": [
            {
                "text": _("AI model type"),
                "icon": {"name": "rocket", "size": "small"},
                "name": "model_type_filter",
                "values": model_type_options,
                "explanation": _("To filter by the type of AI-Model."),
            },
            {
                "text": _("Runtime"),
                "icon": {"name": "clock", "size": "small"},
                "name": "runtime_filter",
                "values": runtime_options,
                "explanation": _("To filter by the runtime."),
            },
            {
                "text": _("License"),
                "icon": {"name": "doc", "size": "small"},
                "name": _("To filter by license."),
                "values": license_options,
            },
        ],
        "filter_view_name": "index_view",
    }


@register_demo_context(Component.QUERY_BUILDER)
def get_query_builder_context() -> dict:
    """Serve data for the query-builder detailpage."""
    return {"model_fields": DEMO_FIELDS}


@register_demo_context(Component.CARD)
def get_cards_context() -> dict:
    """Serve data for cards detailpage."""
    return {
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
                "title": _("Card with actions"),
                "content": _("This card has some action buttons."),
                "actions": [
                    {"text": _("Learn more"), "url": "#", "type": "secondary"},
                    {"text": _("Share"), "url": "#", "type": "primary"},
                ],
            },
        ],
        "app_cards": [
            {
                "title": _("App Card"),
                "content": _("A card with its content arranged horizontally."),
                "image": {"url": static("insight_ui/img/thumbnail.png"), "alt": _("Card-Image")},
                "tags": ["Test", "Test2", "Test3"],
                "actions": [
                    {"text": _("Learn more"), "url": "#", "type": "secondary"},
                    {"text": _("Share"), "url": "#", "type": "primary"},
                ],
            }
        ],
        "flip_cards": [
            {
                "title": _("Flip Card"),
                "content": _("A card that rotates 180° and has additional content on the back."),
                "image": {"url": static("insight_ui/img/thumbnail.png"), "alt": _("Card-Image")},
                "tags": ["Test", "Test2", "Test3"],
                "actions": [
                    {"text": _("Learn more"), "url": "#", "type": "secondary"},
                    {"text": _("Share"), "url": "#", "type": "primary"},
                ],
            }
        ],
    }


@register_demo_context(Component.CARD_CAROUSEL)
def get_card_carousel_context() -> dict:
    """Serve data for card carousel detailpage."""
    return {"carousel_items": map_payload_to_cards(generate_payload())}


@register_demo_context(Component.IMAGE_CAROUSEL)
def get_image_carousel_context() -> dict:
    """Serve data for image carousel detailpage."""
    seeds = ["neuschwanstein", "berlin-night", "hamburg-harbour"]
    lorem_blocks = paragraphs(len(seeds), common=False)

    image_carousel_items = [
        {
            "description": lorem_blocks[index],
            "url": f"https://picsum.photos/seed/{seed}/1200/675",
            "alt": _("Placeholder image %(index)s") % {"index": index + 1},
        }
        for index, seed in enumerate(seeds)
    ]

    return {"image_carousel_items": image_carousel_items}


@register_demo_context(Component.TOGGLE_VIEW)
def get_toggle_view_context() -> dict:
    """Serve data for toggle-view detailpage."""
    payload = generate_payload()
    headers, rows = map_payload_to_table(payload)

    return {
        "toggle_table": {"empty_msg": _("No data available!"), "headers": headers, "rows": rows},
        "toggle_start_view": "table",
        "view_radio_config": {
            "name": "view",
            "items": [
                {"tag_id": "card-view", "value": "card", "icon": {"name": "cards"}},
                {"tag_id": "table-view", "value": "table", "icon": {"name": "list"}},
                {"tag_id": "carousel-view", "value": "carousel", "icon": {"name": "carousel"}},
            ],
        },
    }


@register_demo_context(Component.FORM)
def get_form_context() -> dict:
    """Serve data for form detailpage."""
    return {
        "form_fields": [
            {
                "input_type": "select",
                "tag_id": "title",
                "name": "title",
                "label": _("Title"),
                "placeholder": _("Your title"),
                "options": [_("No title"), "Prof.", "Dr.", _("King")],
            },
            {
                "input_type": "text",
                "tag_id": "firstname",
                "name": "firstname",
                "label": _("First name"),
                "placeholder": _("Type in your first name"),
                "required": True,
            },
            {
                "input_type": "text",
                "tag_id": "lastname",
                "name": "lastname",
                "label": _("Last name"),
                "placeholder": _("Type in your last name"),
                "required": True,
            },
            {
                "input_type": "email",
                "tag_id": "email",
                "name": "email",
                "label": _("E-mail"),
                "placeholder": _("Type in your.email@example.com"),
                "required": True,
            },
            {
                "input_type": "password",
                "tag_id": "password",
                "name": "password",
                "label": _("Password"),
                "placeholder": _("Type in your password"),
                "required": True,
            },
            {
                "input_type": "textarea",
                "tag_id": "message",
                "name": "message",
                "label": _("Message"),
                "placeholder": _("Do you want to tell us something?..."),
                "rows": 3,
            },
        ],
        "show_reset_button": True,
        "htmx_config": {"target": "#htmx-form", "swap": "innerHTML"},
    }


@register_demo_context(Component.BULLET_POINT_LIST)
def get_bullet_point_list_context() -> dict:
    """Server data for bullet point list detailpage."""
    return {
        "bulletpoints": [
            {
                "title": _("Contact Details"),
                "description": _("Information about the person and address."),
                "completed": True,
            },
            {"title": _("Payment Method"), "description": _("Select the payment method."), "current": True},
            {"title": _("Review"), "description": _("Review the data and pay.")},
        ]
    }


@register_demo_context(Component.ACCORDION)
def get_accordion_context() -> dict:
    """Serve data for accordion detailpage."""
    return {
        "accordion_items": [
            {"title": _("What is Django?"), "content": _("Django is a web framework for Python.")},
            {"title": _("What is Tailwind?"), "content": _("Tailwind is a CSS utility framework")},
            {"title": _("What is ARIA?"), "content": _("ARIA is short for Accessible Rich Internet Applications.")},
        ]
    }


@register_demo_context(Component.TABS)
def get_tabs_context() -> dict:
    """Serve data for tabs detailpage."""
    return {
        "tabs_config": {
            "tag_id": "example_tabs",
            "label": _("Tabs Example"),
            "tabs": [
                {"tag_id": "first", "url": reverse("tabs_view", kwargs={"tab_id": "first"}), "title": _("First Tab")},
                {
                    "tag_id": "second",
                    "url": reverse("tabs_view", kwargs={"tab_id": "second"}),
                    "title": _("Second Tab"),
                },
                {"tag_id": "third", "url": reverse("tabs_view", kwargs={"tab_id": "third"}), "title": _("Third Tab")},
            ],
        }
    }


@register_demo_context(Component.THREE_D_CAROUSEL)
def get_3d_carousel_context() -> dict:
    """Serve data for 3D carousel detailpage."""
    return {"3D_carousel": {"items": map_payload_to_cards(generate_payload())}}


@register_demo_context(Component.CHART)
def get_charts_context() -> dict:
    """Serve data for charts detailpage."""
    return {
        "chart_data": {
            "title": _("Chart Example"),
            "x_axis_legend": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
            "series": ["Email", "Union Ads", "Video Ads", "Direct", "Search Engine"],
            "data": [
                [100, 302, 301, 334, 390, 330, 320],
                [320, 132, 101, 134, 90, 230, 210],
                [220, 182, 191, 234, 290, 330, 310],
                [150, 212, 201, 154, 190, 330, 410],
                [820, 832, 901, 934, 1290, 1330, 1320],
            ],
        }
    }


@register_demo_context(Component.GEO_MAP)
def get_geo_map_context() -> dict:
    """Serve data for geo-map detailpage."""
    return {
        "geo_map_data": {
            "initial_coords": [52.5200, 13.4050],
            "initial_zoom": 8,
            "datasets": [
                {
                    "name": "population",
                    "type": "circle",
                    "min": 300000,
                    "max": 3800000,
                    "data": [
                        {"title": "Berlin", "value": 3769000, "lat": 52.5200, "lon": 13.4050},
                        {"title": "Hamburg", "value": 1850000, "lat": 53.5511, "lon": 9.9937},
                        {"title": "München", "value": 1488000, "lat": 48.1351, "lon": 11.5820},
                        {"title": "Köln", "value": 1086000, "lat": 50.9375, "lon": 6.9603},
                        {"title": "Frankfurt am Main", "value": 763000, "lat": 50.1109, "lon": 8.6821},
                        {"title": "Stuttgart", "value": 635000, "lat": 48.7758, "lon": 9.1829},
                        {"title": "Düsseldorf", "value": 620000, "lat": 51.2277, "lon": 6.7735},
                        {"title": "Leipzig", "value": 612000, "lat": 51.3397, "lon": 12.3731},
                        {"title": "Dortmund", "value": 588000, "lat": 51.5136, "lon": 7.4653},
                        {"title": "Essen", "value": 582000, "lat": 51.4556, "lon": 7.0116},
                        {"title": "Bremen", "value": 569000, "lat": 53.0793, "lon": 8.8017},
                        {"title": "Dresden", "value": 558000, "lat": 51.0504, "lon": 13.7373},
                        {"title": "Hannover", "value": 540000, "lat": 52.3759, "lon": 9.7320},
                        {"title": "Nürnberg", "value": 523000, "lat": 49.4521, "lon": 11.0767},
                        {"title": "Duisburg", "value": 499000, "lat": 51.4344, "lon": 6.7623},
                        {"title": "Bochum", "value": 363000, "lat": 51.4818, "lon": 7.2162},
                        {"title": "Wuppertal", "value": 361000, "lat": 51.2562, "lon": 7.1508},
                        {"title": "Bielefeld", "value": 341000, "lat": 52.0302, "lon": 8.5325},
                        {"title": "Bonn", "value": 330000, "lat": 50.7374, "lon": 7.0982},
                        {"title": "Münster", "value": 323000, "lat": 51.9607, "lon": 7.6261},
                    ],
                },
                {
                    "name": "hanseatic_cities",
                    "type": "marker",
                    "data": [
                        {
                            "title": "Lübeck",
                            "lat": 53.8655,
                            "lon": 10.6866,
                            "description": "Hauptstadt der Hanse („Königin der Hanse“); Sitz der Hansetage und Zentrum des Ostseehandels.",  # noqa: E501
                        },
                        {
                            "title": "Hamburg",
                            "lat": 53.5511,
                            "lon": 9.9937,
                            "description": "Wichtiger Nordseehafen; Umschlagplatz für den England- und Nordseehandel.",
                        },
                        {
                            "title": "Bremen",
                            "lat": 53.0793,
                            "lon": 8.8017,
                            "description": "Bedeutend im England- und Skandinavienhandel; Nordseezugang der Hanse.",
                        },
                        {
                            "title": "Köln",
                            "lat": 50.9375,
                            "lon": 6.9603,
                            "description": "Größte Stadt der Hanse; zentraler Binnenhandelsknoten am Rhein.",
                        },
                        {
                            "title": "Danzig (Gdańsk)",
                            "lat": 54.3520,
                            "lon": 18.6466,
                            "description": "Wichtigster Hafen im Ostseeraum; Export von Getreide, Holz und Bernstein.",
                        },
                        {
                            "title": "Riga",
                            "lat": 56.9496,
                            "lon": 24.1052,
                            "description": "Zentrum des Hansehandels im Baltikum; Umschlagplatz für Waren aus Russland und Skandinavien.",  # noqa: E501
                        },
                        {
                            "title": "Reval (Tallinn)",
                            "lat": 59.4370,
                            "lon": 24.7536,
                            "description": "Wichtige Zwischenstation für Russland- und Skandinavienhandel.",
                        },
                        {
                            "title": "Visby",
                            "lat": 57.6409,
                            "lon": 18.2960,
                            "description": "Frühes Hansezentrum auf Gotland; Knotenpunkt des Ostseehandels.",
                        },
                        {
                            "title": "Bergen",
                            "lat": 60.3913,
                            "lon": 5.3221,
                            "description": "Kontorstadt der Hanse in Norwegen; Handel mit Stockfisch und Pelzen.",
                        },
                        {
                            "title": "Brügge",
                            "lat": 51.2093,
                            "lon": 3.2247,
                            "description": "Zentrale für Tuchhandel in Flandern; wichtiges westliches Handelszentrum.",
                        },
                        {
                            "title": "London (Stalhof)",
                            "lat": 51.5074,
                            "lon": -0.1278,
                            "description": "Hanse-Kontor für den Englandhandel; Sitz des „Stalhofs“ im Mittelalter.",
                        },
                        {
                            "title": "Nowgorod",
                            "lat": 58.5215,
                            "lon": 31.2755,
                            "description": "Östlichstes Hansekontor; Handel mit Fellen, Wachs und Honig im Russlandgeschäft.",  # noqa: E501
                        },
                    ],
                },
            ],
        }
    }


def get_empty_context() -> dict:
    """Serve an empty dictionary."""
    return {}
