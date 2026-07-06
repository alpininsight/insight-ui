"""Template tags for Insight UI asset URLs."""

from django import template

from insight_ui.asset_urls import insight_asset_url

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
