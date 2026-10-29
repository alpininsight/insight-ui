# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for the design token checker used as pre-commit hook."""

from pathlib import Path

import pytest
from scripts.check_design_tokens import (
    build_color_config,
    build_family_text_config,
    build_radius_config,
    build_shadow_config,
    build_verbose_config,
    find_template_files,
    find_violations,
)

CONFIGS = [build_color_config(), build_radius_config(), build_shadow_config(), build_verbose_config()]


def violations(tmp_path: Path, classes: str) -> list[str]:
    """Return the classes the checker reports for a template with the given class attribute."""
    template = tmp_path / "component.html"
    template.write_text(f'<div class="{classes}"></div>\n', encoding="utf-8")
    return [violation.class_name for violation in find_violations(template, CONFIGS)]


@pytest.mark.parametrize(
    "classes",
    [
        pytest.param("bg-insight-bg-base-dark", id="dark-token-has-no-shorthand"),
        pytest.param("text-insight-text-link-hover", id="longer-token"),
        pytest.param("bg-insight-bg-raised/50", id="opacity-needs-the-token"),
        pytest.param("rounded-insight-surface shadow-insight-raised", id="semantic-tokens"),
    ],
)
def test_whole_classes_only(tmp_path: Path, classes: str) -> None:
    """A verbose token inside a longer class is not reported; its suggestion would not exist."""
    assert violations(tmp_path, classes) == []


@pytest.mark.parametrize(
    ("classes", "reported"),
    [
        pytest.param("bg-insight-bg-base", "bg-insight-bg-base", id="verbose"),
        pytest.param("hover:bg-insight-bg-raised", "hover:bg-insight-bg-raised", id="verbose-with-variant"),
        pytest.param("p-4 bg-gray-300", "bg-gray-300", id="raw-color"),
        pytest.param("rounded-lg", "rounded-lg", id="raw-radius"),
        pytest.param("shadow-md", "shadow-md", id="raw-shadow"),
    ],
)
def test_reports_raw_and_verbose_classes(tmp_path: Path, classes: str, reported: str) -> None:
    """Raw Tailwind values and verbose tokens with a shorthand are reported."""
    assert violations(tmp_path, classes) == [reported]


@pytest.mark.parametrize(
    ("classes", "reported"),
    [
        pytest.param("text-white bg-insight-primary-action", "text-white", id="white-on-fill"),
        pytest.param("bg-white", "bg-white", id="white-background"),
        pytest.param("dark:text-black", "dark:text-black", id="black-with-variant"),
    ],
)
def test_white_and_black_are_reported(tmp_path: Path, classes: str, reported: str) -> None:
    """White and black follow no theme; text on a fill uses its -on-action token."""
    assert violations(tmp_path, classes) == [reported]


def test_translucent_backdrop_is_allowed(tmp_path: Path) -> None:
    """A translucent black backdrop dims whatever lies below, in both themes."""
    assert violations(tmp_path, "fixed inset-0 bg-black/50") == []


def test_class_attribute_with_template_code_is_checked(tmp_path: Path) -> None:
    """Template code in the attribute may use the other quote; the classes around it are still checked."""
    assert violations(tmp_path, "{% if side == 'right' %}end-0{% endif %} text-white") == ["text-white"]


def check_file(tmp_path: Path, name: str, content: str) -> list[str]:
    """Return the classes the checker reports for a script or stylesheet with the given content."""
    path = tmp_path / name
    path.write_text(content, encoding="utf-8")
    return [violation.class_name for violation in find_violations(path, CONFIGS)]


def test_class_strings_in_scripts_are_checked(tmp_path: Path) -> None:
    """Scripts build class lists in strings; their raw colors are reported, comments are not."""
    script = "// was bg-gray-100\nitem.classList.add('bg-gray-100', 'rounded-lg');\n"

    assert check_file(tmp_path, "widget.js", script) == ["bg-gray-100"]


def test_apply_rules_in_the_stylesheet_are_checked(tmp_path: Path) -> None:
    """@apply rules are checked for colors; verbose tokens are fine there, CSS has no variants."""
    css = "/* bg-white in a comment */\n.tag {\n    @apply bg-white text-insight-text-body;\n}\n"

    assert check_file(tmp_path, "input.css", css) == ["bg-white"]


def test_package_uses_design_tokens() -> None:
    """Templates, package scripts and input.css use tokens, so a theme can restyle all of them."""
    root = Path(__file__).parents[3]
    files = find_template_files(root)
    configs = [*CONFIGS, build_family_text_config()]
    found = [
        f"{path.relative_to(root)}:{violation.line_number} {violation.class_name}"
        for path in files
        for violation in find_violations(path, configs)
    ]

    assert {path.suffix for path in files} == {".html", ".js", ".css"}
    assert found == []
