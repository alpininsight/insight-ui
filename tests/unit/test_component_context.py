"""Tests for parameter documentation tree building in component_context."""

from dataclasses import dataclass, field

from insight_ui.component_details.component_context import get_component_parameter_doc
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
