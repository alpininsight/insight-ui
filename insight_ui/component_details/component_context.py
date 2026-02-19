from insight_ui.component_details import (
    a11y_context,
    description_context,
    parameter_context,
    related_components_context,
    usage_context,
)

CONTEXT_COMPONENT_ALIASES = {
    "3D_carousel": "3d_carousel",
    "chart": "charts",
    "range_slider": "rangle_slider",
    "toggle_button": "toggle",
}

CANONICAL_COMPONENT_ALIASES = {
    "3d_carousel": "3D_carousel",
    "charts": "chart",
    "rangle_slider": "range_slider",
    "toggle": "toggle_button",
}


def _resolve_component_key(component_name: str) -> str:
    """Map route component names to their context function naming variants."""
    return CONTEXT_COMPONENT_ALIASES.get(component_name, component_name)


def _resolve_component_context(module: object, component_name: str, section: str) -> dict:
    """Resolve and execute the component context function of the given section."""
    key = _resolve_component_key(component_name)
    getter_name = f"get_{key}_{section}_context"
    getter = getattr(module, getter_name, None)
    if getter is None:
        return {}
    return getter()


def _discover_valid_component_names() -> set[str]:
    """Build a set of canonical component names from available parameter context functions."""
    valid_components: set[str] = set()
    prefix = "get_"
    suffix = "_parameter_context"

    for attr in dir(parameter_context):
        if not attr.startswith(prefix) or not attr.endswith(suffix):
            continue
        component_key = attr[len(prefix) : -len(suffix)]
        canonical_name = CANONICAL_COMPONENT_ALIASES.get(component_key, component_key)
        valid_components.add(canonical_name)

    return valid_components


VALID_COMPONENT_NAMES = _discover_valid_component_names()


def get_component_context(component_name: str) -> dict:
    """Serve documentation context of the specified component."""
    related_components = {
        "related_topics": related_components_context.get_related_components_context(
            component_name, valid_component_names=VALID_COMPONENT_NAMES
        )
    }

    return (
        {"component_name": component_name.replace("_", " ").title()}
        | {"usage_summary": ""}
        | _resolve_component_context(description_context, component_name, "description")
        | _resolve_component_context(usage_context, component_name, "usage")
        | _resolve_component_context(parameter_context, component_name, "parameter")
        | _resolve_component_context(a11y_context, component_name, "a11y")
        | related_components
    )
