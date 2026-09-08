# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for the brand_mark component."""

import re
from pathlib import Path

import pytest
from insight_ui.configs.utils import BrandMarkConfig

import insight_ui
from tests.insight_ui.unit.components.test_template_tags import TemplateTagsTestCase


@pytest.mark.parametrize(
    ("class_name", "property_name", "value"),
    [
        ("sm:gap-3", "gap", "calc(var(--spacing) * 3)"),
        ("sm:text-xl", "font-size", "var(--text-xl)"),
        ("sm:text-xl", "line-height", "var(--tw-leading, var(--text-xl--line-height))"),
    ],
)
def test_brand_mark_responsive_rules_are_packaged(class_name: str, property_name: str, value: str) -> None:
    """The shipped stylesheet restores desktop sizing at the sm breakpoint."""
    css = (Path(insight_ui.__file__).parent / "static/insight_ui/css/tailwind.css").read_text(encoding="utf-8")
    # Keep flat utility rules inside sm blocks, excluding other breakpoints.
    media_blocks = re.findall(r"@media\s*\(width\s*>=\s*40rem\)\s*\{((?:[^{}]|\{[^{}]*\})*)\}", css)
    assert media_blocks, "Missing packaged sm media query"
    selector = class_name.replace(":", r"\:")
    rule = re.search(rf"\.{re.escape(selector)}\s*\{{([^{{}}]*)\}}", "\n".join(media_blocks))
    assert rule is not None, f"Missing packaged responsive rule for {class_name}"
    assert re.search(rf"\b{property_name}:\s*{re.escape(value)}\s*;", rule[1]), (
        f"Missing packaged {property_name} declaration for {class_name}"
    )


class TestBrandMark(TemplateTagsTestCase):
    """Test suite for the brand_mark component."""

    def test_brand_mark_renders_default_text(self) -> None:
        """Default brand mark renders without errors."""
        rendered = self.render_template("{% load insight_tags %}{% brand_mark %}")
        assert rendered.strip() != ""
        assert '<span class="font-medium text-insight-headline">' in rendered
        assert '<span class="font-bold text-insight-secondary">' in rendered

    def test_brand_mark_custom_text(self) -> None:
        """primary_text / secondary_text override the wordmark runs."""
        rendered = self.render_template(
            '{% load insight_tags %}{% brand_mark primary_text="Foo Bar" secondary_text="Cloud" %}'
        )
        assert '<span class="font-medium text-insight-headline">Foo Bar</span>' in rendered
        assert '<span class="font-bold text-insight-secondary">Cloud</span>' in rendered

    def test_brand_mark_config(self) -> None:
        """A config dict configures the mark."""
        rendered = self.render_template(
            "{% load insight_tags %}{% brand_mark config=cfg %}",
            context={"cfg": BrandMarkConfig(primary_text="Custom", secondary_text="Brand")},
        )
        assert "Custom" in rendered
        assert "Brand" in rendered

    def test_brand_mark_keeps_long_product_names_compact_on_mobile(self) -> None:
        """Long wordmarks leave room for the navbar disclosure control."""
        rendered = self.render_template(
            '{% load insight_tags %}{% brand_mark primary_text="Alpin Insight" secondary_text="OIDC Provider" %}'
        )
        assert "items-center min-w-0" in rendered
        assert "text-sm tracking-tight whitespace-nowrap sm:text-xl" in rendered

    def test_brand_mark_secondary_text_uses_the_accent_token(self) -> None:
        """The wordmark's second half is the accent, not the primary.

        insight-brand DESIGN.md makes Signal Orange the single accent and keeps
        it constant across the Light and Dark palettes, while text colours flip
        between them. The template carried ``text-insight-primary`` here, so the
        word rendered in Berliner Blau in both themes -- off-brand, and on the
        dark canvas it was dark navy on near-black at roughly 1.3:1.

        Pinned separately from the render smoke tests above because both classes
        are valid CSS and both render without error: nothing else in the suite
        can tell the difference.
        """
        rendered = self.render_template(
            '{% load insight_tags %}{% brand_mark primary_text="Foo Bar" secondary_text="Cloud" %}'
        )
        assert '<span class="font-bold text-insight-secondary">Cloud</span>' in rendered
