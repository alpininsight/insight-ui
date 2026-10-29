# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for the shared Insight UI base template."""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

import pytest
from bs4 import BeautifulSoup
from django.core.management import call_command
from django.template import Context, Template
from django.template.loader import render_to_string
from django.test import TestCase, override_settings
from insight_ui.config import CONFIG_DEFAULTS, get_config

if TYPE_CHECKING:
    from pathlib import Path

urlpatterns = []


class TestBaseTemplate(TestCase):
    """Test suite for the base template contract."""

    @override_settings(
        ROOT_URLCONF=__name__,
        STORAGES={"staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"}},
    )
    def test_base_template_does_not_require_javascript_catalog_url(self) -> None:
        """Host apps may render the base template without installing Django's JavaScriptCatalog URL."""
        sys.modules[__name__].urlpatterns = []

        rendered = render_to_string("insight_ui/base.html", get_config())

        assert "<!DOCTYPE html>" in rendered
        assert "javascript-catalog" not in rendered

    @override_settings(
        ROOT_URLCONF=__name__,
        STORAGES={"staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"}},
        INSIGHT_UI={"webmanifest": "example_app/favicon/site.webmanifest"},
    )
    def test_base_template_uses_configured_webmanifest(self) -> None:
        """Host apps should be able to provide their own web app manifest."""
        sys.modules[__name__].urlpatterns = []

        rendered = render_to_string("insight_ui/base.html", get_config())

        assert '<link rel="manifest" href="/static/example_app/favicon/site.webmanifest">' in rendered

    @override_settings(
        ROOT_URLCONF=__name__,
        STORAGES={"staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"}},
        INSIGHT_UI={"safari_mask_icon_color": "#123456"},
    )
    def test_base_template_renders_mobile_icon_contract(self) -> None:
        """Default manifest and platform icon metadata should remain complete."""
        sys.modules[__name__].urlpatterns = []

        rendered = render_to_string("insight_ui/base.html", get_config())

        assert '<link rel="manifest" href="/static/insight_ui/favicon/site.webmanifest">' in rendered
        assert '<link rel="apple-touch-icon" sizes="180x180"' in rendered
        assert 'color="#123456"' in rendered


@override_settings(
    ROOT_URLCONF=__name__,
    STORAGES={"staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"}},
)
class TestBaseTemplateThemeAndHtmx(TestCase):
    """Pre-paint theme follows the system preference; HTMX sources are configurable."""

    def render_base(self) -> str:
        """Render the base template with the resolved settings context."""
        sys.modules[__name__].urlpatterns = []
        return render_to_string("insight_ui/base.html", get_config())

    def test_pre_paint_script_falls_back_to_system_preference(self) -> None:
        """Without a saved theme the pre-paint script uses prefers-color-scheme."""
        assert "prefers-color-scheme: dark" in self.render_base()

    def test_default_htmx_sources_keep_sri(self) -> None:
        """Default output loads the jsdelivr URLs with their SRI hashes."""
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
        htmx_scripts = Template("{% load insight_assets %}{% insight_htmx_scripts %}").render(Context({}))
        assert len(BeautifulSoup(htmx_scripts, "html.parser").find_all("script")) == 1

    def test_htmx_scripts_do_not_need_the_context_processor(self) -> None:
        """The tag reads settings directly."""
        rendered = Template("{% load insight_assets %}{% insight_htmx_scripts %}").render(Context({}))
        assert CONFIG_DEFAULTS["htmx"]["src"] in rendered

    def test_tooltip_delay_defaults_to_the_library_setting(self) -> None:
        """All tooltips share one hover delay, set on <html> for the floater script."""
        html = BeautifulSoup(self.render_base(), "html.parser").find("html")

        assert html["data-tooltip-delay"] == str(CONFIG_DEFAULTS["tooltip_show_delay"])

    @override_settings(INSIGHT_UI={"tooltip_show_delay": 250})
    def test_tooltip_delay_follows_the_host_setting(self) -> None:
        """Hosts change the hover delay for all tooltips in one place."""
        html = BeautifulSoup(self.render_base(), "html.parser").find("html")

        assert html["data-tooltip-delay"] == "250"

    @override_settings(INSIGHT_UI={"htmx": {"src": 'x" onload="alert(1)'}})
    def test_htmx_src_is_escaped(self) -> None:
        """Configured URLs are HTML-escaped."""
        rendered = Template("{% load insight_assets %}{% insight_htmx_scripts %}").render(Context({}))
        assert 'onload="alert(1)"' not in rendered


@pytest.mark.parametrize("brand", [{}, {"title": "Host application"}, {"title": "<Host>"}])
def test_base_page_title_preserves_host_configuration(brand: dict[str, str]) -> None:
    """The fallback stays nonempty, while legacy host titles remain escaped."""
    with override_settings(
        ROOT_URLCONF=__name__,
        STORAGES={"staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"}},
        INSIGHT_UI={"brand": brand},
    ):
        rendered = render_to_string("insight_ui/base.html", get_config())
        expected = {"Host application": "Host application", "<Host>": "&lt;Host&gt;"}.get(
            brand.get("title", ""), "Django-Insight-UI"
        )
        assert f"<title>{expected}</title>" in rendered
        override = Template(
            '{% extends "insight_ui/base.html" %}{% block title %}Page-specific title{% endblock %}'
        ).render(Context(get_config()))
        assert "<title>Page-specific title</title>" in override


def test_default_base_page_renders_with_strict_staticfiles(tmp_path: Path) -> None:
    """Production defaults must work without icon overrides or lenient storage."""
    with override_settings(
        DEBUG=False,
        ROOT_URLCONF=__name__,
        STATIC_ROOT=tmp_path,
        STORAGES={"staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"}},
        INSIGHT_UI={},
    ):
        call_command("collectstatic", interactive=False, verbosity=0)
        rendered = render_to_string("insight_ui/base.html", get_config())
        assert "<title>Django-Insight-UI</title>" in rendered
        assert 'rel="mask-icon" href="/static/insight_ui/svg/insight-ui-logo.' in rendered


def test_global_loading_bar_is_hidden_from_assistive_technology() -> None:
    """The bar is decorative; a permanent progressbar role would be announced as busy all the time."""
    soup = BeautifulSoup(render_to_string("insight_ui/components/htmx_loading_indicator.html"), "html.parser")

    bar = soup.find(id="insight-global-loading-indicator")
    assert bar["aria-hidden"] == "true"
    assert not bar.has_attr("role")
    assert soup.find(attrs={"role": "progressbar"}) is None


def test_slow_requests_are_announced_through_a_polite_status_region() -> None:
    """Screen reader users get feedback for slow requests of components without their own indicator."""
    soup = BeautifulSoup(render_to_string("insight_ui/components/htmx_loading_indicator.html"), "html.parser")

    region = soup.find(id="insight-global-loading-status")
    assert region["role"] == "status"
    assert region["aria-live"] == "polite"
    assert region["data-message"] == "Loading..."
    assert region.get_text(strip=True) == ""


@override_settings(STORAGES={"staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"}})
def test_skip_link_is_the_first_stop_on_every_page() -> None:
    """Every page, with or without the package navbar, starts with a link that jumps over the navigation."""
    soup = BeautifulSoup(render_to_string("insight_ui/base.html", get_config()), "html.parser")

    first_link = soup.body.find(["a", "button", "input", "select", "textarea"])
    assert first_link["href"] == "#main-content"
    assert first_link.get_text(strip=True) == "Jump to main content"


@override_settings(STORAGES={"staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"}})
def test_skip_link_target_takes_the_focus() -> None:
    """The target is focusable, so screen readers continue reading there after the jump."""
    soup = BeautifulSoup(render_to_string("insight_ui/base.html", get_config()), "html.parser")

    assert soup.find(id="main-content")["tabindex"] == "-1"


def test_navbar_has_no_skip_link_of_its_own() -> None:
    """The base template provides the skip link once; a navbar must not add a second one."""
    soup = BeautifulSoup(Template("{% load insight_tags %}{% navbar %}").render(Context()), "html.parser")

    assert soup.find("a", href="#main-content") is None
