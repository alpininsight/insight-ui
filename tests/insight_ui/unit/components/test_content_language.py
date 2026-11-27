# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Content components take the language of the page.

base.html sets lang on <html> from the active language, and every element inherits it. A component that sets its own
lang would mark content in another language wrongly: screen readers read it with the wrong pronunciation and automatic
hyphenation follows the wrong rules. Content in a different language is marked by the host around the component.
"""

import pytest
from bs4 import BeautifulSoup
from django.template import Context, Template

COMPONENTS = {
    "app_card": '{% app_card title="Release notes" content="Install the package and run the migrations." %}',
    "flip_card": (
        '{% flip_card title="Release notes" content="Install the package and run the migrations." '
        'back_content="Details" %}'
    ),
    "article": '{% article title="Release notes" content="Install the package and run the migrations." %}',
}


@pytest.mark.parametrize("tag", list(COMPONENTS))
def test_content_inherits_the_page_language(tag: str) -> None:
    """No element of the component sets its own lang, so the content follows the page language."""
    html = Template("{% load insight_tags %}" + COMPONENTS[tag]).render(Context())
    soup = BeautifulSoup(html, "html.parser")

    assert "Install the package" in soup.get_text()
    assert soup.find(attrs={"lang": True}) is None
