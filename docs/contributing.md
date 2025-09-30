# Leitfaden für Beitragende (Version 0.1.0)

Danke, dass du Insight UI weiterentwickelst. Dieses Dokument fasst zusammen, wie neue Komponenten, Dokumentation und Tests nach unseren Richtlinien erstellt werden.

## Voraussetzungen
- Python 3.12+
- [`uv`](https://github.com/astral-sh/uv) für das Abhängigkeitsmanagement
- Node.js, falls du Tailwind anpassen möchtest

Lokales Setup:

```bash
uv sync --all-groups
uv run python manage.py migrate
uv run python manage.py runserver
```

## Arbeitsablauf
1. Feature-Branch anlegen.
2. Für geänderte Dateien `uv run ruff format` sowie `uv run ruff check --fix` ausführen.
3. Tests mit `uv run --extra test pytest` laufen lassen.
4. Dokumentation und Demos aktualisieren, bevor du einen Pull Request eröffnest.

## Komponenten ergänzen oder erweitern
- Beachte die [Benennungskonventionen](guides/naming_conventions.md) für Templates, Assets und Kontext-Helfer.
- Neue Templates kommen nach `insight_ui/templates/insight_ui/components/…`, der zugehörige Inclusion-Tag nach `insight_ui/templatetags/insight_tags.py`.
- Komponenten-spezifische JS/CSS-Dateien landen unter `insight_ui/static/insight_ui/`.
- Demo-Daten in `insight_ui/demo_context.py` pflegen, damit Showroom und Dokumentation die Komponente anzeigen.

## Dokumentation
- Jede neue Komponente oder größere Änderung benötigt Seiten in `docs/de/components/` und `docs/en/components/`.
- Passe die Beispiel-Templates unter `insight_ui/templates/insight_ui/docs/partial/` an, wenn sich die Ausgabe verändert.
- Halte beide Sprachvarianten im selben Commit aktuell.

## Test-Checkliste
- Template-Tags oder Python-Logik: Tests in `insight_ui/tests/test_template_tags.py` oder eigenem Testmodul ergänzen.
- Frontend-Verhalten: Bei Bedarf Regressionstests (z. B. HTMX-Requests oder Screenshots) hinzufügen.
- Demo-Skripte (`utils/`) sollen über den Projekt-Logger loggen und ohne globale Zustände auskommen.

## Pull-Request-Richtlinien
- Verwende Conventional Commits (`feat:`, `fix:`, `chore:`, `docs:`, …).
- Verweise auf Issues und beschreibe den Nutzer-Impact.
- Füge Testnachweise bei (Konsolen-Output, Screenshots, Preview-Link).
- Review erst anfragen, wenn Linting und Tests grün sind und die Dokumentation aktualisiert wurde.

So bleibt Insight UI nachvollziehbar und lässt sich von allen Teammitgliedern gut warten.
