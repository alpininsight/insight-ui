from dataclasses import dataclass

from django.utils.translation import gettext as _

from insight_ui.component_details.component_context import register_component
from insight_ui.component_details.components import Component


@dataclass
class ParameterDetails:
    """Describes a component parameter, with a 'name', 'type', 'description' and the 'default' value."""

    name: str
    type: str
    description: str
    default: str


@dataclass
class ParameterDoc:
    """Represents the documentation of a component parameter."""

    details: ParameterDetails
    params_table: list[ParameterDetails]
    example_data: str
    notes: list[dict[str, str]] = None


@register_component(Component.PAGE_HEADER)
def get_page_header_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the page_header component."""
    main_params = [
        ParameterDetails("title", "str", _("The page title, displayed as h1 in white text."), "''"),
        ParameterDetails("description", "str or list[str]", _("An optional description below the title."), "''"),
    ]

    return {"params": [main_params]}


@register_component(Component.HEADING_DECORATION)
def get_heading_decoration_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the heading_decoration component."""
    config_param = ParameterDoc(
        ParameterDetails(
            "config",
            "dict[str, Any]",
            _("Alternative dictionary-based configuration for all heading decoration parameters."),
            "{}",
        ),
        [
            ParameterDetails(
                "style",
                "str",
                _("Decoration style: 'waves', 'image', 'gradient', or 'none'. Unknown values fall back to 'waves'."),
                "'waves'",
            ),
            ParameterDetails(
                "color",
                "str",
                _("Optional CSS color override. By default the component follows --color-insight-primary."),
                "''",
            ),
            ParameterDetails("image_url", "str", _("Background image URL used when style is 'image'."), "''"),
            ParameterDetails("height", "int", _("Decoration height in pixels."), "90"),
        ],
        """
        {
            "style": "gradient",
            "height": 72,
        }
        """,
    )

    main_params = [
        ParameterDetails(
            "style",
            "str",
            _("Decoration style: 'waves', 'image', 'gradient', or 'none'. Unknown values fall back to 'waves'."),
            "'waves'",
        ),
        ParameterDetails(
            "color",
            "str",
            _("Optional CSS color override. By default the component follows --color-insight-primary."),
            "''",
        ),
        ParameterDetails("image_url", "str", _("Background image URL used when style is 'image'."), "''"),
        ParameterDetails("height", "int", _("Decoration height in pixels."), "90"),
        config_param.details,
    ]

    return {"params": [main_params, config_param]}


@register_component(Component.ARTICLE)
def get_article_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the article component."""
    main_params = [
        ParameterDetails("content", "str", _("The text content of the article (can contain HTML)."), "''"),
        ParameterDetails("columns", "int", _("The number of columns for the CSS columns layout."), "2"),
        ParameterDetails("column_gap", "str", _("The gap between the columns (CSS unit)."), "'2rem'"),
        ParameterDetails("title", "str", _("An optional title above the article."), "''"),
    ]

    return {"params": [main_params]}


@register_component(Component.HERO)
def get_hero_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the hero component."""
    cta_param = ParameterDoc(
        ParameterDetails("cta_primary", "dict[str, str]", _("Primary 'Call-to-Action' button."), "{}"),
        [
            ParameterDetails("url", "str", _("URL to be called when the button is clicked."), "''"),
            ParameterDetails("text", "str", _("Button label."), "''"),
        ],
        """
            {"url": "/newsletter", "content": "Subscribe to Newsletter"}
        """,
    )

    badge_param = ParameterDoc(
        ParameterDetails("badge", "dict[str, str]", _("A badge with icon and text."), "{}"),
        [
            ParameterDetails("text", "str", _("Badge label."), "''"),
            ParameterDetails("icon", "dict[str, str]", _("An optional icon displayed before the text."), "{}"),
        ],
        """
            {"url": "/newsletter", "content": "Subscribe to Newsletter"}
        """,
    )

    main_params = [
        ParameterDetails("title", "str", _("Title of the Hero section."), "''"),
        ParameterDetails("subtitle", "int", _("Subtitle of the Hero section, displayed below the title."), "''"),
        ParameterDetails(
            "description",
            "str",
            _("Description of the Hero section, displayed below the title and above the subtitle."),
            "''",
        ),
        cta_param.details,
        ParameterDetails("cta_secondary", "dict[str, str]", _("Secondary 'Call-to-Action' button."), "{}"),
        ParameterDetails("background_image_url", "str", _("URL of the background image."), "''"),
        badge_param.details,
    ]

    return {"params": [main_params, cta_param, badge_param]}


@register_component(Component.CORNER_RIBBON)
def get_corner_ribbon_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the corner_ribbon component."""
    config_param = ParameterDoc(
        ParameterDetails(
            "config",
            "dict[str, Any]",
            _("Alternative dictionary-based configuration for all corner ribbon parameters."),
            "{}",
        ),
        [
            ParameterDetails("text", "str", _("The text displayed in the ribbon."), "''"),
            ParameterDetails(
                "position",
                "str",
                _(
                    "Corner position: 'top-right', 'top-left', 'bottom-right', 'bottom-left'. "
                    "Invalid values fall back to 'top-right'."
                ),
                "'top-right'",
            ),
            ParameterDetails(
                "color",
                "str",
                _(
                    "Color variant: 'primary', 'success', 'warning', 'danger', 'info'. "
                    "Invalid values fall back to 'primary'."
                ),
                "'primary'",
            ),
            ParameterDetails("tag_id", "str", _("An optional, unique ID for JavaScript/CSS targeting."), "''"),
        ],
        """
        {
            "text": "New Feature",
            "position": "top-right",
            "color": "success",
        }
        """,
    )

    main_params = [
        ParameterDetails("text", "str", _("The text displayed in the ribbon."), "''"),
        ParameterDetails(
            "position",
            "str",
            _(
                "Corner position: 'top-right', 'top-left', 'bottom-right', 'bottom-left'. "
                "Invalid values fall back to 'top-right'."
            ),
            "'top-right'",
        ),
        ParameterDetails(
            "color",
            "str",
            _(
                "Color variant: 'primary', 'success', 'warning', 'danger', 'info'. "
                "Invalid values fall back to 'primary'."
            ),
            "'primary'",
        ),
        ParameterDetails("tag_id", "str", _("An optional, unique ID for JavaScript/CSS targeting."), "''"),
        config_param.details,
    ]

    return {"params": [main_params, config_param]}


@register_component(Component.NAVBAR)
def get_navbar_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the navbar component."""
    logo_param = ParameterDoc(
        ParameterDetails("logo", "dict[str, str]", _("Describes the logo that is displayed next to the title."), "{}"),
        [
            ParameterDetails(
                "url", "str", _("Path to the logo file for the light theme."), "insight_ui/svg/ai-logo.svg"
            ),
            ParameterDetails(
                "url_dark", "str", _("Path to the logo file for the dark theme."), "insight_ui/svg/ai-logo-dark.svg"
            ),
            ParameterDetails("alt", "str", _("Alternative text of the logo."), "Insight UI Logo"),
            ParameterDetails("height", "str", _("This value determines the size of the logo."), "2rem"),
        ],
        """""",
    )

    brand_param = ParameterDoc(
        ParameterDetails(
            "brand", "dict[str, Any]", _("Describes the title and the logo of the application in the navbar."), "{}"
        ),
        [
            ParameterDetails("title", "str", _("The title of the application."), "''"),
            ParameterDetails("view_name", "str", _("Name of the URL to be called when clicking on the title."), "''"),
            ParameterDetails(
                "gap", "str", _("This value determines the spacing between the logo and the title."), "0.5rem"
            ),
            logo_param.details,
        ],
        """""",
    )

    links_param = ParameterDoc(
        ParameterDetails("links", "list[dict]", _("Contains and describes the navigation items of the navbar."), "[]"),
        [
            ParameterDetails("text", "str", _("Label of the link."), "''"),
            ParameterDetails("icon", "dict[str, str]", _("An optional icon displayed before the text."), "{}"),
            ParameterDetails("view_name", "str", _("Name of the URL to be called when clicking on the link."), "''"),
            ParameterDetails(
                "open_modal", "str", _("ID of the modal dialog to be displayed when clicking on the link."), "''"
            ),
            ParameterDetails(
                "active",
                "bool",
                _(
                    "Visually distinguishes the link from the others to indicate that the user is currently on that page."
                ),
                "True",
            ),
            ParameterDetails("need_auth", "bool", _("The link is only displayed for logged-in users."), "False"),
            ParameterDetails("staff_only", "bool", _("The link is only displayed for administrators."), "False"),
        ],
        """""",
    )

    config_param = ParameterDoc(
        ParameterDetails(
            "config",
            "dict[str, Any]",
            _("A dictionary containing the entire configuration of the navigation bar."),
            "{}",
        ),
        [
            brand_param.details,
            links_param.details,
            ParameterDetails(
                "searchbar_request_view",
                "str",
                _("Name of the URL to be called when performing a search. If empty, no search bar will be displayed."),
                "''",
            ),
            ParameterDetails(
                "show_usermenu", "bool", _("Displays a dropdown menu with at least a logout button."), "False"
            ),
            ParameterDetails(
                "show_language_selector",
                "bool",
                _("Displays a dropdown menu for selecting the display language (if defined)."),
                "False",
            ),
            ParameterDetails(
                "show_theme_toggle",
                "bool",
                _("Displays a button to switch between the light and dark theme of the page."),
                "False",
            ),
        ],
        """
        {
            "brand": {
                "title": "Insight UI",
                "view_name": "storybook_view",
                "gap": "0.5rem",
                "logo": {
                    "url": "insight_ui/svg/ai-logo.svg",
                    "url_dark": "insight_ui/svg/ai-logo-dark.svg",
                    "alt": "Insight UI Logo",
                    "height": "2rem",
                },
            },
            "links": [
                {
                    "text": _("Startseite"),
                    "icon": {"name": "home", "size": "s"},
                    "view_name": "storybook_view",
                    "active": True,
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
            ],
            "searchbar_request_view": "search_view",
            "show_usermenu": True,
            "show_language_selector": True,
            "show_theme_toggle": True,
        }
        """,
    )

    main_params = [
        config_param.details,
        ParameterDetails(
            "user", "User", _("The _user_ object of the request (usually available via _request.user_)."), "None"
        ),
        ParameterDetails("user_dropdown_links", "list", _("A list of links to be displayed in the user menu."), "[]"),
        ParameterDetails("show_login", "bool", _("**True** if a button for logging in should be displayed."), "false"),
        ParameterDetails("search_query", "str", _("Search string for the search bar."), "''"),
    ]

    notes_begin = [
        {
            "type": "info",
            "message": _(
                "The external parameter **show_login** is used to hide the login button on certain pages, such as the login page."
            ),
        }
    ]

    return {
        "params": [main_params, config_param, brand_param, logo_param, links_param],
        "params_notes_begin": notes_begin,
    }


@register_component(Component.SIDEBAR)
def get_sidebar_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the sidebar component."""
    main_params = [
        ParameterDetails(
            "sidebar_data", "dict[str, Any]", _("Content of the sidebar (title and navigation elements)."), "None"
        ),
        ParameterDetails("side", "str", _("Determines on which side the sidebar should be placed."), "right"),
        ParameterDetails("static", "bool", _("**True** if the sidebar should not be collapsible."), "True"),
        ParameterDetails(
            "auto_close", "bool", _("If **True** the sidebar closes as soon as the cursor leaves it."), "False"
        ),
        ParameterDetails(
            "mobile_hidden", "bool", _("If **True** the static sidebar is hidden on a smaller viewport."), "False"
        ),
        ParameterDetails(
            "navbar_fixed",
            "bool",
            _("If **True** the position of the content is adjusted. (FOR CUSTOM SIDEBAR ONLY!)"),
            "False",
        ),
    ]

    return {"params": [main_params]}


@register_component(Component.FOOTER)
def get_footer_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the footer component."""
    image_param = ParameterDoc(
        ParameterDetails("image", "dict[str, str]", _("Optional image displayed below the description text."), "{}"),
        [
            ParameterDetails(
                "url", "str", _("Path to the image file for the light theme."), "insight_ui/svg/ai-logo.svg"
            ),
            ParameterDetails(
                "url_dark", "str", _("Path to the image file for the dark theme."), "insight_ui/svg/ai-logo-dark.svg"
            ),
            ParameterDetails("alt", "str", _("Alternative text of the logo."), "Insight UI Logo"),
            ParameterDetails("height", "str", _("This value determines the size of the logo."), "2rem"),
        ],
        """
        {
            "url": "insight_ui/svg/ai-logo.svg",
            "url_dark": "insight_ui/svg/ai-logo-dark.svg",
            "alt": "Insight UI Logo",
            "height": "6rem",
        }
        """,
    )

    description_param = ParameterDoc(
        ParameterDetails(
            "description", "dict[str, Any]", _("Brief description of the application with optional image."), "{}"
        ),
        [
            ParameterDetails("title", "str", _("Heading of the description."), "''"),
            ParameterDetails("text", "str", _("Brief summary of the application."), "''"),
            image_param.details,
        ],
        """
        {
            "title": "Insight UI",
            "text": "A modern UI library for Django applications to get started quickly.",
            "image": {
                "url": "insight_ui/svg/ai-logo.svg",
                "url_dark": "insight_ui/svg/ai-logo-dark.svg",
                "alt": "Insight UI Logo",
                "height": "6rem",
            },
        },
        """,
    )

    links_param = ParameterDoc(
        ParameterDetails(
            "links", "list[dict[str, Any]]", _("List of the main navigation items of the application."), "[]"
        ),
        [
            ParameterDetails("text", "str", _("Label of the link."), "''"),
            ParameterDetails("icon", "dict[str, str]", _("An optional icon displayed before the text."), "{}"),
            ParameterDetails("view_name", "str", _("Name of the URL to be called when clicking on the link."), "''"),
            ParameterDetails(
                "open_modal", "str", _("ID of the modal dialog to be displayed when clicking on the link."), "''"
            ),
            ParameterDetails(
                "active",
                "bool",
                _(
                    "Visually distinguishes the link from the others to indicate that the user is currently on that page."
                ),
                "True",
            ),
            ParameterDetails("need_auth", "bool", _("The link is only displayed for logged-in users."), "False"),
            ParameterDetails("staff_only", "bool", _("The link is only displayed for administrators."), "False"),
        ],
        """
        [
            {"text": _("Indexpage"), "icon": {"name": "home", "size": "s"}, "view_name": "index_view"},
            {"text": _("Storybook"), "view_name": "storybook_view"},
            {"text": _("Documentation"), "view_name": "doc_view"},
        ]
        """,
    )

    contact_param = ParameterDoc(
        ParameterDetails(
            "contact",
            "dict[str, Any]",
            _("Contact information, link to the imprint, privacy policy and a contact email address."),
            "{}",
        ),
        [
            ParameterDetails("mail_url", "str", _("URL of a contact email address."), "''"),
            ParameterDetails("imprint", "str", _("Link to an imprint."), "''"),
            ParameterDetails("privacy", "str", _("Link to a privacy policy."), "''"),
        ],
        """
        {
            "mail_url": "support@alpininsight.com",
            "imprint": "https://alpininsight.com/imprint/",
            "privacy": "https://alpininsight.com/privacy/",
        }
        """,
    )

    copyright_param = ParameterDoc(
        ParameterDetails(
            "copyright",
            "dict[str, str]",
            _("Copyright information, such as the year, holder, source label, and license text."),
            "{}",
        ),
        [
            ParameterDetails("year", "int", _("Typically the current year (not strictly required)."), "undefined"),
            ParameterDetails("holder", "str", _("The copyright holder. Falls back to app_name."), "''"),
            ParameterDetails("app_name", "str", _("Backwards-compatible fallback for the holder name."), "''"),
            ParameterDetails("source_label", "str", _("Optional source model label, for example Open Source."), "''"),
            ParameterDetails("license_text", "str", _("Optional license label, for example AGPL-3.0."), "''"),
            ParameterDetails("license_url", "str", _("Optional URL for the license label."), "''"),
            ParameterDetails("separator", "str", _("Separator between legal metadata parts."), "'·'"),
            ParameterDetails("rights_text", "str", _("Optional rights statement."), "'All rights reserved.'"),
        ],
        """
        {
            "year": 2026,
            "holder": "Alpin Insight Solutions GmbH & Co. KG",
            "source_label": "Open Source",
            "license_text": "AGPL-3.0",
            "license_url": "https://github.com/alpininsight/insight-ui/blob/develop/LICENSE",
        }
        """,
    )

    data_param = ParameterDoc(
        ParameterDetails("data", "dict[str, Any]", _("Data to be displayed in the footer."), "{}"),
        [
            description_param.details,
            links_param.details,
            contact_param.details,
            copyright_param.details,
            ParameterDetails("version", "str", _("Information about the current version."), "''"),
        ],
        """
        {
            "description": {
                "title": "Insight UI",
                "text": "A modern UI library for Django applications to get started quickly.",
                "image": {
                    "url": "insight_ui/svg/ai-logo.svg",
                    "url_dark": "insight_ui/svg/ai-logo-dark.svg",
                    "alt": "Insight UI Logo",
                    "height": "6rem",
                },
            },
            "links": [
                {"text": _("Indexpage"), "icon": {"name": "home", "size": "s"}, "view_name": "index_view"},
                {"text": _("Storybook"), "view_name": "storybook_view"},
                {"text": _("Documentation"), "view_name": "doc_view"},
            ],
            "contact": {
                "mail_url": "support@alpininsight.com",
                "imprint": "https://alpininsight.com/imprint/",
                "privacy": "https://alpininsight.com/privacy/",
            },
            "copyright": {
                "year": 2026,
                "holder": "Alpin Insight Solutions GmbH & Co. KG",
                "source_label": "Open Source",
                "license_text": "AGPL-3.0",
                "license_url": "https://github.com/alpininsight/insight-ui/blob/develop/LICENSE",
            },
            "version": "v1.0.0",
        }
        """,
    )

    main_params = [data_param.details]

    return {
        "params": [main_params, data_param, description_param, image_param, links_param, contact_param, copyright_param]
    }


@register_component(Component.BREADCRUMBS)
def get_breadcrumb_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the breadcrumbs component."""
    links_param = ParameterDoc(
        ParameterDetails("items", "list[dict[str, Any]]", _("List of navigation items."), "[]"),
        [
            ParameterDetails("text", "str", _("Label of the link."), "''"),
            ParameterDetails(
                "icon", "dict[str, str]", _("An optional parameter, in case the view to be called requires one."), "{}"
            ),
            ParameterDetails("view_name", "str", _("Name of the URL to be called when clicking on the link."), "''"),
            ParameterDetails(
                "query_params", "str", _("An optional parameter, in case the view to be called requires one."), "''"
            ),
        ],
        """
        [
            {"text": _("Indexpage"), "icon": {"name": "home", "size": "s" %}, "view_name": "index_view"},
            {"text": _("Components"), "view_name": "components_view"},
            {"text": _("Breadcrumbs")},
        ]
        """,
    )

    main_params = [links_param.details]

    return {"params": [main_params, links_param]}


@register_component(Component.STEP_BAR)
def get_step_bar_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the step bar component."""
    step_param = ParameterDoc(
        ParameterDetails("items", "list[dict]", _("List of process steps."), "[]"),
        [
            ParameterDetails("title", "str", _("Title of the step."), "''"),
            ParameterDetails("description", "str", _("Additional description of the step below the title."), "''"),
            ParameterDetails("url", "str", _("URL called when the user clicks on the title of the step."), "''"),
            ParameterDetails("success", "bool", _("Displays a checkmark instead of the step number."), "False"),
            ParameterDetails("failed", "bool", _("Displays an X instead of the step number."), "False"),
            ParameterDetails("current", "bool", _("Highlights the title in color and makes the text pulse."), "False"),
        ],
        """
        [
            {"title": "Contact Information", "description": "Personal information and address.", "completed": True},
            {"title": "Payment method", "description": "Method of payment.", "current": True},
            {"title": "Check", "description": "Review the details and pay."},
        ]
        """,
    )

    main_params = [step_param.details]

    return {"params": [main_params, step_param]}


@register_component(Component.MINIMAL_STEP_BAR)
def get_minimal_step_bar_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the minimal step bar component."""
    config_param = ParameterDoc(
        ParameterDetails("config", "dict[str, Any]", _("Configuration of the step bar."), "{}"),
        [
            ParameterDetails(
                "items",
                "list[str]",
                _(
                    "List of states for the process steps. Possible values: 'success', 'failed', 'active' and '' for inactive."
                ),
                "[]",
            ),
            ParameterDetails("step_count", "int", _("Number of process steps. (Only if 'items' is not set!)"), "0"),
            ParameterDetails(
                "current_step", "int", _("Current step of the process. (Only if 'items' is not set!)"), "0"
            ),
            ParameterDetails(
                "current_step_status", "str", _("Status of the current step. (Only if 'items' is not set!)"), "'active'"
            ),
            ParameterDetails("icon_size", "str", _("Size of the icons in the progress bar."), "xs"),
        ],
        """""",
    )

    main_params = [config_param.details]

    return {"params": [main_params, config_param]}


@register_component(Component.BULLET_POINT_LIST)
def get_bullet_point_list_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the bullet point list component."""
    step_param = ParameterDoc(
        ParameterDetails("items", "list[dict]", _("List of the individual items."), "[]"),
        [
            ParameterDetails("title", "str", _("Title of the step."), "''"),
            ParameterDetails("description", "str", _("Additional description of the step below the title."), "''"),
            ParameterDetails(
                "bullet_icon",
                "dict[str, str]",
                _("An optional icon displayed instead of the normal bullet point."),
                "''",
            ),
            ParameterDetails(
                "bullet_text", "str", _("An optional text displayed instead of the normal bullet point."), "''"
            ),
            ParameterDetails(
                "view_name", "str", _("Name of the URL to be called when clicking on the respective item."), "''"
            ),
            ParameterDetails("completed", "bool", _("Displays a checkmark instead of a bullet point."), "False"),
            ParameterDetails("current", "bool", _("Highlights the title by color."), "False"),
        ],
        """
        [
            {"title": _("Kontaktdaten"), "description": _("Informationen zur Person und Anschrift."), "completed": True},
            {"title": _("Zahlungsmethode"), "description": _("Art der Bezahlung auswählen."), "current": True},
            {"title": _("Überprüfen"), "description": _("Prüfen der Angaben und Bezahlen.")},
        ]
        """,
    )

    main_params = [step_param.details]

    return {"params": [main_params, step_param]}


@register_component(Component.ACCORDION)
def get_accordion_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the accordion component."""
    item_param = ParameterDoc(
        ParameterDetails("items", "list[dict]", _("List of individual sections."), "[]"),
        [
            ParameterDetails("title", "str", _("Section title."), "''"),
            ParameterDetails("content", "str", _("Section content."), "''"),
        ],
        """
        [
            {"title": "What is Django?", "content": "Django is a web framework for Python."},
            {"title": "What is Tailwind?", "content": "Tailwind is a CSS utility framework"},
            {"title": "What is ARIA?", "content": "ARIA is short for Accessible Rich Internet Applications."},
        ]
        """,
    )

    main_params = [
        ParameterDetails("tag_id", "str", _("Unique tag ID for identifying the element in JavaScript."), "''"),
        item_param.details,
        ParameterDetails("exclusive", "bool", _("If **True** only one section can be open at a time."), "False"),
    ]

    return {"params": [main_params, item_param]}


@register_component(Component.TABS)
def get_tabs_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the tabs component."""
    tabs_param = ParameterDoc(
        ParameterDetails("tabs", "list[dict]", _("List of tab buttons."), "[]"),
        [
            ParameterDetails("id", "str", _("Unique tag ID for identifying the element in JavaScript."), "''"),
            ParameterDetails("url", "str", _("The URL to be called when the tab is clicked."), "''"),
            ParameterDetails("title", "str", _("Label of the tab button."), "''"),
            ParameterDetails("icon", "dict[str, str]", _("An optional icon displayed before the label."), "{}"),
        ],
        """
        [
            {
                "id": "First",
                "url": reverse("tabs_view", kwargs={"tab_id": "first"}),
                "title": _("First Tab"),
            },
            {
                "id": "Second",
                "url": reverse("tabs_view", kwargs={"tab_id": "second"}),
                "title": _("Second Tab"),
            },
            {
                "id": "Third",
                "url": reverse("tabs_view", kwargs={"tab_id": "third"}),
                "title": _("Third Tab"),
            }
        ]
        """,
    )

    config_param = ParameterDoc(
        ParameterDetails(
            "config", "dict[str, Any]", _("Describes the buttons used to switch between individual tabs."), "{}"
        ),
        [
            ParameterDetails("id", "str", _("Unique tag ID for identifying the element in JavaScript."), "''"),
            ParameterDetails(
                "label", "str", _("Non-visible additional title that is to be read aloud by screen readers."), "''"
            ),
            tabs_param.details,
        ],
        """
        {
            "id": "example_tabs",
            "label": "Tabs Example",
            "tabs": [
                {
                    "id": "First",
                    "url": reverse("tabs_view", kwargs={"tab_id": "first"}),
                    "title": _("First Tab"),
                },
                {
                    "id": "Second",
                    "url": reverse("tabs_view", kwargs={"tab_id": "second"}),
                    "title": _("Second Tab"),
                },
                {
                    "id": "Third",
                    "url": reverse("tabs_view", kwargs={"tab_id": "third"}),
                    "title": _("Third Tab"),
                }
            ]
        }
        """,
    )

    main_params = [config_param.details]

    return {"params": [main_params, config_param, tabs_param]}


@register_component(Component.INPUT_FIELD)
def get_input_field_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the input field component."""
    main_params = [
        ParameterDetails(
            "tag_id", "str", _("Optional, unique tag ID for identifying the element in JavaScript."), "''"
        ),
        ParameterDetails("name", "str", _("Required for a `<form>`, as the name of the request parameter."), "''"),
        ParameterDetails(
            "input_type", "str", _("The type of the input field, e.g.: 'text', 'password', 'date', etc."), "''"
        ),
        ParameterDetails(
            "placeholder",
            "str",
            _("Placeholder text, displayed in the field as long as it has not been selected."),
            "''",
        ),
        ParameterDetails("value", "str", _("The value of the input field."), "''"),
        ParameterDetails("minimum", "int", _("Smallest numeric value (for `input_type='number'`)."), "undefined"),
        ParameterDetails("maximum", "int", _("Largest numeric value (for `input_type='number'`)."), "undefined"),
        ParameterDetails("min_length", "int", _("Minimum number of characters in a text field."), "undefined"),
        ParameterDetails("max_length", "int", _("Maximum number of characters in a text field."), "undefined"),
        ParameterDetails(
            "checked", "bool", _("**True** if `input_type='checkbox'` and the checkbox should be selected."), "False"
        ),
        ParameterDetails("required", "bool", _("**True** if the field must be filled in."), "False"),
        ParameterDetails("disabled", "bool", _("**True** if the field should be disabled."), "False"),
        ParameterDetails("label", "str", _("A text label displayed above the input field."), "''"),
        ParameterDetails(
            "config",
            "dict[str, Any]",
            _("An alternative configuration with keys corresponding to the previous parameters."),
            "{}",
        ),
    ]

    return {"params": [main_params]}


@register_component(Component.TEXTAREA)
def get_textarea_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the textarea component."""
    main_params = [
        ParameterDetails(
            "tag_id", "str", _("Optional, unique tag ID for identifying the element in JavaScript."), "''"
        ),
        ParameterDetails("name", "str", _("Required for a `<form>`, as the name of the request parameter."), "''"),
        ParameterDetails(
            "placeholder",
            "str",
            _("Placeholder text, displayed in the field as long as it has not been selected."),
            "''",
        ),
        ParameterDetails("value", "str", _("The value of the input field."), "''"),
        ParameterDetails("rows", "int", _("Determines the number of lines."), "undefined"),
        ParameterDetails("cols", "int", _("Determines the number of characters in a line."), "undefined"),
        ParameterDetails("required", "bool", _("**True** if the field must be filled in."), "False"),
        ParameterDetails("disabled", "bool", _("**True** if the field should be disabled."), "False"),
        ParameterDetails("label", "str", _("A text label displayed above the input field."), "''"),
        ParameterDetails(
            "config",
            "dict[str, Any]",
            _("An alternative configuration with keys corresponding to the previous parameters."),
            "{}",
        ),
    ]

    return {"params": [main_params]}


@register_component(Component.CHECKBOX)
def get_checkbox_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the checkbox component."""
    main_params = [
        ParameterDetails(
            "tag_id", "str", _("Optional, unique tag ID for identifying the element in JavaScript."), "''"
        ),
        ParameterDetails("name", "str", _("Required for a `<form>`, as the name of the request parameter."), "''"),
        ParameterDetails(
            "value", "str", _("The value of the checkbox (this is not the state, see 'checked' for that)."), "''"
        ),
        ParameterDetails("label", "str", _("A text label displayed above the checkbox."), "''"),
        ParameterDetails("checked", "bool", _("**True** if the checkbox should be selected."), "False"),
        ParameterDetails("disabled", "bool", _("**True** if the checkbox should be disabled."), "False"),
        ParameterDetails(
            "config",
            "dict[str, Any]",
            _("An alternative configuration with keys corresponding to the previous parameters."),
            "{}",
        ),
    ]

    return {"params": [main_params]}


@register_component(Component.CHECKBOX_GROUP)
def get_checkbox_group_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the checkbox group component."""
    config_param = ParameterDoc(
        ParameterDetails(
            "config", "dict[str, Any]", _("Describes the checkbox group and the individual checkbox elements."), "{}"
        ),
        [
            ParameterDetails("name", "str", _("Required for a `<form>`, as the name of the request parameter."), "''"),
            ParameterDetails("label", "str", _("Text label displayed above the checkbox elements."), "''"),
            ParameterDetails(
                "as_row", "bool", _("**True** if the checkbox elements should be displayed side by side."), "False"
            ),
            ParameterDetails(
                "minimum_checked",
                "int",
                _("Number of checkbox elements that must be selected at minimum."),
                "undefined",
            ),
            ParameterDetails(
                "maximum_checked",
                "int",
                _("Number of checkbox elements that may be selected at the same time."),
                "undefined",
            ),
            ParameterDetails("items", "list[dict[str, Any]]", _("List of the checkbox elements."), "[]"),
        ],
        """
        {
            "name": "language_select",
            "label": "Choose languages: (max. 3)",
            "as_row": True,
            "minimum_checked": 1,
            "maximum_checked": 3,
            "items": [
                {"tag_id": "english", "value": "english", "text": _("English")},
                {"tag_id": "german", "value": "german", "text": _("German"), "checked": True},
                {"tag_id": "italian", "value": "italian", "text": _("Italian (coming soon)"), "disabled": True},
            ],
        }
        """,
    )

    main_params = [config_param.details]

    return {"params": [main_params, config_param]}


@register_component(Component.DROPDOWN)
def get_dropdown_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the dropdown component."""
    item_param = ParameterDoc(
        ParameterDetails("items", "list[dict[str, Any]]", _("A list of the menu elements."), "[]"),
        [
            ParameterDetails("text", "str", _("Label of the dropdown element."), "''"),
            ParameterDetails(
                "view_name", "str", _("Name of the URL to be called when clicking on the respective item."), "''"
            ),
            ParameterDetails("icon", "dict[str, str]", _("An optional icon displayed before the label."), "{}"),
        ],
        """
        [
            {
                "text": _("Profile"),
                "view_name": "profile_view",
                "icon": {"name": "user", "size": "s"},
            },
        ]
        """,
    )

    dropdown_menu_param = ParameterDoc(
        ParameterDetails(
            "dropdown_menu", "dict[str, Any]", _("Describes the dropdown button and the menu elements."), "{}"
        ),
        [
            ParameterDetails(
                "tag_id", "str", _("Optional, unique tag ID for identifying the element in JavaScript."), "''"
            ),
            ParameterDetails("title", "str", _("Label of the dropdown button."), "''"),
            ParameterDetails("show_arrow", "bool", _("**True** displays an arrow behind the title."), "False"),
            item_param.details,
        ],
        """
        {
            "tag_id": "user_dropdown",
            "title": _("User"),
            "show_arrow": True,
            "items": [
                {
                    "text": _("Profile"),
                    "view_name": "profile_view",
                    "icon": {"name": "user", "size": "s"},
                },
                {
                    "text": _("Settings"),
                    "view_name": "settings_view",
                    "icon": {"name": "gear", "size": "s"},
                },
                {
                    "text": _("Logout"),
                    "view_name": "logout_view",
                    "icon": {"name": "leave", "size": "s"},
                },
            ],
        }
        """,
    )

    main_params = [dropdown_menu_param.details]

    return {"params": [main_params, dropdown_menu_param, item_param]}


@register_component(Component.RADIO_GROUP)
def get_radio_group_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the radio_group component."""
    items_param = ParameterDoc(
        ParameterDetails("items", "list[dict[str, Any]]", _("A list of the radio elements."), "[]"),
        [
            ParameterDetails(
                "tag_id", "str", _("Optional, unique tag ID for identifying the element in JavaScript."), "''"
            ),
            ParameterDetails("value", "str", _("Value of the respective radio button."), "''"),
            ParameterDetails("text", "str", _("Label of the respective radio button."), "''"),
            ParameterDetails("disabled", "bool", _("**True** if the radio button should be disabled."), "False"),
        ],
        """
        [
            {"tag_id": "model1", "value": "BERT", "text": _("BERT"), "disabled": False},
            {"tag_id": "model2", "value": "PaLM 2", "text": _("PaLM 2"), "disabled": False},
            {"tag_id": "model3", "value": "LLaMA 2", "text": _("LLaMA 2 (currently not available)"), "disabled": True},
        ]
        """,
    )

    main_params = [
        ParameterDetails("name", "str", _("Optional, unique tag ID for identifying the element in JavaScript."), "''"),
        ParameterDetails("label", "str", _("A text label displayed above the radio elements."), "''"),
        items_param.details,
        ParameterDetails(
            "as_row", "bool", _("**True** if the radio elements should be displayed side by side."), "False"
        ),
        ParameterDetails("current_value", "str", _("The value of the currently selected radio button."), "''"),
        ParameterDetails(
            "config",
            "dict[str, Any]",
            _("An alternative configuration with keys corresponding to the previous parameters."),
            "{}",
        ),
    ]

    return {"params": [main_params, items_param]}


@register_component(Component.RADIO_BLOCK)
def get_radio_block_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the radio_block component."""
    items_param = ParameterDoc(
        ParameterDetails("items", "list[dict[str, Any]]", _("A list of the radio elements."), "[]"),
        [
            ParameterDetails(
                "tag_id", "str", _("Optional, unique tag ID for identifying the element in JavaScript."), "''"
            ),
            ParameterDetails("value", "str", _("Value of the respective radio button."), "''"),
            ParameterDetails("text", "str", _("Label of the respective radio button."), "''"),
            ParameterDetails("icon", "dict[str, str]", _("Optional icon displayed before the label."), "{}"),
            ParameterDetails("disabled", "bool", _("**True** if the radio button should be disabled."), "False"),
        ],
        """
        [
            {"tag_id": "model1", "value": "BERT", "text": _("BERT"), "disabled": False},
            {"tag_id": "model2", "value": "PaLM 2", "text": _("PaLM 2"), "disabled": False},
            {"tag_id": "model3", "value": "LLaMA 2", "text": _("LLaMA 2 (currently not available)"), "disabled": True},
        ]
        """,
    )

    main_params = [
        ParameterDetails("name", "str", _("Optional, unique tag ID for identifying the element in JavaScript."), "''"),
        ParameterDetails("label", "str", _("A text label displayed above the radio elements."), "''"),
        items_param.details,
        ParameterDetails(
            "integrated",
            "bool",
            _("**True** if the group is inside a `<form>`. If **False** the group gets its own `<form>`."),
            "False",
        ),
        ParameterDetails(
            "as_row", "bool", _("**True** if the radio elements should be displayed side by side."), "False"
        ),
        ParameterDetails(
            "view_name",
            "str",
            _("Name of the URL to which the request should be sent when clicking one of the radio buttons."),
            "''",
        ),
        ParameterDetails(
            "query_params", "str", _("A string of query parameters to be sent along with the request."), "''"
        ),
        ParameterDetails(
            "hx_target_id", "str", _("The ID of the HTML tag to be replaced when switching the radio button."), "''"
        ),
        ParameterDetails("hx_swap_method", "str", _("The way in which the target is to be replaced."), "'outerHTML'"),
        ParameterDetails(
            "method",
            "str",
            _("Name of the JavaScript method to be executed when clicking one of the radio buttons."),
            "''",
        ),
        ParameterDetails("current_value", "str", _("The value of the currently selected radio button."), "''"),
        ParameterDetails(
            "config",
            "dict[str, Any]",
            _("An alternative configuration with keys corresponding to the previous parameters."),
            "{}",
        ),
    ]

    return {"params": [main_params, items_param]}


@register_component(Component.RANGE_SLIDER)
def get_rangle_slider_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the range slider component."""
    main_params = [
        ParameterDetails(
            "tag_id", "str", _("Optional, unique tag ID for identifying the element in JavaScript."), "''"
        ),
        ParameterDetails("name", "str", _("Required for a `<form>`, as the name of the request parameter."), "''"),
        ParameterDetails("label", "str", _("A text label displayed above the range slider."), "''"),
        ParameterDetails("value", "int", _("The value of the range slider."), "0"),
        ParameterDetails("minimum", "int", _("Smallest configurable value of the range slider."), "undefined"),
        ParameterDetails("maximum", "int", _("Largest configurable value of the range slider."), "undefined"),
        ParameterDetails(
            "step_size", "int", _("The size of the steps by which the value changes when moving the range slider."), "1"
        ),
        ParameterDetails("disabled", "bool", _("**True** if the range slider should be disabled."), "False"),
        ParameterDetails("items", "list[str]", _("A list of texts displayed as a legend below the slider."), "[]"),
        ParameterDetails(
            "config",
            "dict[str, Any]",
            _("An alternative configuration with keys corresponding to the previous parameters."),
            "{}",
        ),
    ]

    return {"params": [main_params]}


@register_component(Component.TOGGLE)
def get_toggle_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the toggle component."""
    main_params = [
        ParameterDetails(
            "tag_id", "str", _("Optional, unique tag ID for identifying the element in JavaScript."), "''"
        ),
        ParameterDetails("name", "str", _("Required for a `<form>`, as the name of the request parameter."), "''"),
        ParameterDetails("label", "str", _("A text label displayed above the toggle button."), "''"),
        ParameterDetails("value", "str", _("The value of the toggle button."), "''"),
        ParameterDetails(
            "switch", "bool", _("**True** if the toggle button should look like a typical switch select."), "False"
        ),
        ParameterDetails("checked", "bool", _("**True** if the toggle button should be selected."), "False"),
        ParameterDetails("disabled", "bool", _("**True** if the toggle button should be disabled."), "False"),
        ParameterDetails(
            "method", "str", _("Name of the JavaScript method to be executed when the toggle button is clicked."), "''"
        ),
        ParameterDetails(
            "config",
            "dict[str, Any]",
            _("An alternative configuration with keys corresponding to the previous parameters."),
            "{}",
        ),
    ]

    return {"params": [main_params]}


@register_component(Component.SELECT)
def get_select_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the select component."""
    main_params = [
        ParameterDetails("name", "str", _("Required for a `<form>`, as the name of the request parameter."), "''"),
        ParameterDetails("label", "str", _("A text label displayed above the select."), "''"),
        ParameterDetails("explanation", "str", _("A brief description of the filter that appears in a tooltip."), "''"),
        ParameterDetails("options", "list[str] oder dict[str, str]", _("List of values that can be selected."), "[]"),
        ParameterDetails(
            "selected_option",
            "str",
            _("Value (the key value, if the options were passed as a dict) of the currently selected option."),
            "''",
        ),
        ParameterDetails(
            "config",
            "dict[str, Any]",
            _("An alternative configuration with keys corresponding to the previous parameters."),
            "{}",
        ),
    ]

    notes_end = [{"type": "info", "message": _("If `options` is a list, the value is also used as the name.")}]

    return {"params": [main_params], "params_notes_end": notes_end}


@register_component(Component.MULTISELECT)
def get_multiselect_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the multiselect component."""
    main_params = [
        ParameterDetails("name", "str", _("Required for a `<form>`, as the name of the request parameter."), "''"),
        ParameterDetails("label", "str", _("A text label displayed above the select."), "''"),
        ParameterDetails("maximum", "int", _("Maximum number of selectable options."), "undefined"),
        ParameterDetails(
            "show_buttons", "bool", _("Show additional buttons for 'Select All' and 'Deselect All'."), "False"
        ),
        ParameterDetails("options", "list[str] oder dict[str, str]", _("List of values that can be selected."), "[]"),
        ParameterDetails("selected_options", "list[str]", _("List of currently selected options."), "[]"),
        ParameterDetails(
            "config",
            "dict[str, Any]",
            _("An alternative configuration with keys corresponding to the previous parameters."),
            "{}",
        ),
    ]

    notes_end = [{"type": "info", "message": _("If `options` is a list, the value is also used as the name.")}]

    return {"params": [main_params], "params_notes_end": notes_end}


@register_component(Component.CHAT)
def get_chat_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the chat component."""
    main_params = [
        ParameterDetails(
            "request_url", "str", _("The URL to which the request should be sent when submitting a message."), "''"
        )
    ]

    return {"params": [main_params]}


@register_component(Component.ALERT)
def get_alert_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the alert component."""
    main_params = [
        ParameterDetails(
            "tag_id", "str", _("Optional, unique tag ID for identifying the element in JavaScript."), "''"
        ),
        ParameterDetails("message", "str", _("Message displayed in the alert."), "''"),
        ParameterDetails(
            "type", "str", _("Type of the alert. Possible values are 'info', 'success', 'warning' and 'error'."), "info"
        ),
        ParameterDetails(
            "dismissible", "bool", _("Shows a button to close the alert at the end of the alert container."), "False"
        ),
    ]

    return {"params": [main_params]}


@register_component(Component.MODAL)
def get_modal_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the modal component."""
    action_button_param = ParameterDoc(
        ParameterDetails(
            "actions", "Sequence[Mapping[str, str]]", _("List of buttons displayed at the bottom of the dialog."), "[]"
        ),
        [
            ParameterDetails("text", "str", _("Button label."), "''"),
            ParameterDetails(
                "type",
                "str",
                _(
                    "Describes the importance of the button (purely visual). Possible values are: 'primary' and 'secondary'.."
                ),
                "''",
            ),
            ParameterDetails("onclick", "str", _("Call a JavaScript function, e.g.: alert('Confirmed!')"), "''"),
            ParameterDetails("dismiss", "bool", _("Closes the dialog on click."), "False"),
        ],
        """
        {
            {"text": _("Learn more"), "url": "#", "type": "secondary"},
        }
        """,
    )

    main_params = [
        ParameterDetails(
            "tag_id", "str", _("Optional, unique tag ID for identifying the element in JavaScript."), "''"
        ),
        ParameterDetails("title", "str", _("Heading of the modal dialog."), "''"),
        ParameterDetails(
            "description",
            "str or list[str]",
            _("A text in the center of the modal dialog. This can be exchanged by extending the template."),
            "[]",
        ),
        ParameterDetails(
            "width", "int", _("The maximum width of the dialog box relative to the screen in 'rem'."), "32"
        ),
        action_button_param.details,
    ]

    return {"params": [main_params, action_button_param]}


@register_component(Component.POPOVER)
def get_popover_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the popover component."""
    main_params = [
        ParameterDetails(
            "data-insight-popover='<target-id>'",
            "str",
            _("Determines the popover object to be displayed on hover."),
            "''",
        ),
        ParameterDetails(
            "data-position='<position>'",
            "str",
            _(
                "Determines where the popover should be displayed relative to the element. Possible values are: 'top', 'bottom', 'right', and 'left'."
            ),
            "''",
        ),
        ParameterDetails(
            "data-show-arrow",
            "bool",
            _("Shows an arrow at the edge of the popover pointing to the triggering object."),
            "False",
        ),
    ]

    return {"params": [main_params]}


@register_component(Component.TOOLTIP)
def get_tooltip_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the tooltip component."""
    main_params = [
        ParameterDetails(
            "data-insight-tooltip='<text>'",
            "str",
            _("Shows a tooltip with the specified text when hovering over the element."),
            "''",
        ),
        ParameterDetails(
            "data-position='<position>'",
            "str",
            _(
                "Determines where the tooltip should be displayed relative to the element. Possible values are: 'top', 'bottom', 'right', and 'left'."
            ),
            "''",
        ),
        ParameterDetails(
            "data-show-arrow",
            "bool",
            _("Shows an arrow at the edge of the tooltip pointing to the triggering object."),
            "False",
        ),
    ]

    return {"params": [main_params]}


@register_component(Component.INFOBOX)
def get_infobox_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the infobox component."""
    main_params = [
        ParameterDetails(
            "info_type",
            "str",
            _("Importance level of the message. Possible values are 'info', 'success', 'warn' or 'danger'."),
            "'info'",
        ),
        ParameterDetails("message", "str", _("Descriptive message."), "''"),
    ]

    return {"params": [main_params]}


@register_component(Component.CODE_BLOCK)
def get_code_block_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the code block component."""
    main_params = [
        ParameterDetails("id", "str", _("Optional, unique tag ID for identifying the element in JavaScript."), "''"),
        ParameterDetails(
            "data-insight-code-block",
            "str",
            _("Identifies this object as a code block and specifies the used language."),
            "''",
        ),
        ParameterDetails(
            "data-filename", "str", _("Displays the text as a hint for the user in the header of the code block."), "''"
        ),
    ]

    return {"params": [main_params]}


@register_component(Component.COPYRIGHT_NOTICE)
def get_copyright_notice_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the copyright notice component."""
    config_param = ParameterDoc(
        ParameterDetails("config", "dict[str, Any]", _("Dictionary-based copyright notice configuration."), "{}"),
        [
            ParameterDetails("year", "int | str", _("Optional copyright year."), "''"),
            ParameterDetails("holder", "str", _("Copyright holder name."), "''"),
            ParameterDetails(
                "app_name", "str", _("Backwards-compatible fallback for existing footer copyright configuration."), "''"
            ),
            ParameterDetails("source_label", "str", _("Optional source or distribution label."), "''"),
            ParameterDetails("license_text", "str", _("Optional license label."), "''"),
            ParameterDetails("license_url", "str", _("Optional URL for the license label."), "''"),
            ParameterDetails("separator", "str", _("Separator between legal metadata parts."), "'·'"),
            ParameterDetails("rights_text", "str", _("Optional rights statement."), "'All rights reserved.'"),
            ParameterDetails("class", "str", _("Additional CSS classes for the rendered notice."), "''"),
        ],
        """
        {
            "year": 2026,
            "holder": "Alpin Insight Solutions GmbH & Co. KG",
            "source_label": "Open Source",
            "license_text": "AGPL-3.0",
            "license_url": "https://github.com/alpininsight/insight-ui/blob/develop/LICENSE",
        }
        """,
    )

    main_params = [
        ParameterDetails("year", "int | str", _("Optional copyright year."), "''"),
        ParameterDetails("holder", "str", _("Copyright holder name."), "''"),
        ParameterDetails("app_name", "str", _("Backwards-compatible fallback for the holder name."), "''"),
        ParameterDetails("source_label", "str", _("Optional source or distribution label."), "''"),
        ParameterDetails("license_text", "str", _("Optional license label."), "''"),
        ParameterDetails("license_url", "str", _("Optional URL for the license label."), "''"),
        ParameterDetails("separator", "str", _("Separator between legal metadata parts."), "'·'"),
        ParameterDetails("rights_text", "str", _("Optional rights statement."), "'All rights reserved.'"),
        ParameterDetails("css_class", "str", _("Additional CSS classes for the rendered notice."), "''"),
        config_param.details,
    ]

    return {"params": [main_params, config_param]}


@register_component(Component.DIFFERENTIATOR)
def get_differentiator_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the differentiator component."""
    main_params = [
        ParameterDetails("textA", "str", _("First or older version of the text."), "''"),
        ParameterDetails("textB", "str", _("Second or newer version of the text."), "''"),
    ]

    return {"params": [main_params]}


@register_component(Component.LOGO)
def get_logo_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the logo component."""
    icon_param = ParameterDoc(
        ParameterDetails("icon", "dict[str, str] | str", _("Icon configuration used when type is 'icon'."), "{}"),
        [
            ParameterDetails("name", "str", _("Name of the Insight UI icon."), "''"),
            ParameterDetails("size", "str", _("Icon size: 'xl', 'l', 'm', 's', or 'xs'."), "'m'"),
        ],
        """
        {"name": "sparkles", "size": "xl"}
        """,
    )

    config_param = ParameterDoc(
        ParameterDetails("config", "dict[str, Any]", _("Dictionary-based logo configuration."), "{}"),
        [
            ParameterDetails("type", "str", _("Logo type: 'image', 'svg', or 'icon'."), "'image'"),
            ParameterDetails(
                "url", "str", _("Static, absolute, root-relative, or data URL for image/svg logos."), "''"
            ),
            ParameterDetails("url_dark", "str", _("Optional dark-theme URL for image/svg logos."), "''"),
            ParameterDetails("alt", "str", _("Accessible text. Empty values make image/svg logos decorative."), "''"),
            icon_param.details,
            ParameterDetails("height", "str", _("CSS height for image/svg logos."), "'2rem'"),
            ParameterDetails("width", "str", _("Optional CSS width for image/svg logos."), "''"),
            ParameterDetails("class", "str", _("Additional CSS classes for the rendered logo root."), "''"),
        ],
        """
        {
            "type": "svg",
            "url": "insight_ui/svg/ai-logo.svg",
            "url_dark": "insight_ui/svg/ai-logo-dark.svg",
            "alt": "Insight UI Logo",
            "height": "2rem",
        }
        """,
        notes=[
            {
                "type": "info",
                "message": _(
                    "Use type='svg' for SVG files stored as static assets. Use type='icon' when the mark should come from the built-in Insight UI icon set."
                ),
            }
        ],
    )

    main_params = [
        ParameterDetails("logo_type", "str", _("Logo type: 'image', 'svg', or 'icon'. Config key: 'type'."), "'image'"),
        ParameterDetails("url", "str", _("Static, absolute, root-relative, or data URL for image/svg logos."), "''"),
        ParameterDetails("url_dark", "str", _("Optional dark-theme URL for image/svg logos."), "''"),
        ParameterDetails("alt", "str", _("Accessible text. Empty values make image/svg logos decorative."), "''"),
        ParameterDetails("icon_name", "str", _("Insight UI icon name used when logo_type is 'icon'."), "''"),
        ParameterDetails("icon_size", "str", _("Icon size used when logo_type is 'icon'."), "'medium'"),
        ParameterDetails("height", "str", _("CSS height for image/svg logos."), "'2rem'"),
        ParameterDetails("width", "str", _("Optional CSS width for image/svg logos."), "''"),
        ParameterDetails("css_class", "str", _("Additional CSS classes for the rendered logo root."), "''"),
        config_param.details,
    ]

    return {"params": [main_params, config_param, icon_param]}


@register_component(Component.PROGRESS_BAR)
def get_progress_bar_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the progress bar component."""
    main_params = [ParameterDetails("TODO!", "-", "-", "-")]

    return {"params": [main_params]}


@register_component(Component.GEO_MAP)
def get_geo_map_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the geo map component."""
    data_param = ParameterDoc(
        ParameterDetails("data", "list[dict]", _("List of data entries."), "-"),
        [
            ParameterDetails("lat", "double", _("Latitude of the data entry."), "-"),
            ParameterDetails("lon", "double", _("Longitude of the data entry."), "-"),
            ParameterDetails("title", "str", _("Displayed as the heading in the popover of the data entry."), "-"),
            ParameterDetails(
                "description", "str", _("Displayed below the title in the popover of the data entry."), "-"
            ),
            ParameterDetails(
                "value", "int", _("Used only for 'circle' data entries and defines the size/color of the circle."), "-"
            ),
        ],
        """
        [
            {"title": "Berlin", "value": 3769000, "lat": 52.5200, "lon": 13.4050},
            {"title": "Hamburg", "value": 1850000, "lat": 53.5511, "lon": 9.9937},
            {"title": "München", "value": 1488000, "lat": 48.1351, "lon": 11.5820},
        ]
        """,
    )

    datasets_param = ParameterDoc(
        ParameterDetails("datasets", "list[dict[str, Any]]", _("Datasets to be displayed on the map."), "{}"),
        [
            ParameterDetails("name", "str", _("The name of the dataset, used internally for identification."), "-"),
            ParameterDetails(
                "type", "str", _("How the data should be displayed. Possible values are: 'marker' and 'circle'."), "-"
            ),
            data_param.details,
        ],
        """
        [
            {
                "name": "population",
                "type": "circle",
                "data": [
                    {"title": "Berlin", "value": 3769000, "lat": 52.5200, "lon": 13.4050},
                    {"title": "Hamburg", "value": 1850000, "lat": 53.5511, "lon": 9.9937},
                    {"title": "München", "value": 1488000, "lat": 48.1351, "lon": 11.5820},
                ],
            }
        ],
        """,
    )

    config_param = ParameterDoc(
        ParameterDetails("data", "dict[str, Any]", _("Describes the map and the data to be displayed on it."), "{}"),
        [
            ParameterDetails(
                "initial_coords",
                "set(int, int)",
                _("Starting position on the map when the page is loaded."),
                "undefined",
            ),
            ParameterDetails("initial_zoom", "int", _("Zoom level on the map when the page is loaded."), "undefined"),
            datasets_param.details,
        ],
        """
        {
            "initial_coords": [52.5200, 13.4050],
            "initial_zoom": 8,
            "datasets": [
                {
                    "name": "population",
                    "type": "circle",
                    "data": [
                        {"title": "Berlin", "value": 3769000, "lat": 52.5200, "lon": 13.4050},
                        {"title": "Hamburg", "value": 1850000, "lat": 53.5511, "lon": 9.9937},
                        {"title": "München", "value": 1488000, "lat": 48.1351, "lon": 11.5820},
                    ],
                }
            ],
        }
        """,
    )

    main_params = [config_param.details, ParameterDetails("map_height", "int", _("Height of the map in 'rem'."), "36")]

    return {"params": [main_params, config_param, datasets_param, data_param]}


@register_component(Component.CHART)
def get_charts_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the charts component."""
    chart_param = ParameterDoc(
        ParameterDetails("chart", "dict[str, Any]", _("Information and data of the chart."), "{}"),
        [
            ParameterDetails("title", "str", _("Displayed as the heading above the chart."), "-"),
            ParameterDetails("x_axis_legend", "list[str]", _("Label of the x-axis."), "-"),
            ParameterDetails("series", "list[str]", _("Names of the individual datasets."), "-"),
            ParameterDetails("data", "list[list[int]]", _("The data of the individual datasets."), "-"),
        ],
        """
       {
            "title": "Chart Example",
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
        """,
    )

    main_params = [
        ParameterDetails("chart_id", "str", _("Unique tag ID for identifying the element in JavaScript."), "''"),
        chart_param.details,
    ]

    return {"params": [main_params, chart_param]}


@register_component(Component.LIVE_CONTENT)
def get_live_content_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the live content component."""
    main_params = [
        ParameterDetails(
            "tag_id", "str", _("Optional, unique tag ID for identifying the element in JavaScript."), "''"
        ),
        ParameterDetails("url", "str", _("URL of the API endpoint for querying data."), "''"),
        ParameterDetails("interval", "int", _("Interval of data retrieval in seconds."), "10"),
        ParameterDetails("initial_content", "str", _("Optional initial content."), "''"),
    ]

    return {"params": [main_params]}


@register_component(Component.WEB_SOCKET)
def get_web_socket_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the web socket component."""
    main_params = [
        ParameterDetails(
            "tag_id", "str", _("Optional, unique tag ID for identifying the element in JavaScript."), "''"
        ),
        ParameterDetails("url", "str", _("URL of the WebSocket API endpoint."), "''"),
        ParameterDetails("initial_content", "str", _("Optional initial content."), "''"),
    ]

    return {"params": [main_params]}


@register_component(Component.INFINITE_SCROLL)
def get_infinite_scroll_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the infinite scroll component."""
    main_params = [
        ParameterDetails(
            "tag_id", "str", _("Optional, unique tag ID for identifying the element in JavaScript."), "''"
        ),
        ParameterDetails(
            "view_name",
            "str",
            _("Name of the URL to which the request for loading more elements should be send."),
            "''",
        ),
        ParameterDetails("items", "list[dict]", _("List of already loaded elements."), "[]"),
        ParameterDetails(
            "auto_fetch",
            "bool",
            _(
                "**True**, new entries are loaded as soon as the specified scroll threshold is exceeded. **False**, at the end of the list a button to fetch more entries is shown instead."
            ),
            "True",
        ),
        ParameterDetails(
            "threshold",
            "int",
            _("The pixel threshold for loading more elements (only when **auto_fetch=False**)."),
            "100",
        ),
    ]

    return {"params": [main_params]}


@register_component(Component.PAGINATION)
def get_pagination_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the pagination component."""
    main_params = [
        ParameterDetails(
            "current_page", "Page", _("A Django-generated pagination object for the current page."), "None"
        ),
        ParameterDetails("surrounding_pages", "list[str]", _("List of adjacent pages."), "[]"),
        ParameterDetails(
            "ipp", "dict[str, Any]", _("Configuration of an 'Items per Page' select (select component)"), "[]"
        ),
    ]

    return {"params": [main_params]}


@register_component(Component.TABLE)
def get_table_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the table component."""
    data_param = ParameterDoc(
        ParameterDetails("data", "dict[str, Any]", _("Describes the table and the data to be displayed in it."), "{}"),
        [
            ParameterDetails("caption", "str", _("Heading of the table."), "''"),
            ParameterDetails("empty_msg", "str", _("Displayed when no data entries are present ('rows=[]')."), "''"),
            ParameterDetails("headers", "list[str]", _("List of headings for the individual columns."), "[]"),
            ParameterDetails("rows", "list[list[str]]", _("List of data for the individual rows."), "[]"),
        ],
        """
        {
            "caption": _("All registered users and their current status."),
            "empty_msg": _("No data available!"),
            "headers": [_("Name"), _("E-Mail"), _("Status")],
            "rows": [
                [
                    "Max Mustermann",
                    "max@example.com",
                    _("Active"),
                ],
                [
                    "Erika Mustermann",
                    "erika@example.com",
                    _("Inactive"),
                ]
            ],
        }
        """,
    )

    main_params = [data_param.details]

    return {"params": [main_params, data_param]}


@register_component(Component.GENERIC_FILTER)
def get_generic_filter_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the generic filter component."""
    htmx_config_params = ParameterDoc(
        ParameterDetails(
            "htmx_config", "dict[str, str]", _("Configuration of the HTMX request for asynchronous requests."), "{}"
        ),
        [
            ParameterDetails(
                "target", "str", _("ID of the HTML container whose content should be replaced upon response."), "''"
            ),
            ParameterDetails(
                "swap",
                "str",
                _(
                    "The way the target should be replaced: only the content ('innerHTML') or the container itself ('outerHTML')."
                ),
                "innerHTML",
            ),
            ParameterDetails(
                "push_url",
                "str",
                _("**True** to register filter changes in the browser history, for backward navigation support."),
                "'true'",
            ),
            ParameterDetails(
                "loading_indicator_id", "str", _("ID of the loading indicator container."), "'#loading-indicator'"
            ),
        ],
        """""",
    )

    filter_params = ParameterDoc(
        ParameterDetails("filters", "list[dict[str, Any]]", _("Definition of the individual filters."), "[]"),
        [
            ParameterDetails("name", "str", _("Required for a `<form>`, as the name of the request parameter."), "''"),
            ParameterDetails("label", "str", _("A text label displayed above the select."), "''"),
            ParameterDetails(
                "explanation", "str", _("A brief description of the filter that appears in a tooltip."), "''"
            ),
            ParameterDetails(
                "options", "list[str] oder dict[str, str]", _("List of values that can be selected."), "[]"
            ),
            ParameterDetails(
                "selected_option",
                "str",
                _("Value (the key value, if the options were passed as a dict) of the currently selected option."),
                "''",
            ),
        ],
        """
        [
            {
                "name": "model_type_filter",
                "label": _("AI model type"),
                "explanation": _("To filter by the type of AI-Model."),
                "icon": {"name": "rocket", "size": "small"},
                "options": {
                    "placeholder": "-- Select model --",
                    "language": "Language Model",
                    "vision": "Vision Model",
                    "multimodal": "Multimodal Model",
                    "audio": "Audio / Speech Processing",
                    "recommendation": "Recommendation System",
                    "generative": "Generative Model",
                },
            },
        ]
        """,
    )

    main_params = [
        ParameterDetails("request_url", "str", _("The URL to which the request should be sent."), "''"),
        filter_params.details,
        ParameterDetails("vertical", "bool", _("**True** if the filters should be arranged in a column."), "False"),
        htmx_config_params.details,
        ParameterDetails(
            "query_params",
            "dict[str, str]",
            _("Contains the currently selected values of the individual filters to restore them after the request."),
            "''",
        ),
    ]

    notes_end = [
        {
            "type": "info",
            "message": _(
                "In the `values` filters, the value `-` serves as a separator that cannot be clicked. The value `placeholder` serves as a placeholder."
            ),
        }
    ]

    return {"params": [main_params, filter_params, htmx_config_params], "params_notes_end": notes_end}


@register_component(Component.SEARCH_BAR)
def get_search_bar_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the search bar component."""
    main_params = [
        ParameterDetails(
            "request_view",
            "str",
            _("Name of the URL to which the request should be sent when submitting the search."),
            "''",
        ),
        ParameterDetails(
            "simple", "bool", _("**True** if the search bar should be displayed without a button and smaller."), "False"
        ),
        ParameterDetails("search_query", "str", _("Optional value automatically displayed in the text field."), "''"),
    ]

    return {"params": [main_params]}


@register_component(Component.QUERY_BUILDER)
def get_query_builder_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the query builder component."""
    model_field_params = ParameterDoc(
        ParameterDetails(
            "model_fields",
            "list[dict[str, Any]]",
            "A list of filter fields with suitable operators and possible values.",
            "[]",
        ),
        [
            ParameterDetails("field", "str", _("Filter name, e.g., Modelfield."), "''"),
            ParameterDetails("name", "str", _("Display name in the drop-down menu."), "''"),
            ParameterDetails("type", "str", _("Type of value, e.g., 'text', 'date', or 'number'."), "''"),
            ParameterDetails(
                "operations",
                "dict[str, str]",
                _(
                    "List of applicable operations, such as 'iexact', 'icontains', or 'gte', etc. The key is the operation, and the value is the display text."
                ),
                "{}",
            ),
            ParameterDetails(
                "values",
                "dict[str, Any]",
                _(
                    "A list of possible values, if they need to be restricted. The key is the filter value, and the value is the display text."
                ),
                "{}",
            ),
        ],
        """
        [
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
        """,
    )

    main_params = [model_field_params.details]

    return {"params": [main_params, model_field_params]}


@register_component(Component.CARD)
def get_card_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the card component."""
    image_param = ParameterDoc(
        ParameterDetails(
            "image", "dict[str]", _("Describes an image displayed as background for the title and subtitle."), "{}"
        ),
        [
            ParameterDetails("url", "str", _("URL to the image resource."), "''"),
            ParameterDetails(
                "alt",
                "str",
                _("Displayed alternative text used for screen readers if the image cannot be loaded."),
                "''",
            ),
        ],
        """
        {
            "url": static("insight_ui/img/thumbnail.png"),
            "alt": "Card-Image"
        }
        """,
    )

    action_button_param = ParameterDoc(
        ParameterDetails(
            "actions", "list[dict[str, str]]", _("List of buttons displayed at the bottom edge of the card."), "[]"
        ),
        [
            ParameterDetails("text", "str", _("Button label."), "''"),
            ParameterDetails(
                "type",
                "str",
                _(
                    "Describes the importance of the button (purely visual). Possible values are: 'primary' and 'secondary'."
                ),
                "''",
            ),
            ParameterDetails("url", "str", _("URL to be called when the button is clicked."), "''"),
        ],
        """
        [
            {"text": _("Learn more"), "url": "#", "type": "secondary"},
        ]
        """,
    )

    main_params = [
        ParameterDetails("title", "str", _("Heading of the card."), "''"),
        ParameterDetails("subtitle", "str", _("Optional subtitle displayed directly below the title."), "''"),
        ParameterDetails(
            "content",
            "str",
            _("Text content of the card. Displayed below the title or subtitle if there is one."),
            "''",
        ),
        image_param.details,
        action_button_param.details,
    ]

    return {"params": [main_params, image_param, action_button_param]}


@register_component(Component.APP_CARD)
def get_app_card_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the app card component."""
    image_param = ParameterDoc(
        ParameterDetails("image", "dict[str]", _("Describes an image displayed at the top."), "{}"),
        [
            ParameterDetails("url", "str", _("URL to the image resource."), "''"),
            ParameterDetails(
                "alt",
                "str",
                _("Displayed alternative text used for screen readers if the image cannot be loaded."),
                "''",
            ),
        ],
        """
        {
            "url": static("insight_ui/img/thumbnail.png"),
            "alt": "Card-Image"
        }
        """,
    )

    action_button_param = ParameterDoc(
        ParameterDetails(
            "actions", "list[dict[str, str]]", _("List of buttons displayed at the bottom edge of the card."), "[]"
        ),
        [
            ParameterDetails("text", "str", _("Button label."), "''"),
            ParameterDetails(
                "type",
                "str",
                _(
                    "Describes the importance of the button (purely visual). Possible values are: 'primary' and 'secondary'."
                ),
                "''",
            ),
            ParameterDetails("url", "str", _("URL to be called when the button is clicked."), "''"),
        ],
        """
        [
            {"text": _("Learn more"), "url": "#", "type": "secondary"},
        ]
        """,
    )

    main_params = [
        ParameterDetails("title", "str", _("Heading of the card."), "''"),
        ParameterDetails(
            "content",
            "str",
            _("Text content of the card. Displayed below the title or subtitle if there is one."),
            "''",
        ),
        ParameterDetails("tags", "list[str]", _("A list of small buttons, placed below the content text."), "[]"),
        ParameterDetails("url", "str", _("A URL that is called up when the user clicks on the title."), ""),
        image_param.details,
        action_button_param.details,
    ]

    return {"params": [main_params, image_param, action_button_param]}


@register_component(Component.FLIP_CARD)
def get_flip_card_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the flip card component."""
    image_param = ParameterDoc(
        ParameterDetails("image", "dict[str]", _("Describes an image displayed at the top."), "{}"),
        [
            ParameterDetails("url", "str", _("URL to the image resource."), "''"),
            ParameterDetails(
                "alt",
                "str",
                _("Displayed alternative text used for screen readers if the image cannot be loaded."),
                "''",
            ),
        ],
        """
        {
            "url": static("insight_ui/img/thumbnail.png"),
            "alt": "Card-Image"
        }
        """,
    )

    action_button_param = ParameterDoc(
        ParameterDetails(
            "actions", "list[dict[str, str]]", _("List of buttons displayed at the bottom edge of the card."), "[]"
        ),
        [
            ParameterDetails("text", "str", _("Button label."), "''"),
            ParameterDetails(
                "type",
                "str",
                _(
                    "Describes the importance of the button (purely visual). Possible values are: 'primary' and 'secondary'."
                ),
                "''",
            ),
            ParameterDetails("url", "str", _("URL to be called when the button is clicked."), "''"),
        ],
        """
        [
            {"text": _("Learn more"), "url": "#", "type": "secondary"},
        ]
        """,
    )

    main_params = [
        ParameterDetails("title", "str", _("Heading of the card."), "''"),
        ParameterDetails(
            "content",
            "str",
            _("Text content of the card. Displayed below the title or subtitle if there is one."),
            "''",
        ),
        ParameterDetails("tags", "list[str]", _("A list of small buttons, placed below the content text."), "[]"),
        ParameterDetails("url", "str", _("A URL that is called up when the user clicks on the title."), ""),
        image_param.details,
        action_button_param.details,
    ]

    return {"params": [main_params, image_param, action_button_param]}


@register_component(Component.CARD_CAROUSEL)
def get_card_carousel_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the card carousel component."""
    main_params = [
        ParameterDetails(
            "carousel_items", "list[dict]", _("Data to be displayed within the carousel (freely definable)."), "[]"
        ),
        ParameterDetails(
            "show_index",
            "bool",
            _("**True** if the current page should be displayed in the bottom right corner."),
            "False",
        ),
        ParameterDetails(
            "show_dots",
            "bool",
            _("**True** if a simple pagination should be displayed below the carousel content."),
            "True",
        ),
        ParameterDetails(
            "autoplay", "bool", _("**True** if the carousel should iterate through the content automatically."), "False"
        ),
        ParameterDetails("items_per_slide", "int", _("Number of 'carousel_items' per page."), "1"),
    ]

    return {"params": [main_params]}


@register_component(Component.IMAGE_CAROUSEL)
def get_image_carousel_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the image carousel component."""
    image_param = ParameterDoc(
        ParameterDetails("images", "list[dict]", _("Images to be displayed within the carousel."), "[]"),
        [
            ParameterDetails(
                "description",
                "str",
                _("Optional description of the image displayed at the top edge of the image."),
                "''",
            ),
            ParameterDetails("url", "str", _("URL to the image resource."), "''"),
            ParameterDetails(
                "alt",
                "str",
                _("Displayed alternative text used for screen readers if the image cannot be loaded."),
                "''",
            ),
        ],
        """""",
    )

    main_params = [
        image_param.details,
        ParameterDetails(
            "show_index",
            "bool",
            _("**True** if the current page should be displayed in the bottom right corner."),
            "False",
        ),
        ParameterDetails(
            "show_dots",
            "bool",
            _("**True** if a simple pagination should be displayed below the carousel content."),
            "True",
        ),
        ParameterDetails(
            "autoplay", "bool", _("**True** if the carousel should iterate through the content automatically."), "False"
        ),
        ParameterDetails("items_per_slide", "int", _("Number of images per page."), "1"),
    ]

    return {"params": [main_params, image_param]}


@register_component(Component.THREE_D_CAROUSEL)
def get_3d_carousel_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the 3D carousel component."""
    main_params = [
        ParameterDetails(
            "tag_id", "str", _("Optional, unique tag ID for identifying the element in JavaScript."), "''"
        ),
        ParameterDetails("velocity", "int", _("Rotation speed of the carousel."), "1000"),
        ParameterDetails("tilt", "int", _("Vertical tilt of the carousel towards the camera."), "0"),
        ParameterDetails(
            "face_camera", "bool", _("**True** if all cards should face the camera at all times."), "False"
        ),
        ParameterDetails(
            "carousel_items", "list[dict]", _("Data to be displayed within the carousel (freely definable)."), "[]"
        ),
    ]

    return {"params": [main_params]}


@register_component(Component.TOGGLE_VIEW)
def get_toggle_view_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the toggle view component."""
    items_param = ParameterDoc(
        ParameterDetails("items", "list[dict]", _("A list of the radio elements."), "[]"),
        [
            ParameterDetails(
                "tag_id", "str", _("Optional, unique tag ID for identifying the element in JavaScript."), "''"
            ),
            ParameterDetails("value", "str", _("Value of the respective radio button."), "''"),
            ParameterDetails("text", "str", _("Label of the respective radio button."), "''"),
            ParameterDetails("icon", "dict[str, str]", _("Optional icon displayed before the label."), "{}"),
            ParameterDetails("disabled", "bool", _("**True** if the radio button should be disabled."), "False"),
        ],
        """""",
    )

    view_radio_config_param = ParameterDoc(
        ParameterDetails(
            "view_radio_config",
            "dict[str, Any]",
            _("Configuration of the radio group for switching the view type."),
            "{}",
        ),
        [
            ParameterDetails(
                "name", "str", _("Optional, unique tag ID for identifying the element in JavaScript."), "''"
            ),
            items_param.details,
        ],
        """""",
    )

    main_params = [
        ParameterDetails(
            "tag_id",
            "str",
            _("Unique tag ID for identifying the element in JavaScript (required for switching the view)."),
            "''",
        ),
        ParameterDetails("data", "list[dict]", _("Data to be displayed."), "[]"),
        view_radio_config_param.details,
        ParameterDetails("current_view", "str", _("Name of the currently selected view type."), "''"),
    ]

    return {"params": [main_params, view_radio_config_param, items_param]}


@register_component(Component.FORM)
def get_form_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the form component."""
    htmx_config_params = ParameterDoc(
        ParameterDetails(
            "htmx_config", "dict[str, str]", _("Configuration of the HTMX request for asynchronous requests."), "{}"
        ),
        [
            ParameterDetails(
                "target", "str", _("ID of the HTML container whose content should be replaced upon response."), "''"
            ),
            ParameterDetails(
                "swap",
                "str",
                _(
                    "The way the target should be replaced: only the content ('innerHTML') or the container itself ('outerHTML')."
                ),
                "innerHTML",
            ),
        ],
        """""",
    )

    main_params = [
        ParameterDetails(
            "tag_id", "str", _("Optional, unique tag ID for identifying the element in JavaScript."), "''"
        ),
        ParameterDetails("title", "str", _("Heading of the form."), "''"),
        ParameterDetails("description", "str", _("Description of the form displayed directly below the title."), "''"),
        ParameterDetails("fields", "list[dict[str, str]]", _("List of the individual form fields."), "[]"),
        ParameterDetails(
            "show_reset_button",
            "bool",
            _("**True** if a 'Reset' button should be displayed next to the 'Submit' button."),
            "False",
        ),
        ParameterDetails(
            "view_name", "str", _("Name of the URL to which the request should be sent when submitting the form."), "''"
        ),
        htmx_config_params.details,
    ]

    return {"params": [main_params, htmx_config_params]}
