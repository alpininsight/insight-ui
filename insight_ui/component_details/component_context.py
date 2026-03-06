from collections import defaultdict
from collections.abc import Callable
from typing import Any

from insight_ui.component_details.components import Component
from insight_ui.component_details.related_components_context import get_related_components_context

Context = dict[str, Any]
ContextBuilder = Callable[[], Context]

COMPONENT_CONTEXT_BUILDERS: dict[str, list[ContextBuilder]] = defaultdict(list)
DEMO_CONTEXT_BUILDERS: dict[str, ContextBuilder] = {}


def register_component(component: Component) -> Callable[[ContextBuilder], ContextBuilder]:
    """Register context method for the specified component."""

    def decorator(func: ContextBuilder) -> ContextBuilder:
        COMPONENT_CONTEXT_BUILDERS[component.value].append(func)
        return func

    return decorator


def get_component_context(component: Component) -> dict:
    """Serve docs of the specified component."""
    if component.value not in COMPONENT_CONTEXT_BUILDERS:
        raise ValueError(  # noqa: TRY003
            f"Unknown component: {component.value} accessible components are {COMPONENT_CONTEXT_BUILDERS.keys()}."
        )

    context = {"component_name": component.value, "formatted_name": component.value.replace("_", " ").title()}

    for builder in COMPONENT_CONTEXT_BUILDERS.get(component.value, []):
        part = builder()
        context.update(part)

    related_components = {"related_topics": get_related_components_context(component.value)}
    context.update(related_components)

    return context


def register_demo_context(component: Component) -> Callable[[ContextBuilder], ContextBuilder]:
    """Register a demo context method for the specified component."""

    def decorator(func: ContextBuilder) -> ContextBuilder:
        key = component.value

        if key in DEMO_CONTEXT_BUILDERS:
            raise ValueError(f"Component '{key}' already has a registered demo context!")  # noqa: TRY003

        DEMO_CONTEXT_BUILDERS[key] = func
        return func

    return decorator


def get_demo_context(component: Component) -> dict | None:
    """Serve demo context of the specified component."""
    return DEMO_CONTEXT_BUILDERS.get(component.value)
