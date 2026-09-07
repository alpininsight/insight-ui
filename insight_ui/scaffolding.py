# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Generate contributor-owned components, without depending on a docs project.

The naming/category layout is retained from the original create_component
command. Planning all edits first prevents partially registered components.
"""

from __future__ import annotations

import ast
import json
import keyword
import re
import shutil
import subprocess  # nosec B404
import tomllib
from dataclasses import MISSING, dataclass, fields, is_dataclass
from pathlib import Path
from typing import Any, Literal, get_args, get_origin, get_type_hints

from insight_ui.component_manifest import CATEGORIES, LEVELS, parse_manifest, validate_slug

# REUSE-IgnoreStart
HEADER = (
    "# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG\n"
    "# SPDX-License-Identifier: AGPL-3.0-only\n"
)
# REUSE-IgnoreEnd


@dataclass(frozen=True)
class FileChange:
    """One prevalidated edit and the state which must still exist when applying."""

    path: Path
    before: str | None
    after: str


@dataclass(frozen=True)
class ComponentScaffold:
    """A component's identity and developer-selected composition."""

    name: str
    category: str
    level: str = "atom"
    compose: tuple[str, ...] = ()
    javascript: bool = False

    @property
    def slug(self) -> str:
        """Return the existing snake_case tag and manifest identifier."""
        return self.name.lower().replace(" ", "_")

    @property
    def class_name(self) -> str:
        """Return the generated Config name."""
        return "".join(word[:1].upper() + word[1:] for word in self.name.split()) + "Config"

    def validate(self) -> None:
        """Reject ambiguous names and unsupported compositions before writes."""
        if not re.fullmatch(r"[A-Za-z][A-Za-z0-9]*(?: [A-Za-z0-9]+)*", self.name):
            message = "Use a component name such as 'Example Panel', with letters, digits and single spaces."
            raise ValueError(message)
        validate_slug(self.slug)
        if keyword.iskeyword(self.slug) or self.category not in CATEGORIES or self.level not in LEVELS:
            message = "Invalid name, category or atomic level."
            raise ValueError(message)
        if len(set(self.compose)) != len(self.compose):
            message = "--compose needs unique component names."
            raise ValueError(message)
        for child in self.compose:
            validate_slug(child)
            if child in {self.slug, "label", "tag_id"} or keyword.iskeyword(child):
                message = f"Invalid composition field {child!r}."
                raise ValueError(message)
        if self.level == "atom" and self.compose:
            message = "An atom does not compose existing components. Use --level molecule or organism."
            raise ValueError(message)
        if self.level != "atom" and not self.compose:
            message = "Molecule and organism templates require --compose with existing component tags."
            raise ValueError(message)


def validate_package_root(root: Path) -> Path:
    """Only modify an explicit source checkout, never site-packages or a host app."""
    root = root.expanduser().resolve(strict=True)
    project = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))
    if project.get("project", {}).get("name") != "insight-ui" or not (root / ".git").exists():
        message = "The target must be an insight-ui Git checkout or worktree."
        raise ValueError(message)
    git = shutil.which("git")
    if git is None:
        message = "Git must be installed to validate the contributor checkout."
        raise ValueError(message)
    # Fixed read-only operation, resolved executable, no shell or interpolated command.
    try:
        result = subprocess.run(  # noqa: S603  # nosec B603
            [str(Path(git).resolve()), "-C", str(root), "rev-parse", "--show-toplevel"],
            check=True,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except subprocess.SubprocessError as error:
        message = "Git could not validate the contributor checkout. Nothing was changed."
        raise ValueError(message) from error
    if Path(result.stdout.strip()).resolve() != root or Path(__file__).resolve().parents[1] != root:
        message = (
            "The imported insight_ui must be the target checkout. Run from that worktree with "
            "PYTHONPATH=. uv run --no-sync python -m devtools create_component ..."
        )
        raise ValueError(message)
    return root


def _insert_import(source: str, statement: str) -> str:
    """Insert an import after the module docstring and any future imports."""
    if statement in source.splitlines():
        return source
    tree = ast.parse(source)
    index = 0
    for node in tree.body:
        if (
            isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str)
        ) or (isinstance(node, ast.ImportFrom) and node.module == "__future__"):
            index = node.end_lineno or node.lineno
        else:
            break
    lines = source.splitlines(keepends=True)
    lines.insert(index, statement + "\n")
    return "".join(lines)


def _export_config(source: str, module: str, class_name: str) -> str:
    """Extend the existing export list instead of depending on comment headings."""
    source = _insert_import(source, f"from insight_ui.configs.{module} import {class_name}")
    for node in ast.parse(source).body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "__all__" for t in node.targets):
            if not isinstance(node.value, ast.List):
                break
            values = ast.literal_eval(node.value)
            if class_name in values:
                message = f"Config {class_name} is already exported."
                raise ValueError(message)
            lines = source.splitlines(keepends=True)
            offset = sum(map(len, lines[: node.value.end_lineno - 1])) + node.value.end_col_offset - 1
            return source[:offset] + f'    "{class_name}",\n' + source[offset:]
    message = "Could not locate the public configs.__all__ list; nothing was changed."
    raise ValueError(message)


def _child_config(child: str) -> type:
    """Resolve an existing tag's actual Config, not a separate component registry."""
    from insight_ui.templatetags import insight_tags  # noqa: PLC0415

    function = getattr(insight_tags, child, None)
    if child not in insight_tags.register.tags or not callable(function):
        message = f"Unknown Insight UI template tag: {child}."
        raise ValueError(message)
    annotation = get_type_hints(function).get("config")
    candidates = [annotation, *get_args(annotation)]
    for candidate in candidates:
        if isinstance(candidate, type) and is_dataclass(candidate):
            return candidate
    message = f"{child} has no composable Config dataclass yet."
    raise ValueError(message)


def _required_value(annotation: object, label: str) -> object:
    """Produce simple example inputs; never evaluate a Python docstring."""
    if annotation is str:
        return label
    if annotation in (bool, int, float):
        return {bool: False, int: 1, float: 1.0}[annotation]
    if get_origin(annotation) is Literal:
        return get_args(annotation)[0]
    if get_origin(annotation) is list:
        return []
    if get_origin(annotation) is dict:
        return {}
    message = "A composed Config needs a complex required value. Supply --example-config with explicit JSON inputs."
    raise ValueError(message)


def _child_example(child: str, config_type: type, parent_slug: str) -> dict[str, Any]:
    """Seed required values and readable labels in a generated preview."""
    hints = get_type_hints(config_type)
    result = {}
    for item in fields(config_type):
        if item.default is MISSING and item.default_factory is MISSING:
            result[item.name] = _required_value(hints.get(item.name), child.replace("_", " ").title())
    available = {item.name for item in fields(config_type)}
    if "label" in available:
        result["label"] = child.replace("_", " ").title()
    if "name" in available:
        result["name"] = child
    if "tag_id" in available:
        result["tag_id"] = f"{parent_slug}-{child}"
    return result


def _config_source(spec: ComponentScaffold, children: dict[str, type]) -> str:
    """Create a normal dataclass with matching docstrings and field metadata."""
    docs = {"label": "Visible label for the component.", "tag_id": "Optional unique HTML ID."}
    docs.update({child: f"Configuration for the existing {child} component." for child in children})
    attributes = "\n".join(f"        {name}: {doc}" for name, doc in docs.items())
    values = [
        f'    label: str = dataclasses.field(default={spec.name!r}, metadata={{"doc": _({docs["label"]!r})}})',
        f'    tag_id: str = dataclasses.field(default="", metadata={{"doc": _({docs["tag_id"]!r})}})',
    ]
    values.extend(
        f'    {child}: {cls.__name__} | None = dataclasses.field(default=None, metadata={{"doc": _({docs[child]!r})}})'
        for child, cls in children.items()
    )
    return (
        f"\n\n@dataclasses.dataclass\nclass {spec.class_name}:\n"
        f'    """Configuration for the {spec.slug} component.\n\n    Attributes:\n{attributes}\n\n    """\n\n'
        f'    __example__ = """{spec.class_name}(label={spec.name!r})"""\n\n' + "\n".join(values) + "\n"
    )


def _template(spec: ComponentScaffold) -> str:
    """Compose public tags and existing role classes, without cloning children."""
    variable = f"{spec.slug}_config"
    marker = f"data-insight-{spec.slug.replace('_', '-')}"
    identifier = f'{{% if {variable}.tag_id %}}id="{{{{ {variable}.tag_id }}}}"{{% endif %}}'
    if spec.level == "atom":
        body = f'<span {identifier} {marker} class="text-insight-body">{{{{ {variable}.label }}}}</span>\n'
    else:
        element = "section" if spec.level == "organism" else "div"
        label = f'    <h2 class="font-semibold text-insight-headline">{{{{ {variable}.label }}}}</h2>\n'
        children = "".join(
            f"        {{% if {variable}.{child} %}}{{% {child} config={variable}.{child} %}}{{% endif %}}\n"
            for child in spec.compose
        )
        body = (
            f'<{element} {identifier} {marker} class="space-y-4">\n'
            + (label if spec.level == "organism" else "")
            + '    <div class="flex flex-wrap gap-4 items-end">\n'
            + children
            + f"    </div>\n</{element}>\n"
        )
    return "{% load insight_tags %}\n\n" + body


def _tag(spec: ComponentScaffold) -> str:
    """Use the existing Config coercion API, including nested dict kwargs."""
    return (
        f'\n\n@register.inclusion_tag("insight_ui/components/{spec.slug}.html")\n'
        f"def {spec.slug}(config: {spec.class_name} | None = None, **kwargs) -> dict[str, object]:\n"
        f'    """Render the {spec.slug} component using its public Config."""\n'
        f'    return {{"{spec.slug}_config": build_config({spec.class_name}, config, **kwargs)}}\n'
    )


def _test_source(spec: ComponentScaffold) -> str:
    """Scaffold an actual example render and escaping regression, not a TODO."""
    return (
        HEADER
        + f'''"""Rendering and escaping checks for {spec.slug}."""

from dataclasses import is_dataclass

from django.template import Context, Template

from insight_ui.component_manifest import build_example_config, load_manifest, manifest_path


def test_{spec.slug}_example_renders() -> None:
    """The same declarative example can be used by preview and downstream hosts."""
    manifest = load_manifest(manifest_path("{spec.slug}"))
    config = build_example_config(manifest)
    assert is_dataclass(config)
    template = Template("{{% load insight_tags %}}{{% {spec.slug} config=config %}}")
    rendered = template.render(Context({{"config": config}}))
    assert "data-insight-{spec.slug.replace("_", "-")}" in rendered


def test_{spec.slug}_id_is_escaped() -> None:
    """A Config value cannot break out of its HTML attribute."""
    rendered = Template("{{% load insight_tags %}}{{% {spec.slug} tag_id=value %}}").render(
        Context({{"value": '\\" onmouseover=\\"alert(1)'}})
    )
    assert '&quot; onmouseover=&quot;alert(1)' in rendered
    assert 'id="" onmouseover=' not in rendered
'''
    )


def _manifest_source(
    spec: ComponentScaffold,
    children: dict[str, type],
    example_config: dict[str, Any] | None,
) -> str:
    """Build and validate the shared example contract before any source mutation."""
    from insight_ui.templatetags.insight_tags import build_config  # noqa: PLC0415

    example = (
        example_config
        if example_config is not None
        else {
            "label": spec.name,
            "tag_id": f"{spec.slug}-example",
            **{child: _child_example(child, cls, spec.slug) for child, cls in children.items()},
        }
    )
    if not isinstance(example, dict) or set(example) - {"label", "tag_id", *children}:
        message = "--example-config must be a JSON object using the generated Config fields."
        raise ValueError(message)
    for child, cls in children.items():
        if example.get(child) is not None:
            build_config(cls, example[child])
    js_module = f"insight_ui/js/insight-ui-{spec.slug.replace('_', '-')}.js" if spec.javascript else None
    manifest = {
        "schema_version": 1,
        "slug": spec.slug,
        "name": spec.name,
        "category": spec.category,
        "level": spec.level,
        "config_class": f"insight_ui.configs.{CATEGORIES[spec.category]}.{spec.class_name}",
        "template": f"insight_ui/components/{spec.slug}.html",
        "uses": list(spec.compose),
        "examples": [{"name": "default", "config": example}],
        "js_module": js_module,
    }
    parse_manifest(manifest)
    return json.dumps(manifest, indent=2) + "\n"


def _config_module(root: Path, spec: ComponentScaffold, children: dict[str, type]) -> str:
    """Extend one category module without assuming the name of its field import."""
    module = CATEGORIES[spec.category]
    source = (root / "insight_ui" / "configs" / f"{module}.py").read_text(encoding="utf-8")
    if any(isinstance(node, ast.ClassDef) and node.name == spec.class_name for node in ast.parse(source).body):
        message = f"Config {spec.class_name} already exists."
        raise ValueError(message)
    source = _insert_import(source, "import dataclasses")
    source = _insert_import(source, "from django.utils.translation import gettext_lazy as _")
    for cls in children.values():
        if cls.__module__ != f"insight_ui.configs.{module}":
            source = _insert_import(source, f"from {cls.__module__} import {cls.__name__}")
    return source.rstrip() + _config_source(spec, children)


def plan_component(
    root: Path, spec: ComponentScaffold, example_config: dict[str, Any] | None = None
) -> list[FileChange]:
    """Validate and prepare all registration, source, example and test changes."""
    from insight_ui.templatetags import insight_tags  # noqa: PLC0415

    root = validate_package_root(root)
    spec.validate()
    if spec.slug in insight_tags.register.tags or hasattr(insight_tags, spec.slug):
        message = f"Component {spec.slug} already exists; nothing was changed."
        raise ValueError(message)
    children = {child: _child_config(child) for child in spec.compose}
    module = CATEGORIES[spec.category]
    manifest = _manifest_source(spec, children, example_config)
    changes = []

    def add(relative: str, content: str, *, new: bool = False) -> None:
        path = root / relative
        if not path.resolve().is_relative_to(root):
            message = "A generated path escapes the target checkout."
            raise ValueError(message)
        before = path.read_text(encoding="utf-8") if path.exists() else None
        if new and before is not None:
            message = f"{relative} already exists; nothing was changed."
            raise ValueError(message)
        if path.suffix == ".py":
            ast.parse(content, filename=relative)
        changes.append(FileChange(path, before, content))

    add(f"insight_ui/configs/{module}.py", _config_module(root, spec, children))
    exports = (root / "insight_ui/configs/__init__.py").read_text(encoding="utf-8")
    add("insight_ui/configs/__init__.py", _export_config(exports, module, spec.class_name))
    tags = (root / "insight_ui/templatetags/insight_tags.py").read_text(encoding="utf-8")
    tags = _insert_import(tags, f"from insight_ui.configs.{module} import {spec.class_name}")
    add("insight_ui/templatetags/insight_tags.py", tags.rstrip() + _tag(spec))
    add(f"insight_ui/templates/insight_ui/components/{spec.slug}.html", _template(spec), new=True)
    add(f"tests/insight_ui/unit/components/test_{spec.slug}.py", _test_source(spec), new=True)
    add(f"insight_ui/component_manifests/{spec.slug}.json", manifest, new=True)
    if spec.javascript:
        from insight_ui.scaffolding_js import javascript_changes  # noqa: PLC0415

        for relative, content, new in javascript_changes(root, spec):
            add(relative, content, new=new)
    return changes


def apply_component(changes: list[FileChange]) -> None:
    """Apply a plan only if unchanged; restore its own edits on write failure."""
    for change in changes:
        current = change.path.read_text(encoding="utf-8") if change.path.exists() else None
        if current != change.before:
            message = f"{change.path} changed after planning; nothing was written."
            raise ValueError(message)
    applied = []
    try:
        for change in changes:
            change.path.parent.mkdir(parents=True, exist_ok=True)
            applied.append(change)
            change.path.write_text(change.after, encoding="utf-8")
    except OSError:
        for change in reversed(applied):
            if change.before is None:
                change.path.unlink(missing_ok=True)
            else:
                change.path.write_text(change.before, encoding="utf-8")
        raise
