# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Verify compiled app-local catalogs, rendered shell text and build failures."""

import gettext
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
from django.utils.translation import override
from django.views.i18n import JavaScriptCatalog
from insight_ui.config import get_config
from insight_ui.configs import FooterConfig, FooterContactConfig, LegalNoticeConfig, NavbarConfig, SearchBarConfig
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


@pytest.mark.parametrize("defect", ["missing", "empty", "fuzzy", "placeholder", "locale"])
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
        else:
            catalog.locale = "fr"
        with source.open("wb") as stream:
            write_po(stream, catalog)
    with pytest.raises(ValueError, match=r"catalog|Catalog"):
        compile_catalogs(tmp_path)


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
