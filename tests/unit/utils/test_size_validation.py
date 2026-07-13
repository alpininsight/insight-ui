"""Tests for size validation utilities."""

import pytest
from insight_ui.configs import SIZE_VALUES, BadgeConfig, ButtonConfig, IconConfig, MinimalStepperConfig, validate_size

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


# --- Config validation via __post_init__ -----------------------------------


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


# --- Default values --------------------------------------------------------


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
