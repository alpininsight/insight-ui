"""Brand default builders for reusable Insight UI contexts."""

from collections.abc import Mapping
from dataclasses import replace
from typing import Any, cast

from insight_ui.config import get_config
from insight_ui.configs import FooterDescriptionConfig, LogoConfig, NavbarBrandConfig


def get_brand_defaults() -> Mapping[str, Any]:
    """Return the resolved central brand defaults from ``settings.INSIGHT_UI``."""
    return cast("Mapping[str, Any]", get_config("brand"))


def get_brand_logo_config(*, height: str | None = None) -> LogoConfig | None:
    """Build a logo config from central brand defaults.

    Args:
        height: Optional height override for a specific context, e.g. login or footer.

    Returns:
        A ``LogoConfig`` or ``None`` if the brand deliberately disables the logo.

    """
    brand = get_brand_defaults()
    logo = brand.get("mark").logo
    if not logo:
        return None

    if height is not None:
        return replace(logo, height=height)

    return logo


def get_navbar_brand_defaults() -> NavbarBrandConfig:
    """Build the default navbar brand from central brand settings."""
    defaults = get_brand_defaults()
    return NavbarBrandConfig(
        request_url=str(defaults.get("home_url", "")),
        mark=defaults.get("mark"),
    )


def get_footer_description_defaults(*, logo_height: str = "6rem") -> FooterDescriptionConfig:
    """Build the default footer description from central brand settings."""
    brand = get_brand_defaults()
    mark = brand.get("mark")
    title = " ".join(filter(None, [mark.primary_text, mark.secondary_text])) if mark else ""
    return FooterDescriptionConfig(
        title=title,
        text=str(brand.get("footer_text", "")),
        logo=get_brand_logo_config(height=logo_height),
    )
