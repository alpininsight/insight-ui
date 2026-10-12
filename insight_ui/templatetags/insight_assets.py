# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Template tags for Insight UI asset URLs."""

from typing import TYPE_CHECKING, cast

from django import template
from django.utils.html import format_html
from django.utils.safestring import SafeString

from insight_ui.asset_urls import insight_asset_url
from insight_ui.config import get_config

if TYPE_CHECKING:
    from collections.abc import Mapping

register = template.Library()


@register.simple_tag
def insight_asset(asset_path: str) -> str:
    """Resolve an Insight UI asset path to a full URL.

    Returns either a local static file URL or a CDN URL depending on
    the ``assets`` configuration in ``settings.INSIGHT_UI``.

    Args:
        asset_path: Relative path to the asset within the Insight UI
            static directory (e.g., ``css/tailwind.css``).

    Returns:
        The resolved URL for the asset, ready for use in templates.

    """
    return insight_asset_url(asset_path)


def _script_tag(src: object, integrity: object) -> SafeString:
    if not src:
        return SafeString("")
    if integrity:
        return format_html(
            '<script src="{}" integrity="{}" crossorigin="anonymous" referrerpolicy="no-referrer"></script>',
            src,
            integrity,
        )
    return format_html('<script src="{}" referrerpolicy="no-referrer"></script>', src)


@register.simple_tag
def insight_htmx_scripts() -> SafeString:
    """Render the HTMX and htmx-ext-ws script tags from ``INSIGHT_UI["htmx"]``.

    Reads settings directly, so it works without the context processor. The
    defaults load both scripts from jsdelivr with SRI hashes. Hosts can point
    ``src``/``ws_src`` at self-hosted copies (updating or clearing the matching
    ``integrity``) or set a ``src`` to an empty string to omit that script.

    Returns:
        The script tags, HTML-escaped and marked safe.

    """
    htmx = cast("Mapping[str, object]", get_config("htmx"))
    return format_html(
        "{}\n{}",
        _script_tag(htmx.get("src"), htmx.get("integrity")),
        _script_tag(htmx.get("ws_src"), htmx.get("ws_integrity")),
    )
