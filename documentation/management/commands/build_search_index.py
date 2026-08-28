"""Management command to generate search-index.json for client-side search."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import TYPE_CHECKING, Any

from django.conf import settings
from django.core.management.base import BaseCommand
from django.urls import reverse
from django.utils import translation
from insight_ui.configs import types

from documentation.component_details.component_context import get_component_context
from documentation.component_details.components import Component, ComponentCategory
from documentation.config_registry import get_config_classes

if TYPE_CHECKING:
    from argparse import ArgumentParser

# Maximum length for description text in search entries
DESCRIPTION_MAX_LENGTH = 150
# Maximum number of type values to preview in description
TYPE_VALUES_PREVIEW_LIMIT = 5

# Types to include in the search index with their value tuples
TYPE_DEFINITIONS: dict[str, tuple[str, ...]] = {
    "Size": types.SIZE_VALUES,
    "ColorType": types.COLOR_TYPE_VALUES,
    "BadgeType": types.BADGE_TYPE_VALUES,
    "ButtonType": types.BUTTON_TYPE_VALUES,
    "StepStatus": types.STEP_STATUS_VALUES,
    "AlertType": types.ALERT_TYPE_VALUES,
    "HtmlButtonType": types.HTML_BUTTON_TYPE_VALUES,
    "HtmlInputType": types.HTML_INPUT_TYPE_VALUES,
    "FormFieldType": types.FORM_FIELD_TYPE_VALUES,
    "CornerPosition": types.CORNER_POSITION_VALUES,
    "InlinePosition": types.INLINE_POSITION_VALUES,
    "HtmxSwapMethod": types.HTMX_SWAP_METHOD_VALUES,
    "HtmxMethod": types.HTMX_METHOD_VALUES,
    "FilterFieldType": types.FILTER_FIELD_TYPE_VALUES,
    "GeoMapMarkerType": types.GEO_MAP_MARKER_TYPE_VALUES,
    "SliderLegendMode": types.SLIDER_LEGEND_MODE_VALUES,
    "ToggleViewType": types.TOGGLE_VIEW_TYPE_VALUES,
}


class Command(BaseCommand):
    """Generate search-index.json for client-side documentation search."""

    help = "Generates search-index.json containing components, types, categories, and configs for Fuse.js search."

    def add_arguments(self, parser: ArgumentParser) -> None:
        """Add command arguments.

        Args:
            parser: The argument parser to add arguments to.

        """
        parser.add_argument(
            "--output",
            type=str,
            default=None,
            help="Output file path (default: insight_ui/static/insight_ui/data/search-index-{locale}.json)",
        )
        parser.add_argument(
            "--locale",
            type=str,
            default=None,
            help="Locale code (e.g., 'en', 'de'). If not specified, generates for all configured languages.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Print the index to stdout instead of writing to file",
        )

    def handle(self, *args: Any, **options: Any) -> None:  # noqa: ANN401, ARG002
        """Execute the command to generate the search index.

        Args:
            *args: Positional arguments (unused).
            **options: Command options.

        """
        # Determine which locales to generate
        locale_arg = options.get("locale")
        locales = [locale_arg] if locale_arg else [lang_code for lang_code, _ in settings.LANGUAGES]

        for locale in locales:
            self._generate_index_for_locale(locale, options)

    def _generate_index_for_locale(self, locale: str, options: dict[str, Any]) -> None:
        """Generate search index for a specific locale.

        Args:
            locale: The locale code (e.g., 'en', 'de').
            options: Command options.

        """
        # Activate the locale for translation
        translation.activate(locale)

        try:
            index: list[dict[str, Any]] = []

            # Add components
            index.extend(self._build_component_entries())

            # Add types
            index.extend(self._build_type_entries())

            # Add categories
            index.extend(self._build_category_entries())

            # Add config dataclasses
            index.extend(self._build_config_entries())

            if options.get("dry_run"):
                self.stdout.write(f"\n=== {locale.upper()} ===\n")
                self.stdout.write(json.dumps(index, ensure_ascii=False, indent=2))
                return

            output_path = options.get("output")
            if output_path:
                # If custom output path, append locale before extension
                path = Path(output_path)
                output_file = path.parent / f"{path.stem}-{locale}{path.suffix}"
            else:
                base_path = Path(__file__).resolve().parent.parent.parent
                output_file = base_path / "static" / "insight_ui" / "data" / f"search-index-{locale}.json"

            output_file.parent.mkdir(parents=True, exist_ok=True)
            output_file.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")

            self.stdout.write(
                self.style.SUCCESS(f"Generated {locale} search index with {len(index)} entries at {output_file}")
            )
        finally:
            # Deactivate translation
            translation.deactivate()

    def _build_component_entries(self) -> list[dict[str, Any]]:
        """Build search index entries for all components.

        Returns:
            List of component search entries.

        """
        entries = []

        for component in Component:
            try:
                ctx = get_component_context(component)
                description = ctx.get("description", [""])[0] if ctx.get("description") else ""
                # Convert lazy string to regular string for JSON serialization
                description = str(description)
                # Truncate description for index size
                if len(description) > DESCRIPTION_MAX_LENGTH:
                    description = description[: DESCRIPTION_MAX_LENGTH - 3] + "..."
            except (ValueError, KeyError):
                description = ""

            # Build keywords from component name parts and group
            keywords = [
                component.value,
                component.group.value,
                *component.formatted_name.lower().split(),
            ]

            # Convert lazy string to regular string for JSON serialization
            group_name = str(component.group.formatted_name)

            entries.append(
                {
                    "id": f"component:{component.value}",
                    "name": component.formatted_name,
                    "category": "component",
                    "group": group_name,
                    "description": description,
                    "keywords": keywords,
                    "url": reverse(
                        "component_detail_page_view",
                        kwargs={"component_name": component.value},
                    ),
                }
            )

        return entries

    def _build_type_entries(self) -> list[dict[str, Any]]:
        """Build search index entries for type definitions.

        Returns:
            List of type search entries.

        """
        entries = []

        for type_name, values in TYPE_DEFINITIONS.items():
            # Format values for display, limit to first few
            values_preview = ", ".join(values[:TYPE_VALUES_PREVIEW_LIMIT])
            if len(values) > TYPE_VALUES_PREVIEW_LIMIT:
                values_preview += f", ... ({len(values)} total)"

            entries.append(
                {
                    "id": f"type:{type_name}",
                    "name": type_name,
                    "category": "type",
                    "group": "Types",
                    "description": f"Values: {values_preview}",
                    "keywords": [type_name.lower(), *list(values)],
                    "url": f"{reverse('types_view')}#{type_name.lower()}",
                }
            )

        return entries

    def _build_category_entries(self) -> list[dict[str, Any]]:
        """Build search index entries for component categories.

        Returns:
            List of category search entries.

        """
        entries = []

        for category in ComponentCategory:
            # Count components in this category
            component_count = sum(1 for c in Component if c.group == category)
            # Convert lazy string to regular string for JSON serialization
            formatted_name = str(category.formatted_name)

            entries.append(
                {
                    "id": f"category:{category.value}",
                    "name": formatted_name,
                    "category": "category",
                    "group": "Categories",
                    "description": f"{component_count} components",
                    "keywords": [category.value, formatted_name.lower()],
                    "url": reverse("storybook_view", kwargs={"storybook_name": category.value}),
                }
            )

        return entries

    def _build_config_entries(self) -> list[dict[str, Any]]:
        """Build search index entries for config dataclasses.

        Returns:
            List of config search entries.

        """
        entries = []

        for config_cls in get_config_classes():
            name = config_cls.__name__
            anchor = name.lower()

            # Extract description from docstring (first line/paragraph)
            description = ""
            if config_cls.__doc__:
                # Get first paragraph (up to empty line or Attributes:)
                lines = config_cls.__doc__.strip().split("\n")
                desc_lines = []
                for line in lines:
                    stripped = line.strip()
                    if not stripped or stripped.startswith("Attributes:"):
                        break
                    desc_lines.append(stripped)
                description = " ".join(desc_lines)

            # Truncate description for index size
            if len(description) > DESCRIPTION_MAX_LENGTH:
                description = description[: DESCRIPTION_MAX_LENGTH - 3] + "..."

            # Build keywords from class name parts
            # E.g., "ButtonConfig" -> ["buttonconfig", "button", "config"]
            keywords = [name.lower(), "config"]
            # Split CamelCase into words
            words = re.findall(r"[A-Z][a-z]+", name)
            keywords.extend(word.lower() for word in words)

            entries.append(
                {
                    "id": f"config:{name}",
                    "name": name,
                    "category": "config",
                    "group": "Configs",
                    "description": description,
                    "keywords": keywords,
                    "url": f"{reverse('config_reference_view')}#{anchor}",
                }
            )

        return entries
