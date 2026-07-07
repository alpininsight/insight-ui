"""Tests for central Insight UI brand defaults."""

from django.test import override_settings
from insight_ui.brand import get_brand_logo_config, get_navbar_brand_defaults
from insight_ui.component_details.demo_context import get_login_screen_context
from insight_ui.context import get_footer_context, get_navbar_context


@override_settings(INSIGHT_UI={"brand": {"logo": {"height": "3rem"}}})
def test_partial_brand_logo_override_keeps_default_asset_metadata() -> None:
    """Partial nested brand settings should keep the default logo URL and alt text."""
    logo = get_brand_logo_config()

    assert logo is not None
    assert logo.url == "insight_ui/svg/ai-logo.svg"
    assert logo.url_dark == "insight_ui/svg/ai-logo.svg"
    assert logo.alt == "Insight UI Logo"
    assert logo.height == "3rem"


@override_settings(
    INSIGHT_UI={
        "brand": {
            "title": "Acme Portal",
            "home_url": "/portal/",
            "logo": {"alt": "Acme Logo"},
            "footer_text": "Reusable app shell for Acme teams.",
        }
    }
)
def test_navbar_and_footer_defaults_use_central_brand_settings() -> None:
    """Navbar and footer defaults should read the same central brand source."""
    navbar_config = get_navbar_context()["nav_config"]
    footer_config = get_footer_context()["footer_config"]

    assert navbar_config.brand.title == "Acme Portal"
    assert navbar_config.brand.request_url == "/portal/"
    assert navbar_config.brand.logo.alt == "Acme Logo"
    assert navbar_config.brand.logo.height == "2rem"

    assert footer_config.description.title == "Acme Portal"
    assert footer_config.description.text == "Reusable app shell for Acme teams."
    assert footer_config.description.logo.alt == "Acme Logo"
    assert footer_config.description.logo.height == "6rem"


@override_settings(
    INSIGHT_UI={
        "brand": {
            "title": "Acme Portal",
            "logo": {"alt": "Acme Login Logo", "height": "3rem"},
        }
    }
)
def test_login_context_uses_brand_logo_with_login_specific_height() -> None:
    """The login screen should share the brand logo while keeping its larger layout height."""
    login_context = get_login_screen_context()

    assert login_context["logo_config"].alt == "Acme Login Logo"
    assert login_context["logo_config"].url == "insight_ui/svg/ai-logo.svg"
    assert login_context["logo_config"].height == "8rem"


@override_settings(
    INSIGHT_UI={
        "brand": {
            "lockup": {
                "primary_text": "Acme",
                "secondary_text": "Develop",
                "variant": "develop",
            }
        }
    }
)
def test_navbar_brand_defaults_can_use_configured_lockup() -> None:
    """A configured lockup should be available to default navbar brand composition."""
    brand = get_navbar_brand_defaults()

    assert brand.lockup is not None
    assert brand.lockup.primary_text == "Acme"
    assert brand.lockup.secondary_text == "Develop"
    assert brand.lockup.variant == "develop"
