# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Management command to scaffold a new UI component in insight_ui/."""

from __future__ import annotations

import re
import subprocess  # nosec B404
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any

from django.core.management.base import BaseCommand

if TYPE_CHECKING:
    from argparse import ArgumentParser

# Category mapping to section headers in insight_tags.py
CATEGORY_TO_SECTION = {
    "layout": "Layout Tags",
    "navigation": "Navigation Tags",
    "input": "Input Tags",
    "popup": "Popup Tags",
    "util": "Util Tags",
    "list": "List Tags",
    "filter": "Filter Tags",
    "card": "Card Tags",
    "form": "Form Tags",
}

CATEGORIES = list(CATEGORY_TO_SECTION.keys())

# Category mapping to config files
CATEGORY_TO_CONFIG_FILE = {
    "layout": "layout.py",
    "navigation": "navigation.py",
    "input": "input.py",
    "popup": "popup.py",
    "util": "utils.py",
    "list": "list.py",
    "filter": "filter.py",
    "card": "card.py",
    "form": "forms.py",
}

# Category mapping to __all__ section comments in configs/__init__.py
CATEGORY_TO_INIT_SECTION = {
    "layout": "# Layout",
    "navigation": "# Navigation",
    "input": "# Inputs",
    "popup": "# Popups",
    "util": "# Utils",
    "list": "# Lists",
    "filter": "# Filters",
    "card": "# Cards",
    "form": "# Forms",
}

COMPONENT_NAME_PATTERN = re.compile(r"^[a-zA-Z][a-zA-Z0-9 ]*$")


@dataclass
class ComponentNames:
    """Derived names for a component in various naming conventions."""

    name: str
    slug: str
    class_name: str
    js_slug: str
    config_class_name: str


class Command(BaseCommand):
    """Create boilerplate code for a new UI component in insight_ui/."""

    help = (
        "Creates boilerplate for a new component: config dataclass, template, inclusion tag, and optional JavaScript."
    )

    def add_arguments(self, parser: ArgumentParser) -> None:
        """Add command arguments."""
        parser.add_argument("--name", type=str, help="Component name in Title Case (e.g., 'My Component')")
        parser.add_argument("--category", type=str, choices=CATEGORIES, help="Component category")
        parser.add_argument("--js", action="store_true", default=None, help="Create JavaScript file for the component")

    def _get_validated_name(self, name: str | None) -> str | None:
        """Get and validate component name from option or user input."""
        if not name:
            name = input("Enter component name (Title Case, e.g., 'My Component'): ").strip()

        if not name:
            self.stderr.write(self.style.ERROR("Component name is required."))
            return None

        if not COMPONENT_NAME_PATTERN.match(name):
            self.stderr.write(
                self.style.ERROR(
                    "Component name must start with a letter and contain only letters, numbers, and spaces."
                )
            )
            return None

        return name

    def _get_category(self, category: str | None) -> str | None:
        """Get category from option or user input."""
        if category:
            return category

        self.stdout.write("\nAvailable categories:")
        for i, cat in enumerate(CATEGORIES, 1):
            self.stdout.write(f"  {i}. {cat}")
        choice = input("\nEnter category number or name: ").strip()

        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(CATEGORIES):
                return CATEGORIES[idx]
            self.stderr.write(self.style.ERROR("Invalid category number."))
            return None

        if choice.lower() in CATEGORIES:
            return choice.lower()

        self.stderr.write(self.style.ERROR(f"Invalid category: {choice}"))
        return None

    def _should_create_js(self, js_option: bool | None) -> bool:
        """Determine if JavaScript file should be created."""
        if js_option is not None:
            return js_option
        js_choice = input("\nDoes this component need JavaScript? [y/N]: ").strip().lower()
        return js_choice in ("y", "yes", "j", "ja")

    def _derive_names(self, name: str) -> ComponentNames:
        """Derive all name variants from the component name."""
        words = re.findall(r"[a-zA-Z0-9]+", name)
        slug = "_".join(word.lower() for word in words)
        class_name = "".join(word[:1].upper() + word[1:] for word in words)
        return ComponentNames(
            name=name,
            slug=slug,
            class_name=class_name,
            js_slug=slug.replace("_", "-"),
            config_class_name=f"{class_name}Config",
        )

    def handle(self, *args: Any, **options: Any) -> None:  # noqa: ANN401, ARG002
        """Execute the command to scaffold a new UI component."""
        name = self._get_validated_name(options.get("name"))
        if not name:
            return

        category = self._get_category(options.get("category"))
        if not category:
            return

        needs_js = self._should_create_js(options.get("js"))
        names = self._derive_names(name)
        git_user = self._get_git_username()

        self.stdout.write(f"\nCreating component '{name}'...")
        self.stdout.write(f"  Slug: {names.slug}")
        self.stdout.write(f"  Category: {category}")
        self.stdout.write(f"  JavaScript: {'yes' if needs_js else 'no'}")
        self.stdout.write(f"  Author: {git_user}")

        # insight_ui/ package path
        ui_path = Path(__file__).resolve().parent.parent.parent.parent / "insight_ui"
        self._scaffold_component(ui_path, names, category, needs_js, git_user)

    def _scaffold_component(
        self, ui_path: Path, names: ComponentNames, category: str, needs_js: bool, git_user: str
    ) -> None:
        """Create all component files in insight_ui/."""
        # 1. Create HTML template
        self._create_template(ui_path, names.slug, names.name, git_user)

        # 2. Create config dataclass
        self._create_config_dataclass(ui_path, names.config_class_name, names.slug, category, names.name, git_user)

        # 3. Add inclusion tag to insight_tags.py
        self._add_inclusion_tag(ui_path, names.slug, category, names.name, names.config_class_name)

        # 4. Create JavaScript file if requested
        if needs_js:
            self._create_javascript(ui_path, names.js_slug, names.class_name, names.slug, git_user)

        self._print_success(names, category, needs_js)

    def _print_success(self, names: ComponentNames, category: str, needs_js: bool) -> None:
        """Print success message and next steps."""
        self.stdout.write(self.style.SUCCESS(f"\nComponent '{names.name}' created successfully!"))
        self.stdout.write("\nNext steps:")
        self.stdout.write(f"  1. Edit the template: insight_ui/templates/insight_ui/components/{names.slug}.html")
        self.stdout.write(f"  2. Add fields to the config: insight_ui/configs/{CATEGORY_TO_CONFIG_FILE[category]}")
        if needs_js:
            self.stdout.write(
                f"  3. Edit the JavaScript: insight_ui/static/insight_ui/js/insight-ui-{names.js_slug}.js"
            )
            self.stdout.write("  4. Register the class in insight-ui-init.js")
        self.stdout.write("\n  5. Test in playground: uv run python manage.py runserver --settings=devtools.settings")
        self.stdout.write(f"     Then edit devtools/views.py to add your {names.config_class_name}")

    def _find_category_section_end(self, content: str, category: str) -> int | None:
        """Find the end position of a category section in insight_tags.py."""
        section_header = CATEGORY_TO_SECTION[category]
        section_pattern = rf"#\s*=+\s*\n#\s*\n#\s+{re.escape(section_header)}\s*\n#\s*\n#\s*=+"
        match = re.search(section_pattern, content, re.IGNORECASE)

        if not match:
            return None

        next_section_pattern = r"#\s*=+\s*\n#\s*\n#\s+\w+.*Tags\s*\n#\s*\n#\s*=+"
        remaining = content[match.end() :]
        next_match = re.search(next_section_pattern, remaining)

        if next_match:
            return match.end() + next_match.start()
        return len(content)

    def _read_file(self, file_path: Path) -> str | None:
        """Read file contents with error handling."""
        try:
            return file_path.read_text(encoding="utf-8")
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f"File not found: {file_path}"))
            return None
        except PermissionError:
            self.stderr.write(self.style.ERROR(f"Permission denied: {file_path}"))
            return None

    def _write_file(self, file_path: Path, content: str) -> bool:
        """Write file contents with error handling."""
        try:
            file_path.write_text(content, encoding="utf-8")
        except PermissionError:
            self.stderr.write(self.style.ERROR(f"Permission denied: {file_path}"))
            return False
        else:
            return True

    def _get_git_username(self) -> str:
        """Get the Git username from the local or global config."""
        try:
            result = subprocess.run(
                ["git", "config", "user.name"],  # noqa: S607  # nosec B603, B607
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
        except FileNotFoundError:
            pass
        return "Unknown"

    def _add_config_import(self, content: str, config_class_name: str) -> str:
        """Add a config class to the parenthesized insight_ui.configs import block."""
        if re.search(rf"^\s+{re.escape(config_class_name)},$", content, re.MULTILINE):
            return content

        import_pattern = r"(from insight_ui\.configs import \(\n)((?:\s+\w+,\n)+)"
        match = re.search(import_pattern, content)
        if not match:
            return content

        imports = match.group(2).splitlines()
        imports.append(f"    {config_class_name},")
        imports = sorted(set(imports), key=str.lower)
        replacement = match.group(1) + "\n".join(imports) + "\n"
        return content[: match.start()] + replacement + content[match.end() :]

    def _create_template(self, ui_path: Path, slug: str, name: str, git_user: str) -> None:
        """Create the HTML template file for the component."""
        template_dir = ui_path / "templates" / "insight_ui" / "components"
        template_path = template_dir / f"{slug}.html"

        if template_path.exists():
            self.stdout.write(f"  [SKIP] Template {slug}.html already exists")
            return

        container_classes = " ".join(
            (
                "insight-surface-base",
                "insight-border-default",
                "rounded-[var(--insight-radius-md)]",
                "border",
                "p-4",
                "text-insight-headline",
            )
        )
        template_content = f"""{{% load insight_tags %}}

<!-- {name} Component -->
<div class="{container_classes}">
    <!-- TODO({git_user}): Implement {name} component -->
    <p class="text-insight-body">{name} component placeholder</p>
</div>
"""
        if self._write_file(template_path, template_content):
            self.stdout.write(self.style.SUCCESS(f"  [OK] Created template {slug}.html"))

    def _add_inclusion_tag(self, ui_path: Path, slug: str, category: str, name: str, config_class_name: str) -> None:
        """Add inclusion tag to insight_tags.py."""
        file_path = ui_path / "templatetags" / "insight_tags.py"
        content = self._read_file(file_path)
        if content is None:
            return

        if f"def {slug}(" in content:
            self.stdout.write(f"  [SKIP] Inclusion tag {slug} already exists")
            return

        content = self._add_config_import(content, config_class_name)
        section_end = self._find_category_section_end(content, category)

        if section_end is None:
            self.stderr.write(
                self.style.WARNING(f"  [WARN] Could not find category section for {category} in insight_tags.py")
            )
            return

        new_tag = f'''@register.inclusion_tag("insight_ui/components/{slug}.html")
def {slug}(config: {config_class_name} | None = None, *, tag_id: str | _Unset = UNSET) -> dict[str, Any]:
    """Render the {name.lower()} component."""
    config = build_config({config_class_name}, config, tag_id=tag_id)
    return {{"{slug}_config": config}}


'''
        new_content = content[:section_end] + new_tag + content[section_end:]
        if self._write_file(file_path, new_content):
            self.stdout.write(self.style.SUCCESS(f"  [OK] Added {slug} inclusion tag to insight_tags.py"))

    def _create_javascript(self, ui_path: Path, js_slug: str, class_name: str, slug: str, git_user: str) -> None:
        """Create the JavaScript file with class boilerplate."""
        js_dir = ui_path / "static" / "insight_ui" / "js"
        js_path = js_dir / f"insight-ui-{js_slug}.js"

        if js_path.exists():
            self.stdout.write(f"  [SKIP] JavaScript file insight-ui-{js_slug}.js already exists")
            return

        data_attr = f"data-insight-{js_slug}"
        slug_readable = slug.replace("_", " ")

        js_content = f"""export class {class_name} {{
    static instances = new WeakMap();

    constructor(element) {{
        if ({class_name}.instances.has(element)) {{
            debugLog("Element already instantiated: ", element);
            return {class_name}.instances.get(element);
        }}

        this.element = element;
        this.boundHandlers = [];

        this.bindEvents();

        this.element.__insightInstance = this;
        {class_name}.instances.set(element, this);

        debugLog("New {slug_readable} created: ", this.element);
    }}

    bindEvents() {{
        // TODO({git_user}): Add event listeners here
    }}

    destroy() {{
        debugLog("Destroy {slug_readable}: ", this.element);

        this.boundHandlers.forEach(({{ element, type, handler }}) => {{
            element.removeEventListener(type, handler);
        }});
        this.boundHandlers = [];

        {class_name}.instances.delete(this.element);
        delete this.element.__insightInstance;

        this.element = null;
    }}

    static initAll() {{
        document.querySelectorAll("[{data_attr}]").forEach(el => new {class_name}(el));
    }}
}}
"""
        if self._write_file(js_path, js_content):
            self.stdout.write(self.style.SUCCESS(f"  [OK] Created JavaScript file insight-ui-{js_slug}.js"))

    def _create_config_dataclass(  # noqa: PLR0913, PLR0917
        self, ui_path: Path, config_class_name: str, slug: str, category: str, name: str, git_user: str
    ) -> None:
        """Create config dataclass in the appropriate config file and update __init__.py."""
        config_file = CATEGORY_TO_CONFIG_FILE[category]
        file_path = ui_path / "configs" / config_file
        content = self._read_file(file_path)
        if content is None:
            return

        if f"class {config_class_name}" in content:
            self.stdout.write(f"  [SKIP] Config class {config_class_name} already exists in {config_file}")
            return

        new_class = f'''

@dataclass
class {config_class_name}:
    """Configuration for the {slug.replace("_", " ")} component.

    Renders a {name.lower()} element.

    Attributes:
        tag_id: Unique ID for JavaScript/CSS targeting.

    """

    __example__ = """
        {config_class_name}(
            tag_id="{slug}-1",
        )
        """

    # TODO({git_user}): Add component-specific configuration fields
    tag_id: str = field(default="", metadata={{"doc": _("Unique ID for JavaScript/CSS targeting.")}})
'''
        new_content = content.rstrip() + new_class + "\n"
        if self._write_file(file_path, new_content):
            self.stdout.write(self.style.SUCCESS(f"  [OK] Added {config_class_name} to configs/{config_file}"))

        self._add_config_to_init(ui_path, config_class_name, config_file, category)

    def _add_config_to_init(self, ui_path: Path, config_class_name: str, config_file: str, category: str) -> None:
        """Add config class to configs/__init__.py imports and __all__."""
        init_path = ui_path / "configs" / "__init__.py"
        content = self._read_file(init_path)
        if content is None:
            return

        if config_class_name in content:
            self.stdout.write(f"  [SKIP] {config_class_name} already in configs/__init__.py")
            return

        module_name = config_file.replace(".py", "")

        # Add to import statement
        import_pattern = rf"(from insight_ui\.configs\.{module_name} import \(\n)((?:\s+\w+,\n)*)"
        import_match = re.search(import_pattern, content)

        if import_match:
            import_end = import_match.end()
            new_import_line = f"    {config_class_name},\n"
            content = content[:import_end] + new_import_line + content[import_end:]
        else:
            single_import_pattern = rf"from insight_ui\.configs\.{module_name} import (\w+(?:,\s*\w+)*)"
            single_match = re.search(single_import_pattern, content)
            if single_match:
                old_import = single_match.group(0)
                imports = single_match.group(1).split(",")
                imports = [i.strip() for i in imports]
                imports.append(config_class_name)
                imports.sort()
                new_import = f"from insight_ui.configs.{module_name} import (\n"
                for imp in imports:
                    new_import += f"    {imp},\n"
                new_import += ")"
                content = content.replace(old_import, new_import)

        # Add to __all__ list
        section_comment = CATEGORY_TO_INIT_SECTION.get(category, f"# {category.title()}")
        all_section_pattern = rf'({re.escape(section_comment)}\n)((?:\s+"[^"]+",\n)*)'
        all_match = re.search(all_section_pattern, content)

        if all_match:
            section_end = all_match.end()
            new_all_entry = f'    "{config_class_name}",\n'
            content = content[:section_end] + new_all_entry + content[section_end:]
        else:
            all_end_pattern = r"(\])\s*$"
            all_end_match = re.search(all_end_pattern, content)
            if all_end_match:
                insert_pos = all_end_match.start()
                new_all_entry = f'    # {category.title()}\n    "{config_class_name}",\n'
                content = content[:insert_pos] + new_all_entry + content[insert_pos:]

        if self._write_file(init_path, content):
            self.stdout.write(self.style.SUCCESS(f"  [OK] Added {config_class_name} to configs/__init__.py"))
