"""Tests for central Insight UI brand defaults."""

from django.test import override_settings
from django.utils.translation import override
from documentation.component_details.demo_context import get_login_screen_context
from documentation.context import get_footer_context, get_navbar_context
from insight_ui.brand import get_brand_logo_config, get_navbar_brand_defaults
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
    navbar_config = get_navbar_context()["nav_config"]
    footer_config = get_footer_context()["footer_config"]

    assert navbar_config.brand.request_url == "/portal/"
    assert navbar_config.brand.mark.primary_text == "Acme Portal"
    assert navbar_config.brand.mark.logo.alt == "Acme Logo"

    assert footer_config.description.title == "Acme Portal"
    assert footer_config.description.text == "Reusable app shell for Acme teams."


@override_settings(
    INSIGHT_UI={
        "brand": {
            "mark": BrandMarkConfig(
                primary_text="Acme",
                secondary_text="",
                logo=LogoConfig(url="acme.svg", url_dark="acme.svg", alt="Acme Login Logo", height="3rem"),
            ),
        }
    }
)
def test_login_context_uses_brand_logo_with_login_specific_height() -> None:
    """The login screen should share the brand logo while keeping its larger layout height."""
    login_context = get_login_screen_context()

    assert login_context["login_config"].logo.alt == "Acme Login Logo"
    assert login_context["login_config"].logo.url == "acme.svg"
    assert login_context["login_config"].logo.height == "8rem"


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


def test_documentation_navbar_uses_the_localized_search_index() -> None:
    """The documentation navbar must not fall back to Insight UI package static files."""
    with override("de"):
        navbar_config = get_navbar_context()["nav_config"]

    assert navbar_config.search_bar.search_index_url == "/static/documentation/data/search-index-de.json"
