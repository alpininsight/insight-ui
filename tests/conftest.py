import os

import django
import pytest
from _pytest.config import Config
from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


def pytest_configure(config: Config) -> None:
    """Configure Django settings for pytest."""
    if not settings.configured:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
        django.setup()

    # Override staticfiles storage for tests to avoid manifest requirement
    # Tests don't run collectstatic, so we use the simple storage backend
    settings.STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"


@pytest.fixture(scope="session")
def live_server_class() -> type[StaticLiveServerTestCase]:
    """Use Django's StaticLiveServerTestCase for serving static files."""
    return StaticLiveServerTestCase


@pytest.fixture
def live_server_url(live_server) -> None:  # noqa: ANN001
    """Fixture für Live-Server-URL."""
    return live_server.url
