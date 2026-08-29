"""URL utilities for resolving static asset paths."""

import re
from collections.abc import Mapping
from typing import Any

from django.conf import settings
from django.templatetags.static import static

MINIFIABLE_EXTENSIONS = (".css", ".js")
SEMVER_PATTERN = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")


def to_minified_asset_path(asset_path: str) -> str:
    """Return the generated minified asset path for CSS and JavaScript files.

    Args:
        asset_path: The original asset path.

    Returns:
        The path with '.min' inserted before the extension, or unchanged
        if already minified or not a minifiable extension.

    """
    for extension in MINIFIABLE_EXTENSIONS:
        min_extension = f".min{extension}"
        if asset_path.endswith(min_extension):
            return asset_path
        if asset_path.endswith(extension):
            return f"{asset_path.removesuffix(extension)}{min_extension}"

    return asset_path


def _normalise_cdn_version(version: str) -> str:
    """Normalize a version string for CDN URLs.

    Args:
        version: The version string to normalize.

    Returns:
        The version prefixed with 'v' if it's a bare semver, otherwise unchanged.

    """
    if version == "latest" or version.startswith("v") or not SEMVER_PATTERN.match(version):
        return version
    return f"v{version}"


def _cdn_relative_path(asset_path: str) -> str:
    """Convert an asset path to a CDN-relative path.

    Args:
        asset_path: The full asset path.

    Returns:
        The path without the 'insight_ui/' prefix and leading slashes.

    """
    return asset_path.removeprefix("insight_ui/").lstrip("/")


def _asset_config() -> Mapping[str, Any]:
    """Retrieve the asset configuration from Django settings.

    Returns:
        The 'assets' mapping from INSIGHT_UI settings, or empty dict if not
        configured or invalid.

    """
    insight_config = getattr(settings, "INSIGHT_UI", {})
    if not isinstance(insight_config, Mapping):
        return {}

    asset_config = insight_config.get("assets", {})
    if not isinstance(asset_config, Mapping):
        return {}

    return asset_config


def insight_asset_url(asset_path: str, *, minified: bool | None = None) -> str:
    """Resolve an Insight UI-owned CSS/JS asset to local staticfiles or CDN.

    Args:
        asset_path: The relative path to the asset.
        minified: Whether to use the minified CDN version. Local staticfiles
            always use the readable package asset.

    Returns:
        The full URL to the asset (local static URL or CDN URL).

    """
    asset_config = _asset_config()
    use_cdn = bool(asset_config.get("cdn_enabled", False))
    use_minified = bool(asset_config.get("use_minified", use_cdn))
    if minified is not None:
        use_minified = minified

    # Generated minified files are CDN-only build artifacts. Local staticfiles
    # deliberately keep serving the readable package sources.
    resolved_path = to_minified_asset_path(asset_path) if use_cdn and use_minified else asset_path
    if not use_cdn:
        return static(resolved_path)

    base_url = str(asset_config.get("cdn_base_url", "https://cdn.alpininsight.ai")).rstrip("/")
    prefix = str(asset_config.get("cdn_prefix", "insight-ui")).strip("/")
    version = _normalise_cdn_version(str(asset_config.get("cdn_version", "latest")).strip() or "latest")
    relative_path = _cdn_relative_path(resolved_path)

    return f"{base_url}/{prefix}/{version}/{relative_path}"
