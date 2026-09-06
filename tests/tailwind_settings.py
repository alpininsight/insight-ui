"""Build-only Django settings; no documentation project or runtime server."""

from tests.settings import BASE_DIR, INSTALLED_APPS

SECRET_KEY = "static-build-only"  # noqa: S105
INSTALLED_APPS = [*INSTALLED_APPS, "django_tailwind_cli"]
STATICFILES_DIRS = [BASE_DIR / "insight_ui/static/insight_ui"]
TAILWIND_CLI_SRC_CSS = BASE_DIR / "insight_ui/utils/input.css"
TAILWIND_CLI_DIST_CSS = "css/tailwind.css"
