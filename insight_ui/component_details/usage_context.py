from insight_ui.component_details.component_context import component


@component("navbar")
def get_navbar_usage_context() -> dict[str, str]:
    """Serve usage documentation for the navbar component."""
    return {
        "usage": """
                {% load insight_tags %}

                {% block navbar %}
                    {% navbar config=nav_config user=user user_dropdown_links=user_dropdown_links show_login=True %}
                {% endblock navbar %}
                """
    }


@component("sidebar")
def get_sidebar_usage_context() -> dict[str, str]:
    """Serve usage documentation for the sidebar component."""
    return {"usage": ""}


@component("footer")
def get_footer_usage_context() -> dict[str, str]:
    """Serve usage documentation for the footer component."""
    return {"usage": ""}


@component("breadcrumb")
def get_breadcrumb_usage_context() -> dict[str, str]:
    """Serve usage documentation for the breadcrumb component."""
    return {"usage": ""}


@component("step_bar")
def get_step_bar_usage_context() -> dict[str, str]:
    """Serve usage documentation for the step bar component."""
    return {"usage": ""}


@component("minimal_step_bar")
def get_minimal_step_bar_usage_context() -> dict[str, str]:
    """Serve usage documentation for the minimal step bar component."""
    return {
        "usage": """
        {% load insight_tags %}

        {% minimal_step_bar config=min_step_bar_config %}
        """
    }


@component("bullet_point_list")
def get_bullet_point_list_usage_context() -> dict[str, str]:
    """Serve usage documentation for the bullet point list component."""
    return {"usage": ""}


@component("accordion")
def get_accordion_usage_context() -> dict[str, str]:
    """Serve usage documentation for the accordion component."""
    return {
        "usage": """
        {% load insight_tags %}

        {% accordion id="faq-exclusive" items=accordion_items exclusive=True %}
        """
    }


@component("tabs")
def get_tabs_usage_context() -> dict[str, str]:
    """Serve usage documentation for the tabs component."""
    return {"usage": ""}


@component("button")
def get_button_usage_context() -> dict[str, str]:
    """Serve usage documentation for the button component."""
    return {"usage": ""}


@component("input_field")
def get_input_field_usage_context() -> dict[str, str]:
    """Serve usage documentation for the input field component."""
    return {"usage": ""}


@component("checkbox")
def get_checkbox_usage_context() -> dict[str, str]:
    """Serve usage documentation for the checkbox component."""
    return {"usage": ""}


@component("checkbox_group")
def get_checkbox_group_usage_context() -> dict[str, str]:
    """Serve usage documentation for the checkbox group component."""
    return {"usage": ""}


@component("dropdown")
def get_dropdown_usage_context() -> dict[str, str]:
    """Serve usage documentation for the dropdown component."""
    return {"usage": ""}


@component("radio_group")
def get_radio_group_usage_context() -> dict[str, str]:
    """Serve usage documentation for the radio_group component."""
    return {"usage": ""}


@component("range_slider")
def get_rangle_slider_usage_context() -> dict[str, str]:
    """Serve usage documentation for the range slider component."""
    return {"usage": ""}


@component("toggle")
def get_toggle_usage_context() -> dict[str, str]:
    """Serve usage documentation for the toggle component."""
    return {"usage": ""}


@component("select")
def get_select_usage_context() -> dict[str, str]:
    """Serve usage documentation for the select component."""
    return {"usage": ""}


@component("multiselect")
def get_multiselect_usage_context() -> dict[str, str]:
    """Serve usage documentation for the multiselect component."""
    return {"usage": ""}


@component("chat")
def get_chat_usage_context() -> dict[str, str]:
    """Serve usage documentation for the chat component."""
    return {"usage": ""}


@component("alert")
def get_alert_usage_context() -> dict[str, str]:
    """Serve usage documentation for the alert component."""
    return {"usage": ""}


@component("modal")
def get_modal_usage_context() -> dict[str, str]:
    """Serve usage documentation for the modal component."""
    return {"usage": ""}


@component("popover")
def get_popover_usage_context() -> dict[str, str]:
    """Serve usage documentation for the popover component."""
    return {"usage": ""}


@component("tooltip")
def get_tooltip_usage_context() -> dict[str, str]:
    """Serve usage documentation for the tooltip component."""
    return {"usage": ""}


@component("code_block")
def get_code_block_usage_context() -> dict[str, str]:
    """Serve usage documentation for the code block component."""
    return {"usage": ""}


@component("differentiator")
def get_differentiator_usage_context() -> dict[str, str]:
    """Serve usage documentation for the differentiator component."""
    return {"usage": ""}


@component("progress_bar")
def get_progress_bar_usage_context() -> dict[str, str]:
    """Serve usage documentation for the progress bar component."""
    return {"usage": ""}


@component("geo_map")
def get_geo_map_usage_context() -> dict[str, str]:
    """Serve usage documentation for the geo map component."""
    return {"usage": ""}


@component("chart")
def get_charts_usage_context() -> dict[str, str]:
    """Serve usage documentation for the charts component."""
    return {"usage": ""}


@component("live_content")
def get_live_content_usage_context() -> dict[str, str]:
    """Serve usage documentation for the live content component."""
    return {"usage": ""}


@component("web_socket")
def get_web_socket_usage_context() -> dict[str, str]:
    """Serve usage documentation for the web socket component."""
    return {"usage": ""}


@component("infinite_scroll")
def get_infinite_scroll_usage_context() -> dict[str, str]:
    """Serve usage documentation for the infinite scroll component."""
    return {"usage": ""}


@component("pagination")
def get_pagination_usage_context() -> dict[str, str]:
    """Serve usage documentation for the pagination component."""
    return {"usage": ""}


@component("table")
def get_table_usage_context() -> dict[str, str]:
    """Serve usage documentation for the table component."""
    return {"usage": ""}


@component("generic_filter")
def get_generic_filter_usage_context() -> dict[str, str]:
    """Serve usage documentation for the generic filter component."""
    return {"usage": ""}


@component("search_bar")
def get_search_bar_usage_context() -> dict[str, str]:
    """Serve usage documentation for the search bar component."""
    return {"usage": ""}


@component("query_builder")
def get_query_builder_usage_context() -> dict[str, str]:
    """Serve usage documentation for the query builder component."""
    return {"usage": ""}


@component("card")
def get_card_usage_context() -> dict[str, str]:
    """Serve usage documentation for the card component."""
    return {"usage": ""}


@component("card_carousel")
def get_card_carousel_usage_context() -> dict[str, str]:
    """Serve usage documentation for the card carousel component."""
    return {"usage": ""}


@component("image_carousel")
def get_image_carousel_usage_context() -> dict[str, str]:
    """Serve usage documentation for the image carousel component."""
    return {"usage": ""}


@component("3d_carousel")
def get_3d_carousel_usage_context() -> dict[str, str]:
    """Serve usage documentation for the 3D carousel component."""
    return {"usage": ""}


@component("toggle_view")
def get_toggle_view_usage_context() -> dict[str, str]:
    """Serve usage documentation for the toggle view component."""
    return {"usage": ""}


@component("form")
def get_form_usage_context() -> dict[str, str]:
    """Serve usage documentation for the form component."""
    return {"usage": ""}
