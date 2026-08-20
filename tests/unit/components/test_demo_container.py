"""Tests for the shared documentation demo container."""

from django.template.loader import render_to_string
from insight_ui.context import get_demo_container_context


def test_demo_container_wraps_controls_without_changing_control_contract() -> None:
    """Narrow documentation columns keep every existing demo control available."""
    context = get_demo_container_context() | {
        "demo": {
            "id": "responsive-demo",
            "title": "Responsive demo",
            "url": "/docs/demo/responsive/",
            "template_repo_url": "https://example.test/template",
            "script_repo_url": "https://example.test/script",
        }
    }

    rendered = render_to_string("insight_ui/docs/demo_container.html", context)

    assert "flex flex-wrap gap-1.5 justify-between items-center p-1.5 h-auto" in rendered
    assert 'name="width-toggle-responsive-demo"' in rendered
    assert 'id="dir-toggle-responsive-demo"' in rendered
    assert 'id="theme-toggle-responsive-demo"' in rendered
