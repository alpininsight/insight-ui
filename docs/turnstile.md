<!--
SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
SPDX-License-Identifier: AGPL-3.0-only
-->

# Optional Turnstile Form Protection

Turnstile is an optional integration for public forms. Rendering its widget
does **not** protect a form on its own: the receiving Django view must verify
the token before any side effect. Private forms and forms that do not need a
challenge remain unchanged.

## Render The Widget

Create a Turnstile widget and keep its secret key outside the template context:

```python
from django.conf import settings
from insight_ui.configs import FormConfig, TurnstileConfig

form_config = FormConfig(
    request_url="/contact/",
    method="post",
    turnstile=TurnstileConfig(
        site_key=settings.TURNSTILE_SITE_KEY,
        action="contact",
    ),
)
```

```django
{% load insight_tags %}
{% form config=form_config %}
```

For a custom `<form method="post">`, place `{% turnstile config=challenge %}`
inside the form. The standard Insight UI JavaScript initializer loads the
Turnstile API from Cloudflare only when a widget is present. Do not mirror or
cache that API script on your own CDN. It also initializes widgets added by
HTMX and refreshes one-use tokens after HTMX submissions. A custom base
template must load the usual Insight UI JavaScript assets.

## Verify Every POST

```python
from django.conf import settings
from django.http import HttpResponseBadRequest
from insight_ui.turnstile import verify_turnstile


def contact(request):
    if request.method != "POST":
        ...  # Render the form.

    result = verify_turnstile(
        request,
        secret_key=settings.TURNSTILE_SECRET_KEY,
        expected_hostname="example.com",
        expected_action="contact",
    )
    if not result.success:
        return HttpResponseBadRequest("Verification failed. Please retry.")

    ...  # Validate the form and perform its side effects only now.
```

`TURNSTILE_SITE_KEY` is public; `TURNSTILE_SECRET_KEY` must stay server-side.
Use the hostname actually serving the browser form, without a port. Siteverify
network errors, missing or duplicate tokens, oversized tokens, and mismatched
hostnames/actions all fail closed. The helper never logs or returns a token or
secret. Configure separate site keys for each environment as needed.

Turnstile is not a replacement for CSRF protection, server-side field
validation, and endpoint rate limits. Apply rate limits before making the
Siteverify network call to bound request costs. For multi-worker deployments,
use a shared rate-limit backend rather than per-process memory.

Cloudflare's [testing keys](https://developers.cloudflare.com/turnstile/troubleshooting/testing/)
allow local and browser tests without a production challenge. If a Content
Security Policy is active, allow `https://challenges.cloudflare.com` in
`script-src` and `frame-src`, as described in Cloudflare's
[CSP guide](https://developers.cloudflare.com/turnstile/reference/content-security-policy/).

[Cloudflare's Siteverify contract](https://developers.cloudflare.com/turnstile/get-started/server-side-validation/)
is the authoritative reference for token expiry, single-use behavior, and
verification responses.
