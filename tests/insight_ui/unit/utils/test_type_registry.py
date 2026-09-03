"""Tests for the type registry module."""

import pytest
from documentation.type_registry import TYPE_DEFINITIONS, get_all_type_definitions, get_type_info, is_known_type

# =============================================================================
# get_type_info function
# =============================================================================


def test_get_type_info_returns_info_for_known_type() -> None:
    """Test that get_type_info returns type info for a known type."""
    result = get_type_info("Size")
    assert result is not None
    assert result["name"] == "Size"
    assert result["anchor"] == "size"
    assert "values" in result
    assert "description" in result


def test_get_type_info_returns_none_for_unknown_type() -> None:
    """Test that get_type_info returns None for unknown types."""
    result = get_type_info("UnknownType")
    assert result is None


def test_get_type_info_case_insensitive() -> None:
    """Test that get_type_info matches case-insensitively."""
    result_lower = get_type_info("size")
    result_upper = get_type_info("SIZE")
    result_mixed = get_type_info("sIzE")

    assert result_lower is not None
    assert result_upper is not None
    assert result_mixed is not None
    assert result_lower["name"] == "Size"
    assert result_upper["name"] == "Size"
    assert result_mixed["name"] == "Size"


def test_get_type_info_exact_match_preferred() -> None:
    """Test that exact case match is preferred over case-insensitive."""
    result = get_type_info("Size")
    assert result["name"] == "Size"


def test_get_type_info_includes_all_expected_fields() -> None:
    """Test that type info includes all expected fields."""
    result = get_type_info("ColorType")
    assert result is not None
    assert "name" in result
    assert "anchor" in result
    assert "values" in result
    assert "description" in result


# =============================================================================
# is_known_type function
# =============================================================================


def test_is_known_type_returns_true_for_known_types() -> None:
    """Test that is_known_type returns True for known types."""
    assert is_known_type("Size") is True
    assert is_known_type("ColorType") is True
    assert is_known_type("ButtonType") is True
    assert is_known_type("AlertType") is True


def test_is_known_type_returns_false_for_unknown_types() -> None:
    """Test that is_known_type returns False for unknown types."""
    assert is_known_type("UnknownType") is False
    assert is_known_type("str") is False
    assert is_known_type("int") is False
    assert is_known_type("bool") is False


def test_is_known_type_case_insensitive() -> None:
    """Test that is_known_type matches case-insensitively."""
    assert is_known_type("size") is True
    assert is_known_type("SIZE") is True
    assert is_known_type("colortype") is True


# =============================================================================
# get_all_type_definitions function
# =============================================================================


def test_get_all_type_definitions_returns_list() -> None:
    """Test that get_all_type_definitions returns a list."""
    result = get_all_type_definitions()
    assert isinstance(result, list)


def test_get_all_type_definitions_includes_all_types() -> None:
    """Test that get_all_type_definitions includes all registered types."""
    result = get_all_type_definitions()
    assert len(result) == len(TYPE_DEFINITIONS)


def test_get_all_type_definitions_item_structure() -> None:
    """Test that each item in get_all_type_definitions has expected fields."""
    result = get_all_type_definitions()
    for item in result:
        assert "name" in item
        assert "anchor" in item
        assert "values" in item
        assert "description" in item


def test_get_all_type_definitions_names_match_keys() -> None:
    """Test that item names match the TYPE_DEFINITIONS keys."""
    result = get_all_type_definitions()
    names = {item["name"] for item in result}
    assert names == set(TYPE_DEFINITIONS.keys())


# =============================================================================
# TYPE_DEFINITIONS structure
# =============================================================================


def test_type_definitions_contains_expected_types() -> None:
    """Test that TYPE_DEFINITIONS contains expected type names."""
    expected_types = [
        "AlertType",
        "BadgeType",
        "ButtonType",
        "ColorType",
        "CornerPosition",
        "FilterFieldType",
        "FormFieldType",
        "GeoMapMarkerType",
        "HtmlButtonType",
        "HtmlInputType",
        "HttpMethod",
        "HtmxSwapMethod",
        "IconColor",
        "InlinePosition",
        "Size",
        "SliderLegendMode",
        "StepStatus",
        "ToggleViewType",
    ]
    for type_name in expected_types:
        assert type_name in TYPE_DEFINITIONS, f"Missing type: {type_name}"


def test_type_definitions_all_have_required_fields() -> None:
    """Test that all type definitions have required fields."""
    required_fields = {"anchor", "values", "description"}
    for type_name, definition in TYPE_DEFINITIONS.items():
        for field in required_fields:
            assert field in definition, f"Type {type_name} missing field: {field}"


def test_type_definitions_anchors_are_lowercase() -> None:
    """Test that all anchors are lowercase for URL consistency."""
    for type_name, definition in TYPE_DEFINITIONS.items():
        anchor = definition["anchor"]
        assert anchor == anchor.lower(), f"Type {type_name} has non-lowercase anchor: {anchor}"


def test_type_definitions_values_are_tuples() -> None:
    """Test that all values are tuples (immutable)."""
    for type_name, definition in TYPE_DEFINITIONS.items():
        values = definition["values"]
        assert isinstance(values, tuple), f"Type {type_name} values should be tuple"


@pytest.mark.parametrize(
    "type_name",
    list(TYPE_DEFINITIONS.keys()),
)
def test_type_definitions_values_not_empty(type_name: str) -> None:
    """Test that each type has at least one value."""
    values = TYPE_DEFINITIONS[type_name]["values"]
    assert len(values) > 0, f"Type {type_name} has no values"
