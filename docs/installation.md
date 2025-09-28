# Installation (Version 0.1.0)

Folge diesen Schritten, um Insight UI in ein bestehendes Django-Projekt einzubinden.

## Paket installieren

```bash
uv add insight-ui

# oder die Git-Quelle verwenden
uv add "git+https://github.com/alpininsight/insight-ui@main"
```

Falls lokale Änderungen nicht erkannt werden:

```bash
uv pip install --force-reinstall "git+https://github.com/alpininsight/insight-ui@main"
```

## Django-Konfiguration

1. App aktivieren:
   ```python
   INSTALLED_APPS = [
       # ...
       "insight_ui",
       # ...
   ]
   ```
2. Einstellungen ergänzen (siehe `INSIGHT_UI`-Beispiel in der Übersicht).
3. Staticfiles sammeln (`python manage.py collectstatic`) oder Tailwind-Workflow einrichten.

Weiterführende Hinweise findest du im [Schnellstart](quickstart.md) sowie im [Customizing-Guide](guides/customization.md).
