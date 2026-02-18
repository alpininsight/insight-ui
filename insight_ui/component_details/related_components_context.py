RELATED_COMPONENTS = {
    "cards": ["carousel", "toggle_view"],
    "flip_card": [],
    "app_card": [],
    "3D_carousel": ["card_carousel", "image_carousel"],
    "card_carousel": ["image_carousel", "three_d_carousel"],
    "image_carousel": ["card_carousel", "three_d_carousel"],
    "accordion": ["tabs"],
    "alert": [],
    "breadcrumbs": [],
    "bullet_point_list": [],
    "buttons": ["input_field", "radio_group", "toggle", "checkbox"],
    "chat": ["search_bar"],
    "checkbox": ["checkbox_group", "radio_group", "button", "toggle", "input_field"],
    "checkbox_group": ["checkbox", "radio_group", "button", "toggle", "input_field"],
    "dropdown": [],
    "footer": ["navbar", "sidebar"],
    "form": ["alert"],
    "generic_filter": ["query_builder", "select", "multiselect"],
    "geo_map": [],
    "infinite_scroll": ["pagination"],
    "input": ["checkbox", "checkbox_group", "radio_group", "button", "toggle"],
    "live_content": ["websocket"],
    "minimal_step_bar": ["step_bar"],
    "modal": ["popover"],
    "multiselect": ["select", "generic_filter", "query_builder"],
    "navbar": ["footer", "sidebar"],
    "pagination": ["infinite_scroll"],
    "popover": ["modal", "tooltip"],
    "progress_bar": ["step_bar"],
    "query_builder": ["generic_filter", "select", "multiselect"],
    "radio_block": ["checkbox_group", "button", "toggle", "input_field"],
    "radio_group": ["checkbox_group", "button", "toggle", "input_field"],
    "range_slider": ["input_field"],
    "search_bar": ["chat", "select", "multiselect"],
    "select": ["multiselect", "generic_filter", "query_builder"],
    "sidebar": ["navbar", "footer", "modal"],
    "step_bar": ["minimal_step_bar", "bullet_point_list"],
    "table": ["pagination", "carousel", "toggle_view"],
    "tabs": ["accordion"],
    "toggle_button": ["checkbox", "button"],
    "toggle_view": ["table", "pagination", "card_carousel"],
    "tooltip": ["popover"],
    "websocket": ["live_content"],
}


def get_related_components_context(component_name: str) -> list[dict[str, str]]:
    """Serve related components context of the specified component."""
    return [
        {"component_name": component, "formatted_name": component.replace("_", " ").title()}
        for component in RELATED_COMPONENTS[component_name]
    ]
