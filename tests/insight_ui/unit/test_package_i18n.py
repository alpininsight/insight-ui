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
    ButtonConfig,
    CarouselConfig,
    FooterConfig,
    FooterContactConfig,
    HtmxConfig,
    IconConfig,
    InfiniteScrollConfig,
    LegalNoticeConfig,
    ListConfig,
    LiveContentConfig,
    MultiselectConfig,
    NavbarConfig,
    NavbarLinkConfig,
    RingCarouselConfig,
    SearchBarConfig,
    ToggleViewConfig,
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


@pytest.mark.parametrize("component", ["button", "navbar", "footer"])
def test_external_link_announces_complete_new_tab_context(component: str) -> None:
    """German accessible names must explain that an external link opens a new tab."""
    link = NavbarLinkConfig(text="Docs", request_url="https://example.com/", external=True)
    configs = {
        "button": ButtonConfig(label="Docs", request_url="https://example.com/", external=True),
        "navbar": NavbarConfig(links=[link], hide_login=True),
        "footer": FooterConfig(links=[link]),
    }
    with override("de"):
        rendered = Template("{% load insight_tags %}{% " + component + " config=config %}").render(
            Context({"config": configs[component]})
        )
    external = BeautifulSoup(rendered, "html.parser").select_one('a[href="https://example.com/"]')
    assert external["target"] == "_blank"
    assert "(wird in einem neuen Tab geöffnet)" in external.get_text(" ", strip=True)


def test_ordered_list_description_translates_prose_around_double_backtick_code() -> None:
    """Protecting RST code spans must not freeze English prose between them."""
    field = next(field for field in fields(ListConfig) if field.name == "ordered")
    with override("de"):
        description = str(field.metadata["doc"])
    assert "Verwenden Sie" in description
    assert "anstelle von" in description
    assert "``<ol>``" in description
    assert "``<ul>``" in description
    assert "instead of" not in description


def test_live_content_description_preserves_htmx_constructor_fields() -> None:
    """Readers must be able to copy documented option names into HtmxConfig."""
    field = next(field for field in fields(LiveContentConfig) if field.name == "htmx")
    with override("de"):
        description = str(field.metadata["doc"])
    assert "Gemeinsame Anfrageoptionen" in description
    assert all(f"`{name}`" in description for name in ("target", "swap_method", "vals"))


def test_infinite_scroll_description_uses_actual_loading_indicator_option() -> None:
    """Both source and German docs must name the real HtmxConfig constructor field."""
    field = next(field for field in fields(InfiniteScrollConfig) if field.name == "htmx")
    for language in ("en", "de"):
        with override(language):
            description = str(field.metadata["doc"])
        assert "loading_indicator_id" in description
        assert "vals" in description
    config = HtmxConfig(loading_indicator_id="#spinner", vals={"page": 2})
    assert config.loading_indicator_id == "#spinner"
    assert config.vals == {"page": 2}


@pytest.mark.parametrize("config", [CarouselConfig, RingCarouselConfig, ToggleViewConfig])
def test_custom_item_template_description_preserves_context_variable(config: type) -> None:
    """Custom template authors need the literal item context key in every carousel."""
    field = next(field for field in fields(config) if field.name == "item_template")
    with override("de"):
        description = str(field.metadata["doc"])
    assert "Kontextvariable `item`" in description


def test_multiselect_bulk_actions_render_grammatical_german_labels() -> None:
    """Both visible controls clearly communicate their opposite bulk actions."""
    config = MultiselectConfig(name="tags", options=["Python", "Django"], show_buttons=True)
    with override("de"):
        rendered = Template("{% load insight_tags %}{% multiselect config=config %}").render(
            Context({"config": config})
        )
    soup = BeautifulSoup(rendered, "html.parser")
    assert soup.select_one("button.select-all").get_text(strip=True) == "Alle auswählen"
    assert soup.select_one("button.deselect-all").get_text(strip=True) == "Alle Optionen abwählen"


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
