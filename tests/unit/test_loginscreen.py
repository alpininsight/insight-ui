import pytest
from django.template.loader import render_to_string
from django.utils.translation import activate
from insight_ui.demo_context import get_footer_context


@pytest.fixture(autouse=True)
def _activate_en() -> None:
    """Activate english translation."""
    activate("en")


def test_base_login_screen() -> None:
    """Check base login screen without logo and alternative login."""
    html = render_to_string("insight_ui/login.html", get_footer_context() | {"app_path": "/login/", "form": {}})

    assert "Login" in html
    assert "/login/" in html
    assert "Or" not in html  # Only appears if alternative login is set


def test_login_screen_with_logo() -> None:
    """Check login screen has a logo with a specific height."""
    html = render_to_string(
        "insight_ui/login.html",
        get_footer_context()
        | {"logo": {"url": "images/logo.png", "alt": "Test Logo", "height": "6rem"}, "app_path": "/login/", "form": {}},
    )

    assert "<img" in html
    assert 'src="/static/images/logo.png"' in html
    assert 'alt="Test Logo"' in html
    assert 'style="height: 6rem"' in html


def test_login_screen_logo_uses_default_height() -> None:
    """Check login screen has a logo with the default height."""
    html = render_to_string(
        "insight_ui/login.html",
        get_footer_context()
        | {"logo": {"url": "images/logo.png", "alt": "My Logo"}, "form": {}, "app_path": "/login/"},
    )

    assert 'style="height: 12rem"' in html


@pytest.mark.django_db
def test_login_screen_alt_login_section_is_rendered() -> None:
    """Check that there is an alternative login section."""
    alt_login = {"url": "/auth/google/", "title": "Login with Google"}
    html = render_to_string(
        "insight_ui/login.html", get_footer_context() | {"alt_login": alt_login, "form": {}, "app_path": "/login/"}
    )

    assert "Or" in html
    assert "Login with Google" in html
    assert 'href="/auth/google/"' in html
