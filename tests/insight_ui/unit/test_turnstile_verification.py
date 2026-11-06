# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Fail-closed Siteverify tests without an external network call."""

import json
from io import BytesIO
from unittest.mock import patch
from urllib.error import URLError
from urllib.parse import parse_qs

import pytest
from django.http import HttpRequest
from django.test import RequestFactory
from insight_ui.turnstile import TURNSTILE_RESPONSE_FIELD, verify_turnstile

TEST_VALUE = "example-secret"
EXPECTED_TIMEOUT = 5.0


@pytest.fixture
def post_request() -> HttpRequest:
    """Create a request with exactly one response token."""
    return RequestFactory().post("/contact/", {TURNSTILE_RESPONSE_FIELD: "example-token"})


def test_valid_token_requires_matching_hostname_and_action(post_request: HttpRequest) -> None:
    """A successful vendor response is accepted only for the intended form and host."""
    payload = {"success": True, "hostname": "example.com", "action": "contact"}
    with patch("insight_ui.turnstile.urlopen", return_value=BytesIO(json.dumps(payload).encode())) as urlopen:
        result = verify_turnstile(
            post_request, secret_key=TEST_VALUE, expected_hostname="example.com", expected_action="contact"
        )

    assert result.success
    sent_request = urlopen.call_args.args[0]
    assert sent_request.full_url == "https://challenges.cloudflare.com/turnstile/v0/siteverify"
    assert parse_qs(sent_request.data.decode()) == {"secret": [TEST_VALUE], "response": ["example-token"]}
    assert urlopen.call_args.kwargs["timeout"] == EXPECTED_TIMEOUT


@pytest.mark.parametrize(
    ("payload", "reason"),
    [
        ({"success": False, "error-codes": ["timeout-or-duplicate"]}, "timeout-or-duplicate"),
        ({"success": True, "hostname": "other.example", "action": "contact"}, "hostname-mismatch"),
        ({"success": True, "hostname": "example.com", "action": "signup"}, "action-mismatch"),
        ({"success": True}, "hostname-mismatch"),
    ],
)
def test_rejects_failed_or_mismatched_siteverify_responses(
    post_request: HttpRequest, payload: dict, reason: str
) -> None:
    """A valid-looking token from another host or action cannot authorize work."""
    with patch("insight_ui.turnstile.urlopen", return_value=BytesIO(json.dumps(payload).encode())):
        result = verify_turnstile(
            post_request, secret_key=TEST_VALUE, expected_hostname="example.com", expected_action="contact"
        )

    assert not result.success
    assert reason in result.error_codes


@pytest.mark.parametrize("tokens", [[], ["one", "two"], [""], ["x" * 2049]])
def test_rejects_missing_duplicate_or_oversized_tokens_without_network(tokens: list[str]) -> None:
    """Reject duplicate form values rather than silently selecting one."""
    request = RequestFactory().post("/contact/", {TURNSTILE_RESPONSE_FIELD: tokens})
    with patch("insight_ui.turnstile.urlopen") as urlopen:
        result = verify_turnstile(request, secret_key=TEST_VALUE, expected_hostname="example.com")

    assert not result.success
    urlopen.assert_not_called()


@pytest.mark.parametrize("response", [b"not-json", b"[]", b"x" * 16_385])
def test_malformed_or_oversized_siteverify_response_fails_closed(post_request: HttpRequest, response: bytes) -> None:
    """No malformed upstream response may be interpreted as success."""
    with patch("insight_ui.turnstile.urlopen", return_value=BytesIO(response)):
        result = verify_turnstile(post_request, secret_key=TEST_VALUE, expected_hostname="example.com")

    assert not result.success


def test_network_error_fails_closed(post_request: HttpRequest) -> None:
    """A vendor outage does not permit unverified form submissions."""
    with patch("insight_ui.turnstile.urlopen", side_effect=URLError("unavailable")):
        result = verify_turnstile(post_request, secret_key=TEST_VALUE, expected_hostname="example.com")

    assert result.success is False
    assert result.error_codes == ("verification-unavailable",)


@pytest.mark.parametrize("configuration", [{"secret_key": ""}, {"expected_hostname": ""}, {"timeout": 0}])
def test_server_misconfiguration_is_not_silently_accepted(post_request: HttpRequest, configuration: dict) -> None:
    """Missing server-only settings must be fixed by the host application."""
    kwargs = {"secret_key": TEST_VALUE, "expected_hostname": "example.com"} | configuration

    with pytest.raises(ValueError, match="requires"):
        verify_turnstile(post_request, **kwargs)
