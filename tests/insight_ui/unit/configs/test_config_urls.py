# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests that every URL field of a config accepts only relative URLs and the schemes of its kind."""

import dataclasses
import inspect
import re
from types import ModuleType
from typing import Any

import pytest
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.test import override_settings
from django.urls import clear_url_caches, path, reverse_lazy
from django.utils.functional import lazy
from django.utils.safestring import mark_safe
from insight_ui.configs import FooterContactConfig, NavbarBrandConfig, PaginationConfig, WebSocketConfig

from insight_ui import configs

# Building a config with every URL field set triggers warnings about combinations, e.g. polling and
# server-sent events at once; they do not matter for the scheme check.
pytestmark = pytest.mark.filterwarnings("ignore::UserWarning")

URL_FIELD = re.compile(r"^url(_dark)?$|_url$|^href$")

# Required fields that are not text.
EXTRA_REQUIRED: dict[type, dict[str, Any]] = {
    PaginationConfig: {"current_page": Paginator(range(5), 2).get_page(1)},
}


def url_fields(config_class: type) -> list[str]:
    """Return the URL fields of a config class."""
    return [field.name for field in dataclasses.fields(config_class) if URL_FIELD.search(field.name)]


def config_classes() -> list[type]:
    """Return every public config class with a URL field."""
    found = {
        value
        for value in vars(configs).values()
        if inspect.isclass(value) and dataclasses.is_dataclass(value) and url_fields(value)
    }
    return sorted(found, key=lambda config_class: config_class.__name__)


def build(config_class: type) -> object:
    """Build a valid config: text for required fields and a relative URL in every URL field."""
    values: dict[str, Any] = {}
    for field in dataclasses.fields(config_class):
        required = field.default is dataclasses.MISSING and field.default_factory is dataclasses.MISSING
        if field.name in url_fields(config_class) or required:
            values[field.name] = "/path"
    values.update(EXTRA_REQUIRED.get(config_class, {}))
    return config_class(**values)


FIELDS = [
    pytest.param(config_class, name, id=f"{config_class.__name__}.{name}")
    for config_class in config_classes()
    for name in url_fields(config_class)
]


@pytest.mark.parametrize(("config_class", "name"), FIELDS)
def test_url_field_rejects_script_urls(config_class: type, name: str) -> None:
    """A URL field rejects a scheme outside its kind, also when the browser would ignore the spaces in it."""
    config = build(config_class)

    for url in ("javascript:alert(1)", " JavaScript:alert(1)", "java\tscript:alert(1)"):
        with pytest.raises(ValueError, match="is not allowed"):
            dataclasses.replace(config, **{name: url})


@pytest.mark.parametrize(("config_class", "name"), FIELDS)
def test_url_field_accepts_relative_and_web_urls(config_class: type, name: str) -> None:
    """Relative URLs, query strings, fragments and web URLs stay valid."""
    config = build(config_class)

    for url in ("/news/?page=2", "news/", "report 1:summary", "#section", "?q=lamp", "https://example.com/a"):
        dataclasses.replace(config, **{name: url})


@pytest.mark.parametrize(("config_class", "name"), FIELDS)
def test_lazy_url_field_rejects_script_urls(config_class: type, name: str) -> None:
    """Django lazy string values obey the same scheme validation as plain strings."""
    config = build(config_class)
    script_url = lazy(lambda: "java\tscript:alert(1)", str)()
    with pytest.raises(ValueError, match="is not allowed"):
        str(getattr(dataclasses.replace(config, **{name: script_url}), name))


@pytest.mark.parametrize(("config_class", "name"), FIELDS)
def test_lazy_url_field_accepts_relative_urls(config_class: type, name: str) -> None:
    """Safe lazy strings stay usable, including spaces in relative path segments."""
    config = build(config_class)
    url = lazy(lambda: "report 1:summary", str)()
    updated = dataclasses.replace(config, **{name: url})
    assert str(getattr(updated, name)) == "report 1:summary"


@pytest.mark.parametrize(("config_class", "name"), FIELDS)
@pytest.mark.parametrize(
    "encoded", ["javascript&colon;alert(1)", "java&#9;script&#58;alert(1)", "&#106;avascript:alert(1)"]
)
def test_safe_url_field_rejects_encoded_script_schemes(config_class: type, name: str, encoded: str) -> None:
    """Trusted HTML entities cannot bypass the URL allowlist."""
    config = build(config_class)
    with pytest.raises(ValueError, match="is not allowed"):
        dataclasses.replace(config, **{name: mark_safe(encoded)})  # noqa: S308 - hostile trusted fixture


@pytest.mark.parametrize(("config_class", "name"), FIELDS)
def test_lazy_safe_url_field_rejects_encoded_script_schemes(config_class: type, name: str) -> None:
    """Lazy values that resolve to trusted HTML get the same entity check."""
    config = build(config_class)
    value = lazy(lambda: mark_safe("javascript&colon;alert(1)"), str)()
    with pytest.raises(ValueError, match="is not allowed"):
        str(getattr(dataclasses.replace(config, **{name: value}), name))


@pytest.mark.parametrize(("config_class", "name"), FIELDS)
def test_plain_url_field_preserves_literal_entity_text(config_class: type, name: str) -> None:
    """An ordinary URL is escaped by Django rather than treated as trusted HTML."""
    config = build(config_class)
    dataclasses.replace(config, **{name: "javascript&colon;label"})


def test_reverse_lazy_waits_until_the_urlconf_is_ready() -> None:
    """Module-level navbar configuration can be created before URL patterns exist."""
    urlconf = ModuleType("deferred_urlconf")
    urlconf.urlpatterns = []
    with override_settings(ROOT_URLCONF=urlconf):
        config = NavbarBrandConfig(request_url=reverse_lazy("home"))
        urlconf.urlpatterns = [path("home/", lambda _: HttpResponse(), name="home")]
        clear_url_caches()
        assert str(config.request_url) == "/home/"
    clear_url_caches()


def test_url_kinds_allow_their_schemes() -> None:
    """Links allow mailto and tel, images data URLs and WebSocket endpoints ws and wss."""
    footer = build(FooterContactConfig)
    dataclasses.replace(footer, privacy_url="mailto:team@example.com", imprint_url="tel:+49301234")
    image = build(configs.ImageConfig)
    dataclasses.replace(image, url="data:image/svg+xml;base64,PHN2Zy8+")
    socket = build(WebSocketConfig)
    dataclasses.replace(socket, request_url="wss://example.com/ws/")

    with pytest.raises(ValueError, match="is not allowed"):
        dataclasses.replace(footer, imprint_url="data:text/html;base64,PGI+")
    with pytest.raises(ValueError, match="is not allowed"):
        dataclasses.replace(socket, request_url="mailto:team@example.com")
