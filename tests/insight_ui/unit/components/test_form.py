# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for the form component."""

import re
import warnings
from pathlib import Path

import pytest
from bs4 import BeautifulSoup
from insight_ui.configs import FormConfig, HtmxConfig

import insight_ui
from tests.insight_ui.unit.components.test_template_tags import TemplateTagsTestCase

INPUT_CSS = Path("insight_ui/utils/input.css")
BUILT_CSS = Path(insight_ui.__file__).parent / "static/insight_ui/css/tailwind.css"

# The idle rule must be the standalone ".htmx-indicator" selector, never the
# ".htmx-request .htmx-indicator" pair, which is followed by a comma.
IDLE_INDICATOR_HIDDEN = re.compile(r"(?<![\w.-])\.htmx-indicator\s*\{[^}]*\bvisibility:\s*hidden\b")
ACTIVE_INDICATOR_VISIBLE = re.compile(r"\.htmx-request\.htmx-indicator\s*\{[^}]*\bvisibility:\s*visible\b")
IDLE_INDICATOR_FADE = re.compile(r"(?<![\w.-])\.htmx-indicator\s*\{[^}]*\btransition:[^}]*\bopacity\b")


class TestForm(TemplateTagsTestCase):
    """Test suite for the form component."""

    def test_form_basic(self) -> None:
        """Test für grundlegende form Funktionalität."""
        template_string = """
        {% load insight_tags %}
        {% form title="Test Form" request_url="/api/form_submit/" %}
        """
        rendered = self.render_template(template_string)
        assert "Test Form" in rendered

    def test_htmx_indicator_is_not_itself_the_live_region(self) -> None:
        """The live region must stay in the accessibility tree while the indicator is hidden."""
        rendered = self.render_template(
            "{% load insight_tags %}{% form title='Contact' htmx_config=htmx %}",
            {"htmx": HtmxConfig(request_url="/submit/", target="#result")},
        )
        soup = BeautifulSoup(rendered, "html.parser")
        indicator = soup.select_one(".htmx-indicator")
        live_region = soup.select_one("[role='status'][aria-live='polite']")

        assert indicator is not None
        assert live_region is not None
        # visibility: hidden drops the indicator from the accessibility tree, so
        # carrying role/aria-live itself would remove the region along with it.
        assert not indicator.has_attr("role")
        assert not indicator.has_attr("aria-live")
        assert "htmx-indicator" not in live_region.get("class", [])
        assert live_region.select_one(".htmx-indicator") is indicator

    def test_form_config_warns_on_conflicting_request_url_and_htmx(self) -> None:
        """FormConfig warns when both request_url and htmx_config.request_url are set."""
        with pytest.warns(UserWarning, match="both 'request_url' and 'htmx_config.request_url'"):
            FormConfig(request_url="/submit/", htmx_config=HtmxConfig(request_url="/submit-htmx/"))

    def test_form_config_no_warning_with_only_request_url(self) -> None:
        """FormConfig does not warn when only request_url is set."""
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            FormConfig(request_url="/submit/")
        assert len(caught) == 0


def test_css_source_hides_idle_htmx_indicator_from_accessibility_tree() -> None:
    """Opacity alone leaves the indicator in the accessibility tree; visibility removes it."""
    css = INPUT_CSS.read_text()

    assert IDLE_INDICATOR_HIDDEN.search(css), "Idle .htmx-indicator must set visibility: hidden"
    assert ACTIVE_INDICATOR_VISIBLE.search(css), ".htmx-request must restore visibility: visible"
    assert IDLE_INDICATOR_FADE.search(css), "The opacity fade must survive the visibility fix"


def test_built_css_hides_idle_htmx_indicator_from_accessibility_tree() -> None:
    """The shipped stylesheet must carry the fix, so a missing rebuild fails here."""
    css = BUILT_CSS.read_text()

    assert IDLE_INDICATOR_HIDDEN.search(css), "Rebuild tailwind.css: idle indicator is still only faded out"
    assert ACTIVE_INDICATOR_VISIBLE.search(css), "Rebuild tailwind.css: .htmx-request never restores visibility"
