# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Server-side verification for the optional Turnstile form component."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import TYPE_CHECKING
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

if TYPE_CHECKING:
    from django.http import HttpRequest

TURNSTILE_RESPONSE_FIELD = "cf-turnstile-response"
_SITEVERIFY_URL = "https://challenges.cloudflare.com/turnstile/v0/siteverify"
_MAX_RESPONSE_BYTES = 16_384
_MAX_TOKEN_LENGTH = 2048


@dataclass(frozen=True)
class TurnstileResult:
    """Verification outcome without the token or secret key."""

    success: bool
    error_codes: tuple[str, ...] = ()


def verify_turnstile(
    request: HttpRequest,
    *,
    secret_key: str,
    expected_hostname: str,
    expected_action: str | None = None,
    timeout: float = 5.0,
) -> TurnstileResult:
    """Verify one POST token with Cloudflare before processing a form.

    The host owns its secret key, rate limits, and response to a failed check.
    Network and malformed-response errors fail closed. Tokens are never cached:
    Turnstile tokens expire and may be verified only once.

    Args:
        request: Django POST request containing the Turnstile response field.
        secret_key: Server-only Turnstile secret key.
        expected_hostname: Browser hostname registered for the widget, without a port.
        expected_action: Optional action set in TurnstileConfig.
        timeout: Maximum seconds to wait for Siteverify.

    Returns:
        Verification result; success is true only for a valid, matching token.

    Raises:
        ValueError: If the server configuration is incomplete or timeout is invalid.

    """
    if not secret_key or not expected_hostname or timeout <= 0:
        raise ValueError("Turnstile verification requires a secret key, hostname, and positive timeout.")  # noqa: TRY003

    tokens = request.POST.getlist(TURNSTILE_RESPONSE_FIELD) if request.method == "POST" else []
    if len(tokens) != 1 or not tokens[0] or len(tokens[0]) > _MAX_TOKEN_LENGTH:
        return TurnstileResult(False, ("invalid-token",))

    body = urlencode({"secret": secret_key, "response": tokens[0]}).encode("ascii")
    siteverify_request = Request(
        _SITEVERIFY_URL,
        data=body,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    try:
        with urlopen(siteverify_request, timeout=timeout) as response:  # noqa: S310
            raw = response.read(_MAX_RESPONSE_BYTES + 1)
        if len(raw) > _MAX_RESPONSE_BYTES:
            return TurnstileResult(False, ("invalid-response",))
        payload = json.loads(raw)
    except (URLError, TimeoutError, ValueError, UnicodeError, OSError):
        return TurnstileResult(False, ("verification-unavailable",))

    if not isinstance(payload, dict) or payload.get("success") is not True:
        codes = payload.get("error-codes", []) if isinstance(payload, dict) else []
        if not isinstance(codes, list) or not all(isinstance(code, str) for code in codes):
            codes = []
        return TurnstileResult(False, tuple(codes) or ("invalid-response",))
    mismatch = None
    if payload.get("hostname") != expected_hostname:
        mismatch = "hostname-mismatch"
    elif expected_action is not None and payload.get("action") != expected_action:
        mismatch = "action-mismatch"
    if mismatch:
        return TurnstileResult(False, (mismatch,))
    return TurnstileResult(True)
