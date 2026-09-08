# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Loopback-only source preview, sharing the package's minimal test host."""

import os
from copy import deepcopy

from tests import settings as package_settings

BASE_DIR = package_settings.BASE_DIR
SECRET_KEY = package_settings.SECRET_KEY
DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
INSTALLED_APPS = [*package_settings.INSTALLED_APPS, "devtools"]
MIDDLEWARE = ["django.middleware.common.CommonMiddleware"]
ROOT_URLCONF = "devtools.urls"
TEMPLATES = deepcopy(package_settings.TEMPLATES)
TEMPLATES[0]["OPTIONS"]["context_processors"] = [
    "django.template.context_processors.request",
    "django.template.context_processors.i18n",
    "tests.context.package_config",
]
DATABASES = deepcopy(package_settings.DATABASES)
LANGUAGE_CODE = package_settings.LANGUAGE_CODE
LANGUAGES = package_settings.LANGUAGES
USE_I18N = package_settings.USE_I18N
USE_TZ = package_settings.USE_TZ
STATIC_URL = "/static/"
STORAGES = deepcopy(package_settings.STORAGES)
DEFAULT_AUTO_FIELD = package_settings.DEFAULT_AUTO_FIELD
INSIGHT_UI = {
    "assets": {"use_minified": False, "cdn_enabled": False},
    "use_tailwind_cli": False,
    "load_prism": False,
    "load_leaflet": False,
    "load_echarts": False,
}
INSIGHT_UI_PREVIEW_COMPONENT = os.environ.get("INSIGHT_UI_PREVIEW_COMPONENT", "")
