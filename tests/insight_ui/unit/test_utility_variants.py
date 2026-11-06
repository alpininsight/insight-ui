# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Utility classes used in templates must exist in the built stylesheet.

A class without a rule is silently ignored by the browser. This catches typos (rounded-insight-control-top),
token names that do not exist (bg-insight-base-dark) and variants of plain classes: Tailwind generates variants
(hover:, even:, md:, after:, ...) only for its own utilities and for those defined with @utility.
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

# Utilities are recognized by their name; other classes (JS hooks, markers) may have no rule.
UTILITY = re.compile(
    r"^(?:bg|text|border|rounded|shadow|ring|outline|fill|stroke|divide|from|via|to|p|px|py|pt|pb|ps|pe|m|mx|my|mt|mb"
    r"|ms|me|gap|space|w|h|size|min|max|inset|top|bottom|start|end|left|right|z|opacity|font|leading|tracking|grid"
    r"|col|row|flex|items|justify|self|place|content|order|translate|rotate|scale|transition|duration|ease|animate"
    r"|cursor|select|overflow|whitespace|break|line|aspect|object|accent|decoration|underline|truncate|sr|not)(?:-|$)"
    r"|^(?:hidden|block|inline|flex|grid|table|contents|absolute|relative|fixed|sticky|static|grow|shrink|uppercase"
    r"|lowercase|capitalize|italic|invisible|visible|isolate|peer|group)$"
)


def css_escape(class_name: str) -> str:
    """Escape a class name the way Tailwind writes it into a selector; a leading digit becomes a code point."""
    escaped = re.sub(r"([^a-zA-Z0-9_-])", r"\\\1", class_name)
    if escaped[0].isdigit():
        escaped = f"\\{ord(escaped[0]):x} {escaped[1:]}"
    return escaped


def base_name(class_name: str) -> str:
    """Return the utility without variants ([&::thumb]:, hover:, md:), important or negative prefix."""
    depth, start = 0, 0
    for index, char in enumerate(class_name):
        depth += {"[": 1, "]": -1, "(": 1, ")": -1}.get(char, 0)
        if char == ":" and depth == 0:
            start = index + 1
    return class_name[start:].lstrip("!-").rstrip("!")


def template_classes() -> dict[str, str]:
    """Map each literal class in the package templates to a template that uses it."""
    found: dict[str, str] = {}
    for path in sorted(TEMPLATES.rglob("*.html")):
        text = path.read_text(encoding="utf-8")
        for value in re.findall(r'class="([^"]*)"', text, re.DOTALL):
            for class_name in TEMPLATE_CODE.sub(" ", value).split():
                # Fragments like "btn-" are completed by template code ("btn-{{ size }}").
                if not class_name.endswith(("-", ":")):
                    found.setdefault(class_name, path.relative_to(TEMPLATES).as_posix())
    return found


@pytest.fixture(scope="module")
def built_css() -> str:
    """Read the compiled stylesheet shipped in the package."""
    return BUILT_CSS.read_text(encoding="utf-8")


def test_template_utilities_are_in_the_stylesheet(built_css: str) -> None:
    """A utility without a rule does nothing: a typo, a missing token or a variant of a plain class."""
    missing = [
        f"{class_name} ({template})"
        for class_name, template in sorted(template_classes().items())
        if UTILITY.match(base_name(class_name))
        and not re.search(rf"\.{re.escape(css_escape(class_name))}(?![\w\\-])", built_css)
    ]

    assert not missing, (
        "Missing in tailwind.css: " + ", ".join(missing) + ". Check the name against the tokens in input.css; "
        "a shorthand used with a variant must be defined with @utility, not as a plain class."
    )


def test_focus_outline_stays_visible_in_forced_colors() -> None:
    """outline-none removes the outline completely since Tailwind 4; outline-hidden keeps it for forced colors.

    Focus rings are box shadows, which forced-colors mode (e.g. Windows high contrast) does not draw.
    """
    using = sorted({template for name, template in template_classes().items() if base_name(name) == "outline-none"})

    assert not using, f"Use outline-hidden instead of outline-none in {', '.join(using)}"


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
