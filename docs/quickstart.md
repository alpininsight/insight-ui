# Schnellstart (Version 0.1.0)

Starte dein Projekt mit Insight UI in wenigen Schritten.

## 1. Projekt vorbereiten
```bash
uv sync --all-groups
uv run python manage.py migrate
uv run python manage.py runserver
```

## 2. Template-Tags laden
```django
{% load insight_tags %}
```

## 3. Komponenten einbinden
```django
{% navbar brand=nav_brand links=nav_links show_searchbar=True %}
{% alert message="Willkommen" type="success" %}
```

## 4. Tailwind-Workflow wählen
- **Vorkompiliertes CSS**: `python manage.py collectstatic`
- **Eigene Erweiterungen**:
  ```bash
  uv add django-tailwind-cli
  python manage.py tailwind setup
  python manage.py tailwind runserver
  ```

## 5. Login-Template nutzen
```python
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path("login/", auth_views.LoginView.as_view(
        template_name="insight_ui/login.html",
        extra_context=get_nav_and_footer_context(),
    ), name="login"),
]
```

Weitere Details findest du in der [Komponentenübersicht](components/index.md) und im [Leitfaden für Beitragende](contributing.md).
