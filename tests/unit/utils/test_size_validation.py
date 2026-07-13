"""Tests for size and type validation utilities."""

import pytest
from insight_ui.configs import (
    BADGE_TYPE_VALUES,
    BUTTON_TYPE_VALUES,
    COLOR_TYPE_VALUES,
    SIZE_VALUES,
    STEP_STATUS_VALUES,
    BadgeConfig,
    ButtonConfig,
    CornerRibbonConfig,
    IconConfig,
    MinimalStepperConfig,
    validate_badge_type,
    validate_button_type,
    validate_color_type,
    validate_size,
    validate_step_status,
)

# =============================================================================
# Size Validation
# =============================================================================


# --- validate_size function ------------------------------------------------


def test_validate_size_accepts_valid_values() -> None:
    """Test that validate_size accepts all valid size values."""
    for size in SIZE_VALUES:
        validate_size(size)  # Should not raise


def test_validate_size_rejects_invalid_value() -> None:
    """Test that validate_size raises ValueError for invalid sizes."""
    with pytest.raises(ValueError, match="Invalid size 'xxl'"):
        validate_size("xxl")


def test_validate_size_error_message_lists_allowed_values() -> None:
    """Test that the error message includes all allowed values."""
    with pytest.raises(ValueError, match="'xs', 's', 'm', 'l', 'xl'"):
        validate_size("invalid")


def test_validate_size_custom_field_name() -> None:
    """Test that validate_size uses the custom field name in error messages."""
    with pytest.raises(ValueError, match="Invalid icon_size 'bad'"):
        validate_size("bad", field_name="icon_size")


# --- SIZE_VALUES constant --------------------------------------------------


def test_size_values_contains_expected_values() -> None:
    """Test that SIZE_VALUES contains all expected size values."""
    assert SIZE_VALUES == ("xs", "s", "m", "l", "xl")


def test_size_values_is_tuple() -> None:
    """Test that SIZE_VALUES is immutable (tuple)."""
    assert isinstance(SIZE_VALUES, tuple)


# --- Config size validation via __post_init__ ------------------------------


def test_icon_config_accepts_valid_size() -> None:
    """Test IconConfig accepts valid size values."""
    for size in SIZE_VALUES:
        config = IconConfig(name="test", size=size)
        assert config.size == size


def test_icon_config_rejects_invalid_size() -> None:
    """Test IconConfig raises ValueError for invalid size."""
    with pytest.raises(ValueError, match="Invalid size"):
        IconConfig(name="test", size="huge")


def test_button_config_accepts_valid_size() -> None:
    """Test ButtonConfig accepts valid size values."""
    for size in SIZE_VALUES:
        config = ButtonConfig(size=size)
        assert config.size == size


def test_button_config_rejects_invalid_size() -> None:
    """Test ButtonConfig raises ValueError for invalid size."""
    with pytest.raises(ValueError, match="Invalid size"):
        ButtonConfig(size="tiny")


def test_badge_config_accepts_valid_size() -> None:
    """Test BadgeConfig accepts valid size values."""
    for size in SIZE_VALUES:
        config = BadgeConfig(label="Test", size=size)
        assert config.size == size


def test_badge_config_rejects_invalid_size() -> None:
    """Test BadgeConfig raises ValueError for invalid size."""
    with pytest.raises(ValueError, match="Invalid size"):
        BadgeConfig(label="Test", size="xxxl")


def test_minimal_stepper_config_accepts_valid_icon_size() -> None:
    """Test MinimalStepperConfig accepts valid icon_size values."""
    for size in SIZE_VALUES:
        config = MinimalStepperConfig(icon_size=size)
        assert config.icon_size == size


def test_minimal_stepper_config_rejects_invalid_icon_size() -> None:
    """Test MinimalStepperConfig raises ValueError for invalid icon_size."""
    with pytest.raises(ValueError, match="Invalid icon_size"):
        MinimalStepperConfig(icon_size="medium")


# --- Default size values ---------------------------------------------------


def test_icon_config_default_size() -> None:
    """Test IconConfig has correct default size."""
    config = IconConfig(name="test")
    assert config.size == "m"


def test_button_config_default_size() -> None:
    """Test ButtonConfig has correct default size."""
    config = ButtonConfig()
    assert config.size == "m"


def test_badge_config_default_size() -> None:
    """Test BadgeConfig has correct default size."""
    config = BadgeConfig(label="Test")
    assert config.size == "m"


def test_minimal_stepper_config_default_icon_size() -> None:
    """Test MinimalStepperConfig has correct default icon_size."""
    config = MinimalStepperConfig()
    assert config.icon_size == "xs"


# =============================================================================
# Type Validation
# =============================================================================


# --- Type value constants --------------------------------------------------


def test_color_type_values_contains_expected_values() -> None:
    """Test that COLOR_TYPE_VALUES contains all expected color type values."""
    assert COLOR_TYPE_VALUES == (
        "primary",
        "secondary",
        "neutral",
        "info",
        "success",
        "warning",
        "danger",
    )


def test_badge_type_values_extends_color_types() -> None:
    """Test that BADGE_TYPE_VALUES includes all color types plus 'disabled'."""
    for color in COLOR_TYPE_VALUES:
        assert color in BADGE_TYPE_VALUES
    assert "disabled" in BADGE_TYPE_VALUES


def test_button_type_values_extends_color_types() -> None:
    """Test that BUTTON_TYPE_VALUES includes all color types plus 'disabled' and 'link'."""
    for color in COLOR_TYPE_VALUES:
        assert color in BUTTON_TYPE_VALUES
    assert "disabled" in BUTTON_TYPE_VALUES
    assert "link" in BUTTON_TYPE_VALUES


def test_type_values_are_tuples() -> None:
    """Test that all type value constants are immutable (tuples)."""
    assert isinstance(COLOR_TYPE_VALUES, tuple)
    assert isinstance(BADGE_TYPE_VALUES, tuple)
    assert isinstance(BUTTON_TYPE_VALUES, tuple)


# --- validate_color_type function ------------------------------------------


def test_validate_color_type_accepts_valid_values() -> None:
    """Test that validate_color_type accepts all valid color type values."""
    for color_type in COLOR_TYPE_VALUES:
        validate_color_type(color_type)  # Should not raise


def test_validate_color_type_rejects_invalid_value() -> None:
    """Test that validate_color_type raises ValueError for invalid types."""
    with pytest.raises(ValueError, match="Invalid type 'invalid'"):
        validate_color_type("invalid")


def test_validate_color_type_rejects_disabled() -> None:
    """Test that validate_color_type rejects 'disabled' (not a color)."""
    with pytest.raises(ValueError, match="Invalid type 'disabled'"):
        validate_color_type("disabled")


# --- validate_badge_type function ------------------------------------------


def test_validate_badge_type_accepts_valid_values() -> None:
    """Test that validate_badge_type accepts all valid badge type values."""
    for badge_type in BADGE_TYPE_VALUES:
        validate_badge_type(badge_type)  # Should not raise


def test_validate_badge_type_rejects_invalid_value() -> None:
    """Test that validate_badge_type raises ValueError for invalid types."""
    with pytest.raises(ValueError, match="Invalid type 'invalid'"):
        validate_badge_type("invalid")


def test_validate_badge_type_rejects_link() -> None:
    """Test that validate_badge_type rejects 'link' (button-only type)."""
    with pytest.raises(ValueError, match="Invalid type 'link'"):
        validate_badge_type("link")


# --- validate_button_type function -----------------------------------------


def test_validate_button_type_accepts_valid_values() -> None:
    """Test that validate_button_type accepts all valid button type values."""
    for button_type in BUTTON_TYPE_VALUES:
        validate_button_type(button_type)  # Should not raise


def test_validate_button_type_rejects_invalid_value() -> None:
    """Test that validate_button_type raises ValueError for invalid types."""
    with pytest.raises(ValueError, match="Invalid type 'invalid'"):
        validate_button_type("invalid")


# --- Config type validation via __post_init__ ------------------------------


def test_button_config_accepts_valid_type() -> None:
    """Test ButtonConfig accepts valid type values."""
    for button_type in BUTTON_TYPE_VALUES:
        config = ButtonConfig(type=button_type)
        assert config.type == button_type


def test_button_config_rejects_invalid_type() -> None:
    """Test ButtonConfig raises ValueError for invalid type."""
    with pytest.raises(ValueError, match="Invalid type"):
        ButtonConfig(type="invalid")


def test_badge_config_accepts_valid_type() -> None:
    """Test BadgeConfig accepts valid type values."""
    for badge_type in BADGE_TYPE_VALUES:
        config = BadgeConfig(label="Test", type=badge_type)
        assert config.type == badge_type


def test_badge_config_rejects_invalid_type() -> None:
    """Test BadgeConfig raises ValueError for invalid type."""
    with pytest.raises(ValueError, match="Invalid type"):
        BadgeConfig(label="Test", type="invalid")


def test_badge_config_rejects_link_type() -> None:
    """Test BadgeConfig raises ValueError for 'link' type (button-only)."""
    with pytest.raises(ValueError, match="Invalid type 'link'"):
        BadgeConfig(label="Test", type="link")


# --- Default type values ---------------------------------------------------


def test_button_config_default_type() -> None:
    """Test ButtonConfig has correct default type."""
    config = ButtonConfig()
    assert config.type == "primary"


def test_badge_config_default_type() -> None:
    """Test BadgeConfig has correct default type."""
    config = BadgeConfig(label="Test")
    assert config.type == "primary"


def test_corner_ribbon_config_default_color() -> None:
    """Test CornerRibbonConfig has correct default color."""
    config = CornerRibbonConfig(text="Test")
    assert config.color == "primary"


# --- CornerRibbonConfig color validation -----------------------------------


def test_corner_ribbon_config_accepts_valid_color() -> None:
    """Test CornerRibbonConfig accepts valid color values."""
    for color in COLOR_TYPE_VALUES:
        config = CornerRibbonConfig(text="Test", color=color)
        assert config.color == color


def test_corner_ribbon_config_rejects_invalid_color() -> None:
    """Test CornerRibbonConfig raises ValueError for invalid color."""
    with pytest.raises(ValueError, match="Invalid color"):
        CornerRibbonConfig(text="Test", color="invalid")


def test_corner_ribbon_config_rejects_disabled_color() -> None:
    """Test CornerRibbonConfig rejects 'disabled' (not a color)."""
    with pytest.raises(ValueError, match="Invalid color 'disabled'"):
        CornerRibbonConfig(text="Test", color="disabled")


# =============================================================================
# Step Status Validation
# =============================================================================


# --- STEP_STATUS_VALUES constant -------------------------------------------


def test_step_status_values_contains_expected_values() -> None:
    """Test that STEP_STATUS_VALUES contains all expected values."""
    assert STEP_STATUS_VALUES == ("active", "success", "failed", "")


def test_step_status_values_is_tuple() -> None:
    """Test that STEP_STATUS_VALUES is immutable (tuple)."""
    assert isinstance(STEP_STATUS_VALUES, tuple)


# --- validate_step_status function -----------------------------------------


def test_validate_step_status_accepts_valid_values() -> None:
    """Test that validate_step_status accepts all valid step status values."""
    for status in STEP_STATUS_VALUES:
        validate_step_status(status)  # Should not raise


def test_validate_step_status_rejects_invalid_value() -> None:
    """Test that validate_step_status raises ValueError for invalid status."""
    with pytest.raises(ValueError, match="Invalid status 'invalid'"):
        validate_step_status("invalid")


def test_validate_step_status_custom_field_name() -> None:
    """Test that validate_step_status uses the custom field name in error messages."""
    with pytest.raises(ValueError, match="Invalid current_step_status 'bad'"):
        validate_step_status("bad", field_name="current_step_status")


# --- MinimalStepperConfig step status validation ---------------------------


def test_minimal_stepper_config_accepts_valid_current_step_status() -> None:
    """Test MinimalStepperConfig accepts valid current_step_status values."""
    for status in ("active", "success", "failed", ""):
        config = MinimalStepperConfig(current_step_status=status)
        assert config.current_step_status == status


def test_minimal_stepper_config_rejects_invalid_current_step_status() -> None:
    """Test MinimalStepperConfig raises ValueError for invalid current_step_status."""
    with pytest.raises(ValueError, match="Invalid current_step_status"):
        MinimalStepperConfig(current_step_status="pending")


def test_minimal_stepper_config_accepts_valid_items() -> None:
    """Test MinimalStepperConfig accepts valid items list."""
    items = ["success", "success", "active", "", ""]
    config = MinimalStepperConfig(items=items)
    assert config.items == items


def test_minimal_stepper_config_rejects_invalid_items() -> None:
    """Test MinimalStepperConfig raises ValueError for invalid items."""
    with pytest.raises(ValueError, match=r"Invalid items\[2\]"):
        MinimalStepperConfig(items=["success", "active", "invalid", ""])


def test_minimal_stepper_config_default_current_step_status() -> None:
    """Test MinimalStepperConfig has correct default current_step_status."""
    config = MinimalStepperConfig()
    assert config.current_step_status == "active"
