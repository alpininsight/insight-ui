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


@register_component(Component.PAGE_HEADER)
def get_page_header_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the page_header component."""
    main_params = [
        ParameterDetails("title", "str", _("The page title, displayed as h1 in white text."), "''"),
        ParameterDetails("description", "str", _("An optional description below the title."), "''"),
    ]

    return {"params": [main_params]}


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
                    "icon": {"name": "home", "size": "small"},
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
            "user",
            "User",
            _("The <i>user</i> object of the request (usually available via <i>request.user</i>)."),
            "None",
        ),
        ParameterDetails("user_dropdown_links", "list", _("A list of links to be displayed in the user menu."), "[]"),
        ParameterDetails(
            "show_login", "bool", _("<b>True</b> if a button for logging in should be displayed."), "false"
        ),
        ParameterDetails("search_query", "str", _("Search string for the search bar."), "''"),
    ]

    return {"params": [main_params, config_param, brand_param, logo_param, links_param]}


@register_component(Component.SIDEBAR)
def get_sidebar_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the sidebar component."""
    main_params = [
        ParameterDetails(
            "sidebar_data", "dict[str, Any]", _("Content of the sidebar (title and navigation elements)."), "None"
        ),
        ParameterDetails("side", "str", _("Determines on which side the sidebar should be placed."), "right"),
        ParameterDetails("static", "bool", _("<b>True</b> if the sidebar should not be collapsible."), "True"),
        ParameterDetails(
            "auto_close", "bool", _("If <b>True</b> the sidebar closes as soon as the cursor leaves it."), "False"
        ),
        ParameterDetails(
            "mobile_hidden", "bool", _("If <b>True</b> the static sidebar is hidden on a smaller viewport."), "False"
        ),
        ParameterDetails(
            "navbar_fixed",
            "bool",
            _("If <b>True</b> the position of the content is adjusted. (FOR CUSTOM SIDEBAR ONLY!)"),
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
        """""",
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
        """""",
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
        """""",
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
        """""",
    )

    copyright_param = ParameterDoc(
        ParameterDetails(
            "copyright", "dict[str, str]", _("Copyright information, such as the year and the protected name."), "{}"
        ),
        [
            ParameterDetails("year", "int", _("Typically the current year (not strictly required)."), "undefined"),
            ParameterDetails("app_name", "str", _("The protected name of the application."), "''"),
        ],
        """""",
    )

    data_param = ParameterDoc(
        ParameterDetails("data", "dict[str, Any]", _("Data to be displayed in the footer."), "{}"),
        [description_param.details, links_param.details, contact_param.details, copyright_param.details],
        """""",
    )

    main_params = [data_param.details]

    return {
        "params": [main_params, data_param, description_param, image_param, links_param, contact_param, copyright_param]
    }


@register_component(Component.BREADCRUMBS)
def get_breadcrumb_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the breadcrumbs component."""
    links_param = ParameterDoc(
        ParameterDetails("items", "list[dict]", _("List of navigation items."), "[]"),
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
        """""",
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
        """""",
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
        """""",
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
        ParameterDetails("id", "str", _("Unique tag ID for identifying the element in JavaScript."), "''"),
        item_param.details,
        ParameterDetails("exclusive", "bool", _("If <b>True</b> only one section can be open at a time."), "False"),
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
        """""",
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
        """""",
    )

    main_params = [config_param.details]

    return {"params": [main_params, config_param, tabs_param]}


@register_component(Component.BUTTON)
def get_button_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the button component."""
    main_params = [ParameterDetails("", "", "", "")]

    return {"params": [main_params]}


@register_component(Component.INPUT_FIELD)
def get_input_field_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the input field component."""
    main_params = [
        ParameterDetails(
            "tag_id", "str", _("Optional, unique tag ID for identifying the element in JavaScript."), "''"
        ),
        ParameterDetails(
            "name",
            "str",
            _("Required for a <span class='inline-tag'>&lt;form&gt;</span>, as the name of the request parameter."),
            "''",
        ),
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
        ParameterDetails("minimum", "int", _("Smallest numeric value (for input_type='number')."), "undefined"),
        ParameterDetails("maximum", "int", _("Largest numeric value (for input_type='number')."), "undefined"),
        ParameterDetails("min_length", "int", _("Minimum number of characters in a text field."), "undefined"),
        ParameterDetails("max_length", "int", _("Maximum number of characters in a text field."), "undefined"),
        ParameterDetails(
            "checked",
            "bool",
            _(
                "<b>True</b> if <span class='inline-tag'>input_type='checkbox'</span> and the checkbox should be selected."
            ),
            "False",
        ),
        ParameterDetails("required", "bool", _("<b>True</b> if the field must be filled in."), "False"),
        ParameterDetails("disabled", "bool", _("<b>True</b> if the field should be disabled."), "False"),
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
        ParameterDetails(
            "name",
            "str",
            _("Required for a <span class='inline-tag'>&lt;form&gt;</span>, as the name of the request parameter."),
            "''",
        ),
        ParameterDetails(
            "value", "str", _("The value of the checkbox (this is not the state, see 'checked' for that)."), "''"
        ),
        ParameterDetails("label", "str", _("A text label displayed above the checkbox."), "''"),
        ParameterDetails("checked", "bool", _("<b>True</b> if the checkbox should be selected."), "False"),
        ParameterDetails("disabled", "bool", _("<b>True</b> if the checkbox should be disabled."), "False"),
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
            ParameterDetails(
                "name",
                "str",
                _("Required for a <span class='inline-tag'>&lt;form&gt;</span>, as the name of the request parameter."),
                "''",
            ),
            ParameterDetails("label", "str", _("Text label displayed above the checkbox elements."), "''"),
            ParameterDetails(
                "as_row", "bool", _("<b>True</b> if the checkbox elements should be displayed side by side."), "False"
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
        """""",
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
        """""",
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
            ParameterDetails("show_arrow", "bool", _("<b>True</b> displays an arrow behind the title."), "False"),
            item_param.details,
        ],
        """""",
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
            ParameterDetails("disabled", "bool", _("<b>True</b> if the radio button should be disabled."), "False"),
        ],
        """""",
    )

    config_param = ParameterDoc(
        ParameterDetails(
            "config", "dict[str, Any]", _("Describes the radio button group and the individual radio elements."), "{}"
        ),
        [
            ParameterDetails(
                "name", "str", _("Optional, unique tag ID for identifying the element in JavaScript."), "''"
            ),
            ParameterDetails("label", "str", _("A text label displayed above the radio elements."), "''"),
            ParameterDetails(
                "as_row", "bool", _("<b>True</b> if the radio elements should be displayed side by side."), "False"
            ),
            items_param.details,
        ],
        """""",
    )

    main_params = [
        config_param.details,
        ParameterDetails("current_value", "str", _("The value of the currently selected radio button."), "''"),
        # Block only
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
            "target_id", "str", _("The ID of the HTML tag to be replaced when switching the radio button."), "''"
        ),
        ParameterDetails(
            "method",
            "str",
            _("Name of the JavaScript method to be executed when clicking one of the radio buttons."),
            "''",
        ),
        ParameterDetails(
            "integrated",
            "bool",
            _(
                "<b>True</b> if the group is inside a &lt;form&gt;. If <b>False</b> the group gets its own &lt;form&gt;."
            ),
            "False",
        ),
    ]

    return {"params": [main_params, config_param, items_param]}


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
            ParameterDetails("disabled", "bool", _("<b>True</b> if the radio button should be disabled."), "False"),
        ],
        """""",
    )

    config_param = ParameterDoc(
        ParameterDetails(
            "config", "dict[str, Any]", _("Describes the radio button group and the individual radio elements."), "{}"
        ),
        [
            ParameterDetails(
                "name", "str", _("Optional, unique tag ID for identifying the element in JavaScript."), "''"
            ),
            ParameterDetails("label", "str", _("A text label displayed above the radio elements."), "''"),
            ParameterDetails(
                "as_row", "bool", _("<b>True</b> if the radio elements should be displayed side by side."), "False"
            ),
            items_param.details,
        ],
        """""",
    )

    main_params = [
        config_param.details,
        ParameterDetails("current_value", "str", _("The value of the currently selected radio button."), "''"),
        # Block only
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
            "target_id", "str", _("The ID of the HTML tag to be replaced when switching the radio button."), "''"
        ),
        ParameterDetails(
            "method",
            "str",
            _("Name of the JavaScript method to be executed when clicking one of the radio buttons."),
            "''",
        ),
        ParameterDetails(
            "integrated",
            "bool",
            _(
                "<b>True</b> if the group is inside a &lt;form&gt;. If <b>False</b> the group gets its own &lt;form&gt;."
            ),
            "False",
        ),
    ]

    return {"params": [main_params, config_param, items_param]}


@register_component(Component.RANGE_SLIDER)
def get_rangle_slider_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the range slider component."""
    main_params = [
        ParameterDetails(
            "tag_id", "str", _("Optional, unique tag ID for identifying the element in JavaScript."), "''"
        ),
        ParameterDetails(
            "name",
            "str",
            _("Required for a <span class='inline-tag'>&lt;form&gt;</span>, as the name of the request parameter."),
            "''",
        ),
        ParameterDetails("label", "str", _("A text label displayed above the range slider."), "''"),
        ParameterDetails("value", "int", _("The value of the range slider."), "0"),
        ParameterDetails("minimum", "int", _("Smallest configurable value of the range slider."), "undefined"),
        ParameterDetails("maximum", "int", _("Largest configurable value of the range slider."), "undefined"),
        ParameterDetails(
            "step_size", "int", _("The size of the steps by which the value changes when moving the range slider."), "1"
        ),
        ParameterDetails("disabled", "bool", _("<b>True</b> if the range slider should be disabled."), "False"),
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
        ParameterDetails(
            "name",
            "str",
            _("Required for a <span class='inline-tag'>&lt;form&gt;</span>, as the name of the request parameter."),
            "''",
        ),
        ParameterDetails("label", "str", _("Ein Label-Text welcher über dem Toggle-Button angezeigt wird."), "''"),
        ParameterDetails("value", "str", _("Der Wert des Toggle-Buttons."), "''"),
        ParameterDetails(
            "switch",
            "bool",
            _("<b>True</b>, wenn der Toggle-Button wie ein typischer Switch-Select aussehen soll."),
            "False",
        ),
        ParameterDetails("checked", "bool", _("<b>True</b>, wenn der Toggle-Button ausgewählt sein soll."), "False"),
        ParameterDetails("disabled", "bool", _("<b>True</b>, wenn der Toggle-Button deaktiviert sein soll."), "False"),
        ParameterDetails(
            "method",
            "str",
            _("Name der JavaScript Methode welche beim Klick auf den Toggle-Button ausgeführt werden soll."),
            "''",
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
        ParameterDetails(
            "name",
            "str",
            _("Required for a <span class='inline-tag'>&lt;form&gt;</span>, as the name of the request parameter."),
            "''",
        ),
        ParameterDetails("label", "str", _("Ein Label-Text welcher über dem Select angezeigt wird."), "''"),
        ParameterDetails(
            "options", "list[str] oder dict[str, str]", _("Liste von Werten welche ausgewählt werden können."), "[]"
        ),
        ParameterDetails(
            "selected_option",
            "str",
            _("Wert (Der Key-Wert, falls die Optionen als Dict übergeben wurden) der aktuell ausgewählten Option."),
            "''",
        ),
        ParameterDetails(
            "config",
            "dict[str, Any]",
            _("An alternative configuration with keys corresponding to the previous parameters."),
            "{}",
        ),
    ]

    return {"params": [main_params]}


@register_component(Component.MULTISELECT)
def get_multiselect_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the multiselect component."""
    main_params = [
        ParameterDetails(
            "name",
            "str",
            _("Required for a <span class='inline-tag'>&lt;form&gt;</span>, as the name of the request parameter."),
            "''",
        ),
        ParameterDetails("label", "str", _("Ein Label-Text welcher über dem Select angezeigt wird."), "''"),
        ParameterDetails("maximum", "int", _("Anzahl der maximal ausgewählten Optionen."), "undefined"),
        ParameterDetails(
            "show_buttons",
            "bool",
            _("zusätzliche Buttons für 'Alle Auswählen' und 'Alle Abwählen' Buttons anzeigen."),
            "False",
        ),
        ParameterDetails(
            "options", "list[str] oder dict[str, str]", _("Liste von Werten welche ausgewählt werden können."), "[]"
        ),
        ParameterDetails("selected_options", "list[str]", _("Liste der aktuell ausgewählten Optionen."), "[]"),
        ParameterDetails(
            "config",
            "dict[str, Any]",
            _("An alternative configuration with keys corresponding to the previous parameters."),
            "{}",
        ),
    ]

    return {"params": [main_params]}


@register_component(Component.CHAT)
def get_chat_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the chat component."""
    main_params = [
        ParameterDetails(
            "view_name",
            "str",
            _("Name der URL an welchen der Request beim absenden einer Nachricht, gesendet werden soll."),
            "''",
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
        ParameterDetails("message", "str", _("Nachricht welche in dem Alert angezeigt wird."), "''"),
        ParameterDetails(
            "type", "str", _("Typ des Alerts. Möglich Werte sind 'info', 'success', 'warning' und 'error'."), "info"
        ),
        ParameterDetails(
            "dismissible",
            "bool",
            _("Zeigt ein Button zum schließen des Alerts am Ende des Alert-Containers an."),
            "False",
        ),
    ]

    return {"params": [main_params]}


@register_component(Component.MODAL)
def get_modal_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the modal component."""
    action_button_param = ParameterDoc(
        ParameterDetails(
            "actions",
            "Sequence[Mapping[str, str]]",
            _("Liste von Buttons, welche um unteren Ende des Dialogs angezeigt werden."),
            "[]",
        ),
        [
            ParameterDetails("text", "str", _("Beschriftung des Buttons."), "''"),
            ParameterDetails(
                "type",
                "str",
                _(
                    "Beschreibt die Wichtigkeit des Buttons (rein visuell). Mögliche Werte sind: 'primary' und 'secondary'."
                ),
                "''",
            ),
            ParameterDetails("onclick", "str", _("Aufruf einer JavaScript Funktion, bspw.: alert('Confirmed!')"), "''"),
            ParameterDetails("dismiss", "bool", _("Schließt den Dialog beim Klick."), "False"),
        ],
        """""",
    )

    main_params = [
        ParameterDetails(
            "tag_id", "str", _("Optional, unique tag ID for identifying the element in JavaScript."), "''"
        ),
        ParameterDetails("title", "str", _("Überschrift des Modal Dialogs."), "''"),
        ParameterDetails("description", "str", _("Text welcher direkt unter dem Titel angezeigt wird."), "''"),
        ParameterDetails(
            "additional_content",
            "str",
            _(
                "Zusätzlicher Text, welcher unter der Kopfzeile, welche aus Titel und Description besteht, angezeigt wird."
            ),
            "''",
        ),
        action_button_param.details,
    ]

    return {"params": [main_params, action_button_param]}


@register_component(Component.POPOVER)
def get_popover_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the popover component."""
    main_params = [
        ParameterDetails(
            "data-popover='<target-id>'",
            "str",
            _("Bestimmt das Popover Objekt, welches beim Hovern angezeigt werden soll."),
            "''",
        ),
        ParameterDetails(
            "data-position='<position>'",
            "str",
            _(
                "Bestimmt wo im Bezug auf das Element, der Popover angezeigt werden soll. Mögliche Werte sind: 'top', 'bottom', 'right', und 'left'."
            ),
            "''",
        ),
        ParameterDetails(
            "data-show-arrow",
            "bool",
            _("Zeigt ein Pfeil am Rand des Popovers, hin zum auslösenden Objekt an."),
            "False",
        ),
    ]

    return {"params": [main_params]}


@register_component(Component.TOOLTIP)
def get_tooltip_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the tooltip component."""
    main_params = [
        ParameterDetails(
            "data-popover='<text>'",
            "str",
            _("Zeigt beim Hovern über das Element, ein Tooltip mit dem angegeben Text an."),
            "''",
        ),
        ParameterDetails(
            "data-position='<position>'",
            "str",
            _(
                "Bestimmt wo im Bezug auf das Element, der Tooltip angezeigt werden soll. Mögliche Werte sind: 'top', 'bottom', 'right', und 'left'."
            ),
            "''",
        ),
        ParameterDetails(
            "data-show-arrow",
            "bool",
            _("Zeigt ein Pfeil am Rand des Tooltips, hin zum auslösenden Objekt an."),
            "False",
        ),
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
            _("Identifiziert dieses Objekt als Code Block und um welche Sprache es sich handelt."),
            "''",
        ),
        ParameterDetails(
            "data-insight-code-block-filename",
            "str",
            _("Zeigt den Text, als Hinweis für den Nutzer in der Kopfzeile des Code Blocks an."),
            "''",
        ),
    ]

    return {"params": [main_params]}


@register_component(Component.DIFFERENTIATOR)
def get_differentiator_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the differentiator component."""
    main_params = [
        ParameterDetails("textA", "str", _("Erste bzw. ältere Version des Textes."), "''"),
        ParameterDetails("textB", "str", _("Zweite bzw. neuere Version des Textes."), "''"),
    ]

    return {"params": [main_params]}


@register_component(Component.PROGRESS_BAR)
def get_progress_bar_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the progress bar component."""
    main_params = [ParameterDetails("", "", "", "")]

    return {"params": [main_params]}


@register_component(Component.GEO_MAP)
def get_geo_map_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the geo map component."""
    data_param = ParameterDoc(
        ParameterDetails("data", "list[dict]", _("Liste der Dateneinträge."), "-"),
        [
            ParameterDetails("lat", "double", _("Breitengrad (Latitude) des Dateneintrags."), "-"),
            ParameterDetails("lon", "double", _("Längengrad (Longitude) des Dateneintrags."), "-"),
            ParameterDetails(
                "title", "str", _("Wird als Überschrift in dem Popover des Dateneintrags angezeigt."), "-"
            ),
            ParameterDetails(
                "description", "str", _("Wird unter dem Title in dem Popover des Dateneintrags angezeigt."), "-"
            ),
            ParameterDetails(
                "value",
                "int",
                _("Wird nur für 'circle' Dateneinträge verwenden und definiert die Größe/Farbe des Kreises."),
                "-",
            ),
        ],
        """""",
    )

    datasets_param = ParameterDoc(
        ParameterDetails(
            "datasets", "dict[str, Any]", _("Datensätze welche auf der Karte dargestellt werden sollen."), "{}"
        ),
        [
            ParameterDetails("name", "str", _("Der Name des Datensatzes, wird intern zur Benennung verwendet."), "-"),
            ParameterDetails(
                "type",
                "str",
                _(
                    "Die Art und Weise wie die Daten dargestellt werden sollen. Mögliche Werte sind: 'marker' und 'circle'."
                ),
                "-",
            ),
            data_param.details,
        ],
        """""",
    )

    config_param = ParameterDoc(
        ParameterDetails(
            "data",
            "dict[str, Any]",
            _("Beschreibt die Karte und die Daten welche auf der Karte dargestellt werden sollen."),
            "{}",
        ),
        [
            ParameterDetails(
                "initial_coords", "set(int, int)", _("Startposition auf der Karte, beim Seitenaufruf."), "undefined"
            ),
            ParameterDetails("initial_zoom", "int", _("Zoom auf der Karte, beim Seitenaufruf"), "undefined"),
            datasets_param.details,
        ],
        """""",
    )

    main_params = [config_param.details, ParameterDetails("map_height", "int", _("Höhe der Karte in 'rem'."), "36")]

    return {"params": [main_params, config_param, datasets_param, data_param]}


@register_component(Component.CHART)
def get_charts_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the charts component."""
    chart_param = ParameterDoc(
        ParameterDetails("chart", "dict[str, Any]", _("Informationen und Daten des Diagramms."), "{}"),
        [
            ParameterDetails("title", "str", _("Wird über dem Diagramm als Überschrift angezeigt."), "-"),
            ParameterDetails("x_axis_legend", "list[str]", _("Beschriftung der X-Achse."), "-"),
            ParameterDetails("series", "list[str]", _("Namen der einzelnen Datensätze."), "-"),
            ParameterDetails("data", "list[list[int]]", _("Die Daten der einzelnen Datensätze."), "-"),
        ],
        """""",
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
        ParameterDetails("url", "str", _("URL des API Endpunkts zum abfragen der Daten."), "''"),
        ParameterDetails("interval", "int", _("Intervall des Datenabrufs in Sekunden."), "10"),
        ParameterDetails("initial_content", "str", _("Optionaler, initialer Inhalt."), "''"),
    ]

    return {"params": [main_params]}


@register_component(Component.WEB_SOCKET)
def get_web_socket_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the web socket component."""
    main_params = [
        ParameterDetails(
            "tag_id", "str", _("Optional, unique tag ID for identifying the element in JavaScript."), "''"
        ),
        ParameterDetails("url", "str", _("URL des Websocket-API Endpunkts."), "''"),
        ParameterDetails("initial_content", "str", _("Optionaler, initialer Inhalt."), "''"),
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
            "view_name", "str", _("Name der URL, an welche der Request zum laden weitere Elemente."), "''"
        ),
        ParameterDetails("items", "list[dict]", _("Liste der bereits geladenen Elemente."), "[]"),
        ParameterDetails(
            "auto_fetch",
            "bool",
            _(
                "<b>True</b>, neue Einträge werden, sobald der angegebenen Threshold beim Scrollen überschritten wird, geladen. <b>False</b>, am Ende der Liste wird ein Button zum Abfragen weiterer Einträge angezeigt."
            ),
            "True",
        ),
        ParameterDetails(
            "threshold",
            "int",
            _("Der Pixel-Schwellenwert für das Laden weiterer Elemente (nur wenn <b>auto_fetch=False</b>)."),
            "100",
        ),
    ]

    return {"params": [main_params]}


@register_component(Component.PAGINATION)
def get_pagination_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the pagination component."""
    main_params = [
        ParameterDetails(
            "current_page", "Page", _("Ein von Django erzeugtes Pagination-Objekt der aktuellen Seite."), "None"
        ),
        ParameterDetails("surrounding_pages", "list[str]", _("Liste der benachbarten Seiten."), "[]"),
    ]

    return {"params": [main_params]}


@register_component(Component.TABLE)
def get_table_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the table component."""
    data_param = ParameterDoc(
        ParameterDetails(
            "data",
            "dict[str, Any]",
            _("Beschreibt die Tabelle und die Daten welche in dieser dargestellt werden sollen."),
            "{}",
        ),
        [
            ParameterDetails("caption", "str", _("Überschrift der Tabelle."), "''"),
            ParameterDetails(
                "empty_msg", "str", _("Wird angezeigt, wenn keine Einträge vorhanden sind (wenn 'rows=[]')."), "''"
            ),
            ParameterDetails("headers", "list[str]", _("Liste der Überschriften der einzelnen Spalten."), "[]"),
            ParameterDetails("rows", "list[list[str]]", _("Liste der Daten der einzelnen Zeilen."), "[]"),
        ],
        """""",
    )

    main_params = [data_param.details]

    return {"params": [main_params, data_param]}


@register_component(Component.GENERIC_FILTER)
def get_generic_filter_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the generic filter component."""
    main_params = [
        ParameterDetails(
            "view_name",
            "str",
            _("Name der URL an welchen der Request beim ändern eines Filters, gesendet werden soll."),
            "''",
        ),
        ParameterDetails(
            "hx_target",
            "str",
            _(
                "ID des HTML-Containers, dessen Inhalt beim Response ausgetauscht werden soll (zum Beispiel eine Liste von Daten, welche gefiltert wird)."
            ),
            "''",
        ),
        ParameterDetails(
            "hx_push_url",
            "bool",
            _("<b>True</b> wenn die ausgewählten Filterwerte in der URL angezeigt werden sollen."),
            "True",
        ),
        ParameterDetails("filters", "list[dict[str, Any]]", _("Definition der einzelnen Filter."), "[]"),
        ParameterDetails(
            "vertical", "bool", _("<b>True</b> wenn die Filter übereinander angeordnet sein sollen."), "False"
        ),
        ParameterDetails(
            "query_params",
            "dict[str, str]",
            _(
                "Enthält die aktuell ausgewählten Werte der einzelnen Filter, um diese nach dem Request wiederherzustellen."
            ),
            "''",
        ),
    ]

    return {"params": [main_params]}


@register_component(Component.SEARCH_BAR)
def get_search_bar_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the search bar component."""
    main_params = [
        ParameterDetails(
            "request_view",
            "str",
            _("Name der URL an welchen der Request beim absenden der Suche, gesendet werden soll."),
            "''",
        ),
        ParameterDetails(
            "simple",
            "bool",
            _("<b>True</b> wenn die Suchleiste ohne Button und kleiner angezeigt werden soll."),
            "False",
        ),
        ParameterDetails(
            "search_query", "str", _("Optionaler Wert der automatisch in dem Textfeld angezeigt wird."), "''"
        ),
    ]

    return {"params": [main_params]}


@register_component(Component.QUERY_BUILDER)
def get_query_builder_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the query builder component."""
    main_params = [ParameterDetails("", "", "", "")]

    return {"params": [main_params]}


@register_component(Component.CARD)
def get_card_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the card component."""
    image_param = ParameterDoc(
        ParameterDetails(
            "image",
            "dict[str]",
            _("Beschreibt ein Bild, welches als Hintergrund für den Title und dem Subtitle angezeigt wird."),
            "{}",
        ),
        [
            ParameterDetails("url", "str", _("URL zu der Bild-Resource."), "''"),
            ParameterDetails(
                "alt",
                "str",
                _(
                    "Alternativtext der angezeigt wird, falls das Bild nicht geladen werden kann und für Screenreader verwendet wird."
                ),
                "''",
            ),
        ],
        """""",
    )

    action_button_param = ParameterDoc(
        ParameterDetails(
            "actions",
            "list[dict[str, str]]",
            _("Liste von Buttons, welche am unteren Rand der Karte angezeigt werden."),
            "[]",
        ),
        [
            ParameterDetails("text", "str", _("Beschriftung des Buttons."), "''"),
            ParameterDetails(
                "type",
                "str",
                _(
                    "Beschreibt die Wichtigkeit des Buttons (rein visuell). Mögliche Werte sind: 'primary' und 'secondary'."
                ),
                "''",
            ),
            ParameterDetails("url", "str", _("URL welche beim Klick auf den Button aufgerufen werden soll."), "''"),
        ],
        """""",
    )

    main_params = [
        ParameterDetails("title", "str", _("Überschrift der Karte."), "''"),
        ParameterDetails(
            "subtitle", "str", _("Optionaler Untertitel, welcher direkt unter dem Title angezeigt wird."), "''"
        ),
        ParameterDetails(
            "content", "str", _("Textinhalt der Karte. Wird unter dem Title bzw. unter dem Subtitle angezeigt."), "''"
        ),
        image_param.details,
        action_button_param.details,
    ]

    return {"params": [main_params, image_param, action_button_param]}


@register_component(Component.CARD_CAROUSEL)
def get_card_carousel_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the card carousel component."""
    main_params = [
        ParameterDetails(
            "carousel_items",
            "list[dict]",
            _("Daten welche innerhalb des Karussell angezeigt werden sollen (frei definierbar)."),
            "[]",
        ),
        ParameterDetails(
            "show_index",
            "bool",
            _("<b>True</b>, wenn in der unteren rechten Ecke die aktuelle Seite angezeigt werden soll."),
            "False",
        ),
        ParameterDetails(
            "show_dots",
            "bool",
            _("<b>True</b>, wenn unter dem Karussell-Inhalt eine einfache Pagination angezeigt werden soll."),
            "True",
        ),
        ParameterDetails(
            "autoplay",
            "bool",
            _("<b>True</b>, wenn das Karussell von alleine durch den Inhalt iterieren soll."),
            "False",
        ),
        ParameterDetails("items_per_slide", "int", _("Anzahl an 'carousel_items' pro Seite."), "1"),
    ]

    return {"params": [main_params]}


@register_component(Component.IMAGE_CAROUSEL)
def get_image_carousel_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the image carousel component."""
    image_param = ParameterDoc(
        ParameterDetails(
            "images", "list[dict]", _("Bilder welche innerhalb des Karussell angezeigt werden sollen."), "[]"
        ),
        [
            ParameterDetails(
                "description",
                "str",
                _("Optionale Beschreibung des Bildes, welche am oberen Rand des Bildes angezeigt wird."),
                "''",
            ),
            ParameterDetails("url", "str", _("URL zu der Bild-Resource."), "''"),
            ParameterDetails(
                "alt",
                "str",
                _(
                    "Alternativtext der angezeigt wird, falls das Bild nicht geladen werden kann und für Screenreader verwendet wird."
                ),
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
            _("<b>True</b>, wenn in der unteren rechten Ecke die aktuelle Seite angezeigt werden soll."),
            "False",
        ),
        ParameterDetails(
            "show_dots",
            "bool",
            _("<b>True</b>, wenn unter dem Karussell-Inhalt eine einfache Pagination angezeigt werden soll."),
            "True",
        ),
        ParameterDetails(
            "autoplay",
            "bool",
            _("<b>True</b>, wenn das Karussell von alleine durch den Inhalt iterieren soll."),
            "False",
        ),
        ParameterDetails("items_per_slide", "int", _("Anzahl der Bilder pro Seite."), "1"),
    ]

    return {"params": [main_params, image_param]}


@register_component(Component.THREE_D_CAROUSEL)
def get_3d_carousel_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the 3D carousel component."""
    main_params = [
        ParameterDetails(
            "tag_id", "str", _("Optional, unique tag ID for identifying the element in JavaScript."), "''"
        ),
        ParameterDetails("velocity", "int", _("Geschwindigkeit mit welcher sich das Karussell dreht."), "1000"),
        ParameterDetails("tilt", "int", _("Vertikale Neigung des Karussell zur Camera."), "0"),
        ParameterDetails(
            "face_camera",
            "bool",
            _("<b>True</b> wenn alle Karten immer in Richtung der Kamera ausgerichtet sein sollen."),
            "False",
        ),
        ParameterDetails(
            "carousel_items",
            "list[dict]",
            _("Daten welche innerhalb des Karussell angezeigt werden sollen (frei definierbar)."),
            "[]",
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
            ParameterDetails("disabled", "bool", _("<b>True</b> if the radio button should be disabled."), "False"),
        ],
        """""",
    )

    view_radio_config_param = ParameterDoc(
        ParameterDetails(
            "view_radio_config",
            "dict[str, Any]",
            _("Konfiguration der Radio-Group, zum wechseln der Ansichtsart."),
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
            _(
                "Eindeutige Tag-ID für die Identifizierung des Elements im JavaScript (wird für den wechsel der Ansicht benötigt)."
            ),
            "''",
        ),
        ParameterDetails("data", "list[dict]", _("Daten, welche angezeigt werden sollen."), "[]"),
        view_radio_config_param.details,
        ParameterDetails("current_view", "str", _("Name der aktuell ausgewählten View-Variante."), "''"),
    ]

    return {"params": [main_params, view_radio_config_param, items_param]}


@register_component(Component.FORM)
def get_form_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the form component."""
    htmx_config_param = ParameterDoc(
        ParameterDetails(
            "htmx_config", "dict[str, str]", _("Konfiguration des HTMX Request, für asynchrone Requests."), "{}"
        ),
        [
            ParameterDetails(
                "target",
                "str",
                _("ID des HTML-Containers, dessen Inhalt beim Response ausgetauscht werden soll."),
                "''",
            ),
            ParameterDetails(
                "swap",
                "str",
                _(
                    "Die Art wie das Target ausgetauscht werden soll, nur der Inhalt mit 'innerHTML' oder der Container selbst mit 'outerHTML'."
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
        ParameterDetails("title", "str", _("Überschrift des Formulars."), "''"),
        ParameterDetails(
            "description", "str", _("Beschreibung des Formulars, welche direkt unter dem Title angezeigt wird."), "''"
        ),
        ParameterDetails("fields", "list[dict[str, str]]", _("Liste der einzelnen Formular-Felder."), "[]"),
        ParameterDetails(
            "show_reset_button",
            "bool",
            _("<b>True</b>, wenn neben dem 'Absenden' Button ein 'Zurücksetzen' Button angezeigt werden soll"),
            "False",
        ),
        ParameterDetails(
            "view_name",
            "str",
            _("Name der URL, an welche beim absenden des Formulars, der Request gesendet werden soll."),
            "''",
        ),
        htmx_config_param.details,
    ]

    return {"params": [main_params, htmx_config_param]}
