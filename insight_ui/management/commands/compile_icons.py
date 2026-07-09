"""Management command to compile custom icons into icons.html template."""

from __future__ import annotations

import re
from pathlib import Path
from typing import TYPE_CHECKING, Any
from xml.etree.ElementTree import Element, ParseError, tostring  # nosec B405

from defusedxml import ElementTree
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

if TYPE_CHECKING:
    from argparse import ArgumentParser


class Command(BaseCommand):
    """Compile custom icons and bundled icons into a single icons.html template."""

    help = (
        "Generates an icons.html template by merging custom icons with bundled icons. "
        "Custom icons override bundled icons with the same name."
    )

    def add_arguments(self, parser: ArgumentParser) -> None:
        """Add command arguments.

        Args:
            parser: The argument parser to add arguments to.

        """
        parser.add_argument("--dir", type=str, help="Directory containing individual SVG files")
        parser.add_argument("--sprite", type=str, help="Path to SVG sprite sheet file")
        parser.add_argument(
            "--output",
            type=str,
            help="Output path for generated icons.html (default: templates/insight_ui/components/icons.html)",
        )
        parser.add_argument("--list-bundled", action="store_true", help="List all bundled icon names and exit")

    def handle(self, *args: Any, **options: Any) -> None:  # noqa: ANN401, ARG002
        """Execute the command.

        Args:
            *args: Positional arguments (unused).
            **options: Command options from argparse.

        """
        if options.get("list_bundled"):
            self._list_bundled_icons()
            return

        if not options.get("dir") and not options.get("sprite"):
            msg = "You must specify either --dir or --sprite (or both)"
            raise CommandError(msg)

        # Collect icons from all sources
        custom_icons: dict[str, str] = {}

        if options.get("dir"):
            dir_icons = self._read_icons_from_directory(Path(options["dir"]))
            custom_icons.update(dir_icons)
            self.stdout.write(f"Loaded {len(dir_icons)} icons from directory")

        if options.get("sprite"):
            sprite_icons = self._read_icons_from_sprite(Path(options["sprite"]))
            custom_icons.update(sprite_icons)
            self.stdout.write(f"Loaded {len(sprite_icons)} icons from sprite sheet")

        # Merge with bundled icons (custom icons take precedence)
        bundled = self._get_bundled_icons()
        merged_icons = {**bundled, **custom_icons}

        self.stdout.write(f"Total icons: {len(merged_icons)} ({len(custom_icons)} custom, {len(bundled)} bundled)")

        # Determine output path
        output_path = self._get_output_path(options.get("output"))

        # Generate and write template
        template_content = self._generate_template(merged_icons)
        self._write_output(output_path, template_content)

        self.stdout.write(self.style.SUCCESS(f"Generated icons.html at {output_path}"))

    def _list_bundled_icons(self) -> None:
        """List all bundled icon names."""
        bundled = self._get_bundled_icons()
        self.stdout.write(f"Bundled icons ({len(bundled)}):")
        for name in sorted(bundled.keys()):
            self.stdout.write(f"  - {name}")

    def _read_icons_from_directory(self, directory: Path) -> dict[str, str]:
        """Read individual SVG files from a directory.

        Args:
            directory: Path to directory containing SVG files.

        Returns:
            Dictionary mapping icon names to SVG content.

        """
        if not directory.exists():
            msg = f"Directory not found: {directory}"
            raise CommandError(msg)

        if not directory.is_dir():
            msg = f"Not a directory: {directory}"
            raise CommandError(msg)

        icons = {}
        for svg_file in directory.glob("*.svg"):
            icon_name = svg_file.stem  # filename without extension
            icon_name = self._normalize_icon_name(icon_name)
            svg_content = self._extract_svg_content(svg_file.read_text(encoding="utf-8"))
            if svg_content:
                icons[icon_name] = svg_content
                self.stdout.write(f"  Loaded: {icon_name}")

        return icons

    def _read_icons_from_sprite(self, sprite_path: Path) -> dict[str, str]:
        """Read icons from an SVG sprite sheet (extracts <symbol> elements).

        Args:
            sprite_path: Path to the SVG sprite sheet file.

        Returns:
            Dictionary mapping icon names to SVG content.

        """
        if not sprite_path.exists():
            msg = f"Sprite file not found: {sprite_path}"
            raise CommandError(msg)

        content = sprite_path.read_text(encoding="utf-8")
        icons = {}

        try:
            # Parse the SVG sprite
            root = ElementTree.fromstring(content)

            # Handle SVG namespace
            namespaces = {"svg": "http://www.w3.org/2000/svg"}

            # Find all symbol elements (with or without namespace)
            symbols = root.findall(".//symbol") + root.findall(".//svg:symbol", namespaces)

            for symbol in symbols:
                icon_id = symbol.get("id", "")
                if not icon_id:
                    continue

                icon_name = self._normalize_icon_name(icon_id)
                viewbox = symbol.get("viewBox", "0 0 24 24")

                # Extract inner content of symbol
                inner_content = self._get_element_inner_xml(symbol)

                # Reconstruct as standalone SVG
                svg_content = (
                    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{viewbox}" '
                    f'fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true">\n'
                    f"            {inner_content}\n"
                    f"        </svg>"
                )

                icons[icon_name] = svg_content
                self.stdout.write(f"  Loaded: {icon_name}")

        except ParseError as e:
            msg = f"Failed to parse sprite sheet: {e}"
            raise CommandError(msg) from e

        return icons

    def _get_element_inner_xml(self, element: Element) -> str:
        """Get the inner XML content of an element (children as string).

        Args:
            element: XML element to extract inner content from.

        Returns:
            String representation of all child elements.

        """
        inner_parts = []
        if element.text:
            inner_parts.append(element.text)
        inner_parts.extend(tostring(child, encoding="unicode") for child in element)
        return "".join(inner_parts)

    def _normalize_icon_name(self, name: str) -> str:
        """Normalize icon name to consistent format (lowercase with hyphens).

        Args:
            name: Raw icon name from filename or symbol ID.

        Returns:
            Normalized icon name in lowercase with hyphens.

        """
        # Remove common prefixes
        name = re.sub(r"^(icon[-_]?|ic[-_]?)", "", name, flags=re.IGNORECASE)
        # Convert to lowercase and replace hyphens with underscores for consistency
        # but keep hyphens in the final output for CSS-friendly names
        return name.lower().replace("_", "-")

    def _extract_svg_content(self, svg_text: str) -> str | None:
        """Extract the SVG element from text, preserving internal structure.

        Args:
            svg_text: Raw SVG file content.

        Returns:
            Cleaned SVG element string, or None if no SVG found.

        """
        # Find the <svg> element and its contents
        match = re.search(r"<svg[^>]*>.*?</svg>", svg_text, re.DOTALL | re.IGNORECASE)
        if match:
            svg = match.group(0)
            # Add aria-hidden if not present
            if "aria-hidden" not in svg:
                svg = svg.replace("<svg", '<svg aria-hidden="true"', 1)
            return svg
        return None

    def _get_output_path(self, output_option: str | None) -> Path:
        """Determine the output path for the generated template.

        Args:
            output_option: User-specified output path, or None for default.

        Returns:
            Path where the icons.html template will be written.

        """
        if output_option:
            return Path(output_option)

        # Default: project templates directory
        # Try to find the project's template directory from settings
        template_dirs = getattr(settings, "TEMPLATES", [{}])
        if template_dirs and template_dirs[0].get("DIRS"):
            base_dir = Path(template_dirs[0]["DIRS"][0])
        else:
            # Fallback to BASE_DIR/templates
            base_dir = Path(getattr(settings, "BASE_DIR", ".")) / "templates"

        output_dir = base_dir / "insight_ui" / "components"
        output_dir.mkdir(parents=True, exist_ok=True)
        return output_dir / "icons.html"

    def _generate_template(self, icons: dict[str, str]) -> str:
        """Generate the icons.html template content.

        Args:
            icons: Dictionary mapping icon names to SVG content.

        Returns:
            Complete icons.html template as string.

        """
        lines = [
            '<div class="{% if icon_config.size == "xl" %}size-10'
            '{% elif icon_config.size == "l" %}size-8'
            '{% elif icon_config.size == "m" %}size-6'
            '{% elif icon_config.size == "s" %}size-5'
            '{% elif icon_config.size == "xs" %}size-4'
            '{% else %}size-6{% endif %}"'
            ' {% if color %}style="color: {{ color }};"{% endif %}>'
        ]

        sorted_icons = sorted(icons.items())
        for i, (name, svg_content) in enumerate(sorted_icons):
            condition = "{% if" if i == 0 else "{% elif"
            # Indent SVG content properly
            indented_svg = self._indent_svg(svg_content, spaces=8)
            lines.append(f'    {condition} icon_config.name == "{name}" %}}')
            lines.append(indented_svg)

        # Add fallback for unknown icons (question mark)
        fallback_svg = (
            '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" '
            'stroke-width="1.5" stroke="currentColor" aria-hidden="true">\n'
            '    <path stroke-linecap="round" stroke-linejoin="round" '
            'd="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 '
            "3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 "
            '1 1-18 0 9 9 0 0 1 18 0Zm-9 5.25h.008v.008H12v-.008Z" />\n'
            "</svg>"
        )
        lines.append("    {% else %}")
        lines.append(self._indent_svg(fallback_svg, spaces=8))
        lines.append("    {% endif %}")
        lines.append("</div>")
        lines.append("")  # Trailing newline

        return "\n".join(lines)

    def _indent_svg(self, svg: str, spaces: int = 8) -> str:
        """Properly indent SVG content.

        Removes existing indentation and applies consistent indentation,
        preserving relative indentation within the SVG.

        Args:
            svg: SVG content to indent.
            spaces: Number of spaces for indentation.

        Returns:
            Indented SVG content.

        """
        indent = " " * spaces
        svg_lines = svg.strip().split("\n")

        # Find minimum indentation of non-empty lines (excluding first line)
        min_indent = float("inf")
        for line in svg_lines[1:]:
            if line.strip():
                leading = len(line) - len(line.lstrip())
                min_indent = min(min_indent, leading)

        if min_indent == float("inf"):
            min_indent = 0

        # Remove common indentation and apply new indentation
        result_lines = []
        for i, line in enumerate(svg_lines):
            if not line.strip():
                result_lines.append(line)
            elif i == 0:
                result_lines.append(indent + line.strip())
            else:
                # Remove min_indent and add new base indent
                dedented = line[min_indent:] if len(line) >= min_indent else line.lstrip()
                result_lines.append(indent + dedented)

        return "\n".join(result_lines)

    def _write_output(self, output_path: Path, content: str) -> None:
        """Write the generated template to file.

        Args:
            output_path: Destination path for the template.
            content: Template content to write.

        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content, encoding="utf-8")

    def _get_bundled_icons(self) -> dict[str, str]:
        """Return the bundled icons from insight-ui.

        Returns:
            Dictionary of bundled icon names to SVG content.

        """
        from insight_ui.icons import BUNDLED_ICONS  # noqa: PLC0415

        return BUNDLED_ICONS
