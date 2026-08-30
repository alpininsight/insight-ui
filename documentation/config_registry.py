"""Registry of all component config dataclasses for the config reference page."""

from dataclasses import is_dataclass
from functools import lru_cache

from insight_ui import configs

from documentation.component_details.component_context import get_dataclass_docs


@lru_cache(maxsize=1)
def get_config_classes() -> tuple[type, ...]:
    """Collect every config dataclass in insight_ui.configs, sorted alphabetically by name."""
    classes = (getattr(configs, name) for name in configs.__all__ if is_dataclass(getattr(configs, name)))
    return tuple(sorted(classes, key=lambda cls: cls.__name__))


def get_all_config_definitions() -> list[dict]:
    """Get flat parameter documentation for every config dataclass.

    Unlike get_component_parameter_doc(), this does not build a nested tree -
    every dataclass is documented as its own, self-contained entry with a
    stable anchor, since the config reference page lists each one as a
    separate top-level section instead of expanding nested ones inline.

    Returns:
        A list of dicts with name, anchor, params_table and example_data for
        every config dataclass, sorted alphabetically by name.

    """
    return [
        {
            "name": cls.__name__,
            "anchor": cls.__name__.lower(),
            "params_table": get_dataclass_docs(cls, False),
            "example_data": getattr(cls, "__example__", None),
        }
        for cls in get_config_classes()
    ]


@lru_cache(maxsize=1)
def get_config_class_names() -> frozenset[str]:
    """Get the names of all documented config dataclasses, for linking type strings to them.

    Returns:
        A frozenset of every config dataclass's `__name__`.

    """
    return frozenset(cls.__name__ for cls in get_config_classes())
