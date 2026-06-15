from django.urls import reverse
from django.utils.translation import gettext as _

from insight_ui.component_details.component_context import register_component
from insight_ui.component_details.components import Component

# =============================================================
#
#   Layout Tags
#
# =============================================================


@register_component(Component.PAGE_HEADER)
def get_page_header_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the page hader component."""
    return {
        "description": [
            _(
                "The `page_header` component can be used to display a header featuring geometric decorations, along with a title, an optional description, and buttons. The header is displayed in the selected primary color to stand out from the rest of the page."
            )
        ]
    }


@register_component(Component.ARTICLE)
def get_article_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the article component."""
    return {
        "description": [
            _(
                "The `article` component renders text content in newspaper style with multi-column CSS columns. The text flows automatically from one column to the next."
            )
        ]
    }


@register_component(Component.HERO)
def get_hero_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the hero component."""
    return {
        "description": [
            _(
                "The `hero` component renders a prominent banner section with title, subtitle, description and Call-to-Action buttons."
            )
        ]
    }


# =============================================================
#
#   Navigation Tags
#
# =============================================================


@register_component(Component.NAVBAR)
def get_navbar_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the navbar component."""
    return {
        "description": [
            _(
                "The `navbar` component provides a customizable navigation bar with various components. The navigation is fixed to the top edge of the browser window and moves along when scrolling down."
            )
        ],
        "features": [
            _("**Brand**: Logo and title on the left edge."),
            _("**Navigation links**: Main navigation, to the right of the logo and title."),
            _("**Search bar**: An optional search bar, to the right of the main navigation."),
            _(
                "**Login/user menu**: An optional, customizable user menu or a login button when the user is not logged in."
            ),
            _(
                "**Language selection**: An optional menu for selecting the language in which the website should be displayed."
            ),
            _("**Theme toggle button**: An optional button for switching between the light and dark theme."),
        ],
    }


@register_component(Component.SIDEBAR)
def get_sidebar_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the sidebar component."""
    return {
        "description": [
            _(
                "The `sidebar` component adds an area to the side of the window. The sidebar can be applied on the left or on the right side, as well as on both sides simultaneously. The sidebar can also be used as a drawer, in which case it can be closed."
            )
        ]
    }


@register_component(Component.FOOTER)
def get_footer_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the footer component."""
    return {
        "description": [
            _(
                "A simple `footer` consisting of three columns with customizable content. The footer is an important part of every website; however, it does not only serve to visually close off the website. It typically contains at least a link to the imprint and the privacy policy. Often the footer also contains navigation to the most important pages of the website and a copyright notice."
            ),
            _("The footer composes the reusable `copyright_notice` component for its legal notice line."),
        ]
    }


@register_component(Component.BREADCRUMBS)
def get_breadcrumb_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the breadcrumbs component."""
    return {
        "description": [
            _(
                "`Breadcrumbs` are a secondary navigation used to provide the user with clarity about the hierarchical structure of a website. This is especially useful for websites with a deep structure, i.e. with many subpages. Websites with a depth of no more than two levels (e.g. Overview -> Product Details) should refrain from using breadcrumbs."
            ),
            _("For good consistency, breadcrumbs should ,when used, be used everywhere, not just sporadically."),
        ]
    }


@register_component(Component.STEP_BAR)
def get_step_bar_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the step bar component."""
    return {
        "description": [
            _(
                "The `step_bar` component can be used to show the user the progress of a manual process. This refers, for example, to a typical checkout process. This typically consists of several steps, such as entering an address, selecting a payment method, and then reviewing the entries once more. The component shows the user where they currently are and which steps remain."
            )
        ]
    }


@register_component(Component.MINIMAL_STEP_BAR)
def get_minimal_step_bar_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the minimal step bar component."""
    return {
        "description": [
            _(
                "The `minimal_step_bar` component can be used to graphically display progress in a multi-step process in a simple way."
            )
        ]
    }


@register_component(Component.BULLET_POINT_LIST)
def get_bullet_point_list_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the bullet point list component."""
    return {
        "description": [
            _(
                "The `bullet_point_list` component can be used to display a sequence of tasks, process steps, or similar. The individual steps can contain a link, for example to link them to a specific page for each task."
            )
        ]
    }


@register_component(Component.ACCORDION)
def get_accordion_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the accordion component."""
    return {
        "description": [
            _(
                "The `accordion` component can be used to add expandable sections for additional information. An accordion can have either one or multiple sections open at the same time. When an accordion section is opened, a URL anchor is automatically set. This allows certain sections to be automatically expanded when the page is loaded via the URL, and the view automatically scrolls to the opened section."
            )
        ]
    }


@register_component(Component.TABS)
def get_tabs_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the tabs component."""
    return {
        "description": [
            _(
                "The `tabs` component can be used to add tabs. This component consists of a series of buttons that swap the main content of the component via HTMX requests. This allows switching between individual tabs without reloading the page."
            )
        ]
    }


# =============================================================
#
#   Input Tags
#
# =============================================================


@register_component(Component.BUTTON)
def get_button_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the button component."""
    return {
        "description": [
            _(
                "For a standard button, our UI framework provides a set of CSS classes. These allow buttons for different scenarios to be integrated with minimal effort using common CSS classes."
            )
        ]
    }


@register_component(Component.INPUT_FIELD)
def get_input_field_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the input field component."""
    return {"description": [_("The `input_field` component can be used to integrate individual `<input>` elements.")]}


@register_component(Component.TEXTAREA)
def get_textarea_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the textarea component."""
    return {"description": [_("The `textarea` component can be used to integrate a text field for longer texts.")]}


@register_component(Component.CHECKBOX)
def get_checkbox_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the checkbox component."""
    checkbox_group_url = reverse("component_detail_page_view", args=[Component.CHECKBOX_GROUP.value])
    return {
        "description": [
            _(
                "The `checkbox` component can be used to integrate individual checkbox elements. For a group of interconnected checkbox elements, see [Checkbox Group](%(url)s)."
            )
            % {"url": checkbox_group_url}
        ]
    }


@register_component(Component.CHECKBOX_GROUP)
def get_checkbox_group_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the checkbox group component."""
    return {
        "description": [
            _(
                "The `checkbox_group` component can be used to integrate groups of checkbox elements that are linked to each other. This allows a restriction to be enabled that, for example, ensures that at least one checkbox element is selected."
            )
        ]
    }


@register_component(Component.DROPDOWN)
def get_dropdown_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the dropdown component."""
    return {
        "description": [
            _(
                "A `dropdown` menu offers the possibility of housing a group of buttons in a collapsible menu. This is very useful whenever space is limited or the number of elements would otherwise be too large and confusing."
            ),
            _(
                "Dropdown menus should not be overloaded. As a rule, a menu should have no more than seven elements, and nested menus, i.e. a dropdown menu within a dropdown menu, should also be avoided."
            ),
        ]
    }


@register_component(Component.RADIO_GROUP)
def get_radio_group_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the radio_group component."""
    return {
        "description": [
            _(
                "The `radio_group` component can be used to integrate groups of radio buttons. This variant of radio buttons uses standard radio buttons for e.g. a form or similar."
            )
        ]
    }


@register_component(Component.RADIO_BLOCK)
def get_radio_block_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the radio_block component."""
    return {
        "description": [
            _(
                "The `radio_block` component can be used to integrate groups of radio buttons. This variant of the radio buttons is displayed as a block of buttons and can be used to trigger a request when the selected value changes."
            )
        ]
    }


@register_component(Component.RANGE_SLIDER)
def get_rangle_slider_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the range slider component."""
    return {
        "description": [
            _(
                "The `slider` component can be used to integrate a range slider into the frontend, allowing a value to be selected within a defined interval."
            ),
            _(
                "The component supports a **dual-thumb mode** (`dual=True`) that allows users to select a range by setting both minimum and maximum values. "
                "In dual mode, two form fields are submitted: `{name}_min` and `{name}_max`."
            ),
            _(
                "The legend below the slider can be configured to respond to limited space using `legend_mode`: "
                "**'skip'** progressively hides items, while **'rotate'** displays text vertically."
            ),
            _(
                "The component fully supports **RTL (right-to-left)** layouts and adapts to **dark mode** automatically."
            ),
        ]
    }


@register_component(Component.TOGGLE)
def get_toggle_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the toggle component."""
    return {
        "description": [
            _(
                "The `toggle` component can be used to integrate a toggle button. It essentially functions like a single checkbox."
            )
        ]
    }


@register_component(Component.SELECT)
def get_select_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the select component."""
    return {"description": [_("The `select` component provides a simple selection box.")]}


@register_component(Component.MULTISELECT)
def get_multiselect_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the multiselect component."""
    return {
        "description": [
            _(
                "The `multiselect` component provides a selection box that allows multiple values to be selected. Additionally, the multiselect has an integrated search bar to allow quick searches for specific values."
            )
        ]
    }


@register_component(Component.CHAT)
def get_chat_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the chat component."""
    return {
        "description": [
            _(
                "The `chat` component provides a simple frontend for a chat application. It consists of a text input and an area for messages. The content of the message area is extended via HTMX with each response, without the page needing to be reloaded."
            )
        ]
    }


# =============================================================
#
#   Popup Tags
#
# =============================================================


@register_component(Component.ALERT)
def get_alert_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the alert component."""
    return {
        "description": [
            _(
                "The `alert` component provides a way to display important information, warnings, or success messages to users."
            )
        ]
    }


@register_component(Component.MODAL)
def get_modal_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the modal component."""
    return {
        "description": [
            _(
                "The `modal` component can be used to integrate customizable dialogs. These can display additional information to the user or be used as confirmation dialogs for various actions."
            )
        ]
    }


@register_component(Component.POPOVER)
def get_popover_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the popover component."""
    return {
        "description": [
            _(
                "The `popover` is a useful component if it is necessary to display additional but rather optional information that would disrupt the overall appearance or for which there simply is not enough space. Similar to a tooltip, popovers are also displayed separately from the rest of the layout and therefore do not disrupt the flow of the layout. A popover is an area for additional information that is only displayed when the user hovers the mouse cursor over a specific element. Unlike the tooltip, popovers do not close automatically and therefor also allow to display interactive elements to the user."
            ),
            _(
                "If only a short explanatory informational text with 1-2 words is to be displayed, the tooltip component is a better option."
            ),
        ]
    }


@register_component(Component.TOOLTIP)
def get_tooltip_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the tooltip component."""
    return {
        "description": [
            _(
                "The `tooltip` is helpful and important for displaying additional information without disrupting the flow of the web interface. If the label or icon of a button or similar element is not clear enough, it leaves room for interpretation, which in the worst case can lead to confusion. Tooltips are only displayed when the user hovers the mouse cursor over the corresponding element. The tooltip is displayed separately from the rest of the layout above all other elements, is therefore always visible and does not disrupt the overall appearance."
            ),
            _(
                "A tooltip should only be used for short informational texts (usually just one word). If more information needs to be displayed, the popover component should be used instead."
            ),
        ]
    }


# =============================================================
#
#   Util Tags
#
# =============================================================


@register_component(Component.INFOBOX)
def get_infobox_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the infobox component."""
    return {
        "description": [
            _(
                "The `infobox` component displays the text it contains in a bordered box, making it slightly more prominent, but not as conspicuous as an `alert`."
            )
        ]
    }


@register_component(Component.CODE_BLOCK)
def get_code_block_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the code block component."""
    return {
        "description": [
            _(
                "The `code_block` component displays source code with syntax highlighting and can copy the displayed source code to the clipboard via a button. The syntax highlighting covers virtually all common and most less common programming languages."
            )
        ]
    }


@register_component(Component.COPYRIGHT_NOTICE)
def get_copyright_notice_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the copyright notice component."""
    return {
        "description": [
            _("The `copyright_notice` component renders a compact, reusable copyright and legal notice line."),
            _(
                "It can be used inside the footer or in other page shells where an application needs a consistent public legal notice."
            ),
        ],
        "features": [
            _("Supports a holder name, source label, license text, optional license link, and rights text."),
            _("Keeps `app_name` as a backwards-compatible fallback for existing footer configuration."),
            _("Uses a dot-style separator by default instead of hyphens."),
        ],
    }


@register_component(Component.DIFFERENTIATOR)
def get_differentiator_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the differentiator component."""
    return {
        "description": [
            _(
                "The `differentiator` component can be used to graphically display differences between two texts, which can be very welcome help especially for longer texts with only small changes. For texts that differ more or less completely from each other, this component is probably less useful."
            )
        ]
    }


@register_component(Component.LOGO)
def get_logo_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the logo component."""
    return {
        "description": [
            _(
                "The `logo` component renders a brand mark from one consistent API. It supports image assets, SVG assets, and Insight UI icons."
            ),
            _(
                "Use `type='svg'` for SVG files stored as static assets, `type='image'` for bitmap images, and `type='icon'` for symbols from the Insight UI icon set. This avoids repeated ad-hoc SVG and dark-mode logo handling in application templates."
            ),
        ],
        "features": [
            _(
                "Image and SVG asset paths are resolved through Django static files unless an absolute, root-relative, or data URL is provided."
            ),
            _("Optional `url_dark` renders a dark-theme variant without custom JavaScript."),
            _("Icon logos reuse the existing Insight UI icon component."),
        ],
    }


@register_component(Component.BRAND_LOCKUP)
def get_brand_lockup_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the brand lockup component."""
    return {
        "description": [
            _(
                "The `brand_lockup` component renders a controlled brand unit made of a public Insight UI icon and a two-tone wordmark."
            ),
            _(
                "Use it when an application needs a recognizable wordmark without embedding private assets in the open-source package."
            ),
        ],
        "features": [
            _("Uses Insight UI design tokens for the primary and secondary brand colours."),
            _("Maps main, develop, and candidate variants to existing public icons from the Insight UI icon list."),
            _("Can be used directly or as the optional `brand.lockup` mode inside the navbar component."),
        ],
    }


@register_component(Component.CORNER_RIBBON)
def get_corner_ribbon_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the corner ribbon component."""
    return {
        "description": [
            _(
                "The `corner_ribbon` component displays a decorative diagonal text ribbon positioned in any of the four browser corners. It's ideal for highlighting new features, displaying status indicators, or adding promotional badges."
            ),
            _(
                "The ribbon appears above most page content, but you can click on elements located behind the component. It supports RTL layouts and multiple color variants for different semantic meanings."
            ),
        ]
    }


@register_component(Component.PROGRESS_BAR)
def get_progress_bar_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the progress bar component."""
    return {
        "description": [
            _(
                "The `progress_bar` component is used to visually display the progress of a background process to the user. A common scenario for such components is, for example, downloads."
            ),
            _(
                "For a progress indicator where progress is made through active user interaction, our Step Bar component is suitable."
            ),
        ],
        "description_notes_begin": [
            {"type": "warning", "message": "Diese Komponente befindet sich noch in Bearbeitung!"}
        ],
    }


@register_component(Component.GEO_MAP)
def get_geo_map_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the geo map component."""
    return {
        "description": [
            _(
                "The `geo_map` component displays a geographic map using leaflet on which geographic information can be easily displayed."
            )
        ]
    }


@register_component(Component.CHART)
def get_charts_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the charts component."""
    return {
        "description": [
            _(
                "The `chart` component allows charts to be displayed without having to customize JavaScript. The component uses Apache ECharts internally."
            ),
            _(
                "This component is currently available in the following variants: line_chart: A line chart. bar_chart: A stacked bar chart."
            ),
        ]
    }


@register_component(Component.LIVE_CONTENT)
def get_live_content_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the live content component."""
    return {
        "description": [
            _(
                "The `live_content` component regularly updates a fragment using HTMX requests. It is ideal for dashboards or status views that need to be updated frequently without reloading the entire page."
            )
        ]
    }


@register_component(Component.WEB_SOCKET)
def get_web_socket_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the web socket component."""
    return {
        "description": [
            _(
                "The `websocket` component is a thin wrapper around the HTMX WebSocket extension. It is designed for host applications that want HTMX-managed WebSocket updates without reloading the page."
            ),
            _(
                "By default the component expects HTML fragments that HTMX can swap into the DOM. Non-HTML frames are surfaced as browser events so host adapters can decide how to render them."
            ),
        ]
    }


# =============================================================
#
#   List Tags
#
# =============================================================


@register_component(Component.INFINITE_SCROLL)
def get_infinite_scroll_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the infinite scroll component."""
    return {
        "description": [
            _(
                "The `infinite_scroll` component represents an alternative to pagination and can be used to display large amounts of data. Instead of switching from page to page, the infinite scroll loads more data from the backend once a certain scroll threshold is reached and appends it to the end using HTMX."
            ),
            _(
                "The component is provided in two variants: one with automatic expansion and a second where a 'Load more' button must be actively clicked to load new elements."
            ),
        ]
    }


@register_component(Component.PAGINATION)
def get_pagination_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the pagination component."""
    return {
        "description": [
            _(
                "The `pagination` component can be used to split a list across multiple pages, which can be switched using the pagination displayed at the end of the list by this component. This is practical for large amounts of data and offers an alternative to the infinite_scroll component."
            )
        ]
    }


@register_component(Component.TABLE)
def get_table_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the table component."""
    return {
        "description": [
            _(
                "The `table` component can be used to display a simple table for any data. The layout is designed to be responsive; if space is insufficient, a horizontal scrollbar is displayed."
            )
        ]
    }


# =============================================================
#
#   Filter Tags
#
# =============================================================


@register_component(Component.SEARCH_BAR)
def get_search_bar_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the search bar component."""
    return {
        "description": [
            _(
                "The `search_bar` component provides a simple text input field with a large button on the right end. When submitted, a request is sent to the specified endpoint. The search_bar component also supports HTMX requests."
            )
        ]
    }


@register_component(Component.GENERIC_FILTER)
def get_generic_filter_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the generic filter component."""
    return {
        "description": [
            _(
                "The `generic_filter` component can be used to build relatively simple standard filters consisting of &lt;select&gt; tags. The filter automatically makes a request to the corresponding endpoint when a change is made and updates the data area using HTMX."
            ),
            _("An alternative is the more flexible but also more complex Query Builder."),
        ]
    }


@register_component(Component.QUERY_BUILDER)
def get_query_builder_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the query builder component."""
    return {
        "description": [
            _("The `query_builder` component represents an alternative to the `generic_filter` component."),
            _(
                "The query builder is far more flexible but also more complex to use than conventional filter methods. It is essentially a kind of graphical representation of an SQL query. The query builder receives a list of model fields that can be searched and for each field a list of allowed operations."
            ),
            _(
                "In special cases, predefined values can also be specified as with the other variant. This aspect makes this type of filtering potentially much more flexible, as it does away with fixed defined values."
            ),
            _("Similar to the other filter variant, only a dictionary with the desired properties is needed here."),
        ]
    }


# =============================================================
#
#   Card Tags
#
# =============================================================


@register_component(Component.CARD)
def get_card_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the card component."""
    return {
        "description": [
            _(
                "The `card` components are used to create information groups. Each card consists of a heading and its main content. There are also further options such as a background image or subtitle, and action buttons."
            ),
            _(
                "For the card component there are several variants to choose from: Card: Standard card in 16:9 format. App Card: The layout of this card is vertically oriented making it taller. Flip Card: This card rotates 180° and holds additional content on its back side."
            ),
        ]
    }


@register_component(Component.APP_CARD)
def get_app_card_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the app card component."""
    return {
        "description": [
            _(
                "The `app_card` component is designed for overview pages featuring multiple apps, demos, products, etc., and begins with a large image followed by the title and a description. Each card can include a set of tags (small buttons) as well as action buttons."
            )
        ]
    }


@register_component(Component.FLIP_CARD)
def get_flip_card_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the flip card component."""
    return {
        "description": [
            _(
                "The `flip_card` component is a variation of the `app_card` and has the unique feature of rotating 180° when hovered over. This special feature allows additional information to be displayed on the back without taking up any extra space."
            )
        ],
        "description_notes_begin": [
            {"type": "info", "message": _("The component is currently still under development.")}
        ],
    }


@register_component(Component.CARD_CAROUSEL)
def get_card_carousel_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the card carousel component."""
    return {
        "description": [
            _(
                "The `carousel` component can be used to display images, but also all kinds of other things, in a compact and interactive way. With having one object always in focus it is especially suited for images."
            )
        ]
    }


@register_component(Component.IMAGE_CAROUSEL)
def get_image_carousel_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the image carousel component."""
    carousel_url = reverse("component_detail_page_view", args=[Component.CARD_CAROUSEL.value])
    return {
        "description": [
            _("The `image_carousel` component is a variant of the carousel component adapted for displaying images.")
        ],
        "description_notes_end": [
            {
                "type": "info",
                "message": _(
                    "This documentation applies only to the image carousel. For more information about the carousel in general, see [Card Carousel](%(url)s)."
                )
                % {"url": carousel_url},
            }
        ],
    }


@register_component(Component.THREE_D_CAROUSEL)
def get_3d_carousel_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the 3D carousel component."""
    return {
        "description": [
            _(
                "The `three_d_carousel` component can be used to display any content in a unique way: arranged in a circle."
            )
        ]
    }


@register_component(Component.TOGGLE_VIEW)
def get_toggle_view_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the toggle view component."""
    return {
        "description": [
            _(
                "The `toggle_view` component combines the table and card view as well as the carousel component. The component is used to display the same data in completely different ways."
            )
        ]
    }


# =============================================================
#
#   Form Tags
#
# =============================================================


@register_component(Component.FORM)
def get_form_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the form component."""
    return {
        "description": [_("The `form` component can be used to build forms without having to edit HTML code yourself.")]
    }
