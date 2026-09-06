# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Build-only Django settings; no documentation project or runtime server."""

from tests.settings import BASE_DIR, INSTALLED_APPS

SECRET_KEY = "static-build-only"  # noqa: S105
INSTALLED_APPS = [*INSTALLED_APPS, "django_tailwind_cli"]
STATICFILES_DIRS = [BASE_DIR / "insight_ui/static/insight_ui"]
TAILWIND_CLI_SRC_CSS = BASE_DIR / "insight_ui/utils/input.css"
TAILWIND_CLI_DIST_CSS = "css/tailwind.css"
