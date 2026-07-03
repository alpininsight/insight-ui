"""Template tags for Insight UI asset URLs."""

from django import template

from insight_ui.asset_urls import insight_asset_url

register = template.Library()


@register.simple_tag
def insight_asset(asset_path: str) -> str:
    """Resolve Insight UI CSS/JS assets for local staticfiles or CDN delivery."""
    return insight_asset_url(asset_path)
