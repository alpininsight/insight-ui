# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Utility classes used with a variant (hover:, even:, md:, after:, ...) must exist in the built stylesheet.

Tailwind generates variants only for its own utilities and for those defined with @utility. A plain class in
@layer utilities gets no variants, and the template class then does nothing without any error.
"""

import re
from pathlib import Path

import pytest

import insight_ui

PACKAGE = Path(insight_ui.__file__).parent
TEMPLATES = PACKAGE / "templates" / "insight_ui"
INPUT_CSS = PACKAGE / "utils" / "input.css"
BUILT_CSS = PACKAGE / "static" / "insight_ui" / "css" / "tailwind.css"

# Template code inside a class attribute is removed; the literal classes around it stay.
TEMPLATE_CODE = re.compile(r"{%.*?%}|{{.*?}}|{#.*?#}", re.DOTALL)


def css_escape(class_name: str) -> str:
    """Escape a class name the way Tailwind writes it into a selector; a leading digit becomes a code point."""
    escaped = re.sub(r"([^a-zA-Z0-9_-])", r"\\\1", class_name)
    if escaped[0].isdigit():
        escaped = f"\\{ord(escaped[0]):x} {escaped[1:]}"
    return escaped


def variant_classes() -> dict[str, str]:
    """Map each variant-prefixed class in the package templates to a template that uses it."""
    found: dict[str, str] = {}
    for path in sorted(TEMPLATES.rglob("*.html")):
        text = path.read_text(encoding="utf-8")
        for value in re.findall(r'class="([^"]*)"', text, re.DOTALL):
            for class_name in TEMPLATE_CODE.sub(" ", value).split():
                if ":" in class_name and not class_name.endswith(":"):
                    found.setdefault(class_name, path.relative_to(TEMPLATES).as_posix())
    return found


@pytest.fixture(scope="module")
def built_css() -> str:
    """Read the compiled stylesheet shipped in the package."""
    return BUILT_CSS.read_text(encoding="utf-8")


@pytest.mark.parametrize(("class_name", "template"), sorted(variant_classes().items()))
def test_variant_class_is_in_the_stylesheet(class_name: str, template: str, built_css: str) -> None:
    """A variant without a rule is silently ignored by the browser."""
    assert f".{css_escape(class_name)}" in built_css, (
        f"{class_name} (used in {template}) is missing in tailwind.css; "
        "define its utility with @utility in input.css, not as a plain class"
    )


def test_custom_utilities_are_not_plain_classes() -> None:
    """Shorthand utilities need @utility; plain classes in @layer utilities get no variants."""
    css = INPUT_CSS.read_text(encoding="utf-8")
    layer = re.search(r"@layer utilities\s*{(.*?)\n}", css, re.DOTALL)

    assert layer is None or not re.search(r"^\s*\.[\w-]+\s*{", layer.group(1), re.MULTILINE)


@pytest.mark.parametrize(
    "class_name",
    re.findall(r"^@utility ([\w-]+)", INPUT_CSS.read_text(encoding="utf-8"), re.MULTILINE),
)
def test_shorthand_utilities_stay_available_for_hosts(class_name: str, built_css: str) -> None:
    """Hosts may use the shorthand classes, so they are in the stylesheet even when no package template does."""
    assert re.search(rf"^\s*\.{re.escape(class_name)} {{", built_css, re.MULTILINE)
