"""Host integration fixture for the library's public configuration function."""

from django.http import HttpRequest
from insight_ui.config import get_config


def package_config(request: HttpRequest) -> object:
    """Supply library defaults without a documentation context processor."""
    return get_config()
