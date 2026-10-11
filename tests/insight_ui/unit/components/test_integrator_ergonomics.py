# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for first-integration ergonomics: form/navbar tag arguments, theme toggle and HTMX sources."""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

import pytest
from bs4 import BeautifulSoup
from django.template import Context, Template
from django.template.loader import render_to_string
from django.test import TestCase, override_settings
from insight_ui.config import CONFIG_DEFAULTS, get_config
from insight_ui.configs import AlertConfig, BrandMarkConfig, FormConfig, InfoboxConfig, NavbarConfig, StatusScreenConfig

from tests.insight_ui.unit.components.test_template_tags import TemplateTagsTestCase

if TYPE_CHECKING:
    from collections.abc import Callable

urlpatterns = []
STATIC_STORAGE = {"staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"}}


class TestFormTagArguments(TemplateTagsTestCase):
    """Common FormConfig options are available as tag arguments (#704)."""

    def test_submit_reset_label_and_method_as_tag_arguments(self) -> None:
        """submit_label, reset_label and method work directly on the tag."""
        rendered = self.render_template(
            '{% load insight_tags %}{% form title="Contact" submit_label="Send" reset_label="Clear" '
            'show_reset_button=True method="get" request_url="/search/" %}'
        )
        soup = BeautifulSoup(rendered, "html.parser")
        form = soup.find("form")
        assert form is not None
        assert form["method"] == "get"
        labels = [button.get_text(strip=True) for button in soup.find_all("button")]
        assert "Send" in labels
        assert "Clear" in labels

    def test_tag_arguments_override_an_existing_config(self) -> None:
        """Tag arguments override a supplied Config without mutating it."""
        config = FormConfig(title="Contact", submit_label="Submit", method="post")
        rendered = self.render_template(
            '{% load insight_tags %}{% form config=form_config submit_label="Send" %}', {"form_config": config}
        )
        assert "Send" in BeautifulSoup(rendered, "html.parser").get_text()
        assert config.submit_label == "Submit"  # the supplied Config is not mutated

    def test_omitted_arguments_keep_config_values(self) -> None:
        """Omitted tag arguments keep the Config's values."""
        config = FormConfig(title="Contact", submit_label="Go", method="get")
        rendered = self.render_template("{% load insight_tags %}{% form config=form_config %}", {"form_config": config})
        soup = BeautifulSoup(rendered, "html.parser")
        assert soup.find("form")["method"] == "get"
        assert "Go" in soup.get_text()


class TestNavbarWithoutConfig(TemplateTagsTestCase):
    """{% navbar %} renders brand defaults without a Config (#704)."""

    @override_settings(INSIGHT_UI={"brand": {"mark": BrandMarkConfig(primary_text="Acme", secondary_text="Prototype")}})
    def test_navbar_without_config_uses_brand_defaults(self) -> None:
        """Without a Config the navbar shows the configured brand."""
        rendered = self.render_template("{% load insight_tags %}{% navbar %}")
        soup = BeautifulSoup(rendered, "html.parser")
        assert soup.find("nav") is not None
        assert "Acme" in soup.get_text()

    def test_explicit_config_still_wins(self) -> None:
        """An explicit NavbarConfig is rendered as supplied."""
        rendered = self.render_template(
            "{% load insight_tags %}{% navbar config=navbar_config %}",
            {"navbar_config": NavbarConfig(show_theme_toggle=True)},
        )
        assert "data-insight-theme-toggle" in rendered


class TestThemeToggleTag(TemplateTagsTestCase):
    """A standalone toggle tag outside the navbar (#702)."""

    def test_theme_toggle_tag_renders_toggle_button(self) -> None:
        """The tag renders the same toggle button as the navbar."""
        rendered = self.render_template("{% load insight_tags %}{% theme_toggle %}")
        button = BeautifulSoup(rendered, "html.parser").find("button")
        assert button is not None
        assert button.has_attr("data-insight-theme-toggle")
        assert button.get("aria-label")


@override_settings(ROOT_URLCONF=__name__, STORAGES=STATIC_STORAGE)
class TestBaseTemplateThemeAndHtmx(TestCase):
    """Pre-paint theme follows the system preference (#702); HTMX sources are configurable (#703)."""

    def render_base(self) -> str:
        """Render the base template with the resolved settings context."""
        sys.modules[__name__].urlpatterns = []
        return render_to_string("insight_ui/base.html", get_config())

    def test_pre_paint_script_falls_back_to_system_preference(self) -> None:
        """Without a saved theme the pre-paint script uses prefers-color-scheme."""
        rendered = self.render_base()
        assert "prefers-color-scheme: dark" in rendered
        assert "getItem('insight-ui-theme') || 'light'" not in rendered

    def test_default_htmx_sources_are_unchanged(self) -> None:
        """Default output keeps today's jsdelivr URLs and SRI hashes."""
        scripts = {
            tag["src"]: tag for tag in BeautifulSoup(self.render_base(), "html.parser").find_all("script", src=True)
        }
        defaults = CONFIG_DEFAULTS["htmx"]
        assert scripts[defaults["src"]]["integrity"] == defaults["integrity"]
        assert scripts[defaults["src"]]["crossorigin"] == "anonymous"
        assert scripts[defaults["ws_src"]]["integrity"] == defaults["ws_integrity"]

    @override_settings(
        INSIGHT_UI={"htmx": {"src": "/static/vendor/htmx.min.js", "integrity": "", "ws_src": "", "ws_integrity": ""}}
    )
    def test_self_hosted_htmx_without_sri_and_omitted_ws(self) -> None:
        """A self-hosted src without SRI renders; an empty ws_src omits the script."""
        rendered = self.render_base()
        assert "cdn.jsdelivr.net" not in rendered
        tag = BeautifulSoup(rendered, "html.parser").find("script", src="/static/vendor/htmx.min.js")
        assert tag is not None
        assert not tag.has_attr("integrity")

    def test_htmx_scripts_do_not_need_the_context_processor(self) -> None:
        """The tag reads settings directly."""
        rendered = Template("{% load insight_assets %}{% insight_htmx_scripts %}").render(Context({}))
        assert CONFIG_DEFAULTS["htmx"]["src"] in rendered

    @override_settings(INSIGHT_UI={"htmx": {"src": 'x" onload="alert(1)'}})
    def test_htmx_src_is_escaped(self) -> None:
        """Configured URLs are HTML-escaped."""
        rendered = Template("{% load insight_assets %}{% insight_htmx_scripts %}").render(Context({}))
        assert 'onload="alert(1)"' not in rendered


@pytest.mark.parametrize(
    ("factory", "field_name"),
    [
        (lambda: AlertConfig(type="danger"), "type"),
        (lambda: InfoboxConfig(message="m", info_type="danger"), "info_type"),
        (lambda: StatusScreenConfig(title="t", status="danger"), "status"),
    ],
)
def test_danger_alert_type_error_points_to_error(factory: Callable[[], object], field_name: str) -> None:
    """'danger' stays rejected for alert types, but the message names the fix (#705)."""
    with pytest.raises(ValueError, match=rf"Invalid {field_name} 'danger'.*Use 'error'"):
        factory()
