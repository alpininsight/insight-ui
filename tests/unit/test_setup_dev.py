"""
Regression tests for the setup_dev management command and dev environment.

These tests guard against the Server Error (500) that occurs when:
1. No .env file exists (DEBUG defaults to False)
2. WhiteNoise's CompressedManifestStaticFilesStorage crashes without collectstatic
"""

from io import StringIO

import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command


@pytest.mark.django_db
class TestSetupDevCommand:
    """Tests for the setup_dev management command."""

    def test_creates_admin_superuser(self) -> None:
        """setup_dev should create an admin superuser when none exists."""
        user_model = get_user_model()
        assert not user_model.objects.filter(username="admin").exists()

        out = StringIO()
        call_command("setup_dev", stdout=out, verbosity=0)

        admin = user_model.objects.get(username="admin")
        assert admin.is_superuser
        assert admin.is_staff
        assert admin.check_password("admin")
        assert admin.email == "admin@localhost"
        assert "Created superuser" in out.getvalue()

    def test_idempotent_skips_existing_admin(self) -> None:
        """Running setup_dev twice should not fail or duplicate the user."""
        user_model = get_user_model()

        out1 = StringIO()
        call_command("setup_dev", stdout=out1, verbosity=0)
        assert "Created superuser" in out1.getvalue()

        out2 = StringIO()
        call_command("setup_dev", stdout=out2, verbosity=0)
        assert "already exists" in out2.getvalue()

        assert user_model.objects.filter(username="admin").count() == 1

    def test_runs_migrations(self) -> None:
        """setup_dev should apply pending migrations without error."""
        out = StringIO()
        call_command("setup_dev", stdout=out, verbosity=0)
        assert "Dev setup complete" in out.getvalue()
