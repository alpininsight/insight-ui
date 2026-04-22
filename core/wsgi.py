"""
WSGI config for insight-ui project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from logging_config import setup_structlog

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
setup_structlog()

application = get_wsgi_application()
