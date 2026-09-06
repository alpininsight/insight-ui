# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for login screen component rendering."""

import pytest
from django.template.loader import render_to_string
from django.utils.translation import activate
from insight_ui.config import get_config
from insight_ui.configs import FooterConfig, LoginScreenConfig, LogoConfig


def login_context() -> dict:
    """Build an ordinary host config instead of importing a demo."""
    return get_config() | {
        "login_config": LoginScreenConfig(
            logo=LogoConfig("insight_ui/svg/insight-ui-logo.svg", alt="Insight UI Logo", height="8rem"),
        ),
        "footer_config": FooterConfig(),
    }


@pytest.fixture(autouse=True)
def _activate_en() -> None:
    """Activate english translation."""
    activate("en")


@pytest.fixture
def mock_form() -> dict:
    """Provide a minimal mock form for login template rendering."""
    return {
        "username": type("Field", (), {"id_for_label": "id_username", "html_name": "username", "label": "Username"})(),
        "password": type("Field", (), {"id_for_label": "id_password", "html_name": "password", "label": "Password"})(),
        "non_field_errors": lambda: "",
    }


def test_base_login_screen(mock_form: dict) -> None:
    """Check base login screen without logo and alternative login."""
    context = login_context()
    context["login_config"] = LoginScreenConfig(alt_login_url="", sign_up_url="")
    context["form"] = mock_form
    context["app_path"] = "/login/"

    html = render_to_string("insight_ui/login.html", context)

    assert "Login" in html
    assert "/login/" in html
    assert "Or" not in html  # Only appears if alternative login is set


def test_login_screen_with_logo(mock_form: dict) -> None:
    """Check login screen has a logo with a specific height."""
    context = login_context()
    context["form"] = mock_form
    context["app_path"] = "/login/"

    html = render_to_string("insight_ui/login.html", context)

    assert "<img" in html
    assert 'src="/static/insight_ui/svg/insight-ui-logo.svg"' in html
    assert 'alt="Insight UI Logo"' in html
    assert 'style="height: 8rem"' in html


@pytest.mark.django_db
def test_login_screen_alt_login_section_is_rendered(mock_form: dict) -> None:
    """Check that there is an alternative login section."""
    context = login_context()
    context["login_config"] = LoginScreenConfig(
        alt_login_url="/auth/google/",
        alt_login_title="Login with Google",
    )
    context["form"] = mock_form
    context["app_path"] = "/login/"

    html = render_to_string("insight_ui/login.html", context)

    assert "Or" in html
    assert "Login with Google" in html
    assert 'href="/auth/google/"' in html
