from django import template

from insight_ui.asset_urls import design_theme_asset_url, insight_asset_url

register = template.Library()


@register.simple_tag
def insight_asset(asset_path: str) -> str:
    """Resolve Insight UI CSS/JS assets for local staticfiles or CDN delivery."""
    return insight_asset_url(asset_path)


@register.simple_tag
def design_theme_asset(asset_path: str) -> str:
    """Resolve built-in or host-owned design theme stylesheet URLs."""
    return design_theme_asset_url(asset_path)
