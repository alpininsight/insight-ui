# Installation (Version 0.1.0)

Follow these steps to add Insight UI to your Django project.

## Install the Package

```bash
uv add insight-ui

# or install straight from Git
uv add "git+https://github.com/alpininsight/insight-ui@main"
```

Need a refresh after local edits?

```bash
uv pip install --force-reinstall "git+https://github.com/alpininsight/insight-ui@main"
```

## Configure Django

1. Enable the app in `INSTALLED_APPS`:
   ```python
   INSTALLED_APPS = [
       # ...
       "insight_ui",
       # ...
   ]
   ```
2. Add an `INSIGHT_UI` block in `settings.py` (see the configuration section on the overview page).
3. Collect static files (`python manage.py collectstatic`) or set up the Tailwind workflow.

Continue with the [Quickstart](quickstart.md) and the [Customization guide](guides/customization.md) for more details.
