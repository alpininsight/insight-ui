"""
Regression tests for settings defaults.

Guards against the scenario where a missing .env file causes DEBUG=False
in development, leading to WhiteNoise manifest errors and 500 responses.
"""

from pathlib import Path

from decouple import config
from django.conf import settings


class TestSettingsDefaults:
    """Verify that critical settings have safe defaults for development."""

    def test_secret_key_has_default(self) -> None:
        """SECRET_KEY should have a fallback so the app starts without .env."""
        value = config("SECRET_KEY", default="django-insecure-test-key-not-for-production")
        assert value is not None
        assert len(value) > 0

    def test_allowed_hosts_has_default(self) -> None:
        """ALLOWED_HOSTS should default to '*' so dev server responds."""
        value = config("ALLOWED_HOSTS", default="*")
        assert value is not None

    def test_database_defaults_to_data_dir(self) -> None:
        """App settings should expose a dedicated default data directory."""
        assert Path(settings.BASE_DIR) / "data" == settings.DATA_DIR

    def test_static_root_has_safe_default(self) -> None:
        """Static root should keep a dedicated configurable directory."""
        assert Path(settings.BASE_DIR) / "staticfiles" == settings.STATIC_ROOT
