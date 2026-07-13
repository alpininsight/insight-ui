"""Tests for size and type validation utilities."""

import pytest
from insight_ui.configs import (
    ALERT_TYPE_VALUES,
    BADGE_TYPE_VALUES,
    BUTTON_TYPE_VALUES,
    COLOR_TYPE_VALUES,
    CORNER_POSITION_VALUES,
    FILTER_FIELD_TYPE_VALUES,
    FORM_FIELD_TYPE_VALUES,
    HORIZONTAL_SIDE_VALUES,
    HTML_BUTTON_TYPE_VALUES,
    HTML_INPUT_TYPE_VALUES,
    INLINE_POSITION_VALUES,
    SIZE_VALUES,
    STEP_STATUS_VALUES,
    AlertConfig,
    BadgeConfig,
    BrandMarkConfig,
    ButtonConfig,
    CornerRibbonConfig,
    FormFieldConfig,
    IconConfig,
    InfoboxConfig,
    InputFieldConfig,
    MinimalStepperConfig,
    QueryBuilderFieldConfig,
    SidebarConfig,
    StatusScreenConfig,
    validate_alert_type,
    validate_badge_type,
    validate_button_type,
    validate_color_type,
    validate_corner_position,
    validate_filter_field_type,
    validate_form_field_type,
    validate_horizontal_side,
    validate_html_button_type,
    validate_html_input_type,
    validate_inline_position,
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
        config = ButtonConfig(button_type=button_type)
        assert config.button_type == button_type


def test_button_config_rejects_invalid_button_type() -> None:
    """Test ButtonConfig raises ValueError for invalid button_type."""
    with pytest.raises(ValueError, match="Invalid button_type"):
        ButtonConfig(button_type="invalid")


def test_button_config_default_button_type() -> None:
    """Test ButtonConfig has correct default button_type."""
    config = ButtonConfig()
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
# Horizontal Side Validation
# =============================================================================


# --- HORIZONTAL_SIDE_VALUES constant ----------------------------------------


def test_horizontal_side_values_contains_expected_values() -> None:
    """Test that HORIZONTAL_SIDE_VALUES contains all expected values."""
    assert HORIZONTAL_SIDE_VALUES == ("left", "right")


def test_horizontal_side_values_is_tuple() -> None:
    """Test that HORIZONTAL_SIDE_VALUES is immutable (tuple)."""
    assert isinstance(HORIZONTAL_SIDE_VALUES, tuple)


# --- validate_horizontal_side function --------------------------------------


def test_validate_horizontal_side_accepts_valid_values() -> None:
    """Test that validate_horizontal_side accepts all valid values."""
    for side in HORIZONTAL_SIDE_VALUES:
        validate_horizontal_side(side)  # Should not raise


def test_validate_horizontal_side_rejects_invalid_value() -> None:
    """Test that validate_horizontal_side raises ValueError for invalid values."""
    with pytest.raises(ValueError, match="Invalid side 'center'"):
        validate_horizontal_side("center")


def test_validate_horizontal_side_custom_field_name() -> None:
    """Test that validate_horizontal_side uses the custom field name in error messages."""
    with pytest.raises(ValueError, match="Invalid panel_side 'bad'"):
        validate_horizontal_side("bad", field_name="panel_side")


# --- SidebarConfig side validation ------------------------------------------


def test_sidebar_config_accepts_valid_side() -> None:
    """Test SidebarConfig accepts valid side values."""
    for side in HORIZONTAL_SIDE_VALUES:
        config = SidebarConfig(side=side)
        assert config.side == side


def test_sidebar_config_rejects_invalid_side() -> None:
    """Test SidebarConfig raises ValueError for invalid side."""
    with pytest.raises(ValueError, match="Invalid side"):
        SidebarConfig(side="center")


def test_sidebar_config_default_side() -> None:
    """Test SidebarConfig has correct default side."""
    config = SidebarConfig()
    assert config.side == "right"


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
