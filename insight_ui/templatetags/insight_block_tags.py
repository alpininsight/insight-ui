from collections.abc import Iterable
from typing import Any

from django import template
from django.template.base import Parser, Token, token_kwargs
from django.template.loader import render_to_string
from django.utils.safestring import SafeString

from insight_ui.config import get_config
from insight_ui.configs.navigation import SidebarConfig
from insight_ui.templatetags.insight_tags import build_config

register = template.Library()


class SidebarNode(template.Node):
    """Configurable sidebar with page navigation."""

    def __init__(self, nodelist: Iterable[str] | None, kwargs: dict[str, Any]) -> None:
        """Create SidebarNode instance."""
        self.nodelist = nodelist
        self.kwargs = kwargs

    def render(self, context: dict[str, Any]) -> SafeString:
        """Render a configurable sidebar with page navigation."""
        resolved = {key: value.resolve(context) for key, value in self.kwargs.items()}

        custom_content = self.nodelist.render(context).strip()

        config = build_config(SidebarConfig, resolved.pop("config", None), **resolved)

        return render_to_string(
            "insight_ui/components/sidebar.html",
            {"sidebar_config": config, "navbar_fixed": get_config("navbar_fixed"), "custom_content": custom_content},
            request=context.get("request"),
        )


@register.tag
def sidebar(parser: Parser, token: Token) -> SidebarNode:
    """Render a configurable sidebar with page navigation."""
    bits = token.split_contents()

    kwargs = token_kwargs(bits[1:], parser)

    nodelist = parser.parse(("endsidebar",))
    parser.delete_first_token()

    return SidebarNode(nodelist, kwargs)
