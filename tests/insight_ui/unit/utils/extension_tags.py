# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Template library shaped like one of an extension package, built only on the public Config API."""

from typing import Any

from django import template
from insight_ui.configs import UNSET, ButtonConfig, Unset
from insight_ui.templatetags import insight_tags

register = template.Library()


@register.inclusion_tag("insight_ui/components/button.html")
def extension_button(
    config: ButtonConfig | None = None, *, label: str | Unset = UNSET, tooltip: str | Unset = UNSET
) -> dict[str, Any]:
    """Compose the Core button and forward the arguments, passed or not."""
    return insight_tags.button(config, label=label, tooltip=tooltip)
