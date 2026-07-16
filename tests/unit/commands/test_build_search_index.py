"""Tests for the build_search_index management command."""

from __future__ import annotations

import json
from io import StringIO

from pytest_django.asserts import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

import pytest
from django.core.management import call_command
from insight_ui.component_details.components import Component, ComponentCategory
from insight_ui.management.commands.build_search_index import DESCRIPTION_MAX_LENGTH


@pytest.fixture
def temp_output_path(tmp_path: Path) -> Path:
    """Provide a temporary output path for the search index."""
    return tmp_path / "search-index.json"


class TestBuildSearchIndexCommand:
    """Tests for the build_search_index management command."""

    def test_command_generates_json_output(self, temp_output_path: Path) -> None:
        """The command should generate a valid JSON file."""
        call_command("build_search_index", output=str(temp_output_path))

        assert temp_output_path.exists()
        content = json.loads(temp_output_path.read_text(encoding="utf-8"))
        assert isinstance(content, list)
        assert len(content) > 0

    def test_command_includes_components(self, temp_output_path: Path) -> None:
        """The index should include component entries."""
        call_command("build_search_index", output=str(temp_output_path))

        content = json.loads(temp_output_path.read_text(encoding="utf-8"))
        component_entries = [e for e in content if e["category"] == "component"]

        assert len(component_entries) > 0
        # Check that Button component is included
        button_entry = next((e for e in component_entries if e["name"] == "Button"), None)
        assert button_entry is not None
        assert button_entry["id"] == "component:button"
        assert button_entry["url"] == "/docs/components/button/"

    def test_command_includes_types(self, temp_output_path: Path) -> None:
        """The index should include type entries."""
        call_command("build_search_index", output=str(temp_output_path))

        content = json.loads(temp_output_path.read_text(encoding="utf-8"))
        type_entries = [e for e in content if e["category"] == "type"]

        assert len(type_entries) > 0
        # Check that Size type is included
        size_entry = next((e for e in type_entries if e["name"] == "Size"), None)
        assert size_entry is not None
        assert size_entry["id"] == "type:Size"
        assert "xs" in size_entry["keywords"]

    def test_command_includes_categories(self, temp_output_path: Path) -> None:
        """The index should include category entries."""
        call_command("build_search_index", output=str(temp_output_path))

        content = json.loads(temp_output_path.read_text(encoding="utf-8"))
        category_entries = [e for e in content if e["category"] == "category"]

        assert len(category_entries) == len(ComponentCategory)
        # Check that Layout category is included
        layout_entry = next((e for e in category_entries if "Layout" in e["name"]), None)
        assert layout_entry is not None

    def test_entry_structure(self, temp_output_path: Path) -> None:
        """Each entry should have the required fields."""
        call_command("build_search_index", output=str(temp_output_path))

        content = json.loads(temp_output_path.read_text(encoding="utf-8"))
        required_fields = {"id", "name", "category", "group", "description", "keywords", "url"}

        for entry in content:
            assert required_fields.issubset(entry.keys()), f"Entry missing fields: {entry}"

    def test_dry_run_outputs_to_stdout(self) -> None:
        """The --dry-run flag should print JSON to stdout without creating a file."""
        out = StringIO()
        call_command("build_search_index", dry_run=True, stdout=out)

        output = out.getvalue()
        content = json.loads(output)
        assert isinstance(content, list)
        assert len(content) > 0

    def test_creates_parent_directories(self, tmp_path: Path) -> None:
        """The command should create parent directories if they don't exist."""
        output_path = tmp_path / "nested" / "dir" / "search-index.json"
        call_command("build_search_index", output=str(output_path))

        assert output_path.exists()

    def test_component_count_matches_enum(self, temp_output_path: Path) -> None:
        """The number of component entries should match the Component enum."""
        call_command("build_search_index", output=str(temp_output_path))

        content = json.loads(temp_output_path.read_text(encoding="utf-8"))
        component_entries = [e for e in content if e["category"] == "component"]

        assert len(component_entries) == len(Component)

    def test_description_truncation(self, temp_output_path: Path) -> None:
        """Long descriptions should be truncated to DESCRIPTION_MAX_LENGTH characters."""
        call_command("build_search_index", output=str(temp_output_path))

        content = json.loads(temp_output_path.read_text(encoding="utf-8"))

        for entry in content:
            if entry["description"]:
                assert len(entry["description"]) <= DESCRIPTION_MAX_LENGTH

    def test_keywords_are_lowercase(self, temp_output_path: Path) -> None:
        """Component name keywords should be lowercase for search."""
        call_command("build_search_index", output=str(temp_output_path))

        content = json.loads(temp_output_path.read_text(encoding="utf-8"))
        component_entries = [e for e in content if e["category"] == "component"]

        for entry in component_entries:
            # At least the component value should be lowercase
            assert entry["id"].split(":")[1] in entry["keywords"]
