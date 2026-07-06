"""Tests for the component scaffold management command."""

from pathlib import Path

from insight_ui.management.commands.create_component import Command


def test_derive_names_preserves_pascal_case_for_multi_word_component() -> None:
    """Verify scaffold names keep valid PascalCase for multi-word components."""
    command = Command()

    names = command._derive_names("Developer Access Card")

    assert names.enum_name == "DEVELOPER_ACCESS_CARD"
    assert names.slug == "developer_access_card"
    assert names.func_name == "developer_access_card"
    assert names.class_name == "DeveloperAccessCard"
    assert names.js_slug == "developer-access-card"
    assert names.config_class_name == "DeveloperAccessCardConfig"


def test_add_to_components_py_registers_config_class(tmp_path: Path) -> None:
    """Verify component registry entries include and import the generated config."""
    command = Command()
    component_details = tmp_path / "component_details"
    component_details.mkdir()
    components_file = component_details / "components.py"
    components_file.write_text(
        """from enum import Enum

from insight_ui.configs import (
    ButtonConfig,
)


class ComponentCategory(Enum):
    INPUT = "input"
    CARD = "card"


class Component(Enum):
    BUTTON = ("button", ComponentCategory.INPUT, ButtonConfig)
    CARD = ("card", ComponentCategory.CARD)
""",
        encoding="utf-8",
    )

    command._add_to_components_py(
        tmp_path,
        enum_name="DEVELOPER_ACCESS_CARD",
        slug="developer_access_card",
        category="card",
        config_class_name="DeveloperAccessCardConfig",
    )

    content = components_file.read_text(encoding="utf-8")
    assert "    DeveloperAccessCardConfig," in content
    assert (
        '    DEVELOPER_ACCESS_CARD = ("developer_access_card", ComponentCategory.CARD, DeveloperAccessCardConfig)'
    ) in content


def test_add_inclusion_tag_uses_generated_config_class(tmp_path: Path) -> None:
    """Verify generated inclusion tags build the generated config class."""
    command = Command()
    templatetags = tmp_path / "templatetags"
    templatetags.mkdir()
    insight_tags_file = templatetags / "insight_tags.py"
    insight_tags_file.write_text(
        """from typing import Any

from insight_ui.configs import (
    ButtonConfig,
)


# =============================================================
#
#   Card Tags
#
# =============================================================


@register.inclusion_tag("insight_ui/components/card.html")
def card() -> dict[str, Any]:
    return {}


# =============================================================
#
#   Input Tags
#
# =============================================================
""",
        encoding="utf-8",
    )

    command._add_inclusion_tag(
        tmp_path,
        func_name="developer_access_card",
        slug="developer_access_card",
        category="card",
        name="Developer Access Card",
        config_class_name="DeveloperAccessCardConfig",
    )

    content = insight_tags_file.read_text(encoding="utf-8")
    assert "    DeveloperAccessCardConfig," in content
    assert "def developer_access_card(config: DeveloperAccessCardConfig | None = None" in content
    assert "build_config(DeveloperAccessCardConfig, config, tag_id=tag_id)" in content
    assert "build_config(WebSocketConfig" not in content


def test_context_configs_include_parameter_documentation() -> None:
    """Verify generated components include parameter self-documentation."""
    command = Command()

    file_names = {config.file_name for config in command._get_context_configs()}

    assert "parameter_context.py" in file_names


def test_add_mapping_entry_adds_template_and_script_links() -> None:
    """Verify source-link mappings can be inserted in documented sections."""
    command = Command()
    content = """TEMPLATE_PATHS = {
    # Cards
    "card": GIT_BASE_FILE + "cards/card.html",
}

SCRIPT_PATHS = {
    # Cards
}
"""

    content = command._add_mapping_entry(
        content,
        mapping_name="TEMPLATE_PATHS",
        section_comment="# Cards",
        key="developer_access_card",
        value='GIT_BASE_FILE + "developer_access_card.html"',
    )
    content = command._add_mapping_entry(
        content,
        mapping_name="SCRIPT_PATHS",
        section_comment="# Cards",
        key="developer_access_card",
        value='GIT_BASE_SCRIPT_FILE + "insight-ui-developer-access-card.js"',
    )

    assert '"developer_access_card": GIT_BASE_FILE + "developer_access_card.html",' in content
    assert '"developer_access_card": GIT_BASE_SCRIPT_FILE + "insight-ui-developer-access-card.js",' in content
