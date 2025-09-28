# Quickstart (Version 0.1.0)

Spin up Insight UI in just a few steps.

## 1. Prepare the Project
```bash
uv sync --all-groups
uv run python manage.py migrate
uv run python manage.py runserver
```

## 2. Load Template Tags
```django
{% load insight_tags %}
```

## 3. Drop Components into Your Templates
```django
{% navbar brand=nav_brand links=nav_links show_searchbar=True %}
{% alert message="Welcome" type="success" %}
```

## 4. Choose Your Tailwind Workflow
- **Use the prebuilt CSS**: `python manage.py collectstatic`
- **Extend the design**:
  ```bash
  uv add django-tailwind-cli
  python manage.py tailwind setup
  python manage.py tailwind runserver
  ```

## 5. Enable the Login Template
```python
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="insight_ui/login.html",
            extra_context=get_nav_and_footer_context(),
        ),
        name="login",
    ),
]
```

Explore the [component catalog](components/index.md) and the [contributor guide](contributing.md) to keep going.
