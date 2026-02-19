from insight_ui.component_details.component_context import component


@component("navbar")
def get_navbar_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the navbar component."""
    return {"a11y": []}


@component("sidebar")
def get_sidebar_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the sidebar component."""
    return {"a11y": []}


@component("footer")
def get_footer_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the footer component."""
    return {"a11y": []}


@component("breadcrumbs")
def get_breadcrumb_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the breadcrumb component."""
    return {"a11y": []}


@component("step_bar")
def get_step_bar_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the step bar component."""
    return {"a11y": []}


@component("minimal_step_bar")
def get_minimal_step_bar_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the minimal step bar component."""
    return {"a11y": []}


@component("bullet_point_list")
def get_bullet_point_list_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the bullet point list component."""
    return {"a11y": []}


@component("accordion")
def get_accordion_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the accordion component."""
    return {
        "a11y": [
            "Das aktuell geöffnete Element wird mit aria-expanded='true' markiert.",
            "Die Kopfzeile ist mit aria-controls ausgestattet, wodurch der Bezug zum dem darunter liegenden Container hergestellt wird.",
            "Der Container besitzt zusätzlich das Attribut aria-labelledby.",
            "Der Container ist mit role='region' ausgestattet, damit dieser leicht ansteuerbar ist.",
            "Die Komponente unterstützt die Navigation über die Tastatur mittels der Pfeiltasten (hoch/runter).",
        ]
    }


@component("tabs")
def get_tabs_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the tabs component."""
    return {"a11y": []}


@component("button")
def get_button_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the button component."""
    return {"a11y": []}


@component("input_field")
def get_input_field_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the input field component."""
    return {"a11y": []}


@component("checkbox")
def get_checkbox_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the checkbox component."""
    return {"a11y": []}


@component("checkbox_group")
def get_checkbox_group_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the checkbox group component."""
    return {"a11y": []}


@component("dropdown")
def get_dropdown_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the dropdown component."""
    return {"a11y": []}


@component("radio_group")
def get_radio_group_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the radio_group component."""
    return {"a11y": []}


@component("range_slider")
def get_rangle_slider_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the range slider component."""
    return {"a11y": []}


@component("toggle")
def get_toggle_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the toggle component."""
    return {"a11y": []}


@component("select")
def get_select_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the select component."""
    return {"a11y": []}


@component("multiselect")
def get_multiselect_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the multiselect component."""
    return {"a11y": []}


@component("chat")
def get_chat_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the chat component."""
    return {"a11y": []}


@component("alert")
def get_alert_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the alert component."""
    return {"a11y": []}


@component("modal")
def get_modal_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the modal component."""
    return {"a11y": []}


@component("popover")
def get_popover_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the popover component."""
    return {"a11y": []}


@component("tooltip")
def get_tooltip_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the tooltip component."""
    return {"a11y": []}


@component("code_block")
def get_code_block_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the code block component."""
    return {"a11y": []}


@component("differentiator")
def get_differentiator_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the differentiator component."""
    return {"a11y": []}


@component("progress_bar")
def get_progress_bar_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the progress bar component."""
    return {"a11y": []}


@component("geo_map")
def get_geo_map_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the geo map component."""
    return {"a11y": []}


@component("chart")
def get_charts_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the charts component."""
    return {"a11y": []}


@component("live_content")
def get_live_content_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the live content component."""
    return {"a11y": []}


@component("web_socket")
def get_web_socket_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the web socket component."""
    return {"a11y": []}


@component("infinite_scroll")
def get_infinite_scroll_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the infinite scroll component."""
    return {"a11y": []}


@component("pagination")
def get_pagination_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the pagination component."""
    return {"a11y": []}


@component("table")
def get_table_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the table component."""
    return {"a11y": []}


@component("generic_filter")
def get_generic_filter_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the generic filter component."""
    return {"a11y": []}


@component("search_bar")
def get_search_bar_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the search bar component."""
    return {"a11y": []}


@component("query_builder")
def get_query_builder_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the query builder component."""
    return {"a11y": []}


@component("card")
def get_card_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the card component."""
    return {"a11y": []}


@component("card_carousel")
def get_card_carousel_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the card carousel component."""
    return {"a11y": []}


@component("image_carousel")
def get_image_carousel_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the image carousel component."""
    return {"a11y": []}


@component("3d_carousel")
def get_3d_carousel_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the 3D carousel component."""
    return {"a11y": []}


@component("toggle_view")
def get_toggle_view_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the toggle view component."""
    return {"a11y": []}


@component("form")
def get_form_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the form component."""
    return {"a11y": []}
