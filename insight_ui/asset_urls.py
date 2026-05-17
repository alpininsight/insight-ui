from collections.abc import Mapping
from typing import Any

from django.conf import settings
from django.templatetags.static import static

MINIFIABLE_EXTENSIONS = (".css", ".js")


def to_minified_asset_path(asset_path: str) -> str:
    """Return the generated minified asset path for CSS and JavaScript files."""
    for extension in MINIFIABLE_EXTENSIONS:
        min_extension = f".min{extension}"
        if asset_path.endswith(min_extension):
            return asset_path
        if asset_path.endswith(extension):
            return f"{asset_path.removesuffix(extension)}{min_extension}"

    return asset_path


def _normalise_cdn_version(version: str) -> str:
    if version == "latest" or version.startswith("v"):
        return version
    return f"v{version}"


def _cdn_relative_path(asset_path: str) -> str:
    return asset_path.removeprefix("insight_ui/").lstrip("/")


def _asset_config() -> Mapping[str, Any]:
    insight_config = getattr(settings, "INSIGHT_UI", {})
    if not isinstance(insight_config, Mapping):
        return {}

    asset_config = insight_config.get("assets", {})
    if not isinstance(asset_config, Mapping):
        return {}

    return asset_config


def insight_asset_url(asset_path: str, *, minified: bool | None = None) -> str:
    """Resolve an Insight UI-owned CSS/JS asset to local staticfiles or CDN."""
    asset_config = _asset_config()
    use_cdn = bool(asset_config.get("cdn_enabled", False))
    use_minified = bool(asset_config.get("use_minified", use_cdn))
    if minified is not None:
        use_minified = minified

    resolved_path = to_minified_asset_path(asset_path) if use_minified else asset_path
    if not use_cdn:
        return static(resolved_path)

    base_url = str(asset_config.get("cdn_base_url", "https://cdn.alpininsight.ai")).rstrip("/")
    prefix = str(asset_config.get("cdn_prefix", "insight-ui")).strip("/")
    version = _normalise_cdn_version(str(asset_config.get("cdn_version", "latest")).strip() or "latest")
    relative_path = _cdn_relative_path(resolved_path)

    return f"{base_url}/{prefix}/{version}/{relative_path}"
