"""Utilities owned by the documentation application search."""

from django.templatetags.static import static
from django.utils.translation import get_language


def get_search_index_url() -> str:
    """Return the static search-index URL for the active documentation language."""
    locale = (get_language() or "en").split("-", maxsplit=1)[0]
    return static(f"documentation/data/search-index-{locale}.json")
