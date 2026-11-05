# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Verify compiled app-local catalogs, rendered shell text and build failures."""

import gettext
import re
from dataclasses import fields
from http import HTTPStatus
from io import BytesIO
from pathlib import Path
from unittest.mock import Mock

import pytest
from babel.messages.catalog import Catalog
from babel.messages.pofile import read_po, write_po
from bs4 import BeautifulSoup
from django.template import Context, Template
from django.template.loader import render_to_string
from django.test import RequestFactory, override_settings
from django.utils.translation import gettext as translate, override
from django.views.i18n import JavaScriptCatalog
from insight_ui.config import get_config
from insight_ui.configs import (
    FooterConfig,
    FooterContactConfig,
    IconConfig,
    LegalNoticeConfig,
    NavbarConfig,
    SearchBarConfig,
)
from scripts.hatch_i18n import CustomBuildHook, compile_catalogs

ROOT = Path(__file__).resolve().parents[3]
MESSAGES = {
    "Contact": "Kontakt",
    "Imprint": "Impressum",
    "Privacy": "Datenschutz",
    "Do you have any questions or feedback?": "Haben Sie Fragen oder Anregungen?",
    "All rights reserved.": "Alle Rechte vorbehalten.",
    "Jump to main content": "Zum Hauptinhalt springen",
    "Main navigation": "Hauptnavigation",
    "Side navigation": "Seitennavigation",
    "Search": "Suchen",
    "Search results": "Suchergebnisse",
    "No results found": "Keine Ergebnisse gefunden",
    "Toggle theme": "Design umschalten",
    "Open menu": "Menü öffnen",
    "Close": "Schließen",
}


def _fixture_catalogs(root: Path) -> None:
    """Create independent valid build inputs, including a named placeholder."""
    for domain in ("django", "djangojs"):
        path = root / "insight_ui/locale/de/LC_MESSAGES" / f"{domain}.po"
        path.parent.mkdir(parents=True, exist_ok=True)
        catalog = Catalog(locale="de", domain=domain, fuzzy=False)
        catalog.add("Hello %(name)s", "Hallo %(name)s", flags=["python-format"])
        with path.open("wb") as stream:
            write_po(stream, catalog)


@pytest.mark.parametrize("target", ["wheel", "sdist"])
def test_build_hook_compiles_ignored_catalogs_deterministically(tmp_path: Path, target: str) -> None:
    """Both targets include exact compiled outputs without committing MO files."""
    _fixture_catalogs(tmp_path)
    hook = CustomBuildHook(str(tmp_path), {}, Mock(), Mock(), "dist", target)
    data = {"artifacts": ["existing-artifact"]}
    hook.initialize("standard", data)
    expected = ["insight_ui/locale/de/LC_MESSAGES/django.mo", "insight_ui/locale/de/LC_MESSAGES/djangojs.mo"]
    assert data["artifacts"] == ["existing-artifact", *expected]
    before = [(tmp_path / name).read_bytes() for name in expected]
    compile_catalogs(tmp_path)
    assert [(tmp_path / name).read_bytes() for name in expected] == before
    assert gettext.GNUTranslations(BytesIO(before[0])).gettext("Hello %(name)s") == "Hallo %(name)s"


@pytest.mark.parametrize("defect", ["missing", "empty", "fuzzy", "placeholder", "omitted", "duplicate", "locale"])
def test_build_refuses_incomplete_or_invalid_catalogs(tmp_path: Path, defect: str) -> None:
    """Build failure prevents a superficially successful English-only wheel."""
    _fixture_catalogs(tmp_path)
    source = tmp_path / "insight_ui/locale/de/LC_MESSAGES/django.po"
    if defect == "missing":
        source.unlink()
    else:
        with source.open("rb") as stream:
            catalog = read_po(stream, locale="de", abort_invalid=True)
        message = catalog.get("Hello %(name)s")
        if defect == "empty":
            message.string = ""
        elif defect == "fuzzy":
            message.flags.add("fuzzy")
        elif defect == "placeholder":
            message.string = "Hallo %(other)s"
        elif defect == "omitted":
            message.string = "Hallo"
        elif defect == "duplicate":
            message.string = "Hallo %(name)s %(name)s"
        else:
            catalog.locale = "fr"
        with source.open("wb") as stream:
            write_po(stream, catalog)
    with pytest.raises(ValueError, match=r"catalog|Catalog"):
        compile_catalogs(tmp_path)


def test_build_checks_every_plural_form_and_handles_escaped_percent(tmp_path: Path) -> None:
    """Babel allows omitted named fields, so the package must reject them explicitly."""
    _fixture_catalogs(tmp_path)
    source = tmp_path / "insight_ui/locale/de/LC_MESSAGES/django.po"
    with source.open("rb") as stream:
        catalog = read_po(stream, locale="de", abort_invalid=True)
    message = catalog.add(
        ("%(count)s item for %(name)s", "%(count)s items for %(name)s"),
        ("%(count)s Eintrag für %(name)s", "%(count)s Einträge"),
        flags=["python-format"],
    )
    assert list(catalog.check()) == []
    with source.open("wb") as stream:
        write_po(stream, catalog)
    with pytest.raises(ValueError, match="preserve placeholders"):
        compile_catalogs(tmp_path)
    message.string = ("%(count)s Eintrag für %(name)s", "%(count)s Einträge für %(name)s")
    catalog.add("Literal %%(ignored)s: %%%(name)s", "Literal %%(ignored)s: %%%(name)s")
    with source.open("wb") as stream:
        write_po(stream, catalog)
    assert compile_catalogs(tmp_path)


@pytest.mark.parametrize(
    ("source", "literals"),
    [
        ('Behavior on mobile viewports ("hidden", "drawer").', ("hidden", "drawer")),
        ("Border radius (xs|s|m|l|xl|none).", ("xs", "s", "m", "l", "xl", "none")),
        (
            "Corner position: 'top-right', 'top-left', 'bottom-right', 'bottom-left'.",
            ("top-right", "top-left", "bottom-right", "bottom-left"),
        ),
        (
            "Horizontal alignment (start|center|end|between|around|evenly).",
            ("start", "center", "end", "between", "around", "evenly"),
        ),
        (
            "Horizontal alignment (start|center|end|stretch|baseline).",
            ("start", "center", "end", "stretch", "baseline"),
        ),
        (
            "Vertical alignment (start|center|end|between|around|evenly).",
            ("start", "center", "end", "between", "around", "evenly"),
        ),
        ("Vertical alignment (start|center|end|stretch|baseline).", ("start", "center", "end", "stretch", "baseline")),
        ("Line style (solid|dashed|dotted).", ("solid", "dashed", "dotted")),
        ("Line thickness (thin|medium|thick).", ("thin", "medium", "thick")),
        (
            "List marker style (none|disc|circle|square|decimal|decimal-leading-zero).",
            ("none", "disc", "circle", "square", "decimal", "decimal-leading-zero"),
        ),
        ("Marker position (inside|outside).", ("inside", "outside")),
        ("Orientation (horizontal|vertical).", ("horizontal", "vertical")),
        ('Position of the sidebar ("left" or "right"). Auto-detected from block context.', ("left", "right")),
        ("Spacing size (none|xs|s|m|l|xl).", ("none", "xs", "s", "m", "l", "xl")),
        ("Widget size: normal, flexible, or compact.", ("normal", "flexible", "compact")),
        ('Width of the sidebar ("narrow", "normal", "wide").', ("narrow", "normal", "wide")),
        ("Language for the syntax highlighting, e.g. python.", ("python",)),
        (
            "Settle delay appended to hx-swap, e.g. '300ms', so CSS transitions have time to run.",
            ("hx-swap", "300ms", "CSS"),
        ),
        (
            "URL for form action. Do not use together with htmx; use htmx.request_url instead for HTMX requests.",
            ("htmx.request_url",),
        ),
        (
            "**True** if `input_type='checkbox'` and the checkbox should be selected.",
            ("True", "input_type", "checkbox"),
        ),
    ],
)
def test_german_config_docs_preserve_literal_api_values(source: str, literals: tuple[str, ...]) -> None:
    """A German description must still give working configuration values and examples."""
    with override("de"):
        translated = translate(source)
    assert translated != source
    for literal in literals:
        assert re.search(r"(?<![\w-])" + re.escape(literal) + r"(?![\w-])", translated), literal


def test_flip_back_accessible_name_identifies_card_front_not_home_navigation() -> None:
    """The local flip action must not announce a navigation to a home page."""
    source = '{% load insight_tags %}{% flip_card title="Example" content="Front" back_content="Back" %}'
    with override("de"):
        rendered = Template(source).render(Context(get_config()))
    soup = BeautifulSoup(rendered, "html.parser")
    control = soup.select_one("[data-flip-back] button[data-flip-trigger]")
    assert control["aria-label"] == "Zurück zur Vorderseite dieser Karte"
    assert "Startseite" not in control["aria-label"]


def test_icon_rtl_docs_distinguish_default_none_from_false() -> None:
    """Not supplying a setting must not be described as disabling automatic mirroring."""
    field = next(field for field in fields(IconConfig) if field.name == "mirror_rtl")
    with override("de"):
        description = str(field.metadata["doc"])
    assert "None" in description
    assert "deaktiviert" not in description
    assert IconConfig(name="arrow-left", mirror_rtl=None).mirrors_in_rtl is True
    assert IconConfig(name="arrow-left", mirror_rtl=False).mirrors_in_rtl is False
    assert IconConfig(name="arrow-left", mirror_rtl=True).mirrors_in_rtl is True


@pytest.mark.parametrize("domain", ["django", "djangojs"])
def test_all_package_messages_compile_without_fuzzy_or_missing_forms(domain: str) -> None:
    """Every marked message has a translated form with valid gettext placeholders."""
    source = ROOT / "insight_ui/locale/de/LC_MESSAGES" / f"{domain}.po"
    with source.open("rb") as stream:
        catalog = read_po(stream, locale="de", abort_invalid=True)
    assert str(catalog.locale) == "de"
    assert not catalog.fuzzy
    assert list(catalog.check()) == []
    for message in catalog:
        if message.id:
            assert "fuzzy" not in message.flags
            assert message.string
            if isinstance(message.string, tuple):
                assert all(message.string)


@override_settings(LOCALE_PATHS=[])
@pytest.mark.parametrize("language", ["de", "en"])
def test_app_local_shell_and_accessible_names_render_in_active_language(language: str) -> None:
    """Real package tags translate visible text and aria labels without host catalogs."""
    context = {
        **get_config(),
        "footer": FooterConfig(
            contact=FooterContactConfig("team@example.com", "/imprint/", "/privacy/"),
            legal=LegalNoticeConfig(year=2026, holder="Example"),
        ),
        "navbar": NavbarConfig(show_theme_toggle=True, show_language_selector=True, hide_login=True),
        "search": SearchBarConfig(enable_search=True),
    }
    source = """{% load insight_tags layout_tags %}
        {% navbar config=navbar %}{% footer config=footer %}{% search_bar config=search %}
        {% sidebar static=False %}Contents{% endsidebar %}
        {% modal id="translated-modal" title="Example" %}Content{% endmodal %}"""
    with override(language):
        rendered = Template(source).render(Context(context))
        base = render_to_string("insight_ui/base.html", get_config())
    soup = BeautifulSoup(rendered, "html.parser")
    expected = {message: translated if language == "de" else message for message, translated in MESSAGES.items()}
    for message in ("Contact", "Imprint", "Privacy", "Do you have any questions or feedback?", "All rights reserved."):
        assert expected[message] in soup.get_text(" ", strip=True)
    assert soup.select_one("nav[aria-label]")["aria-label"] == expected["Main navigation"]
    assert soup.select_one("aside[aria-label]")["aria-label"] == expected["Side navigation"]
    assert soup.select_one("button[data-insight-collapsible]")["aria-label"] == expected["Open menu"]
    assert soup.select_one("button[data-insight-theme-toggle]")["aria-label"] == expected["Toggle theme"]
    assert soup.select_one('[data-insight-dismiss="modal"][aria-label]')["aria-label"] == expected["Close"]
    assert soup.select_one('label[for="search"]').get_text(strip=True) == expected["Search"]
    assert soup.select_one('[role="listbox"]')["aria-label"] == expected["Search results"]
    assert expected["No results found"] in str(soup.select_one('template[data-search-template="no-results"]'))
    assert expected["Jump to main content"] in base


def test_javascript_catalog_delivers_translations_and_plural_forms() -> None:
    """Django serves the app's compiled JS domain, not the source checkout's PO text."""
    with override_settings(LOCALE_PATHS=[]), override("de"):
        response = JavaScriptCatalog.as_view(packages=["insight_ui"])(RequestFactory().get("/jsi18n/"))
    assert response.status_code == HTTPStatus.OK
    assert '"Copy": "Kopieren"' in response.content.decode()
    with (ROOT / "insight_ui/locale/de/LC_MESSAGES/djangojs.mo").open("rb") as stream:
        translations = gettext.GNUTranslations(stream)
    singular, plural = "%(count)s option selected", "%(count)s options selected"
    assert translations.ngettext(singular, plural, 1) % {"count": 1} == "1 Option ausgewählt"
    assert translations.ngettext(singular, plural, 2) % {"count": 2} == "2 Optionen ausgewählt"
