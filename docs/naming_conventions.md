# Benennungskonventionen (Version 0.1.0)

Dieser Leitfaden dokumentiert die Namensregeln, die Insight UI in Python, Templates und Assets einheitlich halten. Bitte halte dich beim Erweitern von Komponenten oder Demos an diese Richtlinien.

## Python-Module & Funktionen
- Module und Packages verwenden `snake_case` (`insight_ui/templatetags/insight_tags.py`).
- Öffentliche Funktionen und Variablen ebenfalls `snake_case`, Klassen in `PascalCase`.
- Template-Tags sollten sprechende Namen tragen: `navbar`, `infinite_scroll`, `toggle_view`.
- Tests liegen in Dateien `test_*.py` innerhalb der App (`insight_ui/tests/test_template_tags.py`).

## Templates
- Komponenten-Templates liegen unter `templates/insight_ui/components/` und verwenden `snake_case`, z. B. `image_carousel.html` oder `navbar.html`.
- Varianten werden in Unterordnern abgelegt: `components/cards/card.html`, `components/carousels/image_carousel.html`.
- Jedes Komponenten-Template erwartet ein Kontext-Dictionary, dessen Name der Komponente entspricht (`carousel_items`, `sidebar_data`).

## Statische Assets
- CSS/JS-Dateien verwenden `kebab-case`: `static/insight_ui/js/sidebar.js`, `static/insight_ui/css/tailwind.css`.
- Bilder und SVGs folgen ebenfalls `kebab-case` (`static/insight_ui/svg/logo.svg`).
- Komponenten-spezifische Assets sollten dem Template-Namensraum folgen (`static/insight_ui/js/carousel/...`).

## Demo-Daten & Kontext-Helfer
- Demo-Kontext-Funktionen liegen in `insight_ui/demo_context.py` und erhalten das Präfix `get_…_context` (z. B. `get_image_carousel_context`).
- Hilfsfunktionen zur Datenaufbereitung stehen in `insight_ui/demo_utils.py`.

## Übersetzungen & Texte
- Benutzerrelevante Texte werden in Python mit `gettext` (`_()`) oder in Templates mit `{% trans %}` gekapselt.
- Explizite Schlüssel verwenden den Punktstil: `_("insight_ui.components.carousel.caption")`.

## Zusammenfassung der Präfixe
- `get_…_context` – Demo-Kontext-Helfer.
- `*_detailpage.html` – Dokumentations-Vorlagen für MkDocs.
- `test_*.py` – Komponententests.
- `*_storybook` / `storybook_view` – URL- und Kontextparameter für Dokumentationsansichten.

Die Einhaltung dieser Konventionen sorgt dafür, dass Beiträge leichter geprüft und gewartet werden können.
