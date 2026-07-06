"""Component context registry and parameter documentation utilities."""

import types
from collections import defaultdict
from collections.abc import Callable
from dataclasses import MISSING, Field, dataclass, fields, is_dataclass
from typing import Any, Literal, Union, get_args, get_origin

from django.utils.translation import gettext as _

from insight_ui.component_details.components import Component
from insight_ui.component_details.related_components_context import get_related_components_context

Context = dict[str, Any]
ContextBuilder = Callable[[], Context]

COMPONENT_CONTEXT_BUILDERS: dict[str, list[ContextBuilder]] = defaultdict(list)
DEMO_CONTEXT_BUILDERS: dict[str, ContextBuilder] = {}


@dataclass
class ParameterDetails:
    """Describes a component parameter, with a 'name', 'type', 'description' and the 'default' value."""

    name: str
    type: str
    description: str
    default: str
    required: bool = False


@dataclass
class ParameterDoc:
    """Represents the documentation of a component parameter."""

    details: ParameterDetails
    params_table: list[ParameterDetails]
    example_data: str
    notes: list[dict[str, str]] = None


def format_type(t: object) -> str:  # noqa: PLR0911
    """Create a readable string representation of a type annotation.

    Handles generic types like list, dict, tuple, Union, and Literal,
    converting them to human-readable format for documentation.

    Args:
        t: A type annotation object to format.

    Returns:
        A human-readable string representation of the type.

    """
    origin = get_origin(t)

    if origin is None:
        if hasattr(t, "__name__"):
            return t.__name__
        return str(t)

    if origin is Literal:
        return "str"

    args = ", ".join(format_type(arg) for arg in get_args(t))

    if origin is list:
        return f"list[{args}]"
    if origin is dict:
        return f"dict[{args}]"
    if origin is tuple:
        return f"tuple[{args}]"
    if origin in (Union, types.UnionType):
        return " | ".join(format_type(arg) for arg in get_args(t))

    return str(t)


def _field_to_parameter_details(f: Field) -> ParameterDetails:
    """Convert a dataclass field to a ParameterDetails object.

    Extracts name, type, description, default value, and required status
    from a dataclass field definition.

    Args:
        f: A dataclass Field object to convert.

    Returns:
        A ParameterDetails instance containing the field's documentation.

    """
    if f.default is not MISSING:
        default = f.default
    elif f.default_factory is not MISSING:
        default = f.default_factory
    else:
        default = None

    field_type = format_type(f.type)
    if field_type.startswith("str") and default is not None:
        default = '"' + default + '"'

    field_type = field_type.replace(" | NoneType", "")

    return ParameterDetails(
        f.name, field_type, f.metadata.get("doc", ""), default, f.default is MISSING and f.default_factory is MISSING
    )


def get_dataclass_docs(config: Any, main_config: bool = False) -> list[ParameterDetails]:  # noqa: ANN401
    """Retrieve parameter documentation from a component config dataclass.

    Extracts documentation for all fields defined in the dataclass,
    optionally including a top-level 'config' parameter entry.

    Args:
        config: A dataclass type to extract documentation from.
        main_config: If True, prepends a 'config' parameter entry that
            references the dataclass itself.

    Returns:
        A list of ParameterDetails for each field in the dataclass.

    """
    result = []
    if main_config:
        result.append(ParameterDetails("config", config.__name__, _("Dataclass for component configuration."), "None"))

    result.extend(_field_to_parameter_details(f) for f in fields(config))

    return result


def _get_nested_dataclass_type(field_type: Any) -> type | None:  # noqa: ANN401, C901
    """Extract a dataclass type from a field type annotation.

    Handles complex type annotations including Optional, Union, and list types
    to find nested dataclass definitions that need documentation.

    Args:
        field_type: A type annotation that may contain a nested dataclass.

    Returns:
        The dataclass type if found, or None if the field type does not
        contain a dataclass.

    """
    # Check if the type itself is a dataclass
    if is_dataclass(field_type) and isinstance(field_type, type):
        return field_type

    origin = get_origin(field_type)

    # Handle Union types (e.g., ButtonConfig | None, Optional[ButtonConfig])
    if origin in (Union, types.UnionType):
        for arg in get_args(field_type):
            if arg is not type(None) and is_dataclass(arg) and isinstance(arg, type):
                return arg

    # Handle list types (e.g., list[NavbarLinkConfig])
    if origin is list:
        args = get_args(field_type)
        if args:
            inner_type = args[0]
            # Check if the inner type is directly a dataclass
            if is_dataclass(inner_type) and isinstance(inner_type, type):
                return inner_type
            # Also handle Union inside list (e.g., list[SomeConfig | None])
            inner_origin = get_origin(inner_type)
            if inner_origin in (Union, types.UnionType):
                for arg in get_args(inner_type):
                    if arg is not type(None) and is_dataclass(arg) and isinstance(arg, type):
                        return arg

    return None


def get_component_parameter_doc(config: Any, _main_config: bool = False) -> list[ParameterDoc]:  # noqa: ANN401
    """Generate ParameterDoc objects for a config dataclass and its nested dataclass fields.

    Recursively processes all nested dataclasses, including those inside lists.

    Args:
        config: The dataclass config to document.
        main_config: If True, includes the top-level 'config' parameter in the docs.

    Returns:
        A list of ParameterDoc objects for the main config and all nested dataclass fields.

    """
    docs = [
        ParameterDoc(
            ParameterDetails(
                "config",
                config.__name__ + _(" or as kwargs or as combination of both"),
                _("Dataclass for component configuration."),
                "None",
            ),
            get_dataclass_docs(config, False),
            getattr(config, "__example__", None),
        )
    ]

    # Track processed types to avoid duplicates
    processed_types: set[type] = {config}

    def process_dataclass(dc_type: type) -> None:
        """Recursively process a dataclass and its nested dataclass fields."""
        for f in fields(dc_type):
            nested_type = _get_nested_dataclass_type(f.type)
            if nested_type is not None and nested_type not in processed_types:
                processed_types.add(nested_type)
                docs.append(
                    ParameterDoc(
                        _field_to_parameter_details(f),
                        get_dataclass_docs(nested_type),
                        getattr(nested_type, "__example__", None),
                    )
                )
                # Recursively process nested dataclass
                process_dataclass(nested_type)

    process_dataclass(config)

    return docs


def register_component(component: Component) -> Callable[[ContextBuilder], ContextBuilder]:
    """Register a context builder function for a component.

    Use as a decorator to register functions that provide context data
    for component documentation pages. Multiple builders can be registered
    for the same component; their outputs are merged.

    Args:
        component: The Component enum member to register the builder for.

    Returns:
        A decorator that registers the function and returns it unchanged.

    """

    def decorator(func: ContextBuilder) -> ContextBuilder:
        COMPONENT_CONTEXT_BUILDERS[component.value].append(func)
        return func

    return decorator


def get_component_context(component: Component) -> dict:
    """Build the complete documentation context for a component.

    Aggregates context from all registered builders, adds related components,
    and includes parameter documentation from the component's config class.

    Args:
        component: The Component enum member to build context for.

    Returns:
        A dictionary containing all context data for rendering the
        component's documentation page.

    Raises:
        ValueError: If the component has no registered context builders.

    """
    if component.value not in COMPONENT_CONTEXT_BUILDERS:
        raise ValueError(  # noqa: TRY003
            f"Unknown component: {component.value} accessible components are {COMPONENT_CONTEXT_BUILDERS.keys()}."
        )

    context = {"component_name": component.value, "formatted_name": component.formatted_name}

    for builder in COMPONENT_CONTEXT_BUILDERS.get(component.value, []):
        part = builder()
        context.update(part)

    related_components = {"related_topics": get_related_components_context(component)}
    context.update(related_components)

    if component.config_class:
        params = {"params": get_component_parameter_doc(component.config_class, True)}
        context.update(params)

    return context


def register_demo_context(component: Component) -> Callable[[ContextBuilder], ContextBuilder]:
    """Register a demo context builder for a component.

    Use as a decorator to register the function that provides context data
    for rendering component demos. Only one demo builder can be registered
    per component.

    Args:
        component: The Component enum member to register the demo builder for.

    Returns:
        A decorator that registers the function and returns it unchanged.

    Raises:
        ValueError: If the component already has a registered demo context.

    """

    def decorator(func: ContextBuilder) -> ContextBuilder:
        key = component.value

        if key in DEMO_CONTEXT_BUILDERS:
            raise ValueError(f"Component '{key}' already has a registered demo context!")  # noqa: TRY003

        DEMO_CONTEXT_BUILDERS[key] = func
        return func

    return decorator


def get_demo_context(component: Component) -> dict | None:
    """Retrieve the demo context builder for a component.

    Args:
        component: The Component enum member to get the demo builder for.

    Returns:
        The registered demo context builder function, or None if no demo
        context has been registered for this component.

    """
    return DEMO_CONTEXT_BUILDERS.get(component.value)
