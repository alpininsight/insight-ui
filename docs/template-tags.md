# Template-Tags (Version 0.1.0)

Insight UI stellt zahlreiche Inclusion-Tags bereit, um Komponenten schnell einzubinden. Die wichtigsten findest du in `insight_ui/templatetags/insight_tags.py`.

| Tag | Beschreibung | Template |
| --- | --- | --- |
| `navbar` | Navigationsleiste mit Branding, Links und Nutzermenü | `components/navbar.html` |
| `footer` | Seitenfooter mit Linkspalten | `components/footer.html` |
| `alert` | Hinweisbox mit Typen wie `info`, `success`, `warning`, `error` | `components/alert.html` |
| `infinite_scroll` | Container mit HTMX-Infinite-Scroll-Verhalten | `components/infinite_scroll.html` |
| `sidebar` | Seitliche Navigation mit Kategorien | `components/sidebar.html` |

Weitere Tags findest du direkt im Code. Jeder Tag gibt ein Dictionary zurück, das im jeweiligen Template erwartet wird.

## Eigene Tags erstellen
1. Funktion in `insight_ui/templatetags/insight_tags.py` ergänzen und mit `@register.inclusion_tag` dekorieren.
2. Template unter `templates/insight_ui/components/` anlegen.
3. Optional Demo-Context in `insight_ui/demo_context.py` hinzufügen.

Ausführlichere Beispiele stehen in der Komponenten-Dokumentation.
