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

SOURCE_COMPONENT_ALIASES = {
    "breadcrumb": "breadcrumbs",
    "button": "buttons",
    "card": "cards",
    "input_field": "input",
    "web_socket": "websocket",
}

RELATED_COMPONENT_ALIASES = {
    "breadcrumbs": "breadcrumb",
    "buttons": "button",
    "cards": "card",
    "input": "input_field",
    "three_d_carousel": "3D_carousel",
    "toggle": "toggle_button",
    "websocket": "web_socket",
}


def _normalize_source_component_name(component_name: str) -> str:
    """Normalize component names used as dictionary keys in RELATED_COMPONENTS."""
    return SOURCE_COMPONENT_ALIASES.get(component_name, component_name)


def _normalize_related_component_name(component_name: str) -> str:
    """Normalize related component names to route-compatible component names."""
    return RELATED_COMPONENT_ALIASES.get(component_name, component_name)


def get_related_components_context(
    component_name: str, valid_component_names: set[str] | None = None
) -> list[dict[str, str]]:
    """Serve related components context of the specified component."""
    source_component = _normalize_source_component_name(component_name)
    related_components = RELATED_COMPONENTS.get(source_component, [])

    normalized_components = []
    seen_components: set[str] = set()

    for component in related_components:
        normalized_component = _normalize_related_component_name(component)
        if valid_component_names is not None and normalized_component not in valid_component_names:
            continue
        if normalized_component in seen_components:
            continue

        seen_components.add(normalized_component)
        normalized_components.append(
            {"component_name": normalized_component, "formatted_name": normalized_component.replace("_", " ").title()}
        )

    return normalized_components
