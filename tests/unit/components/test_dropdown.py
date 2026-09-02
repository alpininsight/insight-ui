"""Tests for the dropdown component."""

import pytest
from insight_ui.configs import DropdownConfig, DropdownItemConfig, HtmxConfig

from tests.unit.components.test_template_tags import TemplateTagsTestCase


class TestDropdown(TemplateTagsTestCase):
    """Test suite for the dropdown component."""

    def test_dropdown_item_config_requires_request_url(self) -> None:
        """DropdownItemConfig requires request_url (avoids dead '#' links)."""
        with pytest.raises(TypeError):
            DropdownItemConfig(text="Profile")  # type: ignore[call-arg]

    def test_dropdown_item_with_htmx(self) -> None:
        """DropdownItemConfig accepts optional htmx configuration."""
        item = DropdownItemConfig(
            text="Dashboard",
            request_url="/dashboard/",
            htmx=HtmxConfig(target="#content", push_url=True),
        )
        assert item.htmx is not None
        assert item.htmx.target == "#content"
        assert item.htmx.push_url is True

    def test_dropdown_renders_htmx_attributes(self) -> None:
        """Dropdown template renders HTMX attributes when htmx config is provided."""
        config = DropdownConfig(
            tag_id="test-dropdown",
            title="Menu",
            items=[
                DropdownItemConfig(
                    text="Dashboard",
                    request_url="/dashboard/",
                    htmx=HtmxConfig(target="#content", push_url=True),
                ),
            ],
        )
        rendered = self.render_template(
            "{% load insight_tags %}{% dropdown config=config %}",
            {"config": config},
        )
        assert 'hx-get="/dashboard/"' in rendered
        assert 'hx-target="#content"' in rendered
        assert 'hx-push-url="true"' in rendered

    def test_dropdown_without_htmx(self) -> None:
        """Dropdown template does not render HTMX attributes when htmx is None."""
        config = DropdownConfig(
            tag_id="test-dropdown",
            title="Menu",
            items=[
                DropdownItemConfig(text="Profile", request_url="/profile/"),
            ],
        )
        rendered = self.render_template(
            "{% load insight_tags %}{% dropdown config=config %}",
            {"config": config},
        )
        assert 'href="/profile/"' in rendered
        assert "hx-get" not in rendered
        assert "hx-target" not in rendered

    def test_dropdown_htmx_request_url_takes_precedence(self) -> None:
        """htmx.request_url takes precedence over item.request_url for hx-get."""
        config = DropdownConfig(
            tag_id="test-dropdown",
            title="Menu",
            items=[
                DropdownItemConfig(
                    text="Dashboard",
                    request_url="/dashboard/",  # fallback href
                    htmx=HtmxConfig(
                        request_url="/dashboard/partial/",  # HTMX endpoint
                        target="#content",
                    ),
                ),
            ],
        )
        rendered = self.render_template(
            "{% load insight_tags %}{% dropdown config=config %}",
            {"config": config},
        )
        assert 'href="/dashboard/"' in rendered  # fallback href preserved
        assert 'hx-get="/dashboard/partial/"' in rendered  # htmx.request_url used

    def test_dropdown_htmx_falls_back_to_request_url(self) -> None:
        """hx-get falls back to item.request_url when htmx.request_url is empty."""
        config = DropdownConfig(
            tag_id="test-dropdown",
            title="Menu",
            items=[
                DropdownItemConfig(
                    text="Reports",
                    request_url="/reports/",
                    htmx=HtmxConfig(target="#content"),  # no request_url
                ),
            ],
        )
        rendered = self.render_template(
            "{% load insight_tags %}{% dropdown config=config %}",
            {"config": config},
        )
        assert 'href="/reports/"' in rendered
        assert 'hx-get="/reports/"' in rendered  # falls back to request_url
