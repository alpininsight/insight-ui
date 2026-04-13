from django.utils.translation import gettext as _

from insight_ui.component_details.component_context import register_component
from insight_ui.component_details.components import Component


@register_component(Component.PAGE_HEADER)
def get_page_header_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the page header component."""
    return {
        "a11y": [
            _("The title is rendered as a semantic `<h1>` element."),
            _("The description uses a `<p>` element with sufficient color contrast (grey on blue)."),
        ]
    }


@register_component(Component.HEADING_DECORATION)
def get_heading_decoration_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the heading decoration component."""
    return {
        "a11y": [
            _("All rendered variants are decorative and use aria-hidden='true'."),
            _("The 'none' style renders no markup and therefore adds no extra accessibility tree content."),
        ]
    }


@register_component(Component.ARTICLE)
def get_article_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the article component."""
    return {
        "a11y": [
            _("The article uses the semantic `<article>` element."),
            _("The column structure is purely visual and does not influence the reading order for screen readers."),
            _("The column separation is visually represented with column-rule."),
        ]
    }


@register_component(Component.HERO)
def get_hero_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the hero component."""
    return {
        "a11y": [
            _("The title is rendered as a semantic `<h1>` element."),
            _("CTA buttons are implemented as link elements with clear labels."),
            _("Background images are denoted with aria-hidden."),
        ]
    }


@register_component(Component.NAVBAR)
def get_navbar_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the navbar component."""
    return {"a11y": [_("The navbar component contains a skip link to the main content.")]}


@register_component(Component.SIDEBAR)
def get_sidebar_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the sidebar component."""
    return {
        "a11y": [
            _("The sidebar uses an `<aside>` tag and the attribute `role='complementary'` for semantic correctness."),
            _("The drawer variant uses focus-trapping and has a close button to be accessible by keyboard."),
        ]
    }


@register_component(Component.FOOTER)
def get_footer_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the footer component."""
    return {
        "a11y": [
            _("The headings of the three columns use `<h4>` tags so that a screennreader can switch between them."),
            _("The listing of the links uses a semantically correct `<ul>` tag with corresponding `<li>` tags."),
        ]
    }


@register_component(Component.BREADCRUMBS)
def get_breadcrumb_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the breadcrumbs component."""
    return {
        "a11y": [
            _("The component uses a `<nav>` tag with the corresponding `aria-label='Breadcrumb'`."),
            _("The active element has the attribute `aria-current='page'`."),
        ]
    }


@register_component(Component.STEP_BAR)
def get_step_bar_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the step bar component."""
    return {
        "a11y": [
            _(
                "If the graphical element at the start of every entry is not a number, it will be ignored by screenreaders through `aria-hidden`, since it is purely decorative."
            )
        ]
    }


@register_component(Component.MINIMAL_STEP_BAR)
def get_minimal_step_bar_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the minimal step bar component."""
    return {"a11y": []}


@register_component(Component.BULLET_POINT_LIST)
def get_bullet_point_list_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the bullet point list component."""
    return {
        "a11y": [
            _(
                "The graphical element at the start of every entry will be ignored by screen readers through `aria-hidden`, since it is purely decorative."
            )
        ]
    }


@register_component(Component.ACCORDION)
def get_accordion_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the accordion component."""
    return {
        "a11y": [
            _("The currently active element is labeled with `aria-expanded='true'`."),
            _("The header row is equipped with `aria-controls`, establishing the relationship to the container below."),
            _("The container additionally has the attribute `aria-labelledby`."),
            _("The container has the `role='region'` for ease of navigation."),
            _("The component can be navigated by keyboard keys Arrow (up/down)."),
        ]
    }


@register_component(Component.TABS)
def get_tabs_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the tabs component."""
    return {
        "a11y": [
            _(
                "The component supports screen readers with the following roles: `role='tablist'`, `role='tab'`, `role='tabpanel'`."
            ),
            _("Tabs and their contents are connected by `aria-selected`, `aria-controls`, `aria-labelledby.`"),
            _("The currently focused tab has the attribute `tabindex='0'` while all others have `tabindex='1'`."),
            _("The component supports keyboard navigation using the arrow keys (left/right) and Home/End keys."),
        ]
    }


@register_component(Component.BUTTON)
def get_button_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the button component."""
    return {
        "a11y": [
            _("Buttons that only have an icon and no text should have a descriptive `aria-label`."),
            _("A button should, like the rest of the website, always be operable and usable via keyboard."),
            _(
                "For correct semantic compliance, a `<button>` is always preferable to an interactive `<div>` container."
            ),
        ]
    }


@register_component(Component.INPUT_FIELD)
def get_input_field_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the input field component."""
    return {"a11y": [_("The `<label>` and its associated `<input>` are linked using `for` / `id`.")]}


@register_component(Component.CHECKBOX)
def get_checkbox_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the checkbox component."""
    return {"a11y": [_("The `<label>` and its associated `<input>` are linked using `for` / `id`.")]}


@register_component(Component.CHECKBOX_GROUP)
def get_checkbox_group_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the checkbox group component."""
    return {"a11y": [_("See Checkbox")]}


@register_component(Component.DROPDOWN)
def get_dropdown_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the dropdown component."""
    return {
        "a11y": [
            _(
                "The arrow at the end of dropdown buttons is ignored by screen readers using aria-hidden, since it is purely decorative."
            ),
            _("Icons displayed in links or menu items are also ignored by screen readers."),
            _("**TODO: Add support for navigation with arrow keys.**"),
        ]
    }


@register_component(Component.RADIO_GROUP)
def get_radio_group_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the radio_group component."""
    return {"a11y": [_("The component supports keyboard navigation using the arrow keys (up/down, right/left).")]}


@register_component(Component.RADIO_BLOCK)
def get_radio_block_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the radio_block component."""
    return {"a11y": [_("The component supports keyboard navigation using the arrow keys (up/down, right/left).")]}


@register_component(Component.RANGE_SLIDER)
def get_rangle_slider_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the range slider component."""
    return {
        "a11y": [
            _("The `<label>` and its associated `<input>` are linked using `for` / `id`."),
            _("The component supports keyboard navigation using the arrow keys (up/down, right/left)."),
        ]
    }


@register_component(Component.TOGGLE)
def get_toggle_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the toggle component."""
    return {"a11y": [_("The `<label>` and its associated `<input>` are linked using `for` / `id`.")]}


@register_component(Component.SELECT)
def get_select_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the select component."""
    return {
        "a11y": [
            _("The `<label>` and its associated `<input>` are linked using `for` / `id`."),
            _("The component can be navigated by keyboard keys Arrow (up/down)."),
        ]
    }


@register_component(Component.MULTISELECT)
def get_multiselect_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the multiselect component."""
    return {
        "a11y": [
            _("The `<label>` and its associated `<input>` are linked using `for` / `id`."),
            _(
                "The component supports screen readers through the corresponding ARIA attributes: `role='combobox'`, `aria-expanded'`, `aria-selected'`."
            ),
            _("The component can be navigated by keyboard keys Arrow (up/down)."),
        ]
    }


@register_component(Component.CHAT)
def get_chat_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the chat component."""
    return {"a11y": [_("The `<label>` and its associated `<input>` are linked using `for` / `id`.")]}


@register_component(Component.ALERT)
def get_alert_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the alert component."""
    return {
        "a11y": [
            _("The alert box has the attribute `role='alert'` to support screen readers."),
            _("The close button is accessible via keyboard and has a corresponding `aria-label`."),
        ]
    }


@register_component(Component.MODAL)
def get_modal_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the modal component."""
    return {
        "a11y": [
            _(
                "The modal is semantically correctly defined as a dialog window using the attributes `role='dialog'` and `aria-modal='true'`."
            ),
            _(
                "For screen readers, the modal provides a title and an (optional) description, which are linked using `aria-labelledby` and `aria-describedby`."
            ),
            _("The dialog window uses focus trapping and has a close button so that it can be accessed via keyboard."),
        ]
    }


@register_component(Component.POPOVER)
def get_popover_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the popover component."""
    return {"a11y": [_("**TODO: Add keyboard support!**")]}


@register_component(Component.TOOLTIP)
def get_tooltip_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the tooltip component."""
    return {"a11y": [_("**TODO: Add keyboard support!**")]}


@register_component(Component.INFOBOX)
def get_infobox_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the infobox component."""
    return {"a11y": []}


@register_component(Component.CODE_BLOCK)
def get_code_block_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the code block component."""
    return {"a11y": [_("The component is accessible via keyboard.")]}


@register_component(Component.DIFFERENTIATOR)
def get_differentiator_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the differentiator component."""
    return {"a11y": []}


@register_component(Component.PROGRESS_BAR)
def get_progress_bar_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the progress bar component."""
    return {"a11y": ["**TODO**"]}


@register_component(Component.GEO_MAP)
def get_geo_map_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the geo map component."""
    return {"a11y": [_("**TODO: Apply leaflet.js a11y!**")]}


@register_component(Component.CHART)
def get_charts_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the charts component."""
    return {"a11y": [_("**TODO: Apply Apache EChart Web Accessibility!**")]}


@register_component(Component.LIVE_CONTENT)
def get_live_content_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the live content component."""
    return {"a11y": ["**TODO**"]}


@register_component(Component.WEB_SOCKET)
def get_web_socket_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the web socket component."""
    return {"a11y": ["**TODO**"]}


@register_component(Component.INFINITE_SCROLL)
def get_infinite_scroll_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the infinite scroll component."""
    return {"a11y": ["**TODO**"]}


@register_component(Component.PAGINATION)
def get_pagination_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the pagination component."""
    return {
        "a11y": [
            _(
                "The buttons for first page, last page, etc. have a descriptive text that is read aloud by screen readers and also explains why the button is disabled in some cases."
            ),
            _("**TODO: Add support for arrow key navigation (right/left)**"),
        ]
    }


@register_component(Component.TABLE)
def get_table_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the table component."""
    return {"a11y": ["**TODO**"]}


@register_component(Component.GENERIC_FILTER)
def get_generic_filter_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the generic filter component."""
    return {"a11y": ["**TODO**"]}


@register_component(Component.SEARCH_BAR)
def get_search_bar_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the search bar component."""
    return {"a11y": [_("The text input field has an extra title ('Search') for screen readers.")]}


@register_component(Component.QUERY_BUILDER)
def get_query_builder_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the query builder component."""
    return {"a11y": ["**TODO**"]}


@register_component(Component.CARD)
def get_card_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the card component."""
    return {"a11y": []}


@register_component(Component.APP_CARD)
def get_app_card_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the app card component."""
    return {"a11y": []}


@register_component(Component.FLIP_CARD)
def get_flip_card_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the flip card component."""
    return {"a11y": []}


@register_component(Component.CARD_CAROUSEL)
def get_card_carousel_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the card carousel component."""
    return {
        "a11y": [
            _("The carousel is accessible via keyboard."),
            _("**TODO: Add support for arrow key navigation (right/left)**"),
        ]
    }


@register_component(Component.IMAGE_CAROUSEL)
def get_image_carousel_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the image carousel component."""
    return {"a11y": [_("See Card Carousel")]}


@register_component(Component.THREE_D_CAROUSEL)
def get_3d_carousel_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the 3D carousel component."""
    return {"a11y": [_("The carousel is accessible via keyboard.")]}


@register_component(Component.TOGGLE_VIEW)
def get_toggle_view_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the toggle view component."""
    return {"a11y": [_("See Radio Group")]}


@register_component(Component.FORM)
def get_form_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the form component."""
    return {"a11y": []}
