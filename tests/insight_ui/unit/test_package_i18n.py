# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Verify compiled app-local catalogs, rendered shell text and build failures."""

import gettext
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
from django.utils.translation import override
from django.views.i18n import JavaScriptCatalog
from insight_ui.config import get_config
from insight_ui.configs import (
    ButtonConfig,
    FooterConfig,
    FooterContactConfig,
    HeroConfig,
    LegalNoticeConfig,
    NavbarConfig,
    SearchBarConfig,
)
from scripts.hatch_i18n import CustomBuildHook, compile_catalogs, extract_source_messages

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
    (root / "insight_ui/messages.py").write_text('gettext_lazy("Hello %(name)s")', encoding="utf-8")
    (root / "insight_ui/messages.js").write_text('gettext("Hello %(name)s");', encoding="utf-8")


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
    ("filename", "content", "message_id", "context"),
    [
        ("added.py", 'gettext_lazy("New label")', "New label", None),
        ("added.py", 'pgettext_lazy("menu", "New label")', "New label", "menu"),
        ("added.py", 'ngettext_lazy("one new", "many new", count)', ("one new", "many new"), None),
        ("added.html", '  {% translate "New label" %}', "New label", None),
        ("added.txt", '{% trans "New label" context "menu" %}', "New label", "menu"),
        (
            "added.html",
            "  <div>\n    {% blocktranslate trimmed count n=items|length %}\n      {{ n }} new item\n"
            "    {% plural %}\n      {{ n }} new items\n    {% endblocktranslate %}\n  </div>",
            ("%(n)s new item", "%(n)s new items"),
            None,
        ),
        ("added.js", 'gettext("New label");', "New label", None),
        ("added.js", 'pgettext("menu", "New label");', "New label", "menu"),
        ("added.js", 'ngettext("one new", "many new", count);', ("one new", "many new"), None),
    ],
)
def test_build_rejects_new_source_messages_until_catalog_is_updated(
    tmp_path: Path, filename: str, content: str, message_id: str | tuple[str, str], context: str | None
) -> None:
    """Real source additions cannot pass by validating only existing PO entries."""
    _fixture_catalogs(tmp_path)
    domain = "djangojs" if filename.endswith(".js") else "django"
    (tmp_path / "insight_ui" / filename).write_text(content, encoding="utf-8")
    path = tmp_path / f"insight_ui/locale/de/LC_MESSAGES/{domain}.po"
    with path.open("rb") as stream:
        catalog = read_po(stream)
    # A wrong context or stale plural is not a match for the new source message.
    if context:
        catalog.add(message_id, "Andere Bedeutung", context="other")
    elif isinstance(message_id, tuple):
        catalog.add((message_id[0], message_id[1] + " stale"), message_id)
    with path.open("wb") as stream:
        write_po(stream, catalog)
    with pytest.raises(ValueError, match="omits source messages"):
        compile_catalogs(tmp_path)
    assert not list(tmp_path.rglob("*.mo"))
    catalog.delete(message_id, context=context)
    catalog.add(message_id, message_id, context=context)
    with path.open("wb") as stream:
        write_po(stream, catalog)
    assert compile_catalogs(tmp_path)


def test_source_extraction_excludes_hosts_and_generated_minified_javascript(tmp_path: Path) -> None:
    """Only reusable package sources belong to the package catalog gate."""
    _fixture_catalogs(tmp_path)
    (tmp_path / "host.py").write_text('_("Host-only message")', encoding="utf-8")
    (tmp_path / "insight_ui/generated.min.js").write_text('gettext("Generated duplicate");', encoding="utf-8")
    assert compile_catalogs(tmp_path)


def test_installed_legacy_api_contract_remains_composable() -> None:
    """Keep the accepted host's button, hero and legal-footer constructor contract."""
    assert "type" in {field.name for field in fields(ButtonConfig)}
    assert "badge_config" in {field.name for field in fields(HeroConfig)}
    assert {"holder_url", "holder_logo"} <= {field.name for field in fields(LegalNoticeConfig)}
    assert ButtonConfig(label="Docs", type="primary").type == "primary"


def test_javascript_catalog_delivers_package_translation() -> None:
    """Serve the legacy package's actual five-message JS domain without host catalogs."""
    with override_settings(LOCALE_PATHS=[]), override("de"):
        response = JavaScriptCatalog.as_view(packages=["insight_ui"])(RequestFactory().get("/jsi18n/"))
    assert response.status_code == HTTPStatus.OK
    assert '"Page %(current)s / %(total)s": "Seite %(current)s / %(total)s"' in response.content.decode()


@pytest.mark.parametrize("domain", ["django", "djangojs"])
def test_all_package_messages_compile_without_fuzzy_or_missing_forms(domain: str) -> None:
    """Every marked message has a translated form with valid gettext placeholders."""
    source = ROOT / "insight_ui/locale/de/LC_MESSAGES" / f"{domain}.po"
    with source.open("rb") as stream:
        catalog = read_po(stream, locale="de", abort_invalid=True)
    assert str(catalog.locale) == "de"
    assert not catalog.fuzzy
    assert list(catalog.check()) == []
    assert extract_source_messages(ROOT)[domain] <= {(message.id, message.context) for message in catalog if message.id}
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
    assert expected["Jump to main content"] in base + rendered
