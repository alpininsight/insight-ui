"""Django settings."""

import os
from pathlib import Path

from decouple import config

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY", default="django-insecure-test-key-not-for-production")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=False, cast=bool)
IS_PROD = config("IS_PROD", default=False, cast=bool)

if DEBUG:
    print("Running in DEBUG mode!")

ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=lambda v: [s.strip() for s in v.split(",")], default="*")

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "insight_ui",
    "core",
]

# Additional apps which are only for development
if not IS_PROD:
    INSTALLED_APPS += ["rosetta", "django_tailwind_cli"]

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

ROOT_URLCONF = "core.urls"

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
                "core.context_processor.project_context",
            ]
        },
    }
]

WSGI_APPLICATION = "core.wsgi.application"
ASGI_APPLICATION = "core.asgi.application"

# Database
DATA_DIR = Path(config("DATA_DIR", default=str(BASE_DIR / "data")))
DATA_DIR.mkdir(parents=True, exist_ok=True)

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": DATA_DIR / "db.sqlite3"}}

# Internationalization
LANGUAGE_CODE = "de-de"
TIME_ZONE = "Europe/Berlin"
USE_I18N = True
USE_TZ = True

LANGUAGES = [("de", "Deutsch"), ("en", "English")]

LOCALE_PATHS = [os.path.join(BASE_DIR, "insight_ui", "locale")]

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATIC_ROOT = Path(config("STATIC_ROOT", default=str(BASE_DIR / "staticfiles")))
STATIC_ROOT.mkdir(parents=True, exist_ok=True)
STATICFILES_DIRS = [BASE_DIR / "insight_ui/static/insight_ui/"]

# Tailwind source file
TAILWIND_CLI_SRC_CSS = os.path.join(BASE_DIR, "insight_ui/utils/input.css")

# WhiteNoise configuration
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Login/Logout paths
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"
LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL_FAILURE = "/login/failure"

# Env-Variables
PROJECT_NAME = config("PROJECT_NAME", default="Insight UI")
PROJECT_DESCRIPTION = config("PROJECT_DESCRIPTION", default="Our base template to build Web UI's for our applications.")
PROJECT_AUTHOR = config("PROJECT_AUTHOR", default="Alpin Insight AI")
VERSION = "0.0.0"

# Insight UI configuration
INSIGHT_UI = {
    "favicon": "insight_ui/favicon/favicon.ico",
    "favicon_32": "insight_ui/favicon/favicon-32x32.png",
    "favicon_16": "insight_ui/favicon/favicon-16x16.png",
    "apple_touch_icon": "insight_ui/favicon/apple-touch-icon.png",
    "safari_mask_icon": "insight_ui/svg/logo.svg",  # Used by Safari pinned tab
    "msapplication_TileColor": "#da532c",  # Sets the background color for a live tile (MS Edge only)
    "theme_color": "#ffffff",  # For the search bar on mobile devices
    "stylesheet": "insight_ui/css/tailwind.css",  # Only change in case of using alternative stylesheet (currently not supported)  # noqa: E501
    "navbar_fixed": True,  # Should the navigation stick at the top of the window (has impact on the sidebars as well)
    "meta": {"seo": {"description": "My indispensable app", "keywords": "Django, Insight UI", "author": "It's me"}},
    "load_prism": True,  # Turn to 'True' to use syntax highlighting
    "load_leaflet": True,  # Turn to 'True' to use geo-maps
    "load_echarts": True,  # Turn to 'True' to use Chart-Components
    "JS_DEBUG": True,  # Turn to 'True' to enable build in browser console logging
}
