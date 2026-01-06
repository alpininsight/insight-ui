from django.utils.translation import gettext as _

from insight_ui import config


def get_navbar_context() -> dict:
    """Serve data for main navbar."""
    return {
        "nav_config": {
            "brand": {
                "title": "Insight UI",
                "view_name": "index_view",
                "gap": "0.5rem",
                "logo": {
                    "url": "insight_ui/svg/ai-logo.svg",
                    "url_dark": "insight_ui/svg/ai-logo.svg",
                    "alt": "Insight UI Logo",
                    "height": "2rem",
                },
            },
            "links": [
                {
                    "text": _("Startpage"),
                    "icon": {"name": "home", "size": "small"},
                    "view_name": "index_view",
                    "active": True,
                    "need_auth": False,
                    "staff_only": False,
                },
                {
                    "text": _("Components"),
                    "open_dropdown": "components-menu",
                    "items": [
                        {
                            "text": "Main / Navigation",
                            "view_name": "storybook_view",
                            "view_arg": "main",
                            "htmx": {"target": "#content"},
                        },
                        {
                            "text": "Input Elements",
                            "view_name": "storybook_view",
                            "view_arg": "input",
                            "htmx": {"target": "#content"},
                        },
                        {
                            "text": "Popups",
                            "view_name": "storybook_view",
                            "view_arg": "popup",
                            "htmx": {"target": "#content"},
                        },
                        {
                            "text": "Utils",
                            "view_name": "storybook_view",
                            "view_arg": "util",
                            "htmx": {"target": "#content"},
                        },
                        {
                            "text": "List & Tables",
                            "view_name": "storybook_view",
                            "view_arg": "table",
                            "htmx": {"target": "#content"},
                        },
                        {
                            "text": "Cards",
                            "view_name": "storybook_view",
                            "view_arg": "card",
                            "htmx": {"target": "#content"},
                        },
                        {
                            "text": "Forms",
                            "view_name": "storybook_view",
                            "view_arg": "form",
                            "htmx": {"target": "#content"},
                        },
                        {
                            "text": "Search & Filters",
                            "view_name": "storybook_view",
                            "view_arg": "filter",
                            "htmx": {"target": "#content"},
                        },
                    ],
                    "chevron": {"name": "chevron_down", "size": "small"},
                    "active": False,
                    "need_auth": False,
                    "staff_only": False,
                },
            ],
            "searchbar_request_view": "index_view",
            "show_usermenu": False,
            "show_language_selector": True,
            "show_theme_toggle": True,
        }
    }


def get_footer_context() -> dict:
    """Server data for main footer."""
    return {
        "footer_data": {
            "description": {
                "title": "Insight UI",
                "text": "A modern, accessible, and responsive UI library for Django projects.",
            },
            "links": [
                {"text": _("Startpage"), "icon": {"name": "home", "size": "xs"}, "view_name": "index_view"},
                {"text": _("Storybook"), "view_name": "index_view"},
                {"text": _("Documentation"), "view_name": "index_view"},
            ],
            "contact": {"mail": {"url": "support@alpininsight.com"}, "imprint": "https://alpininsight.com/imprint/"},
            "copyright": {"year": 2025, "app_name": "Insight UI"},
        }
    }


def get_base_context() -> dict:
    """Serve basic context data, like navbar, footer and settings."""
    return config.get_config() | get_navbar_context() | get_footer_context()
