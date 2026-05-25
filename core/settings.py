"""Django settings."""

import os
from pathlib import Path
from typing import Any

from decouple import UndefinedValueError, config

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).resolve().parent.parent


def split_csv(value: str) -> list[str]:
    """Split a comma-separated env var into a trimmed list."""
    return [item.strip() for item in value.split(",") if item.strip()]


def normalize_log_level(value: str) -> str:
    """Normalize env-provided log levels for Django's logging config."""
    return value.strip().upper()


def get_secret_key(*, is_prod: bool) -> str:
    """Resolve the Django secret key with a fail-fast production path."""
    if is_prod:
        return config("SECRET_KEY")
    return config("SECRET_KEY", default="django-insecure-test-key-not-for-production")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=False, cast=bool)
IS_PROD = config("IS_PROD", default=False, cast=bool)
USE_TAILWIND_CLI = config("USE_TAILWIND_CLI", default=False, cast=bool)

try:
    SECRET_KEY = get_secret_key(is_prod=IS_PROD)
except UndefinedValueError as exc:
    msg = "SECRET_KEY must be set when IS_PROD=true."
    raise RuntimeError(msg) from exc

SERVICE_NAMESPACE = config("SERVICE_NAMESPACE", default="alpininsight")
SERVICE_NAME = config("SERVICE_NAME", default="insight-ui")
PLATFORM_NAMESPACE = config("PLATFORM_NAMESPACE", default="demo")
DEPLOYMENT_ENVIRONMENT = config("DEPLOYMENT_ENVIRONMENT", default="local")
DEPLOYMENT_LANE = config("DEPLOYMENT_LANE", default="")
DEPLOYMENT_SLOT = config("DEPLOYMENT_SLOT", default="")
PUBLIC_BASE_URL = config("PUBLIC_BASE_URL", default="http://localhost:8000").strip()
ARTIFACT_VERSION = config("ARTIFACT_VERSION", default="0.0.0")
GIT_COMMIT_SHA = config("GIT_COMMIT_SHA", default="unknown")
INSIGHT_UI_USE_MINIFIED_ASSETS = config("INSIGHT_UI_USE_MINIFIED_ASSETS", default=IS_PROD, cast=bool)
INSIGHT_UI_CDN_ENABLED = config("INSIGHT_UI_CDN_ENABLED", default=False, cast=bool)
INSIGHT_UI_CDN_BASE_URL = config("INSIGHT_UI_CDN_BASE_URL", default="https://cdn.alpininsight.ai").strip().rstrip("/")
INSIGHT_UI_CDN_PREFIX = config("INSIGHT_UI_CDN_PREFIX", default="insight-ui").strip().strip("/")
INSIGHT_UI_CDN_VERSION = config("INSIGHT_UI_CDN_VERSION", default="latest").strip()
INSIGHT_UI_JS_DEBUG = config("INSIGHT_UI_JS_DEBUG", default=not IS_PROD, cast=bool)
LOG_LEVEL = config("LOG_LEVEL", default="WARNING", cast=normalize_log_level)
APP_LOG_LEVEL = config("APP_LOG_LEVEL", default="INFO", cast=normalize_log_level)
DJANGO_LOG_LEVEL = config("DJANGO_LOG_LEVEL", default=LOG_LEVEL, cast=normalize_log_level)
SERVER_LOG_LEVEL = config("SERVER_LOG_LEVEL", default=LOG_LEVEL, cast=normalize_log_level)
LOG_FORMAT = config("LOG_FORMAT", default="console")
ACCESS_LOG_ENABLED = config("ACCESS_LOG_ENABLED", default=False, cast=bool)
USE_X_FORWARDED_HOST = config("USE_X_FORWARDED_HOST", default=False, cast=bool)
TRUST_X_FORWARDED_PROTO = config("TRUST_X_FORWARDED_PROTO", default=True, cast=bool)

if DEBUG:
    print("Running in DEBUG mode!")

ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=split_csv, default="*")
CSRF_TRUSTED_ORIGINS = config("CSRF_TRUSTED_ORIGINS", cast=split_csv, default="")

if TRUST_X_FORWARDED_PROTO:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SECURE_SSL_REDIRECT = config("SECURE_SSL_REDIRECT", default=False, cast=bool)
SESSION_COOKIE_SECURE = config("SESSION_COOKIE_SECURE", default=False, cast=bool)
CSRF_COOKIE_SECURE = config("CSRF_COOKIE_SECURE", default=False, cast=bool)
SECURE_HSTS_SECONDS = config("SECURE_HSTS_SECONDS", default=0, cast=int)
SECURE_HSTS_INCLUDE_SUBDOMAINS = config("SECURE_HSTS_INCLUDE_SUBDOMAINS", default=False, cast=bool)
SECURE_HSTS_PRELOAD = config("SECURE_HSTS_PRELOAD", default=False, cast=bool)

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
    INSTALLED_APPS += ["rosetta"]
    if USE_TAILWIND_CLI:
        INSTALLED_APPS += ["django_tailwind_cli"]

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

LOGGING: dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        }
    },
    "root": {
        "handlers": ["console"],
        "level": LOG_LEVEL,
    },
    "loggers": {
        "django": {"handlers": ["console"], "level": DJANGO_LOG_LEVEL, "propagate": False},
        "gunicorn": {"handlers": ["console"], "level": SERVER_LOG_LEVEL, "propagate": False},
        "uvicorn": {"handlers": ["console"], "level": SERVER_LOG_LEVEL, "propagate": False},
        "uvicorn.error": {"handlers": ["console"], "level": SERVER_LOG_LEVEL, "propagate": False},
        "uvicorn.access": {
            "handlers": ["console"],
            "level": "INFO" if ACCESS_LOG_ENABLED else "WARNING",
            "propagate": False,
        },
    },
}

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Login/Logout paths
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"
LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL_FAILURE = "/login/failure"

# Insight UI configuration (see insight_ui/config.py for available settings)
INSIGHT_UI = {
    "load_prism": True,  # Turn to 'True' to use syntax highlighting
    "load_leaflet": True,  # Turn to 'True' to use geo-maps
    "load_echarts": True,  # Turn to 'True' to use Chart-Components
    "JS_DEBUG": INSIGHT_UI_JS_DEBUG,  # Turn to 'True' to enable build in browser console logging
    "use_tailwind_cli": USE_TAILWIND_CLI,  # Turn to 'True' to enable the tailwind cli, if you want to modify the styles
    "design_themes": {
        "enabled": True,
    },
    "assets": {
        "use_minified": INSIGHT_UI_USE_MINIFIED_ASSETS,
        "cdn_enabled": INSIGHT_UI_CDN_ENABLED,
        "cdn_base_url": INSIGHT_UI_CDN_BASE_URL,
        "cdn_prefix": INSIGHT_UI_CDN_PREFIX,
        "cdn_version": INSIGHT_UI_CDN_VERSION,
    },
}
