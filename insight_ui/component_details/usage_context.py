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


def get_sidebar_usage_context() -> dict[str, str]:
    """Serve usage documentation for the sidebar component."""
    return {"usage": ""}


def get_footer_usage_context() -> dict[str, str]:
    """Serve usage documentation for the footer component."""
    return {"usage": ""}


def get_breadcrumb_usage_context() -> dict[str, str]:
    """Serve usage documentation for the breadcrumb component."""
    return {"usage": ""}


def get_step_bar_usage_context() -> dict[str, str]:
    """Serve usage documentation for the step bar component."""
    return {"usage": ""}


def get_minimal_step_bar_usage_context() -> dict[str, str]:
    """Serve usage documentation for the minimal step bar component."""
    return {
        "usage": """
            {% load insight_tags %}

            {% minimal_step_bar config=min_step_bar_config %}
            """
    }


def get_bullet_point_list_usage_context() -> dict[str, str]:
    """Serve usage documentation for the bullet point list component."""
    return {"usage": ""}


def get_accordion_usage_context() -> dict[str, str]:
    """Serve usage documentation for the accordion component."""
    return {
        "usage": """
        {% load insight_tags %}

        {% accordion id="faq-exclusive" items=accordion_items exclusive=True %}
        """
    }


def get_tabs_usage_context() -> dict[str, str]:
    """Serve usage documentation for the tabs component."""
    return {"usage": ""}


def get_button_usage_context() -> dict[str, str]:
    """Serve usage documentation for the button component."""
    return {"usage": ""}


def get_input_field_usage_context() -> dict[str, str]:
    """Serve usage documentation for the input field component."""
    return {"usage": ""}


def get_checkbox_usage_context() -> dict[str, str]:
    """Serve usage documentation for the checkbox component."""
    return {"usage": ""}


def get_checkbox_group_usage_context() -> dict[str, str]:
    """Serve usage documentation for the checkbox group component."""
    return {"usage": ""}


def get_dropdown_usage_context() -> dict[str, str]:
    """Serve usage documentation for the dropdown component."""
    return {"usage": ""}


def get_radio_group_usage_context() -> dict[str, str]:
    """Serve usage documentation for the radio_group component."""
    return {"usage": ""}


def get_rangle_slider_usage_context() -> dict[str, str]:
    """Serve usage documentation for the range slider component."""
    return {"usage": ""}


def get_toggle_usage_context() -> dict[str, str]:
    """Serve usage documentation for the toggle component."""
    return {"usage": ""}


def get_select_usage_context() -> dict[str, str]:
    """Serve usage documentation for the select component."""
    return {"usage": ""}


def get_multiselect_usage_context() -> dict[str, str]:
    """Serve usage documentation for the multiselect component."""
    return {"usage": ""}


def get_chat_usage_context() -> dict[str, str]:
    """Serve usage documentation for the chat component."""
    return {"usage": ""}


def get_alert_usage_context() -> dict[str, str]:
    """Serve usage documentation for the alert component."""
    return {"usage": ""}


def get_modal_usage_context() -> dict[str, str]:
    """Serve usage documentation for the modal component."""
    return {"usage": ""}


def get_popover_usage_context() -> dict[str, str]:
    """Serve usage documentation for the popover component."""
    return {"usage": ""}


def get_tooltip_usage_context() -> dict[str, str]:
    """Serve usage documentation for the tooltip component."""
    return {"usage": ""}


def get_code_block_usage_context() -> dict[str, str]:
    """Serve usage documentation for the code block component."""
    return {"usage": ""}


def get_differentiator_usage_context() -> dict[str, str]:
    """Serve usage documentation for the differentiator component."""
    return {"usage": ""}


def get_progress_bar_usage_context() -> dict[str, str]:
    """Serve usage documentation for the progress bar component."""
    return {"usage": ""}


def get_geo_map_usage_context() -> dict[str, str]:
    """Serve usage documentation for the geo map component."""
    return {"usage": ""}


def get_charts_usage_context() -> dict[str, str]:
    """Serve usage documentation for the charts component."""
    return {"usage": ""}


def get_live_content_usage_context() -> dict[str, str]:
    """Serve usage documentation for the live content component."""
    return {"usage": ""}


def get_web_socket_usage_context() -> dict[str, str]:
    """Serve usage documentation for the web socket component."""
    return {"usage": ""}


def get_infinite_scroll_usage_context() -> dict[str, str]:
    """Serve usage documentation for the infinite scroll component."""
    return {"usage": ""}


def get_pagination_usage_context() -> dict[str, str]:
    """Serve usage documentation for the pagination component."""
    return {"usage": ""}


def get_table_usage_context() -> dict[str, str]:
    """Serve usage documentation for the table component."""
    return {"usage": ""}


def get_generic_filter_usage_context() -> dict[str, str]:
    """Serve usage documentation for the generic filter component."""
    return {"usage": ""}


def get_search_bar_usage_context() -> dict[str, str]:
    """Serve usage documentation for the search bar component."""
    return {"usage": ""}


def get_query_builder_usage_context() -> dict[str, str]:
    """Serve usage documentation for the query builder component."""
    return {"usage": ""}


def get_card_usage_context() -> dict[str, str]:
    """Serve usage documentation for the card component."""
    return {"usage": ""}


def get_card_carousel_usage_context() -> dict[str, str]:
    """Serve usage documentation for the card carousel component."""
    return {"usage": ""}


def get_image_carousel_usage_context() -> dict[str, str]:
    """Serve usage documentation for the image carousel component."""
    return {"usage": ""}


def get_3d_carousel_usage_context() -> dict[str, str]:
    """Serve usage documentation for the 3D carousel component."""
    return {"usage": ""}


def get_toggle_view_usage_context() -> dict[str, str]:
    """Serve usage documentation for the toggle view component."""
    return {"usage": ""}


def get_form_usage_context() -> dict[str, str]:
    """Serve usage documentation for the form component."""
    return {"usage": ""}
