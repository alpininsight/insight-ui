"""Tests for parameter documentation tree building in component_context."""

from dataclasses import dataclass, field

from django.utils import translation
from documentation.component_details.component_context import get_component_parameter_doc, resolve_parameter_path
from insight_ui.configs.navigation import NavbarConfig


@dataclass
class _LeafConfig:
    """Leaf.

    Attributes:
        label: Leaf label.

    """

    label: str = field(default="", metadata={"doc": "Leaf label."})


@dataclass
class _BranchConfig:
    """Branch.

    Attributes:
        title: Branch title.
        leaf: Nested leaf config.
        leaves: List of nested leaf configs.

    """

    title: str = field(default="", metadata={"doc": "Branch title."})
    leaf: _LeafConfig | None = field(default=None, metadata={"doc": "Nested leaf config."})
    leaves: list[_LeafConfig] = field(default_factory=list, metadata={"doc": "List of nested leaf configs."})


def test_nested_dataclass_is_attached_to_its_row() -> None:
    """A field referencing a dataclass carries the nested doc on its own row, not as a sibling entry."""
    docs = get_component_parameter_doc(_BranchConfig, True)

    assert len(docs) == 1
    rows_by_name = {row.name: row for row in docs[0].params_table}

    assert rows_by_name["title"].nested is None
    assert rows_by_name["leaf"].nested is not None
    assert [r.name for r in rows_by_name["leaf"].nested.params_table] == ["label"]


def test_list_of_dataclass_is_attached_to_its_row() -> None:
    """A field referencing list[Dataclass] also carries the nested doc on its own row."""

    @dataclass
    class _ListOnlyConfig:
        """List only.

        Attributes:
            leaves: List of nested leaf configs.

        """

        leaves: list[_LeafConfig] = field(default_factory=list, metadata={"doc": "List of nested leaf configs."})

    docs = get_component_parameter_doc(_ListOnlyConfig, True)
    rows_by_name = {row.name: row for row in docs[0].params_table}

    assert rows_by_name["leaves"].nested is not None
    assert [r.name for r in rows_by_name["leaves"].nested.params_table] == ["label"]


def test_repeated_type_is_only_attached_once() -> None:
    """The same nested dataclass referenced from two rows is only expanded on its first occurrence."""

    @dataclass
    class _TwiceConfig:
        """Twice.

        Attributes:
            first: First leaf.
            second: Second leaf.

        """

        first: _LeafConfig | None = field(default=None, metadata={"doc": "First leaf."})
        second: _LeafConfig | None = field(default=None, metadata={"doc": "Second leaf."})

    docs = get_component_parameter_doc(_TwiceConfig, True)
    rows_by_name = {row.name: row for row in docs[0].params_table}

    assert rows_by_name["first"].nested is not None
    assert rows_by_name["second"].nested is None


def test_navbar_config_produces_a_deep_nested_tree() -> None:
    """Real-world regression check: NavbarConfig nests brand/links without errors or infinite recursion."""
    docs = get_component_parameter_doc(NavbarConfig, True)

    assert len(docs) == 1
    rows_by_name = {row.name: row for row in docs[0].params_table}

    assert rows_by_name["brand"].nested is not None
    assert rows_by_name["links"].nested is not None


def test_resolve_parameter_path_empty_string_resolves_to_root() -> None:
    """An empty path resolves to the root doc with only the 'Overview' breadcrumb."""
    with translation.override("en"):
        root = get_component_parameter_doc(_BranchConfig, True)[0]

        result = resolve_parameter_path(root, "", "/docs/components/branch/")

        assert result["active_param"] is root
        assert [c.text for c in result["param_breadcrumb_items"]] == ["Overview"]
        assert result["active_param_name"] is None


def test_resolve_parameter_path_walks_into_nested_doc() -> None:
    """A valid single-segment path resolves to the referenced nested doc and extends the breadcrumb."""
    with translation.override("en"):
        root = get_component_parameter_doc(_BranchConfig, True)[0]
        leaf_doc = next(r for r in root.params_table if r.name == "leaf").nested

        result = resolve_parameter_path(root, "leaf", "/docs/components/branch/")

        assert result["active_param"] is leaf_doc
        assert [c.text for c in result["param_breadcrumb_items"]] == ["Overview", "leaf"]
        assert result["active_param_name"] == "leaf"


def test_resolve_parameter_path_invalid_segment_stops_at_last_valid_step() -> None:
    """An unknown field name in the path is ignored, falling back to the deepest still-valid doc."""
    with translation.override("en"):
        root = get_component_parameter_doc(_BranchConfig, True)[0]

        result = resolve_parameter_path(root, "leaf.does_not_exist", "/docs/components/branch/")

        leaf_doc = next(r for r in root.params_table if r.name == "leaf").nested
        assert result["active_param"] is leaf_doc
        assert [c.text for c in result["param_breadcrumb_items"]] == ["Overview", "leaf"]


def test_resolve_parameter_path_non_nested_field_stops_immediately() -> None:
    """Pointing the path at a plain (non-nested) field falls back to the root."""
    with translation.override("en"):
        root = get_component_parameter_doc(_BranchConfig, True)[0]

        result = resolve_parameter_path(root, "title", "/docs/components/branch/")

        assert result["active_param"] is root
        assert [c.text for c in result["param_breadcrumb_items"]] == ["Overview"]
