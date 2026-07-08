"""Brand default builders for reusable Insight UI contexts."""

from collections.abc import Mapping
from dataclasses import replace
from typing import Any, cast

from insight_ui.config import get_config
from insight_ui.configs import BrandMarkConfig, FooterDescriptionConfig, LogoConfig, NavbarBrandConfig


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
    logo = brand.get("logo")
    if not logo:
        return None

    if height is not None:
        return replace(logo, height=height)

    return logo


def get_brand_mark_config() -> BrandMarkConfig | None:
    """Build an optional brand mark from central brand defaults."""
    brand = get_brand_defaults()
    mark = brand.get("mark")
    if not mark:
        return None

    return mark


def get_navbar_brand_defaults() -> NavbarBrandConfig:
    """Build the default navbar brand from central brand settings."""
    brand = get_brand_defaults()
    return NavbarBrandConfig(
        title=str(brand.get("title", "")),
        request_url=str(brand.get("home_url", "")),
        logo=get_brand_logo_config(),
        gap="0.5rem",
        mark=get_brand_mark_config(),
    )


def get_footer_description_defaults(*, logo_height: str = "6rem") -> FooterDescriptionConfig:
    """Build the default footer description from central brand settings."""
    brand = get_brand_defaults()
    return FooterDescriptionConfig(
        title=str(brand.get("title", "")),
        text=str(brand.get("footer_text", "")),
        logo=get_brand_logo_config(height=logo_height),
    )
