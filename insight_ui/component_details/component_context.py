from insight_ui.component_details import (
    a11y_context,
    description_context,
    parameter_context,
    related_components_context,
    usage_context,
)


def get_component_context(component_name: str) -> dict:
    """Serve docs of the specified component."""
    related_components = {"related_topics": related_components_context.get_related_components_context(component_name)}

    return (
        {"component_name": component_name.replace("_", " ").title()}
        | description_context.get_minimal_step_bar_description_context()
        | usage_context.get_minimal_step_bar_usage_context()
        | parameter_context.get_minimal_step_bar_parameter_context()
        | a11y_context.get_minimal_step_bar_a11y_context()
        | related_components
    )
