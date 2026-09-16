# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Django settings for devtools - local development only."""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = True
SECRET_KEY = "django-insecure-test-key-not-for-production"  # noqa: S105  # nosec B105


# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_tailwind_cli",
    "insight_ui",
    "devtools",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "devtools.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.i18n",
                "insight_ui.context_processors.insight_ui_context",
            ]
        },
    }
]

WSGI_APPLICATION = "devtools.wsgi.application"
ASGI_APPLICATION = "devtools.asgi.application"

# Database
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": DATA_DIR / "db.sqlite3"}}

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Europe/Berlin"
USE_I18N = True
USE_TZ = True

LANGUAGES = [("de", "Deutsch"), ("en", "English")]

LOCALE_PATHS = [BASE_DIR / "locale"]

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATIC_ROOT = Path(BASE_DIR / "staticfiles")
STATIC_ROOT.mkdir(parents=True, exist_ok=True)
STATICFILES_DIRS = [BASE_DIR / "insight_ui/static/insight_ui/"]

# Tailwind source file
TAILWIND_CLI_SRC_CSS = BASE_DIR / "insight_ui" / "utils" / "input.css"

# WhiteNoise configuration
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Insight UI configuration (see insight_ui/config.py for available settings)
INSIGHT_UI = {
    "load_prism": True,  # Turn to 'True' to use syntax highlighting
    "load_leaflet": True,  # Turn to 'True' to use geo-maps
    "load_echarts": True,  # Turn to 'True' to use Chart-Components
    "JS_DEBUG": True,  # Turn to 'True' to enable build in browser console logging
    "use_tailwind_cli": True,  # Turn to 'True' to enable the tailwind cli, if you want to modify the styles
}
