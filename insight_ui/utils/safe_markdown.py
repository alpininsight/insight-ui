# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Markdown for text that may come from users: no raw HTML, only allowed link and image schemes."""

from __future__ import annotations

from html import unescape
from typing import TYPE_CHECKING

from markdown import Extension, Markdown, util
from markdown.treeprocessors import Treeprocessor

from insight_ui.configs.types import IMAGE_URL_SCHEMES, LINK_URL_SCHEMES, url_scheme

if TYPE_CHECKING:
    # Type only: Markdown builds the tree, nothing is parsed here.
    from xml.etree.ElementTree import Element  # nosec B405

# Attribute and the schemes it accepts besides relative URLs.
_URL_ATTRIBUTES: tuple[tuple[str, tuple[str, ...]], ...] = (("href", LINK_URL_SCHEMES), ("src", IMAGE_URL_SCHEMES))


class _UrlSchemeFilter(Treeprocessor):
    """Drop link and image URLs whose scheme is not allowed, e.g. ``javascript:``."""

    def run(self, root: Element) -> None:
        """Check every URL attribute after the inline patterns have built links and images.

        Args:
            root: Root element of the rendered document.

        """
        for element in root.iter():
            for attribute, allowed in _URL_ATTRIBUTES:
                url = element.get(attribute)
                if url is None:
                    continue
                # Markdown keeps character references in URLs and the browser decodes them in the attribute.
                scheme = url_scheme(unescape(url.replace(util.AMP_SUBSTITUTE, "&")))
                if scheme and scheme not in allowed:
                    del element.attrib[attribute]


class _UntrustedTextExtension(Extension):
    """Treat raw HTML as text and filter URL schemes."""

    def extendMarkdown(self, md: Markdown) -> None:  # noqa: N802 (Markdown API)
        """Remove the raw HTML processors and add the URL filter.

        Args:
            md: The Markdown instance to extend.

        """
        md.preprocessors.deregister("html_block")
        md.inlinePatterns.deregister("html")
        # After the inline processor (priority 20), which creates the links and images.
        md.treeprocessors.register(_UrlSchemeFilter(md), "insight_url_schemes", 5)


def render_untrusted(text: str) -> str:
    """Render Markdown from a source that is not trusted with HTML.

    Args:
        text: Markdown source.

    Returns:
        HTML in which raw HTML from the source is escaped and disallowed URLs are removed.

    """
    html: str = Markdown(extensions=[_UntrustedTextExtension()]).convert(text)
    return html
