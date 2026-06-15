from collections.abc import Mapping
from typing import Any, cast

from django.conf import settings

CONFIG_DEFAULTS: dict[str, Any] = {
    "favicon": "insight_ui/favicon/favicon.ico",
    "favicon_32": "insight_ui/favicon/favicon-32x32.png",
    "favicon_16": "insight_ui/favicon/favicon-16x16.png",
    "apple_touch_icon": "insight_ui/favicon/apple-touch-icon.png",
    "safari_mask_icon": "insight_ui/svg/logo.svg",  # Used by Safari pinned tab
    "msapplication_TileColor": "#da532c",  # Sets the background color for a live tile (MS Edge only)
    "theme_color": "#ffffff",  # For the search bar on mobile devices
    "stylesheet": "insight_ui/css/tailwind.css",  # Only change in case of using alternative stylesheet (currently not supported)  # noqa: E501
    "navbar_fixed": True,  # Should the navigation stick at the top of the window (has impact on the sidebars as well)
    "title": "My indispensable app",  # Default title if the {% title %} block is not overridden
    "meta": {"seo": {"description": "My indispensable app", "keywords": "Django, Insight UI", "author": "It's me"}},
    "load_prism": False,  # Turn to 'True' to use syntax highlighting
    "load_leaflet": False,  # Turn to 'True' to use geo-maps
    "load_echarts": False,  # Turn to 'True' to use Chart-Components
    "JS_DEBUG": False,  # Turn to 'True' to enable build in browser console logging
    "use_tailwind_cli": False,  # Turn to 'True' to enable the tailwind cli, if you want to modify the styles
    "design_themes": {
        "enabled": False,
        "default": "default",
        "storage_key": "insight-ui-design-theme",
        "labels": {
            "default": "Original",
            "alpin": "Alpin",
            "foundry": "Foundry",
            "brite": "Brite",
            "bento": "Bento",
            "cerulean": "Cerulean",
            "cosmo": "Cosmo",
            "cyborg": "Cyborg",
            "darkly": "Darkly",
            "drawn": "Drawn",
            "flatly": "Flatly",
            "flat": "Flat",
            "glass": "Glass",
            "journal": "Journal",
            "litera": "Litera",
            "lumen": "Lumen",
            "lux": "Lux",
            "material": "Material",
            "materia": "Materia",
            "minty": "Minty",
            "morph": "Morph",
            "neumorphic": "Neumorphic",
            "pulse": "Pulse",
            "quartz": "Quartz",
            "sandstone": "Sandstone",
            "simplex": "Simplex",
            "sketchy": "Sketchy",
            "skeuomorphic": "Skeuomorphic",
            "slate": "Slate",
            "solar": "Solar",
            "spacelab": "Spacelab",
            "superhero": "Superhero",
            "united": "United",
            "vapor": "Vapor",
            "yeti": "Yeti",
            "zephyr": "Zephyr",
        },
        "stylesheets": {
            "default": "insight_ui/css/themes/default.css",
            "alpin": "insight_ui/css/themes/alpin.css",
            "foundry": "insight_ui/css/themes/foundry.css",
            "brite": "insight_ui/css/themes/brite.css",
            "bento": "insight_ui/css/themes/bento.css",
            "cerulean": "insight_ui/css/themes/cerulean.css",
            "cosmo": "insight_ui/css/themes/cosmo.css",
            "cyborg": "insight_ui/css/themes/cyborg.css",
            "darkly": "insight_ui/css/themes/darkly.css",
            "drawn": "insight_ui/css/themes/drawn.css",
            "flat": "insight_ui/css/themes/flat.css",
            "flatly": "insight_ui/css/themes/flatly.css",
            "glass": "insight_ui/css/themes/glass.css",
            "journal": "insight_ui/css/themes/journal.css",
            "litera": "insight_ui/css/themes/litera.css",
            "lumen": "insight_ui/css/themes/lumen.css",
            "lux": "insight_ui/css/themes/lux.css",
            "material": "insight_ui/css/themes/material.css",
            "materia": "insight_ui/css/themes/materia.css",
            "minty": "insight_ui/css/themes/minty.css",
            "morph": "insight_ui/css/themes/morph.css",
            "neumorphic": "insight_ui/css/themes/neumorphic.css",
            "pulse": "insight_ui/css/themes/pulse.css",
            "quartz": "insight_ui/css/themes/quartz.css",
            "sandstone": "insight_ui/css/themes/sandstone.css",
            "simplex": "insight_ui/css/themes/simplex.css",
            "sketchy": "insight_ui/css/themes/sketchy.css",
            "skeuomorphic": "insight_ui/css/themes/skeuomorphic.css",
            "slate": "insight_ui/css/themes/slate.css",
            "solar": "insight_ui/css/themes/solar.css",
            "spacelab": "insight_ui/css/themes/spacelab.css",
            "superhero": "insight_ui/css/themes/superhero.css",
            "united": "insight_ui/css/themes/united.css",
            "vapor": "insight_ui/css/themes/vapor.css",
            "yeti": "insight_ui/css/themes/yeti.css",
            "zephyr": "insight_ui/css/themes/zephyr.css",
        },
        "display_order": (
            "default",
            "skeuomorphic",
            "flat",
            "material",
            "neumorphic",
            "glass",
            "brite",
            "bento",
            "drawn",
        ),
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
    merged = dict(defaults)
    for key, value in user_config.items():
        default_value = merged.get(key)
        if isinstance(default_value, Mapping) and isinstance(value, Mapping):
            merged[key] = _merge_config(cast(Mapping[str, Any], default_value), value)
        else:
            merged[key] = value
    return merged


def get_config(attribute_name: str = "") -> object:
    """Serve insight-ui configuration."""
    user_config = cast(Mapping[str, Any], getattr(settings, "INSIGHT_UI", {}))
    resolved_config = _merge_config(CONFIG_DEFAULTS, user_config)

    if attribute_name != "":
        return resolved_config[attribute_name]

    return {"INSIGHT_UI": resolved_config}
