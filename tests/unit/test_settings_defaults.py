"""
Regression tests for settings defaults.

Guards against the scenario where a missing .env file causes DEBUG=False
in development, leading to WhiteNoise manifest errors and 500 responses.
"""

from pathlib import Path

import pytest
from core.settings import get_secret_key
from decouple import UndefinedValueError, config
from django.conf import settings


class TestSettingsDefaults:
    """Verify that critical settings have safe defaults for development."""

    def test_secret_key_has_default(self) -> None:
        """SECRET_KEY should have a fallback so the app starts without .env."""
        value = config("SECRET_KEY", default="django-insecure-test-key-not-for-production")
        assert value is not None
        assert len(value) > 0

    def test_secret_key_requires_explicit_value_in_prod(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Production config should fail fast if SECRET_KEY is missing."""
        monkeypatch.delenv("SECRET_KEY", raising=False)

        with pytest.raises(UndefinedValueError):
            get_secret_key(is_prod=True)

    def test_secret_key_keeps_dev_fallback_outside_prod(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Development config may still use the standard local fallback."""
        monkeypatch.delenv("SECRET_KEY", raising=False)

        assert get_secret_key(is_prod=False) == "django-insecure-test-key-not-for-production"

    def test_allowed_hosts_has_default(self) -> None:
        """ALLOWED_HOSTS should default to '*' so dev server responds."""
        value = config("ALLOWED_HOSTS", default="*")
        assert value is not None

    def test_use_x_forwarded_host_defaults_to_off(self) -> None:
        """Forwarded host trust should only be enabled explicitly."""
        value = config("USE_X_FORWARDED_HOST", default=False, cast=bool)
        assert value is False

    def test_database_defaults_to_data_dir(self) -> None:
        """App settings should expose a dedicated default data directory."""
        assert Path(settings.BASE_DIR) / "data" == settings.DATA_DIR

    def test_static_root_has_safe_default(self) -> None:
        """Static root should keep a dedicated configurable directory."""
        assert Path(settings.BASE_DIR) / "staticfiles" == settings.STATIC_ROOT
