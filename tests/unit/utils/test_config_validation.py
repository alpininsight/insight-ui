"""Tests for config validation utilities."""

import pytest
from insight_ui.configs import (
    ALERT_TYPE_VALUES,
    BADGE_TYPE_VALUES,
    BUTTON_TYPE_VALUES,
    COLOR_TYPE_VALUES,
    CORNER_POSITION_VALUES,
    FILTER_FIELD_TYPE_VALUES,
    FORM_FIELD_TYPE_VALUES,
    GEO_MAP_MARKER_TYPE_VALUES,
    HTML_BUTTON_TYPE_VALUES,
    HTML_INPUT_TYPE_VALUES,
    HTMX_METHOD_VALUES,
    HTMX_SWAP_METHOD_VALUES,
    ICON_COLOR_VALUES,
    INLINE_POSITION_VALUES,
    SIZE_VALUES,
    SLIDER_LEGEND_MODE_VALUES,
    STEP_STATUS_VALUES,
    TOGGLE_VIEW_TYPE_VALUES,
    AlertConfig,
    BadgeConfig,
    BrandMarkConfig,
    ButtonConfig,
    CornerRibbonConfig,
    FormFieldConfig,
    GeoMapDatasetConfig,
    HtmxConfig,
    IconConfig,
    InfoboxConfig,
    InputFieldConfig,
    MinimalStepperConfig,
    QueryBuilderFieldConfig,
    RadioBlockConfig,
    SliderConfig,
    StatusScreenConfig,
    ToggleViewConfig,
    validate_alert_type,
    validate_badge_type,
    validate_button_type,
    validate_color_type,
    validate_corner_position,
    validate_filter_field_type,
    validate_form_field_type,
    validate_geo_map_marker_type,
    validate_html_button_type,
    validate_html_input_type,
    validate_htmx_method,
    validate_htmx_swap_method,
    validate_icon_color,
    validate_inline_position,
    validate_size,
    validate_slider_legend_mode,
    validate_step_status,
    validate_toggle_view_type,
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
        config = ButtonConfig(label="Test", size=size)
        assert config.size == size


def test_button_config_rejects_invalid_size() -> None:
    """Test ButtonConfig raises ValueError for invalid size."""
    with pytest.raises(ValueError, match="Invalid size"):
        ButtonConfig(label="Test", size="tiny")


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
    config = ButtonConfig(label="Test")
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
# Icon Color Validation
# =============================================================================


# --- ICON_COLOR_VALUES constant ----------------------------------------------


def test_icon_color_values_contains_expected_values() -> None:
    """Test that ICON_COLOR_VALUES contains all expected color values."""
    expected = (
        "",
        "primary",
        "secondary",
        "success",
        "warning",
        "danger",
        "info",
        "text-primary",
        "text-secondary",
        "text-hint",
        "text-link",
    )
    assert expected == ICON_COLOR_VALUES


def test_icon_color_values_is_tuple() -> None:
    """Test that ICON_COLOR_VALUES is immutable (tuple)."""
    assert isinstance(ICON_COLOR_VALUES, tuple)


def test_icon_color_values_includes_empty_string() -> None:
    """Test that ICON_COLOR_VALUES includes empty string for inheritance."""
    assert "" in ICON_COLOR_VALUES


# --- validate_icon_color function --------------------------------------------


def test_validate_icon_color_accepts_valid_values() -> None:
    """Test that validate_icon_color accepts all valid icon color values."""
    for color in ICON_COLOR_VALUES:
        validate_icon_color(color)  # Should not raise


def test_validate_icon_color_rejects_invalid_value() -> None:
    """Test that validate_icon_color raises ValueError for invalid colors."""
    with pytest.raises(ValueError, match="Invalid color 'invalid'"):
        validate_icon_color("invalid")


def test_validate_icon_color_rejects_hex_code() -> None:
    """Test that validate_icon_color rejects hex color codes."""
    with pytest.raises(ValueError, match="Invalid color '#FF0000'"):
        validate_icon_color("#FF0000")


def test_validate_icon_color_custom_field_name() -> None:
    """Test that validate_icon_color uses the custom field name in error messages."""
    with pytest.raises(ValueError, match="Invalid icon_color 'bad'"):
        validate_icon_color("bad", field_name="icon_color")


# --- IconConfig color validation ---------------------------------------------


def test_icon_config_accepts_valid_color() -> None:
    """Test IconConfig accepts valid color values."""
    for color in ICON_COLOR_VALUES:
        config = IconConfig(name="test", color=color)
        assert config.color == color


def test_icon_config_rejects_invalid_color() -> None:
    """Test IconConfig raises ValueError for invalid color."""
    with pytest.raises(ValueError, match="Invalid color"):
        IconConfig(name="test", color="invalid")


def test_icon_config_rejects_hex_color() -> None:
    """Test IconConfig rejects hex color codes (use tokens instead)."""
    with pytest.raises(ValueError, match="Invalid color"):
        IconConfig(name="test", color="#4183EA")


def test_icon_config_default_color() -> None:
    """Test IconConfig has correct default color (empty = inherit)."""
    config = IconConfig(name="test")
    assert config.color == ""


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
    """Test that BUTTON_TYPE_VALUES includes all color types plus 'link'."""
    for color in COLOR_TYPE_VALUES:
        assert color in BUTTON_TYPE_VALUES
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
        config = ButtonConfig(label="Test", type=button_type)
        assert config.type == button_type


def test_button_config_rejects_invalid_type() -> None:
    """Test ButtonConfig raises ValueError for invalid type."""
    with pytest.raises(ValueError, match="Invalid type"):
        ButtonConfig(label="Test", type="invalid")


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
    config = ButtonConfig(label="Test")
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


# =============================================================================
# Alert Type Validation
# =============================================================================


# --- ALERT_TYPE_VALUES constant ---------------------------------------------


def test_alert_type_values_contains_expected_values() -> None:
    """Test that ALERT_TYPE_VALUES contains all expected values."""
    assert ALERT_TYPE_VALUES == ("info", "success", "warning", "error")


def test_alert_type_values_is_tuple() -> None:
    """Test that ALERT_TYPE_VALUES is immutable (tuple)."""
    assert isinstance(ALERT_TYPE_VALUES, tuple)


def test_alert_type_values_uses_error_not_danger() -> None:
    """Test that ALERT_TYPE_VALUES uses 'error' (semantic) not 'danger' (color token)."""
    assert "error" in ALERT_TYPE_VALUES
    assert "danger" not in ALERT_TYPE_VALUES


# --- validate_alert_type function -------------------------------------------


def test_validate_alert_type_accepts_valid_values() -> None:
    """Test that validate_alert_type accepts all valid alert type values."""
    for alert_type in ALERT_TYPE_VALUES:
        validate_alert_type(alert_type)  # Should not raise


def test_validate_alert_type_rejects_invalid_value() -> None:
    """Test that validate_alert_type raises ValueError for invalid types."""
    with pytest.raises(ValueError, match="Invalid type 'invalid'"):
        validate_alert_type("invalid")


def test_validate_alert_type_rejects_danger() -> None:
    """Test that validate_alert_type rejects 'danger' (use 'error' instead)."""
    with pytest.raises(ValueError, match="Invalid type 'danger'"):
        validate_alert_type("danger")


def test_validate_alert_type_custom_field_name() -> None:
    """Test that validate_alert_type uses the custom field name in error messages."""
    with pytest.raises(ValueError, match="Invalid status 'bad'"):
        validate_alert_type("bad", field_name="status")


# --- AlertConfig type validation --------------------------------------------


def test_alert_config_accepts_valid_type() -> None:
    """Test AlertConfig accepts valid type values."""
    for alert_type in ALERT_TYPE_VALUES:
        config = AlertConfig(type=alert_type)
        assert config.type == alert_type


def test_alert_config_rejects_invalid_type() -> None:
    """Test AlertConfig raises ValueError for invalid type."""
    with pytest.raises(ValueError, match="Invalid type"):
        AlertConfig(type="invalid")


def test_alert_config_rejects_danger_type() -> None:
    """Test AlertConfig rejects 'danger' type (use 'error' instead)."""
    with pytest.raises(ValueError, match="Invalid type 'danger'"):
        AlertConfig(type="danger")


def test_alert_config_default_type() -> None:
    """Test AlertConfig has correct default type."""
    config = AlertConfig()
    assert config.type == "info"


# --- InfoboxConfig info_type validation -------------------------------------


def test_infobox_config_accepts_valid_info_type() -> None:
    """Test InfoboxConfig accepts valid info_type values."""
    for alert_type in ALERT_TYPE_VALUES:
        config = InfoboxConfig(message="Test", info_type=alert_type)
        assert config.info_type == alert_type


def test_infobox_config_rejects_invalid_info_type() -> None:
    """Test InfoboxConfig raises ValueError for invalid info_type."""
    with pytest.raises(ValueError, match="Invalid info_type"):
        InfoboxConfig(message="Test", info_type="invalid")


def test_infobox_config_default_info_type() -> None:
    """Test InfoboxConfig has correct default info_type."""
    config = InfoboxConfig(message="Test")
    assert config.info_type == "info"


# --- StatusScreenConfig status validation -----------------------------------


def test_status_screen_config_accepts_valid_status() -> None:
    """Test StatusScreenConfig accepts valid status values."""
    for alert_type in ALERT_TYPE_VALUES:
        config = StatusScreenConfig(title="Test", status=alert_type)
        assert config.status == alert_type


def test_status_screen_config_rejects_invalid_status() -> None:
    """Test StatusScreenConfig raises ValueError for invalid status."""
    with pytest.raises(ValueError, match="Invalid status"):
        StatusScreenConfig(title="Test", status="invalid")


def test_status_screen_config_rejects_danger_status() -> None:
    """Test StatusScreenConfig rejects 'danger' status (use 'error' instead)."""
    with pytest.raises(ValueError, match="Invalid status 'danger'"):
        StatusScreenConfig(title="Test", status="danger")


def test_status_screen_config_default_status() -> None:
    """Test StatusScreenConfig has correct default status."""
    config = StatusScreenConfig(title="Test")
    assert config.status == "info"


# =============================================================================
# HTML Button Type Validation
# =============================================================================


# --- HTML_BUTTON_TYPE_VALUES constant ---------------------------------------


def test_html_button_type_values_contains_expected_values() -> None:
    """Test that HTML_BUTTON_TYPE_VALUES contains all expected values."""
    assert HTML_BUTTON_TYPE_VALUES == ("button", "submit", "reset")


def test_html_button_type_values_is_tuple() -> None:
    """Test that HTML_BUTTON_TYPE_VALUES is immutable (tuple)."""
    assert isinstance(HTML_BUTTON_TYPE_VALUES, tuple)


# --- validate_html_button_type function -------------------------------------


def test_validate_html_button_type_accepts_valid_values() -> None:
    """Test that validate_html_button_type accepts all valid values."""
    for button_type in HTML_BUTTON_TYPE_VALUES:
        validate_html_button_type(button_type)  # Should not raise


def test_validate_html_button_type_rejects_invalid_value() -> None:
    """Test that validate_html_button_type raises ValueError for invalid types."""
    with pytest.raises(ValueError, match="Invalid button_type 'invalid'"):
        validate_html_button_type("invalid")


def test_validate_html_button_type_custom_field_name() -> None:
    """Test that validate_html_button_type uses the custom field name in error messages."""
    with pytest.raises(ValueError, match="Invalid html_type 'bad'"):
        validate_html_button_type("bad", field_name="html_type")


# --- ButtonConfig button_type validation ------------------------------------


def test_button_config_accepts_valid_button_type() -> None:
    """Test ButtonConfig accepts valid button_type values."""
    for button_type in HTML_BUTTON_TYPE_VALUES:
        config = ButtonConfig(label="Test", button_type=button_type)
        assert config.button_type == button_type


def test_button_config_rejects_invalid_button_type() -> None:
    """Test ButtonConfig raises ValueError for invalid button_type."""
    with pytest.raises(ValueError, match="Invalid button_type"):
        ButtonConfig(label="Test", button_type="invalid")


def test_button_config_default_button_type() -> None:
    """Test ButtonConfig has correct default button_type."""
    config = ButtonConfig(label="Test")
    assert config.button_type == "button"


# =============================================================================
# Corner Position Validation
# =============================================================================


# --- CORNER_POSITION_VALUES constant ----------------------------------------


def test_corner_position_values_contains_expected_values() -> None:
    """Test that CORNER_POSITION_VALUES contains all expected values."""
    assert CORNER_POSITION_VALUES == ("top-right", "top-left", "bottom-right", "bottom-left")


def test_corner_position_values_is_tuple() -> None:
    """Test that CORNER_POSITION_VALUES is immutable (tuple)."""
    assert isinstance(CORNER_POSITION_VALUES, tuple)


# --- validate_corner_position function --------------------------------------


def test_validate_corner_position_accepts_valid_values() -> None:
    """Test that validate_corner_position accepts all valid values."""
    for position in CORNER_POSITION_VALUES:
        validate_corner_position(position)  # Should not raise


def test_validate_corner_position_rejects_invalid_value() -> None:
    """Test that validate_corner_position raises ValueError for invalid values."""
    with pytest.raises(ValueError, match="Invalid position 'center'"):
        validate_corner_position("center")


def test_validate_corner_position_custom_field_name() -> None:
    """Test that validate_corner_position uses the custom field name in error messages."""
    with pytest.raises(ValueError, match="Invalid ribbon_position 'bad'"):
        validate_corner_position("bad", field_name="ribbon_position")


# --- CornerRibbonConfig position validation ---------------------------------


def test_corner_ribbon_config_accepts_valid_position() -> None:
    """Test CornerRibbonConfig accepts valid position values."""
    for position in CORNER_POSITION_VALUES:
        config = CornerRibbonConfig(text="Test", position=position)
        assert config.position == position


def test_corner_ribbon_config_rejects_invalid_position() -> None:
    """Test CornerRibbonConfig raises ValueError for invalid position."""
    with pytest.raises(ValueError, match="Invalid position"):
        CornerRibbonConfig(text="Test", position="center")


def test_corner_ribbon_config_default_position() -> None:
    """Test CornerRibbonConfig has correct default position."""
    config = CornerRibbonConfig(text="Test")
    assert config.position == "top-right"


# =============================================================================
# Inline Position Validation
# =============================================================================


# --- INLINE_POSITION_VALUES constant ----------------------------------------


def test_inline_position_values_contains_expected_values() -> None:
    """Test that INLINE_POSITION_VALUES contains all expected values."""
    assert INLINE_POSITION_VALUES == ("start", "end")


def test_inline_position_values_is_tuple() -> None:
    """Test that INLINE_POSITION_VALUES is immutable (tuple)."""
    assert isinstance(INLINE_POSITION_VALUES, tuple)


# --- validate_inline_position function --------------------------------------


def test_validate_inline_position_accepts_valid_values() -> None:
    """Test that validate_inline_position accepts all valid values."""
    for position in INLINE_POSITION_VALUES:
        validate_inline_position(position)  # Should not raise


def test_validate_inline_position_rejects_invalid_value() -> None:
    """Test that validate_inline_position raises ValueError for invalid values."""
    with pytest.raises(ValueError, match="Invalid position 'middle'"):
        validate_inline_position("middle")


def test_validate_inline_position_custom_field_name() -> None:
    """Test that validate_inline_position uses the custom field name in error messages."""
    with pytest.raises(ValueError, match="Invalid logo_position 'bad'"):
        validate_inline_position("bad", field_name="logo_position")


# --- BrandMarkConfig logo_position validation -------------------------------


def test_brand_mark_config_accepts_valid_logo_position() -> None:
    """Test BrandMarkConfig accepts valid logo_position values."""
    for position in INLINE_POSITION_VALUES:
        config = BrandMarkConfig(logo_position=position)
        assert config.logo_position == position


def test_brand_mark_config_rejects_invalid_logo_position() -> None:
    """Test BrandMarkConfig raises ValueError for invalid logo_position."""
    with pytest.raises(ValueError, match="Invalid logo_position"):
        BrandMarkConfig(logo_position="middle")


def test_brand_mark_config_default_logo_position() -> None:
    """Test BrandMarkConfig has correct default logo_position."""
    config = BrandMarkConfig()
    assert config.logo_position == "start"


# =============================================================================
# Filter Field Type Validation
# =============================================================================


# --- FILTER_FIELD_TYPE_VALUES constant --------------------------------------


def test_filter_field_type_values_contains_expected_values() -> None:
    """Test that FILTER_FIELD_TYPE_VALUES contains all expected values."""
    assert FILTER_FIELD_TYPE_VALUES == ("text", "number", "date", "datetime", "time", "boolean", "choice")


def test_filter_field_type_values_is_tuple() -> None:
    """Test that FILTER_FIELD_TYPE_VALUES is immutable (tuple)."""
    assert isinstance(FILTER_FIELD_TYPE_VALUES, tuple)


# --- validate_filter_field_type function ------------------------------------


def test_validate_filter_field_type_accepts_valid_values() -> None:
    """Test that validate_filter_field_type accepts all valid values."""
    for field_type in FILTER_FIELD_TYPE_VALUES:
        validate_filter_field_type(field_type)  # Should not raise


def test_validate_filter_field_type_rejects_invalid_value() -> None:
    """Test that validate_filter_field_type raises ValueError for invalid values."""
    with pytest.raises(ValueError, match="Invalid type 'invalid'"):
        validate_filter_field_type("invalid")


def test_validate_filter_field_type_custom_field_name() -> None:
    """Test that validate_filter_field_type uses the custom field name in error messages."""
    with pytest.raises(ValueError, match="Invalid field_type 'bad'"):
        validate_filter_field_type("bad", field_name="field_type")


# --- QueryBuilderFieldConfig type validation --------------------------------


def test_query_builder_field_config_accepts_valid_type() -> None:
    """Test QueryBuilderFieldConfig accepts valid type values."""
    for field_type in FILTER_FIELD_TYPE_VALUES:
        config = QueryBuilderFieldConfig(field="test", label="Test", type=field_type)
        assert config.type == field_type


def test_query_builder_field_config_rejects_invalid_type() -> None:
    """Test QueryBuilderFieldConfig raises ValueError for invalid type."""
    with pytest.raises(ValueError, match="Invalid type"):
        QueryBuilderFieldConfig(field="test", label="Test", type="invalid")


def test_query_builder_field_config_default_type() -> None:
    """Test QueryBuilderFieldConfig has correct default type."""
    config = QueryBuilderFieldConfig(field="test", label="Test")
    assert config.type == "text"


# =============================================================================
# HTML Input Type Validation
# =============================================================================


# --- HTML_INPUT_TYPE_VALUES constant ----------------------------------------


def test_html_input_type_values_contains_expected_values() -> None:
    """Test that HTML_INPUT_TYPE_VALUES contains all expected values."""
    expected = (
        "text",
        "password",
        "email",
        "number",
        "tel",
        "url",
        "date",
        "time",
        "datetime-local",
        "month",
        "week",
        "color",
        "file",
        "hidden",
        "checkbox",
        "radio",
    )
    assert expected == HTML_INPUT_TYPE_VALUES


def test_html_input_type_values_is_tuple() -> None:
    """Test that HTML_INPUT_TYPE_VALUES is immutable (tuple)."""
    assert isinstance(HTML_INPUT_TYPE_VALUES, tuple)


# --- validate_html_input_type function --------------------------------------


def test_validate_html_input_type_accepts_valid_values() -> None:
    """Test that validate_html_input_type accepts all valid values."""
    for input_type in HTML_INPUT_TYPE_VALUES:
        validate_html_input_type(input_type)  # Should not raise


def test_validate_html_input_type_rejects_invalid_value() -> None:
    """Test that validate_html_input_type raises ValueError for invalid values."""
    with pytest.raises(ValueError, match="Invalid input_type 'invalid'"):
        validate_html_input_type("invalid")


def test_validate_html_input_type_custom_field_name() -> None:
    """Test that validate_html_input_type uses the custom field name in error messages."""
    with pytest.raises(ValueError, match="Invalid type 'bad'"):
        validate_html_input_type("bad", field_name="type")


# --- InputFieldConfig input_type validation ---------------------------------


def test_input_field_config_accepts_valid_input_type() -> None:
    """Test InputFieldConfig accepts valid input_type values."""
    for input_type in HTML_INPUT_TYPE_VALUES:
        config = InputFieldConfig(input_type=input_type)
        assert config.input_type == input_type


def test_input_field_config_rejects_invalid_input_type() -> None:
    """Test InputFieldConfig raises ValueError for invalid input_type."""
    with pytest.raises(ValueError, match="Invalid input_type"):
        InputFieldConfig(input_type="invalid")


def test_input_field_config_default_input_type() -> None:
    """Test InputFieldConfig has correct default input_type."""
    config = InputFieldConfig()
    assert config.input_type == "text"


# =============================================================================
# Form Field Type Validation
# =============================================================================


# --- FORM_FIELD_TYPE_VALUES constant ----------------------------------------


def test_form_field_type_values_contains_expected_values() -> None:
    """Test that FORM_FIELD_TYPE_VALUES contains all expected values."""
    expected = ("text", "password", "email", "number", "tel", "url", "date", "textarea", "select")
    assert expected == FORM_FIELD_TYPE_VALUES


def test_form_field_type_values_is_tuple() -> None:
    """Test that FORM_FIELD_TYPE_VALUES is immutable (tuple)."""
    assert isinstance(FORM_FIELD_TYPE_VALUES, tuple)


# --- validate_form_field_type function --------------------------------------


def test_validate_form_field_type_accepts_valid_values() -> None:
    """Test that validate_form_field_type accepts all valid values."""
    for field_type in FORM_FIELD_TYPE_VALUES:
        validate_form_field_type(field_type)  # Should not raise


def test_validate_form_field_type_rejects_invalid_value() -> None:
    """Test that validate_form_field_type raises ValueError for invalid values."""
    with pytest.raises(ValueError, match="Invalid input_type 'invalid'"):
        validate_form_field_type("invalid")


def test_validate_form_field_type_custom_field_name() -> None:
    """Test that validate_form_field_type uses the custom field name in error messages."""
    with pytest.raises(ValueError, match="Invalid type 'bad'"):
        validate_form_field_type("bad", field_name="type")


# --- FormFieldConfig input_type validation ----------------------------------


def test_form_field_config_accepts_valid_input_type() -> None:
    """Test FormFieldConfig accepts valid input_type values."""
    for field_type in FORM_FIELD_TYPE_VALUES:
        config = FormFieldConfig(input_type=field_type)
        assert config.input_type == field_type


def test_form_field_config_rejects_invalid_input_type() -> None:
    """Test FormFieldConfig raises ValueError for invalid input_type."""
    with pytest.raises(ValueError, match="Invalid input_type"):
        FormFieldConfig(input_type="invalid")


def test_form_field_config_default_input_type() -> None:
    """Test FormFieldConfig has correct default input_type."""
    config = FormFieldConfig()
    assert config.input_type == "text"


# =============================================================================
# HTMX Swap Method Validation
# =============================================================================


# --- HTMX_SWAP_METHOD_VALUES constant ----------------------------------------


def test_htmx_swap_method_values_contains_expected_values() -> None:
    """Test that HTMX_SWAP_METHOD_VALUES contains all expected values."""
    expected = (
        "innerHTML",
        "outerHTML",
        "beforebegin",
        "afterbegin",
        "beforeend",
        "afterend",
        "delete",
        "none",
    )
    assert expected == HTMX_SWAP_METHOD_VALUES


def test_htmx_swap_method_values_is_tuple() -> None:
    """Test that HTMX_SWAP_METHOD_VALUES is immutable (tuple)."""
    assert isinstance(HTMX_SWAP_METHOD_VALUES, tuple)


# --- validate_htmx_swap_method function --------------------------------------


def test_validate_htmx_swap_method_accepts_valid_values() -> None:
    """Test that validate_htmx_swap_method accepts all valid values."""
    for swap_method in HTMX_SWAP_METHOD_VALUES:
        validate_htmx_swap_method(swap_method)  # Should not raise


def test_validate_htmx_swap_method_rejects_invalid_value() -> None:
    """Test that validate_htmx_swap_method raises ValueError for invalid values."""
    with pytest.raises(ValueError, match="Invalid swap_method 'invalid'"):
        validate_htmx_swap_method("invalid")


def test_validate_htmx_swap_method_custom_field_name() -> None:
    """Test that validate_htmx_swap_method uses the custom field name in error messages."""
    with pytest.raises(ValueError, match="Invalid hx_swap 'bad'"):
        validate_htmx_swap_method("bad", field_name="hx_swap")


# --- HtmxConfig swap_method validation ---------------------------------------


def test_htmx_config_accepts_valid_swap_method() -> None:
    """Test HtmxConfig accepts valid swap_method values."""
    for swap_method in HTMX_SWAP_METHOD_VALUES:
        config = HtmxConfig(swap_method=swap_method)
        assert config.swap_method == swap_method


def test_htmx_config_rejects_invalid_swap_method() -> None:
    """Test HtmxConfig raises ValueError for invalid swap_method."""
    with pytest.raises(ValueError, match="Invalid swap_method"):
        HtmxConfig(swap_method="invalid")


def test_htmx_config_default_swap_method() -> None:
    """Test HtmxConfig has correct default swap_method."""
    config = HtmxConfig()
    assert config.swap_method == "innerHTML"


# --- RadioBlockConfig hx_swap_method validation ------------------------------


def test_radio_block_config_accepts_valid_hx_swap_method() -> None:
    """Test RadioBlockConfig accepts valid hx_swap_method values."""
    for swap_method in HTMX_SWAP_METHOD_VALUES:
        config = RadioBlockConfig(name="test", hx_swap_method=swap_method)
        assert config.hx_swap_method == swap_method


def test_radio_block_config_rejects_invalid_hx_swap_method() -> None:
    """Test RadioBlockConfig raises ValueError for invalid hx_swap_method."""
    with pytest.raises(ValueError, match="Invalid hx_swap_method"):
        RadioBlockConfig(name="test", hx_swap_method="invalid")


def test_radio_block_config_default_hx_swap_method() -> None:
    """Test RadioBlockConfig has correct default hx_swap_method."""
    config = RadioBlockConfig(name="test")
    assert config.hx_swap_method == "outerHTML"


# =============================================================================
# HTMX Method Validation
# =============================================================================


# --- HTMX_METHOD_VALUES constant ---------------------------------------------


def test_htmx_method_values_contains_expected_values() -> None:
    """Test that HTMX_METHOD_VALUES contains all expected values."""
    assert HTMX_METHOD_VALUES == ("get", "post")


def test_htmx_method_values_is_tuple() -> None:
    """Test that HTMX_METHOD_VALUES is immutable (tuple)."""
    assert isinstance(HTMX_METHOD_VALUES, tuple)


# --- validate_htmx_method function -------------------------------------------


def test_validate_htmx_method_accepts_valid_values() -> None:
    """Test that validate_htmx_method accepts all valid values."""
    for method in HTMX_METHOD_VALUES:
        validate_htmx_method(method)  # Should not raise


def test_validate_htmx_method_rejects_invalid_value() -> None:
    """Test that validate_htmx_method raises ValueError for invalid values."""
    with pytest.raises(ValueError, match="Invalid method 'put'"):
        validate_htmx_method("put")


def test_validate_htmx_method_custom_field_name() -> None:
    """Test that validate_htmx_method uses the custom field name in error messages."""
    with pytest.raises(ValueError, match="Invalid http_method 'bad'"):
        validate_htmx_method("bad", field_name="http_method")


# --- HtmxConfig method validation --------------------------------------------


def test_htmx_config_accepts_valid_method() -> None:
    """Test HtmxConfig accepts valid method values."""
    for method in HTMX_METHOD_VALUES:
        config = HtmxConfig(method=method)
        assert config.method == method


def test_htmx_config_rejects_invalid_method() -> None:
    """Test HtmxConfig raises ValueError for invalid method."""
    with pytest.raises(ValueError, match="Invalid method"):
        HtmxConfig(method="delete")


def test_htmx_config_default_method() -> None:
    """Test HtmxConfig has correct default method."""
    config = HtmxConfig()
    assert config.method == "get"


# =============================================================================
# Geo Map Marker Type Validation
# =============================================================================


# --- GEO_MAP_MARKER_TYPE_VALUES constant -------------------------------------


def test_geo_map_marker_type_values_contains_expected_values() -> None:
    """Test that GEO_MAP_MARKER_TYPE_VALUES contains all expected values."""
    assert GEO_MAP_MARKER_TYPE_VALUES == ("marker", "circle")


def test_geo_map_marker_type_values_is_tuple() -> None:
    """Test that GEO_MAP_MARKER_TYPE_VALUES is immutable (tuple)."""
    assert isinstance(GEO_MAP_MARKER_TYPE_VALUES, tuple)


# --- validate_geo_map_marker_type function -----------------------------------


def test_validate_geo_map_marker_type_accepts_valid_values() -> None:
    """Test that validate_geo_map_marker_type accepts all valid values."""
    for marker_type in GEO_MAP_MARKER_TYPE_VALUES:
        validate_geo_map_marker_type(marker_type)  # Should not raise


def test_validate_geo_map_marker_type_rejects_invalid_value() -> None:
    """Test that validate_geo_map_marker_type raises ValueError for invalid values."""
    with pytest.raises(ValueError, match="Invalid type 'polygon'"):
        validate_geo_map_marker_type("polygon")


def test_validate_geo_map_marker_type_custom_field_name() -> None:
    """Test that validate_geo_map_marker_type uses the custom field name in error messages."""
    with pytest.raises(ValueError, match="Invalid marker_type 'bad'"):
        validate_geo_map_marker_type("bad", field_name="marker_type")


# --- GeoMapDatasetConfig type validation -------------------------------------


def test_geo_map_dataset_config_accepts_valid_type() -> None:
    """Test GeoMapDatasetConfig accepts valid type values."""
    for marker_type in GEO_MAP_MARKER_TYPE_VALUES:
        config = GeoMapDatasetConfig(name="test", type=marker_type)
        assert config.type == marker_type


def test_geo_map_dataset_config_rejects_invalid_type() -> None:
    """Test GeoMapDatasetConfig raises ValueError for invalid type."""
    with pytest.raises(ValueError, match="Invalid type"):
        GeoMapDatasetConfig(name="test", type="polygon")


def test_geo_map_dataset_config_default_type() -> None:
    """Test GeoMapDatasetConfig has correct default type."""
    config = GeoMapDatasetConfig(name="test")
    assert config.type == "marker"


# =============================================================================
# Slider Legend Mode Validation
# =============================================================================


# --- SLIDER_LEGEND_MODE_VALUES constant --------------------------------------


def test_slider_legend_mode_values_contains_expected_values() -> None:
    """Test that SLIDER_LEGEND_MODE_VALUES contains all expected values."""
    assert SLIDER_LEGEND_MODE_VALUES == ("static", "skip", "rotate")


def test_slider_legend_mode_values_is_tuple() -> None:
    """Test that SLIDER_LEGEND_MODE_VALUES is immutable (tuple)."""
    assert isinstance(SLIDER_LEGEND_MODE_VALUES, tuple)


# --- validate_slider_legend_mode function ------------------------------------


def test_validate_slider_legend_mode_accepts_valid_values() -> None:
    """Test that validate_slider_legend_mode accepts all valid values."""
    for mode in SLIDER_LEGEND_MODE_VALUES:
        validate_slider_legend_mode(mode)  # Should not raise


def test_validate_slider_legend_mode_rejects_invalid_value() -> None:
    """Test that validate_slider_legend_mode raises ValueError for invalid values."""
    with pytest.raises(ValueError, match="Invalid legend_mode 'hide'"):
        validate_slider_legend_mode("hide")


def test_validate_slider_legend_mode_custom_field_name() -> None:
    """Test that validate_slider_legend_mode uses the custom field name in error messages."""
    with pytest.raises(ValueError, match="Invalid mode 'bad'"):
        validate_slider_legend_mode("bad", field_name="mode")


# --- SliderConfig legend_mode validation -------------------------------------


def test_slider_config_accepts_valid_legend_mode() -> None:
    """Test SliderConfig accepts valid legend_mode values."""
    for mode in SLIDER_LEGEND_MODE_VALUES:
        config = SliderConfig(legend_mode=mode)
        assert config.legend_mode == mode


def test_slider_config_rejects_invalid_legend_mode() -> None:
    """Test SliderConfig raises ValueError for invalid legend_mode."""
    with pytest.raises(ValueError, match="Invalid legend_mode"):
        SliderConfig(legend_mode="hide")


def test_slider_config_default_legend_mode() -> None:
    """Test SliderConfig has correct default legend_mode."""
    config = SliderConfig()
    assert config.legend_mode == "static"


# =============================================================================
# Toggle View Type Validation
# =============================================================================


# --- TOGGLE_VIEW_TYPE_VALUES constant ----------------------------------------


def test_toggle_view_type_values_contains_expected_values() -> None:
    """Test that TOGGLE_VIEW_TYPE_VALUES contains all expected values."""
    assert TOGGLE_VIEW_TYPE_VALUES == ("card", "table", "carousel")


def test_toggle_view_type_values_is_tuple() -> None:
    """Test that TOGGLE_VIEW_TYPE_VALUES is immutable (tuple)."""
    assert isinstance(TOGGLE_VIEW_TYPE_VALUES, tuple)


# --- validate_toggle_view_type function --------------------------------------


def test_validate_toggle_view_type_accepts_valid_values() -> None:
    """Test that validate_toggle_view_type accepts all valid values."""
    for view_type in TOGGLE_VIEW_TYPE_VALUES:
        validate_toggle_view_type(view_type)  # Should not raise


def test_validate_toggle_view_type_rejects_invalid_value() -> None:
    """Test that validate_toggle_view_type raises ValueError for invalid values."""
    with pytest.raises(ValueError, match="Invalid current_view 'grid'"):
        validate_toggle_view_type("grid")


def test_validate_toggle_view_type_custom_field_name() -> None:
    """Test that validate_toggle_view_type uses the custom field name in error messages."""
    with pytest.raises(ValueError, match="Invalid view 'bad'"):
        validate_toggle_view_type("bad", field_name="view")


# --- ToggleViewConfig current_view validation --------------------------------


def test_toggle_view_config_accepts_valid_current_view() -> None:
    """Test ToggleViewConfig accepts valid current_view values."""
    for view_type in TOGGLE_VIEW_TYPE_VALUES:
        config = ToggleViewConfig(tag_id="test", current_view=view_type)
        assert config.current_view == view_type


def test_toggle_view_config_rejects_invalid_current_view() -> None:
    """Test ToggleViewConfig raises ValueError for invalid current_view."""
    with pytest.raises(ValueError, match="Invalid current_view"):
        ToggleViewConfig(tag_id="test", current_view="grid")


def test_toggle_view_config_default_current_view() -> None:
    """Test ToggleViewConfig has correct default current_view."""
    config = ToggleViewConfig(tag_id="test")
    assert config.current_view == "card"
