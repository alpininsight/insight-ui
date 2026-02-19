from collections import defaultdict
from collections.abc import Callable
from typing import Any

from insight_ui.component_details.related_components_context import get_related_components_context

Context = dict[str, Any]
ContextBuilder = Callable[[], Context]

CONTEXT_BUILDERS: dict[str, list[ContextBuilder]] = defaultdict(list)


def component(component_name: str) -> Callable[[ContextBuilder], ContextBuilder]:
    """Register context method for the specified component."""

    def decorator(func: ContextBuilder) -> ContextBuilder:
        CONTEXT_BUILDERS[component_name].append(func)
        return func

    return decorator


def get_component_context(component_name: str) -> dict:
    """Serve docs of the specified component."""
    if component_name not in CONTEXT_BUILDERS:
        raise ValueError(f"Unknown component: {component_name}")  # noqa: TRY003

    context = {}

    for builder in CONTEXT_BUILDERS.get(component_name, []):
        part = builder()
        context.update(part)

    related_components = {"related_topics": get_related_components_context(component_name)}
    context.update(related_components)

    return context
