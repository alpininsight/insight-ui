"""Tests for component demo static asset availability."""

from django.contrib.staticfiles import finders
from django.core.management import call_command
from django.test import override_settings
from documentation.component_details.demo_context import (
    DEMO_CARD_IMAGE_PATH,
    get_app_card_context,
    get_flip_card_context,
)

MANIFEST_STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}


def test_card_demo_image_asset_exists() -> None:
    """Card demos must only reference bundled static assets."""
    assert finders.find(DEMO_CARD_IMAGE_PATH) is not None


def test_card_demo_contexts_resolve_images_with_manifest_storage(tmp_path) -> None:  # noqa: ANN001
    """Regression test for production WhiteNoise manifest staticfiles storage."""
    with override_settings(STATIC_ROOT=tmp_path, STORAGES=MANIFEST_STORAGES):
        call_command("collectstatic", interactive=False, verbosity=0, clear=True)

        app_card_context = get_app_card_context()["app_card_config"]
        flip_card_context = get_flip_card_context()["flip_card_config"]

    assert app_card_context.image.url.startswith("/static/insight_ui/favicon/")
    assert flip_card_context.image.url.startswith("/static/insight_ui/favicon/")
