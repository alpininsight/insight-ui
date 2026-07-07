"""Brand default builders for reusable Insight UI contexts."""

from collections.abc import Mapping
from typing import Any, cast

from insight_ui.config import get_config
from insight_ui.configs import BrandLockupConfig, FooterDescriptionConfig, LogoConfig, NavbarBrandConfig


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

    logo_data = dict(cast("Mapping[str, Any]", logo))
    if height is not None:
        logo_data["height"] = height

    return LogoConfig(**logo_data)


def get_brand_lockup_config() -> BrandLockupConfig | None:
    """Build an optional brand lockup from central brand defaults."""
    brand = get_brand_defaults()
    lockup = brand.get("lockup")
    if not lockup:
        return None

    return BrandLockupConfig(**dict(cast("Mapping[str, Any]", lockup)))


def get_navbar_brand_defaults() -> NavbarBrandConfig:
    """Build the default navbar brand from central brand settings."""
    brand = get_brand_defaults()
    return NavbarBrandConfig(
        title=str(brand.get("title", "")),
        request_url=str(brand.get("home_url", "")),
        logo=get_brand_logo_config(),
        gap="0.5rem",
        lockup=get_brand_lockup_config(),
    )


def get_footer_description_defaults(*, logo_height: str = "6rem") -> FooterDescriptionConfig:
    """Build the default footer description from central brand settings."""
    brand = get_brand_defaults()
    return FooterDescriptionConfig(
        title=str(brand.get("title", "")),
        text=str(brand.get("footer_text", "")),
        logo=get_brand_logo_config(height=logo_height),
    )
