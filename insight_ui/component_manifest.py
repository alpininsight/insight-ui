# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Small component contracts shared by contributor tools and downstream hosts.

Examples are data, not executable Python. Config field documentation remains on
the dataclass; a manifest does not duplicate the parameter reference or a site.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, is_dataclass
from importlib import import_module
from pathlib import Path, PurePosixPath
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Mapping

CATEGORIES = {
    "layout": "layout",
    "navigation": "navigation",
    "input": "input",
    "popup": "popup",
    "util": "utils",
    "list": "list",
    "filter": "filter",
    "card": "card",
    "form": "forms",
}
LEVELS = ("atom", "molecule", "organism")
SLUG_PATTERN = re.compile(r"[a-z][a-z0-9]*(?:_[a-z0-9]+)*\Z")


@dataclass(frozen=True)
class ComponentExample:
    """A named, declarative input to the component's public Config."""

    name: str
    config: dict[str, Any]


@dataclass(frozen=True)
class ComponentManifest:
    """Versioned metadata, independent of website categories and audit status."""

    schema_version: int
    slug: str
    name: str
    category: str
    level: str
    config_class: str
    template: str
    uses: tuple[str, ...]
    examples: tuple[ComponentExample, ...]
    js_module: str | None = None


def validate_slug(slug: str) -> str:
    """Accept only component identifiers, never paths or template expressions."""
    if not isinstance(slug, str) or not SLUG_PATTERN.fullmatch(slug):
        message = "Component names must be lowercase snake_case identifiers."
        raise ValueError(message)
    return slug


def manifest_path(slug: str) -> Path:
    """Locate one contract in the imported Insight UI package."""
    return Path(__file__).resolve().parent / "component_manifests" / f"{validate_slug(slug)}.json"


def _package_asset(value: object, prefix: str, suffix: str) -> str:
    """Validate a package-relative template or static asset name."""
    if not isinstance(value, str):
        message = "Component asset names must be strings."
        raise TypeError(message)
    path = PurePosixPath(value)
    if (
        not value.startswith(prefix)
        or not value.endswith(suffix)
        or ".." in path.parts
        or "\\" in value
        or path.as_posix() != value
    ):
        message = f"Invalid package asset: {value!r}"
        raise ValueError(message)
    return value


def _parse_examples(examples: object) -> tuple[ComponentExample, ...]:
    """Keep example validation independent of metadata and Config construction."""
    if not isinstance(examples, list) or not examples:
        message = "At least one declarative example is required."
        raise ValueError(message)
    parsed = []
    for example in examples:
        if not isinstance(example, dict) or set(example) != {"name", "config"}:
            message = "Each example needs exactly name and config."
            raise ValueError(message)
        if not isinstance(example["config"], dict):
            message = "Example config must be a JSON object."
            raise TypeError(message)
        parsed.append(ComponentExample(validate_slug(example["name"]), example["config"]))
    names = [example.name for example in parsed]
    if "default" not in names or len(set(names)) != len(names):
        message = "Examples need unique names and a default example."
        raise ValueError(message)
    return tuple(parsed)


def parse_manifest(data: Mapping[str, Any]) -> ComponentManifest:
    """Validate the stable v1 contract before imports or rendering."""
    required = {
        "schema_version",
        "slug",
        "name",
        "category",
        "level",
        "config_class",
        "template",
        "uses",
        "examples",
    }
    if not isinstance(data, dict) or required - data.keys() or data.keys() - required - {"js_module"}:
        message = "A component manifest has missing or unknown fields."
        raise ValueError(message)
    if type(data["schema_version"]) is not int or data["schema_version"] != 1:
        message = "Only component manifest schema_version 1 is supported."
        raise ValueError(message)
    slug = validate_slug(data["slug"])
    if data["category"] not in CATEGORIES or data["level"] not in LEVELS:
        message = "Unknown component category or atomic level."
        raise ValueError(message)
    if not isinstance(data["name"], str) or not data["name"].strip():
        message = "The component needs a display name."
        raise ValueError(message)
    config_class = data["config_class"]
    if not isinstance(config_class, str) or not re.fullmatch(
        r"insight_ui\.configs\.[a-z][a-z0-9_]*\.[A-Z][A-Za-z0-9]*Config", config_class
    ):
        message = "config_class must reference a public Insight UI Config dataclass."
        raise ValueError(message)
    if not isinstance(data["uses"], list) or not all(isinstance(child, str) for child in data["uses"]):
        message = "uses must be a list of component identifiers."
        raise ValueError(message)
    if len(set(data["uses"])) != len(data["uses"]):
        message = "uses must be a list of unique component identifiers."
        raise ValueError(message)
    uses = tuple(validate_slug(child) for child in data["uses"])
    if slug in uses or (data["level"] == "atom" and uses):
        message = "Components cannot compose themselves; atoms do not compose other components."
        raise ValueError(message)
    parsed_examples = _parse_examples(data["examples"])
    js_module = data.get("js_module")
    return ComponentManifest(
        schema_version=1,
        slug=slug,
        name=data["name"],
        category=data["category"],
        level=data["level"],
        config_class=config_class,
        template=_package_asset(data["template"], "insight_ui/components/", ".html"),
        uses=uses,
        examples=tuple(parsed_examples),
        js_module=_package_asset(js_module, "insight_ui/js/", ".js") if js_module is not None else None,
    )


def load_manifest(path: Path) -> ComponentManifest:
    """Read a JSON contract without evaluating example code."""
    return parse_manifest(json.loads(Path(path).read_text(encoding="utf-8")))


def build_example_config(manifest: ComponentManifest, example_name: str = "default") -> object:
    """Build an example using the package's existing nested-Config coercion."""
    from insight_ui.templatetags.insight_tags import build_config  # noqa: PLC0415

    example = next((entry for entry in manifest.examples if entry.name == example_name), None)
    if example is None:
        message = f"Unknown example {example_name!r} for {manifest.slug}."
        raise ValueError(message)
    module_name, class_name = manifest.config_class.rsplit(".", 1)
    config_type = getattr(import_module(module_name), class_name)
    if not isinstance(config_type, type) or not is_dataclass(config_type):
        message = "The manifest config_class is not a dataclass."
        raise ValueError(message)
    return build_config(config_type, example.config)
