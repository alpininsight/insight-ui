"""Tests for the build_search_index management command."""

from __future__ import annotations

import json
from io import StringIO
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

import pytest
from django.core.management import call_command
from documentation.component_details.components import Component, ComponentCategory
from documentation.management.commands.build_search_index import DESCRIPTION_MAX_LENGTH


@pytest.fixture
def temp_output_path(tmp_path: Path) -> Path:
    """Provide a temporary output path for the search index.

    Note: The command appends locale codes to the filename, so
    search-index.json becomes search-index-en.json, search-index-de.json, etc.
    """
    return tmp_path / "search-index.json"


@pytest.fixture
def temp_output_path_en(tmp_path: Path) -> Path:
    """Provide the expected English output path."""
    return tmp_path / "search-index-en.json"


class TestBuildSearchIndexCommand:
    """Tests for the build_search_index management command."""

    def test_command_generates_json_output(self, temp_output_path: Path, temp_output_path_en: Path) -> None:
        """The command should generate a valid JSON file."""
        call_command("build_search_index", output=str(temp_output_path), locale="en")

        assert temp_output_path_en.exists()
        content = json.loads(temp_output_path_en.read_text(encoding="utf-8"))
        assert isinstance(content, list)
        assert len(content) > 0

    def test_command_includes_components(self, temp_output_path: Path, temp_output_path_en: Path) -> None:
        """The index should include component entries."""
        call_command("build_search_index", output=str(temp_output_path), locale="en")

        content = json.loads(temp_output_path_en.read_text(encoding="utf-8"))
        component_entries = [e for e in content if e["category"] == "component"]

        assert len(component_entries) > 0
        # Check that Button component is included
        button_entry = next((e for e in component_entries if e["name"] == "Button"), None)
        assert button_entry is not None
        assert button_entry["id"] == "component:button"
        assert button_entry["url"] == "/docs/components/button/"

    def test_command_includes_types(self, temp_output_path: Path, temp_output_path_en: Path) -> None:
        """The index should include type entries."""
        call_command("build_search_index", output=str(temp_output_path), locale="en")

        content = json.loads(temp_output_path_en.read_text(encoding="utf-8"))
        type_entries = [e for e in content if e["category"] == "type"]

        assert len(type_entries) > 0
        # Check that Size type is included
        size_entry = next((e for e in type_entries if e["name"] == "Size"), None)
        assert size_entry is not None
        assert size_entry["id"] == "type:Size"
        assert "xs" in size_entry["keywords"]

    def test_command_includes_categories(self, temp_output_path: Path, temp_output_path_en: Path) -> None:
        """The index should include category entries."""
        call_command("build_search_index", output=str(temp_output_path), locale="en")

        content = json.loads(temp_output_path_en.read_text(encoding="utf-8"))
        category_entries = [e for e in content if e["category"] == "category"]

        assert len(category_entries) == len(ComponentCategory)
        # Check that Layout category is included
        layout_entry = next((e for e in category_entries if "Layout" in e["name"]), None)
        assert layout_entry is not None

    def test_entry_structure(self, temp_output_path: Path, temp_output_path_en: Path) -> None:
        """Each entry should have the required fields."""
        call_command("build_search_index", output=str(temp_output_path), locale="en")

        content = json.loads(temp_output_path_en.read_text(encoding="utf-8"))
        required_fields = {"id", "name", "category", "group", "description", "keywords", "url"}

        for entry in content:
            assert required_fields.issubset(entry.keys()), f"Entry missing fields: {entry}"

    def test_dry_run_outputs_to_stdout(self) -> None:
        """The --dry-run flag should print JSON to stdout without creating a file."""
        out = StringIO()
        call_command("build_search_index", dry_run=True, locale="en", stdout=out)

        output = out.getvalue()
        # Skip the locale header line (e.g., "=== EN ===")
        json_start = output.find("[")
        content = json.loads(output[json_start:])
        assert isinstance(content, list)
        assert len(content) > 0

    def test_creates_parent_directories(self, tmp_path: Path) -> None:
        """The command should create parent directories if they don't exist."""
        output_path = tmp_path / "nested" / "dir" / "search-index.json"
        expected_path = tmp_path / "nested" / "dir" / "search-index-en.json"
        call_command("build_search_index", output=str(output_path), locale="en")

        assert expected_path.exists()

    def test_component_count_matches_enum(self, temp_output_path: Path, temp_output_path_en: Path) -> None:
        """The number of component entries should match the Component enum."""
        call_command("build_search_index", output=str(temp_output_path), locale="en")

        content = json.loads(temp_output_path_en.read_text(encoding="utf-8"))
        component_entries = [e for e in content if e["category"] == "component"]

        assert len(component_entries) == len(Component)

    def test_description_truncation(self, temp_output_path: Path, temp_output_path_en: Path) -> None:
        """Long descriptions should be truncated to DESCRIPTION_MAX_LENGTH characters."""
        call_command("build_search_index", output=str(temp_output_path), locale="en")

        content = json.loads(temp_output_path_en.read_text(encoding="utf-8"))

        for entry in content:
            if entry["description"]:
                assert len(entry["description"]) <= DESCRIPTION_MAX_LENGTH

    def test_keywords_are_lowercase(self, temp_output_path: Path, temp_output_path_en: Path) -> None:
        """Component name keywords should be lowercase for search."""
        call_command("build_search_index", output=str(temp_output_path), locale="en")

        content = json.loads(temp_output_path_en.read_text(encoding="utf-8"))
        component_entries = [e for e in content if e["category"] == "component"]

        for entry in component_entries:
            # At least the component value should be lowercase
            assert entry["id"].split(":")[1] in entry["keywords"]

    def test_command_includes_configs(self, temp_output_path: Path, temp_output_path_en: Path) -> None:
        """The index should include config dataclass entries."""
        call_command("build_search_index", output=str(temp_output_path), locale="en")

        content = json.loads(temp_output_path_en.read_text(encoding="utf-8"))
        config_entries = [e for e in content if e["category"] == "config"]

        assert len(config_entries) > 0
        # Check that ButtonConfig is included
        button_config_entry = next((e for e in config_entries if e["name"] == "ButtonConfig"), None)
        assert button_config_entry is not None
        assert button_config_entry["id"] == "config:ButtonConfig"
        assert button_config_entry["url"] == "/docs/configs#buttonconfig"
        assert button_config_entry["group"] == "Configs"
        assert "button" in button_config_entry["keywords"]
