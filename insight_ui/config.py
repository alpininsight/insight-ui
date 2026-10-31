# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Insight UI configuration utilities."""

from collections.abc import Mapping
from typing import Any, cast

from django.conf import settings

from insight_ui.configs.utils import BrandMarkConfig, LogoConfig

CONFIG_DEFAULTS: dict[str, Any] = {
    "webmanifest": "insight_ui/favicon/site.webmanifest",
    "favicon_svg": "insight_ui/favicon/favicon.svg",
    "favicon": "insight_ui/favicon/favicon.ico",
    "apple_touch_icon": "insight_ui/favicon/apple-touch-icon.png",
    "safari_mask_icon": "insight_ui/svg/insight-ui-logo.svg",  # Used by Safari pinned tab
    "safari_mask_icon_color": "#5bbad5",
    "msapplication_TileColor": "#da532c",  # Sets the background color for a live tile (MS Edge only)
    "theme_color": "#ffffff",  # For the search bar on mobile devices
    "meta": {"seo": {"description": "My indispensable app", "keywords": "Django, Insight UI", "author": "It's me"}},
    "stylesheet": "insight_ui/css/tailwind.css",  # Static path of your own Tailwind build, if you compile one
    "theme_stylesheet": "",  # Static path of a stylesheet that overrides theme tokens in @layer theme (no build needed)
    "navbar_fixed": False,  # Should the navigation stick at the top of the window (has impact on the sidebars as well)
    "content_max_width": "",  # CSS width of the content box, e.g. "64rem"; empty keeps the default of 80rem
    "align_navbar_footer_to_content": False,  # True puts navbar and footer content into the content box
    "load_prism": False,  # Turn to 'True' to use syntax highlighting
    "load_leaflet": False,  # Turn to 'True' to use geo-maps
    "load_echarts": False,  # Turn to 'True' to use Chart-Components
    "JS_DEBUG": False,  # Turn to 'True' to enable build in browser console logging
    "register_url": "",  # URL or URL name for registration page (empty = no register button)
    "tooltip_show_delay": 400,  # Milliseconds before a tooltip appears on hover; keyboard focus shows it at once
    "brand": {
        "home_url": "/",
        "mark": BrandMarkConfig(
            primary_text="Django",
            secondary_text="Insight UI",
            logo=LogoConfig(
                url="insight_ui/svg/insight-ui-logo.svg",
                url_dark="insight_ui/svg/insight-ui-logo.svg",
                alt="Insight UI Logo",
                height="2rem",
            ),
        ),
        "footer_text": "A modern, accessible, and responsive UI library for Django projects.",
    },
    # HTMX and its WebSocket extension, loaded by insight_ui/base.html. Point these at
    # self-hosted copies (and update or clear the SRI hashes) for offline or strict-CSP
    # hosts; an empty src omits the script tag, e.g. when the host loads HTMX itself.
    "htmx": {
        "src": "https://cdn.jsdelivr.net/npm/htmx.org@2.0.8/dist/htmx.min.js",
        "integrity": "sha384-/TgkGk7p307TH7EXJDuUlgG3Ce1UVolAOFopFekQkkXihi5u/6OCvVKyz1W+idaz",
        "ws_src": "https://cdn.jsdelivr.net/npm/htmx-ext-ws@2.0.4",
        "ws_integrity": "sha384-1RwI/nvUSrMRuNj7hX1+27J8XDdCoSLf0EjEyF69nacuWyiJYoQ/j39RT1mSnd2G",
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
