from collections.abc import Mapping
from typing import Any, cast

from django.conf import settings

CONFIG_DEFAULTS: dict[str, Any] = {
    "theme": "light",
    "favicon": "insight_ui/favicon/favicon.ico",
    "favicon_32": "insight_ui/favicon/favicon-32x32.png",
    "favicon_16": "insight_ui/favicon/favicon-16x16.png",
    "apple_touch_icon": "insight_ui/favicon/apple-touch-icon.png",
    "safari_mask_icon": "insight_ui/svg/logo.svg",  # Used by Safari pinned tab
    "msapplication_TileColor": "#da532c",  # Sets the background color for a live tile (MS Edge only)
    "theme_color": "#ffffff",
    "stylesheet": "insight_ui/css/tailwind.css",
    "branding": {"name": "Alpin Insight AI", "logo": None},
    "meta": {
        "seo": {
            "description": "An Alpin Insight AI application",
            "keywords": "Django, Alpin Insight, AI, Webapp",
            "author": "Alpin Insight AI Dev-Team",
        }
    },
}


def get_config(settings_name: str | None = None) -> dict[str, Any]:
    """Get insight-ui configuration."""
    config_attribute = settings_name or "INSIGHT_UI"
    user_config = cast(
        Mapping[str, Any],
        getattr(settings, config_attribute, {}),
    )

    return {"INSIGHT_UI": {**CONFIG_DEFAULTS, **dict(user_config)}}
