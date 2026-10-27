# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests that every URL field of a config accepts only relative URLs and the schemes of its kind."""

import dataclasses
import inspect
import re
from typing import Any

import pytest
from django.core.paginator import Paginator
from insight_ui.configs import FooterContactConfig, PaginationConfig, WebSocketConfig

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

    for url in ("/news/?page=2", "news/", "#section", "?q=lamp", "https://example.com/a"):
        dataclasses.replace(config, **{name: url})


def test_url_kinds_allow_their_schemes() -> None:
    """Links allow mailto and tel, images data URLs and WebSocket endpoints ws and wss."""
    footer = build(FooterContactConfig)
    dataclasses.replace(footer, mail_url="mailto:team@example.com", imprint_url="tel:+49301234")
    image = build(configs.ImageConfig)
    dataclasses.replace(image, url="data:image/svg+xml;base64,PHN2Zy8+")
    socket = build(WebSocketConfig)
    dataclasses.replace(socket, request_url="wss://example.com/ws/")

    with pytest.raises(ValueError, match="is not allowed"):
        dataclasses.replace(footer, mail_url="data:text/html;base64,PGI+")
    with pytest.raises(ValueError, match="is not allowed"):
        dataclasses.replace(socket, request_url="mailto:team@example.com")
