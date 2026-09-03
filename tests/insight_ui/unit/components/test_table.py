"""Tests for the table component."""

from bs4 import BeautifulSoup
from insight_ui.configs.list import TableConfig

from tests.insight_ui.unit.components.test_template_tags import TemplateTagsTestCase


class TestTable(TemplateTagsTestCase):
    """Test suite for the table component."""

    def test_table_basic(self) -> None:
        """Test für grundlegende table Funktionalität."""
        table = TableConfig(
            ["Name", "E-Mail", "Status", "Actions"],
            [
                ["Max Mustermann", "max@example.com", "Active", '<button class="btn btn-primary">Edit</button>'],
                ["Anna Schmidt", "anna@example.com", "Inactive", '<button class="btn btn-primary">Edit</button>'],
                ["Tom Weber", "tom@example.com", "Active", '<button class="btn btn-primary">Edit</button>'],
            ],
            "Example of a table component.",
        )

        template_string = """
        {% load insight_tags %}
        {% table config=user_data %}
        """
        rendered = self.render_template(template_string, context={"user_data": table})
        soup = BeautifulSoup(rendered, "html.parser")

        table = soup.find("table")
        assert table.find("caption") is not None

        header_row = table.find("thead").find("tr")
        headers = [th.get_text(strip=True) for th in header_row.find_all("th")]
        assert headers == ["Name", "E-Mail", "Status", "Actions"]

        rows = table.find("tbody").find_all("tr")
        assert len(rows) == 3  # noqa: PLR2004

        first_row = [td.get_text(strip=True) for td in rows[0].find_all("td")]
        assert first_row == ["Max Mustermann", "max@example.com", "Active", "Edit"]
