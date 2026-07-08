"""Insight UI configuration utilities."""

from collections.abc import Mapping
from typing import Any, cast

from django.conf import settings

from insight_ui.configs.utils import LogoConfig

CONFIG_DEFAULTS: dict[str, Any] = {
    "favicon": "insight_ui/favicon/favicon.ico",
    "favicon_32": "insight_ui/favicon/favicon-32x32.png",
    "favicon_16": "insight_ui/favicon/favicon-16x16.png",
    "apple_touch_icon": "insight_ui/favicon/apple-touch-icon.png",
    "safari_mask_icon": "insight_ui/svg/logo.svg",  # Used by Safari pinned tab
    "msapplication_TileColor": "#da532c",  # Sets the background color for a live tile (MS Edge only)
    "theme_color": "#ffffff",  # For the search bar on mobile devices
    "meta": {"seo": {"description": "My indispensable app", "keywords": "Django, Insight UI", "author": "It's me"}},
    "stylesheet": "insight_ui/css/tailwind.css",  # Only change in case of using alternative stylesheet name
    "navbar_fixed": True,  # Should the navigation stick at the top of the window (has impact on the sidebars as well)
    "load_prism": False,  # Turn to 'True' to use syntax highlighting
    "load_leaflet": False,  # Turn to 'True' to use geo-maps
    "load_echarts": False,  # Turn to 'True' to use Chart-Components
    "JS_DEBUG": False,  # Turn to 'True' to enable build in browser console logging
    "use_tailwind_cli": False,  # Turn to 'True' to enable the tailwind cli, if you want to modify the styles
    "brand": {
        "title": "Insight UI",
        "home_url": "/",
        "logo": LogoConfig(
            "insight_ui/svg/ai-logo.svg", "insight_ui/svg/ai-logo.svg", "Insight UI Logo", height="2rem"
        ),
        "lockup": None,
        "footer_text": "A modern, accessible, and responsive UI library for Django projects.",
    },
    "assets": {
        "use_minified": False,
        "cdn_enabled": False,
        "cdn_base_url": "https://cdn.alpininsight.ai",
        "cdn_prefix": "insight-ui",
        "cdn_version": "latest",
    },
}


def _merge_config(defaults: Mapping[str, Any], user_config: Mapping[str, Any]) -> dict[str, Any]:
    """Deep-merge user configuration into default configuration.

    Nested mappings are merged recursively; scalar values are overwritten.

    Args:
        defaults: The default configuration mapping.
        user_config: User-provided configuration to merge in.

    Returns:
        A new dictionary with user values merged into defaults.

    """
    merged = dict(defaults)
    for key, value in user_config.items():
        if isinstance(merged.get(key), Mapping) and isinstance(value, Mapping):
            merged[key] = _merge_config(cast("Mapping[str, Any]", merged[key]), value)
        else:
            merged[key] = value
    return merged


def get_config(attribute_name: str = "") -> object:
    """Retrieve Insight UI configuration from Django settings.

    Merges user-defined settings from ``settings.INSIGHT_UI`` with
    the library defaults in ``CONFIG_DEFAULTS``.

    Args:
        attribute_name: Optional key to retrieve a specific configuration
            value. If empty, returns the entire configuration dictionary.

    Returns:
        The value for the requested attribute, or a dictionary containing
        the full merged configuration under the key ``INSIGHT_UI``.

    """
    user_config = cast("Mapping[str, Any]", getattr(settings, "INSIGHT_UI", {}))
    resolved_config = _merge_config(CONFIG_DEFAULTS, user_config)

    if attribute_name != "":
        return resolved_config[attribute_name]

    return {"INSIGHT_UI": resolved_config}
