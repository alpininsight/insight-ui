"""Tests for login screen component rendering."""

import pytest
from django.template.loader import render_to_string
from django.utils.translation import activate
from insight_ui.component_details.demo_context import get_footer_context, get_login_screen_context


@pytest.fixture(autouse=True)
def _activate_en() -> None:
    """Activate english translation."""
    activate("en")


def test_base_login_screen() -> None:
    """Check base login screen without logo and alternative login."""
    config = get_login_screen_context()
    config["alt_login"] = None
    html = render_to_string("insight_ui/login.html", config | {"app_path": "/login/", "form": {}})

    assert "Login" in html
    assert "/login/" in html
    assert "Or" not in html  # Only appears if alternative login is set


def test_login_screen_with_logo() -> None:
    """Check login screen has a logo with a specific height."""
    html = render_to_string("insight_ui/login.html", get_login_screen_context())

    assert "<img" in html
    assert 'src="/static/insight_ui/svg/ai-logo.svg"' in html
    assert 'alt="Insight UI Logo"' in html
    assert 'style="height: 8rem"' in html


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
