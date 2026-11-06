# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Native download behavior is additive, escaped and not intercepted by HTMX."""

from dataclasses import replace

import pytest
from bs4 import BeautifulSoup, Tag
from django.template import Context, Template
from django.utils.safestring import mark_safe
from insight_ui.configs import ButtonConfig, HtmxConfig
from insight_ui.configs.base import DataAttrConfig


def render_download(config: ButtonConfig, **kwargs: object) -> Tag:
    """Render the public Django tag, including its shared Config builder."""
    template = Template("{% load insight_tags %}{% button config=config download=download %}")
    context = {"config": config, "download": kwargs.get("download", config.download)}
    element = BeautifulSoup(template.render(Context(context)), "html.parser").find(["a", "button"])
    assert isinstance(element, Tag)
    return element


@pytest.mark.parametrize(("value", "expected"), [(True, ""), ("", ""), ("report.svg", "report.svg")])
def test_public_tag_supports_native_and_named_downloads(value: bool | str, expected: str) -> None:
    """Inline and Config APIs preserve the native advisory filename."""
    element = render_download(ButtonConfig(label="Download", request_url="/files/report.svg", download=value))
    assert element["download"] == expected
    assert element["href"] == "/files/report.svg"
    assert element.has_attr("hx-disable")
    assert element.name == "a"


def test_inline_download_argument_uses_the_same_api() -> None:
    """The new option is an explicit public tag argument, not a dynamic kwarg."""
    template = Template(
        '{% load insight_tags %}{% button label="Download" request_url="/files/report.svg" download=True %}'
    )
    element = BeautifulSoup(template.render(Context()), "html.parser").find("a")
    assert element.has_attr("download")


def test_default_and_explicit_false_keep_existing_links_unchanged() -> None:
    """False overrides are not confused with an omitted UNSET argument."""
    config = ButtonConfig(label="Open", request_url="/files/report.svg")
    for element in (render_download(config), render_download(replace(config, download=True), download=False)):
        assert not element.has_attr("download")
        assert not element.has_attr("hx-disable")
        assert element["href"] == config.request_url


def test_disabled_download_is_not_an_active_link() -> None:
    """Disabled anchors have no request or download behavior."""
    config = ButtonConfig(
        label="Download", request_url="/files/report.svg", download=True, disabled=True, disabled_reason=""
    )
    element = render_download(config)
    assert element["aria-disabled"] == "true"
    assert not element.has_attr("href")
    assert not element.has_attr("download")
    assert not any(name.startswith("hx-") for name in element.attrs)


@pytest.mark.parametrize("safe", [False, True])
def test_suggested_filename_cannot_inject_html_attributes(safe: bool) -> None:
    """Even an explicitly trusted string must be escaped in the attribute."""
    filename = 'report" onmouseover="alert(1)&<.svg'
    value = mark_safe(filename) if safe else filename  # noqa: S308 - deliberate hostile fixture
    element = render_download(ButtonConfig(label="Download", request_url="/file.svg", download=value))
    assert element["download"] == filename
    assert not element.has_attr("onmouseover")


@pytest.mark.parametrize("value", [None, 0, 1, [], {}])
def test_invalid_download_types_fail_early(value: object) -> None:
    """Reject numbers/containers instead of silently treating them as True."""
    with pytest.raises(TypeError, match="bool or a filename string"):
        ButtonConfig(label="Download", request_url="/file.svg", download=value)  # type: ignore[arg-type]


@pytest.mark.parametrize("value", [True, "", "file.svg"])
def test_download_requires_a_link_url(value: bool | str) -> None:
    """Downloads cannot be applied to a form/action button without a URL."""
    with pytest.raises(ValueError, match="request_url"):
        ButtonConfig(label="Download", download=value)


@pytest.mark.parametrize("value", ["report\n.svg", "report\r.svg", "report\x00.svg", "report\x7f.svg"])
def test_filename_control_characters_are_rejected(value: str) -> None:
    """Control characters in an advisory filename are rejected before render."""
    with pytest.raises(ValueError, match="control characters"):
        ButtonConfig(label="Download", request_url="/file.svg", download=value)


def test_download_rejects_explicit_htmx_interception() -> None:
    """A native download cannot also request an HTMX partial update."""
    with pytest.raises(ValueError, match="HTMX request"):
        ButtonConfig(label="Download", request_url="/file.svg", download=True, htmx=HtmxConfig())
    with pytest.raises(ValueError, match="HTMX request"):
        ButtonConfig(
            label="Download", request_url="/file.svg", download=True, hx_attrs=[DataAttrConfig("get", "/file")]
        )


def test_empty_filename_override_enables_native_download() -> None:
    """An empty inline override enables downloads even when the Config disables them."""
    config = ButtonConfig(label="Download", request_url="/file.svg")
    assert ButtonConfig(label="Download", request_url="/file.svg", download="").download is True
    element = render_download(config, download="")
    assert element["download"] == ""
    assert element.has_attr("hx-disable")
