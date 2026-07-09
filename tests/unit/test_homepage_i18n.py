"""Tests for localized homepage copy."""

from pathlib import Path

GERMAN_CATALOG = Path("insight_ui/locale/de/LC_MESSAGES/django.po")


def assert_po_translation(catalog: str, msgid: str, msgstr: str) -> None:
    """Assert that a simple one-line gettext entry has the expected German value."""
    assert f'msgid "{msgid}"\nmsgstr "{msgstr}"' in catalog


def test_homepage_german_catalog_contains_marketing_copy() -> None:
    """German homepage copy should be present in the versioned gettext catalog."""
    catalog = GERMAN_CATALOG.read_text()

    assert_po_translation(catalog, "A Django Component Framework", "Ein Django-Komponenten-Framework")
    assert_po_translation(catalog, "Everything you need", "Alles, was du brauchst")
    assert_po_translation(catalog, "JavaScript Required", "JavaScript erforderlich")
    assert_po_translation(catalog, "Browse components", "Komponenten durchsuchen")
    assert_po_translation(catalog, "Explore by category", "Nach Kategorien entdecken")
    assert_po_translation(catalog, "60+ Components", "Über 60 Komponenten")
    assert_po_translation(catalog, "Input", "Eingabe")
    assert_po_translation(catalog, "Cards", "Karten")
    assert (
        'msgid "%(count)s component"\n'
        'msgid_plural "%(count)s components"\n'
        'msgstr[0] "%(count)s Komponente"\n'
        'msgstr[1] "%(count)s Komponenten"'
    ) in catalog
