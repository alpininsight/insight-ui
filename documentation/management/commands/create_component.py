"""Management command to scaffold a new UI component."""

from __future__ import annotations

import re
import subprocess  # nosec B404
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any

from django.core.management.base import BaseCommand

if TYPE_CHECKING:
    from argparse import ArgumentParser

# Category mapping to section headers in context files
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

# Categories available in ComponentCategory enum
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

CATEGORY_TO_GIT_MAPPING_SECTION = {
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

# Regex pattern for valid component names
COMPONENT_NAME_PATTERN = re.compile(r"^[a-zA-Z][a-zA-Z0-9 ]*$")


@dataclass
class ContextFileConfig:
    """Configuration for adding a function to a context file.

    Attributes:
        file_name: The context file name (e.g., 'a11y_context.py').
        func_suffix: The function name suffix (e.g., 'a11y_context').
        decorator: The decorator to use (e.g., '@register_component').
        return_type: The function return type annotation.
        template: The function body template with placeholders.

    """

    file_name: str
    func_suffix: str
    decorator: str
    return_type: str
    template: str


@dataclass
class ComponentNames:
    """Derived names for a component in various naming conventions.

    Attributes:
        name: Original title case name (e.g., 'My Component').
        enum_name: UPPER_SNAKE_CASE for enum entries (e.g., 'MY_COMPONENT').
        slug: snake_case for file names and identifiers (e.g., 'my_component').
        func_name: snake_case for function names (same as slug).
        class_name: PascalCase for JavaScript classes (e.g., 'MyComponent').
        js_slug: kebab-case for JavaScript file names (e.g., 'my-component').
        config_class_name: PascalCase + Config suffix (e.g., 'MyComponentConfig').

    """

    name: str
    enum_name: str
    slug: str
    func_name: str
    class_name: str
    js_slug: str
    config_class_name: str


class Command(BaseCommand):
    """Create boilerplate code for a new UI component."""

    help = "Creates boilerplate code for a new UI component including enum entry, context functions, template, and inclusion tag."  # noqa: E501

    def add_arguments(self, parser: ArgumentParser) -> None:
        """Add command arguments.

        Args:
            parser: The argument parser to add arguments to.

        """
        parser.add_argument("--name", type=str, help="Component name in Title Case (e.g., 'My Component')")
        parser.add_argument("--category", type=str, choices=CATEGORIES, help="Component category")
        parser.add_argument("--js", action="store_true", default=None, help="Create JavaScript file for the component")

    def _get_validated_name(self, name: str | None) -> str | None:
        """Get and validate component name from option or user input.

        Prompts the user for input if name is not provided. Validates that the name
        starts with a letter and contains only letters, numbers, and spaces.

        Args:
            name: The component name from command options, or None.

        Returns:
            The validated component name, or None if validation failed.

        """
        if not name:
            name = input("Enter component name (Title Case, e.g., 'My Component'): ").strip()

        if not name:
            self.stderr.write(self.style.ERROR("Component name is required."))
            return None

        if not COMPONENT_NAME_PATTERN.match(name):
            self.stderr.write(
                self.style.ERROR(
                    "Component name must start with uppercase and contain only letters, numbers, and spaces."
                )
            )
            return None

        return name

    def _get_category(self, category: str | None) -> str | None:
        """Get category from option or user input.

        Displays available categories and prompts the user for selection if category
        is not provided. Accepts either a category number or name.

        Args:
            category: The category from command options, or None.

        Returns:
            The selected category name, or None if selection failed.

        """
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
        """Determine if JavaScript file should be created.

        Prompts the user for input if js_option is not provided.

        Args:
            js_option: The --js flag from command options, or None.

        Returns:
            True if JavaScript file should be created, False otherwise.

        """
        if js_option is not None:
            return js_option
        js_choice = input("\nDoes this component need JavaScript? [y/N]: ").strip().lower()
        return js_choice in ("y", "yes", "j", "ja")

    def _derive_names(self, name: str) -> ComponentNames:
        """Derive all name variants from the component name.

        Converts the title case component name into various naming conventions
        used throughout the codebase.

        Args:
            name: The component name in Title Case (e.g., 'My Component').

        Returns:
            A dataclass containing all derived name variants.

        """
        words = re.findall(r"[a-zA-Z0-9]+", name)
        enum_name = "_".join(word.upper() for word in words)
        slug = "_".join(word.lower() for word in words)
        class_name = "".join(word[:1].upper() + word[1:] for word in words)
        return ComponentNames(
            name=name,
            enum_name=enum_name,
            slug=slug,
            func_name=slug,
            class_name=class_name,
            js_slug=slug.replace("_", "-"),
            config_class_name=f"{class_name}Config",
        )

    def handle(self, *args: Any, **options: Any) -> None:  # noqa: ANN401, ARG002
        """Execute the command to scaffold a new UI component.

        Args:
            *args: Positional arguments (unused).
            **options: Command options including name, category, and js.

        """
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
        self.stdout.write(f"  Enum name: {names.enum_name}")
        self.stdout.write(f"  Slug: {names.slug}")
        self.stdout.write(f"  Category: {category}")
        self.stdout.write(f"  JavaScript: {'yes' if needs_js else 'no'}")
        self.stdout.write(f"  Author: {git_user}")

        # documentation/ - contains component_details/ and docs templates
        doc_path = Path(__file__).resolve().parent.parent.parent
        # insight_ui/ - contains configs/, templatetags/, templates/components/, static/
        ui_path = doc_path.parent / "insight_ui"
        self._scaffold_component(doc_path, ui_path, names, category, needs_js, git_user)

    def _scaffold_component(  # noqa: PLR0913, PLR0917
        self, doc_path: Path, ui_path: Path, names: ComponentNames, category: str, needs_js: bool, git_user: str
    ) -> None:
        """Create all component files and entries.

        Orchestrates the creation of all necessary files and code entries for a new
        component, including enum entry, context functions, template, config dataclass,
        inclusion tag, and optionally JavaScript.

        Args:
            doc_path: The base path of the documentation package.
            ui_path: The base path of the insight_ui package.
            names: The derived name variants for the component.
            category: The component category (e.g., 'layout', 'input').
            needs_js: Whether to create a JavaScript file for the component.
            git_user: The Git username for TODO comments.

        """
        # 1. Add to components.py (documentation app)
        self._add_to_components_py(doc_path, names.enum_name, names.slug, category, names.config_class_name)

        # 2. Add to context files (documentation app)
        context_configs = self._get_context_configs()
        for config in context_configs:
            self._add_to_context_file(doc_path, names.enum_name, names.func_name, category, config, git_user)

        # 3. Add to related_components_context.py (documentation app)
        self._add_to_related_components(doc_path, names.enum_name, category)

        # 4. Create HTML template (insight_ui app)
        self._create_template(ui_path, names.slug, names.name, git_user)

        # 5. Create config dataclass (insight_ui app)
        self._create_config_dataclass(ui_path, names.config_class_name, names.func_name, category, names.name, git_user)

        # 6. Add inclusion tag to insight_tags.py (insight_ui app)
        self._add_inclusion_tag(ui_path, names.func_name, names.slug, category, names.name, names.config_class_name)

        # 7. Create JavaScript file if requested (insight_ui app)
        if needs_js:
            self._create_javascript(ui_path, names.js_slug, names.class_name, names.slug, git_user)

        # 8. Add demo entry to component_demo.html (documentation app)
        self._add_to_component_demo(doc_path, names.slug, names.func_name)

        # 9. Add GitHub source links for self-documentation (documentation app)
        self._add_to_git_path_mapping(doc_path, names.slug, names.js_slug, category, needs_js)

        self._print_success(names, category, needs_js)

    def _get_context_configs(self) -> list[ContextFileConfig]:
        """Return the list of context file configurations.

        Defines the configuration for each context file that needs a function added
        when creating a new component (a11y, demo, description, usage, parameters).

        Returns:
            List of context file configurations.

        """
        return [
            ContextFileConfig(
                file_name="a11y_context.py",
                func_suffix="a11y_context",
                decorator="@register_component",
                return_type="dict[str, list[str]]",
                template='{{"a11y": []}}  # TODO({git_user}): Add accessibility guidelines',
            ),
            ContextFileConfig(
                file_name="demo_context.py",
                func_suffix="context",
                decorator="@register_demo_context",
                return_type="dict",
                template="{{}}  # TODO({git_user}): Add demo context data",
            ),
            ContextFileConfig(
                file_name="description_context.py",
                func_suffix="description_context",
                decorator="@register_component",
                return_type="dict[str, list[str]]",
                template="""{{"description": [_("The `{func_name}` component ...")]}}  # TODO({git_user}): Write description""",  # noqa: E501
            ),
            ContextFileConfig(
                file_name="usage_context.py",
                func_suffix="usage_context",
                decorator="@register_component",
                return_type="dict[str, str]",
                template="""{{"usage": \"\"\"
        {{% load insight_tags %}}

        {{% {func_name} config={func_name}_config %}}
        \"\"\"
    }}  # TODO({git_user}): Update usage example""",
            ),
            ContextFileConfig(
                file_name="parameter_context.py",
                func_suffix="parameter_context",
                decorator="@register_component",
                return_type="dict[str, list[str]]",
                template="""{{
        "params": [
            ParameterDoc(
                None,
                [
                    ParameterDetails(
                        "tag_id",
                        "str",
                        _("Optional unique ID for JavaScript/CSS targeting."),
                        "''",
                    ),
                ],
                "",
            )
        ]
    }}  # TODO({git_user}): Add component-specific parameter documentation""",
            ),
        ]

    def _print_success(self, names: ComponentNames, category: str, needs_js: bool) -> None:
        """Print success message and next steps.

        Displays a summary of the created component and provides guidance on what
        files to edit next to complete the component implementation.

        Args:
            names: The derived name variants for the component.
            category: The component category for config file reference.
            needs_js: Whether JavaScript was created (affects next steps).

        """
        self.stdout.write(self.style.SUCCESS(f"\nComponent '{names.name}' created successfully!"))
        self.stdout.write("\nNext steps:")
        self.stdout.write(f"  1. Edit the template: templates/insight_ui/components/{names.slug}.html")
        self.stdout.write("  2. Fill in the context functions in component_details/")
        self.stdout.write(f"  3. Add fields to the config dataclass: configs/{CATEGORY_TO_CONFIG_FILE[category]}")
        if needs_js:
            self.stdout.write(f"  4. Edit the JavaScript: static/insight_ui/js/insight-ui-{names.js_slug}.js")
            self.stdout.write("  5. Register the class in insight-ui-init.js")

    def _find_category_section_end(self, content: str, category: str) -> int | None:
        """Find the end position of a category section (before next section or EOF).

        Args:
            content: The file content to search in.
            category: The category name to find the section for.

        Returns:
            The character position of the section end, or None if not found.

        """
        section_header = CATEGORY_TO_SECTION[category]
        # Pattern to find section start - handles multi-line headers like:
        # # =============
        # #
        # #   Util Tags
        # #
        # # =============
        section_pattern = rf"#\s*=+\s*\n#\s*\n#\s+{re.escape(section_header)}\s*\n#\s*\n#\s*=+"
        match = re.search(section_pattern, content, re.IGNORECASE)

        if not match:
            return None

        # Find the next section header or end of file
        next_section_pattern = r"#\s*=+\s*\n#\s*\n#\s+\w+.*Tags\s*\n#\s*\n#\s*=+"
        remaining = content[match.end() :]
        next_match = re.search(next_section_pattern, remaining)

        if next_match:
            return match.end() + next_match.start()
        return len(content)

    def _read_file(self, file_path: Path) -> str | None:
        """Read file contents with error handling.

        Args:
            file_path: The path to the file to read.

        Returns:
            The file contents, or None if reading failed.

        """
        try:
            return file_path.read_text(encoding="utf-8")
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f"File not found: {file_path}"))
            return None
        except PermissionError:
            self.stderr.write(self.style.ERROR(f"Permission denied: {file_path}"))
            return None

    def _write_file(self, file_path: Path, content: str) -> bool:
        """Write file contents with error handling.

        Args:
            file_path: The path to the file to write.
            content: The content to write to the file.

        Returns:
            True if writing succeeded, False otherwise.

        """
        try:
            file_path.write_text(content, encoding="utf-8")
        except PermissionError:
            self.stderr.write(self.style.ERROR(f"Permission denied: {file_path}"))
            return False
        else:
            return True

    def _get_git_username(self) -> str:
        """Get the Git username from the local or global config.

        Returns:
            The Git username, or 'Unknown' if not configured.

        """
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
            pass  # git not installed
        return "Unknown"

    def _add_to_context_file(  # noqa: PLR0913, PLR0917
        self, doc_path: Path, enum_name: str, func_name: str, category: str, config: ContextFileConfig, git_user: str
    ) -> None:
        """Add a function to a context file using the provided configuration.

        Args:
            doc_path: The base path of the documentation package.
            enum_name: The enum name of the component (e.g., 'MY_COMPONENT').
            func_name: The function name prefix (e.g., 'my_component').
            category: The component category (e.g., 'layout', 'input').
            config: Configuration for the context file and function template.
            git_user: The Git username for TODO comments.

        """
        file_path = doc_path / "component_details" / config.file_name
        content = self._read_file(file_path)
        if content is None:
            return

        full_func_name = f"get_{func_name}_{config.func_suffix}"

        # Check if already exists
        if full_func_name in content:
            self.stdout.write(f"  [SKIP] Function {full_func_name} already exists")
            return

        # Find the end of the category section
        section_end = self._find_category_section_end(content, category)

        if section_end is None:
            self.stderr.write(
                self.style.WARNING(f"  [WARN] Could not find category section for {category} in {config.file_name}")
            )
            return

        # Format the template with component-specific values
        func_body = config.template.format(
            enum_name=enum_name,
            func_name=func_name,
            func_suffix=config.func_suffix,
            readable_name=func_name.replace("_", " "),
            git_user=git_user,
        )

        suffix_readable = config.func_suffix.replace("_", " ")
        func_readable = func_name.replace("_", " ")
        new_func = f"""{config.decorator}(Component.{enum_name})
def {full_func_name}() -> {config.return_type}:
    \"\"\"Serve {suffix_readable} documentation for the {func_readable} component.\"\"\"
    return {func_body}


"""
        # Insert before the next section
        new_content = content[:section_end] + new_func + content[section_end:]
        if self._write_file(file_path, new_content):
            self.stdout.write(self.style.SUCCESS(f"  [OK] Added {full_func_name} to {config.file_name}"))

    def _add_to_components_py(
        self, doc_path: Path, enum_name: str, slug: str, category: str, config_class_name: str
    ) -> None:
        """Add enum entry to components.py.

        Args:
            doc_path: The base path of the documentation package.
            enum_name: The enum name of the component (e.g., 'MY_COMPONENT').
            slug: The component slug (e.g., 'my_component').
            category: The component category (e.g., 'layout', 'input').
            config_class_name: The generated config class name.

        """
        file_path = doc_path / "component_details" / "components.py"
        content = self._read_file(file_path)
        if content is None:
            return

        # Check if already exists
        if f"{enum_name} = " in content:
            self.stdout.write(f"  [SKIP] Component {enum_name} already exists in components.py")
            return

        content = self._add_config_import(content, config_class_name)

        # Find the last entry for this category in the Component enum
        category_upper = category.upper()

        # Find all enum entries for this category
        pattern = rf"(\w+)\s*=\s*\([^)]*ComponentCategory\.{category_upper}[^)]*\)"
        matches = list(re.finditer(pattern, content))

        if matches:
            # Insert after the last match of this category
            last_match = matches[-1]
            insert_pos = last_match.end()

            new_entry = f'\n    {enum_name} = ("{slug}", ComponentCategory.{category_upper}, {config_class_name})'

            new_content = content[:insert_pos] + new_entry + content[insert_pos:]
            if self._write_file(file_path, new_content):
                self.stdout.write(self.style.SUCCESS(f"  [OK] Added {enum_name} to components.py"))
        else:
            self.stderr.write(self.style.WARNING(f"  [WARN] Could not find category {category} in components.py"))

    def _add_config_import(self, content: str, config_class_name: str) -> str:
        """Add a config class to the parenthesized ``insight_ui.configs`` import block."""
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

    def _add_to_related_components(self, doc_path: Path, enum_name: str, category: str) -> None:
        """Add entry to related_components_context.py.

        Args:
            doc_path: The base path of the documentation package.
            enum_name: The enum name of the component (e.g., 'MY_COMPONENT').
            category: The component category (e.g., 'layout', 'input').

        """
        file_path = doc_path / "component_details" / "related_components_context.py"
        content = self._read_file(file_path)
        if content is None:
            return

        # Check if already exists
        if f"C.{enum_name}:" in content:
            self.stdout.write(f"  [SKIP] Entry C.{enum_name} already exists in related_components_context.py")
            return

        # Reuse CATEGORY_TO_INIT_SECTION for section comments
        comment = CATEGORY_TO_INIT_SECTION.get(category, f"# {category.title()}")

        # Find the section and the last entry in it
        pattern = rf"{re.escape(comment)}\s*\n((?:\s+C\.\w+:.*\n)*)"
        match = re.search(pattern, content)

        if match:
            # Insert after the last entry in this category section
            section_end = match.end()
            new_entry = f"    C.{enum_name}: [],\n"
            new_content = content[:section_end] + new_entry + content[section_end:]
            if self._write_file(file_path, new_content):
                self.stdout.write(self.style.SUCCESS(f"  [OK] Added C.{enum_name} to related_components_context.py"))
        else:
            self.stderr.write(
                self.style.WARNING(
                    f"  [WARN] Could not find category section for {category} in related_components_context.py"
                )
            )

    def _create_template(self, ui_path: Path, slug: str, name: str, git_user: str) -> None:
        """Create the HTML template file for the component.

        Args:
            ui_path: The base path of the insight_ui package.
            slug: The component slug used for the filename (e.g., 'my_component').
            name: The display name of the component (e.g., 'My Component').
            git_user: The Git username for TODO comments.

        """
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
        placeholder_classes = " ".join(("text-insight-body",))
        template_content = f"""{{% load insight_tags %}}

<!-- {name} Component -->
<div class="{container_classes}">
    <!-- TODO({git_user}): Implement {name} component -->
    <p class="{placeholder_classes}">{name} component placeholder</p>
</div>
"""
        if self._write_file(template_path, template_content):
            self.stdout.write(self.style.SUCCESS(f"  [OK] Created template {slug}.html"))

    def _add_inclusion_tag(  # noqa: PLR0913, PLR0917
        self, ui_path: Path, func_name: str, slug: str, category: str, name: str, config_class_name: str
    ) -> None:
        """Add inclusion tag to insight_tags.py.

        Args:
            ui_path: The base path of the insight_ui package.
            func_name: The function name for the tag (e.g., 'my_component').
            slug: The component slug for the template path (e.g., 'my_component').
            category: The component category (e.g., 'layout', 'input').
            name: The display name of the component (e.g., 'My Component').
            config_class_name: The config dataclass name (e.g., 'MyComponentConfig').

        """
        file_path = ui_path / "templatetags" / "insight_tags.py"
        content = self._read_file(file_path)
        if content is None:
            return

        # Check if already exists
        if f"def {func_name}(" in content:
            self.stdout.write(f"  [SKIP] Inclusion tag {func_name} already exists")
            return

        content = self._add_config_import(content, config_class_name)
        section_end = self._find_category_section_end(content, category)

        if section_end is None:
            self.stderr.write(
                self.style.WARNING(f"  [WARN] Could not find category section for {category} in insight_tags.py")
            )
            return

        # Create new inclusion tag with config parameter
        new_tag = f"""@register.inclusion_tag("insight_ui/components/{slug}.html")
def {func_name}(config: {config_class_name} | None = None, *, tag_id: str | _Unset = UNSET) -> dict[str, Any]:
    \"\"\"Render the {name.lower()} component.\"\"\"
    config = build_config({config_class_name}, config, tag_id=tag_id)
    return {{"{func_name}_config": config}}


"""
        # Insert before the next section
        new_content = content[:section_end] + new_tag + content[section_end:]
        if self._write_file(file_path, new_content):
            self.stdout.write(self.style.SUCCESS(f"  [OK] Added {func_name} inclusion tag to insight_tags.py"))

    def _add_to_git_path_mapping(self, doc_path: Path, slug: str, js_slug: str, category: str, needs_js: bool) -> None:
        """Add template and optional script source links to git_path_mapping.py."""
        file_path = doc_path / "component_details" / "git_path_mapping.py"
        content = self._read_file(file_path)
        if content is None:
            return

        section_comment = CATEGORY_TO_GIT_MAPPING_SECTION.get(category, f"# {category.title()}")
        content = self._add_mapping_entry(
            content,
            mapping_name="TEMPLATE_PATHS",
            section_comment=section_comment,
            key=slug,
            value=f'GIT_BASE_FILE + "{slug}.html"',
        )
        if needs_js:
            content = self._add_mapping_entry(
                content,
                mapping_name="SCRIPT_PATHS",
                section_comment=section_comment,
                key=slug,
                value=f'GIT_BASE_SCRIPT_FILE + "insight-ui-{js_slug}.js"',
            )

        if self._write_file(file_path, content):
            self.stdout.write(self.style.SUCCESS(f"  [OK] Updated git_path_mapping.py for {slug}"))

    def _add_mapping_entry(self, content: str, *, mapping_name: str, section_comment: str, key: str, value: str) -> str:
        """Insert a dict entry in a documented section when the key is not present."""
        mapping_start = content.find(f"{mapping_name} = {{")
        if mapping_start == -1:
            return content

        mapping_end = content.find("\n}", mapping_start)
        if mapping_end == -1:
            return content

        mapping_content = content[mapping_start:mapping_end]
        if re.search(rf'^\s+"{re.escape(key)}":', mapping_content, re.MULTILINE):
            return content

        section_start = content.find(f"    {section_comment}", mapping_start, mapping_end)
        if section_start == -1:
            insert_pos = mapping_end
        else:
            next_section = content.find("\n    # ", section_start + 1, mapping_end)
            insert_pos = next_section if next_section != -1 else mapping_end

        new_entry = f'    "{key}": {value},\n'
        return content[:insert_pos] + new_entry + content[insert_pos:]

    def _create_javascript(self, ui_path: Path, js_slug: str, class_name: str, slug: str, git_user: str) -> None:
        """Create the JavaScript file with class boilerplate.

        Args:
            ui_path: The base path of the insight_ui package.
            js_slug: The slug for the JS filename (e.g., 'my-component').
            class_name: The JavaScript class name (e.g., 'MyComponent').
            slug: The component slug for logging (e.g., 'my_component').
            git_user: The Git username for TODO comments.

        """
        js_dir = ui_path / "static" / "insight_ui" / "js"
        js_path = js_dir / f"insight-ui-{js_slug}.js"

        if js_path.exists():
            self.stdout.write(f"  [SKIP] JavaScript file insight-ui-{js_slug}.js already exists")
            return

        # data-insight attribute for DOM selection (e.g., "data-insight-my-component")
        data_attr = f"data-insight-{js_slug}"

        js_content = f"""export class {class_name} {{
    // Weak references used to prevent multiple initialization of the same instance
    static instances = new WeakMap();

    constructor(element) {{
        // If an instance for this element already exists, return it
        if ({class_name}.instances.has(element)) {{
            debugLog("Element already instantiated: ", element);
            return {class_name}.instances.get(element);
        }}

        this.element = element;

        // Store bound handlers for cleanup
        this.boundHandlers = [];

        this.bindEvents();

        this.element.__insightInstance = this;
        {class_name}.instances.set(element, this);

        debugLog("New {slug.replace("_", " ")} created: ", this.element);
    }}

    bindEvents() {{
        // TODO({git_user}): Add event listeners here
        // Example:
        // const clickHandler = (e) => {{ ... }};
        // this.element.addEventListener("click", clickHandler);
        // this.boundHandlers.push({{ element: this.element, type: "click", handler: clickHandler }});
    }}

    /**
     * Destroys the {slug.replace("_", " ")} instance and removes all event listeners.
     * Call this before removing the element from DOM.
     */
    destroy() {{
        debugLog("Destroy {slug.replace("_", " ")}: ", this.element);

        // Remove all event listeners
        this.boundHandlers.forEach(({{ element, type, handler }}) => {{
            element.removeEventListener(type, handler);
        }});
        this.boundHandlers = [];

        {class_name}.instances.delete(this.element);
        delete this.element.__insightInstance;

        this.element = null;
    }}

    // Static method for initializing all {slug.replace("_", " ")} instances
    static initAll() {{
        document.querySelectorAll("[{data_attr}]").forEach(el => new {class_name}(el));
    }}
}}
"""
        if self._write_file(js_path, js_content):
            self.stdout.write(self.style.SUCCESS(f"  [OK] Created JavaScript file insight-ui-{js_slug}.js"))

    def _add_to_component_demo(self, doc_path: Path, slug: str, func_name: str) -> None:
        """Add demo entry to component_demo.html.

        Args:
            doc_path: The base path of the documentation package.
            slug: The component slug for the condition check (e.g., 'my_component').
            func_name: The template tag function name (e.g., 'my_component').

        """
        file_path = doc_path / "templates" / "documentation" / "docs" / "component_demo.html"
        content = self._read_file(file_path)
        if content is None:
            return

        # Check if already exists
        if f'component.value == "{slug}"' in content:
            self.stdout.write(f"  [SKIP] Demo entry for {slug} already exists in component_demo.html")
            return

        # Find the final {% endif %} and insert before it
        endif_pattern = r"(\{% endif %\}\s*)$"
        match = re.search(endif_pattern, content)

        if not match:
            self.stderr.write(self.style.WARNING("  [WARN] Could not find {% endif %} in component_demo.html"))
            return

        # Create new elif block with config parameter
        # The config variable name is based on the func_name (e.g., "my_component_config")
        config_var = f"{func_name}_config"
        new_block = f"""{{% elif component.value == "{slug}" %}}
    {{% {func_name} config={config_var} %}}
"""
        # Insert before {% endif %}
        insert_pos = match.start()
        new_content = content[:insert_pos] + new_block + content[insert_pos:]
        if self._write_file(file_path, new_content):
            self.stdout.write(self.style.SUCCESS(f"  [OK] Added demo entry for {slug} to component_demo.html"))

    def _create_config_dataclass(  # noqa: PLR0913, PLR0917
        self, ui_path: Path, config_class_name: str, func_name: str, category: str, name: str, git_user: str
    ) -> None:
        """Create config dataclass in the appropriate config file and update __init__.py.

        Args:
            ui_path: The base path of the insight_ui package.
            config_class_name: The config dataclass name (e.g., 'MyComponentConfig').
            func_name: The function name for documentation (e.g., 'my_component').
            category: The component category determining the config file.
            name: The display name of the component (e.g., 'My Component').
            git_user: The Git username for TODO comments.

        """
        config_file = CATEGORY_TO_CONFIG_FILE[category]
        file_path = ui_path / "configs" / config_file
        content = self._read_file(file_path)
        if content is None:
            return

        # Check if already exists
        if f"class {config_class_name}" in content:
            self.stdout.write(f"  [SKIP] Config class {config_class_name} already exists in {config_file}")
            return

        # Create new config dataclass
        new_class = f'''

@dataclass
class {config_class_name}:
    """
    Configuration for the {func_name.replace("_", " ")} component.

    Renders a {name.lower()} element.

    Attributes:
        tag_id: Unique ID for JavaScript/CSS targeting.

    """

    __example__ = """
        {config_class_name}(
            tag_id="{func_name}-1",
        )
        """

    # TODO({git_user}): Add component-specific configuration fields
    tag_id: str = field(default="", metadata={{"doc": _("Unique ID for JavaScript/CSS targeting.")}})
'''
        # Append to end of file
        new_content = content.rstrip() + new_class + "\n"
        if self._write_file(file_path, new_content):
            self.stdout.write(self.style.SUCCESS(f"  [OK] Added {config_class_name} to configs/{config_file}"))

        # Update configs/__init__.py
        self._add_config_to_init(ui_path, config_class_name, config_file, category)

    def _add_config_to_init(self, ui_path: Path, config_class_name: str, config_file: str, category: str) -> None:
        """Add config class to configs/__init__.py imports and __all__.

        Args:
            ui_path: The base path of the insight_ui package.
            config_class_name: The config dataclass name to add (e.g., 'MyComponentConfig').
            config_file: The config module filename (e.g., 'layout.py').
            category: The component category for the __all__ section.

        """
        init_path = ui_path / "configs" / "__init__.py"
        content = self._read_file(init_path)
        if content is None:
            return

        # Check if already imported
        if config_class_name in content:
            self.stdout.write(f"  [SKIP] {config_class_name} already in configs/__init__.py")
            return

        # Module name without .py extension
        module_name = config_file.replace(".py", "")

        # 1. Add to import statement
        # Find the import block for this module
        import_pattern = rf"(from insight_ui\.configs\.{module_name} import \(\n)((?:\s+\w+,\n)*)"
        import_match = re.search(import_pattern, content)

        if import_match:
            # Add to existing import block
            import_end = import_match.end()
            new_import_line = f"    {config_class_name},\n"
            content = content[:import_end] + new_import_line + content[import_end:]
        else:
            # Single-line import or no import yet - find and extend
            single_import_pattern = rf"from insight_ui\.configs\.{module_name} import (\w+(?:,\s*\w+)*)"
            single_match = re.search(single_import_pattern, content)
            if single_match:
                # Convert to multi-line or add to end
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

        # 2. Add to __all__ list in the appropriate section
        section_comment = CATEGORY_TO_INIT_SECTION.get(category, f"# {category.title()}")

        # Find the section in __all__
        all_section_pattern = rf'({re.escape(section_comment)}\n)((?:\s+"[^"]+",\n)*)'
        all_match = re.search(all_section_pattern, content)

        if all_match:
            # Add after the last entry in this section
            section_end = all_match.end()
            new_all_entry = f'    "{config_class_name}",\n'
            content = content[:section_end] + new_all_entry + content[section_end:]
        else:
            # Section not found, add before closing bracket of __all__
            all_end_pattern = r"(\])\s*$"
            all_end_match = re.search(all_end_pattern, content)
            if all_end_match:
                insert_pos = all_end_match.start()
                new_all_entry = f'    # {category.title()}\n    "{config_class_name}",\n'
                content = content[:insert_pos] + new_all_entry + content[insert_pos:]

        if self._write_file(init_path, content):
            self.stdout.write(self.style.SUCCESS(f"  [OK] Added {config_class_name} to configs/__init__.py"))
