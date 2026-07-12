"""Tests for form status partials."""

from bs4 import BeautifulSoup

from tests.unit.components.test_template_tags import TemplateTagsTestCase


class TestFormStatus(TemplateTagsTestCase):
    """Test suite for form error and success status partials."""

    def test_form_errors_use_semantic_status_classes(self) -> None:
        """Form errors use semantic status classes instead of hard-coded red classes."""
        rendered = self.render_template(
            '{% include "insight_ui/components/form_errors.html" with errors=errors %}',
            context={"errors": {"name": "Name is required."}},
        )
        soup = BeautifulSoup(rendered, "html.parser")

        status = soup.select_one(".insight-form-status-error")
        title = soup.select_one(".insight-form-status-title-error")
        body = soup.select_one(".insight-form-status-body-error")

        assert status is not None
        assert "insight-form-status" in status.get("class", [])
        assert title is not None
        assert body is not None
        assert "bg-red-50" not in status.get("class", [])
        assert "dark:bg-red-900/20" not in status.get("class", [])
        assert "text-red-800" not in title.get("class", [])
        assert "text-red-700" not in body.get("class", [])

    def test_form_success_uses_semantic_status_classes(self) -> None:
        """Form success uses semantic status classes instead of hard-coded green classes."""
        rendered = self.render_template(
            (
                '{% include "insight_ui/components/form_success.html" '
                "with title=title firstname=firstname lastname=lastname %}"
            ),
            context={"title": "Dr.", "firstname": "Ada", "lastname": "Lovelace"},
        )
        soup = BeautifulSoup(rendered, "html.parser")

        status = soup.select_one(".insight-form-status-success")
        title = soup.select_one(".insight-form-status-title-success")
        body = soup.select_one(".insight-form-status-body-success")

        assert status is not None
        assert "insight-form-status" in status.get("class", [])
        assert title is not None
        assert body is not None
        assert "bg-green-50" not in status.get("class", [])
        assert "dark:bg-green-900/20" not in status.get("class", [])
        assert "text-green-800" not in title.get("class", [])
        assert "text-green-700" not in body.get("class", [])
