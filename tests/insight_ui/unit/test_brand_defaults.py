# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for central Insight UI brand defaults."""

from django.test import override_settings
from insight_ui.brand import get_brand_logo_config, get_footer_description_defaults, get_navbar_brand_defaults
from insight_ui.configs import BrandMarkConfig, LogoConfig


def test_brand_logo_override_uses_configured_height() -> None:
    """Brand logo override should use the configured height."""
    logo = get_brand_logo_config()

    assert logo is not None
    assert logo.url == "insight_ui/svg/insight-ui-logo.svg"
    assert logo.url_dark == "insight_ui/svg/insight-ui-logo.svg"
    assert logo.alt == "Insight UI Logo"
    assert logo.height == "2rem"


@override_settings(
    INSIGHT_UI={
        "brand": {
            "home_url": "/portal/",
            "mark": BrandMarkConfig(
                primary_text="Acme Portal",
                logo=LogoConfig(url="acme.svg", url_dark="acme.svg", alt="Acme Logo"),
            ),
            "footer_text": "Reusable app shell for Acme teams.",
        }
    }
)
def test_navbar_and_footer_defaults_use_central_brand_settings() -> None:
    """Navbar and footer defaults should read the same central brand source."""
    navbar_brand = get_navbar_brand_defaults()
    footer_description = get_footer_description_defaults()

    assert navbar_brand.request_url == "/portal/"
    assert navbar_brand.mark.primary_text == "Acme Portal"
    assert navbar_brand.mark.logo.alt == "Acme Logo"

    assert footer_description.title == "Acme Portal"
    assert footer_description.text == "Reusable app shell for Acme teams."


@override_settings(
    INSIGHT_UI={
        "brand": {
            "mark": BrandMarkConfig(
                "Acme",
                "",
                LogoConfig(url="acme.svg", url_dark="acme.svg", alt="Acme Login Logo", height="3rem"),
            ),
        }
    }
)
def test_brand_logo_supports_context_specific_height() -> None:
    """Hosts can derive a larger logo without mutating shared defaults."""
    logo = get_brand_logo_config(height="8rem")

    assert logo.alt == "Acme Login Logo"
    assert logo.url == "acme.svg"
    assert logo.height == "8rem"
    assert get_brand_logo_config().height == "3rem"


@override_settings(
    INSIGHT_UI={
        "brand": {
            "mark": BrandMarkConfig(
                primary_text="Acme",
                secondary_text="Develop",
                logo=LogoConfig(url="acme.svg", url_dark="acme.svg", alt="Acme Login Logo", height="3rem"),
            )
        }
    }
)
def test_navbar_brand_defaults_can_use_configured_mark() -> None:
    """A configured brand mark should be available to default navbar brand composition."""
    navbar_brand = get_navbar_brand_defaults()

    assert navbar_brand.mark is not None
    assert navbar_brand.mark.primary_text == "Acme"
    assert navbar_brand.mark.secondary_text == "Develop"
    assert navbar_brand.mark.logo.alt == "Acme Login Logo"
