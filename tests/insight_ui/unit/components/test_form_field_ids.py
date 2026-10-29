# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for the id rule of form fields: the tag_id, otherwise the name."""

import pytest
from bs4 import BeautifulSoup, Tag
from django.template import Context, Template


def render(template: str) -> BeautifulSoup:
    """Render a template snippet with insight_tags loaded."""
    html = Template("{% load insight_tags %}" + template).render(Context({"options": ["a", "b"]}))
    return BeautifulSoup(html, "html.parser")


def is_labelled(soup: BeautifulSoup, control: Tag, text: str) -> bool:
    """Whether the control gets its accessible name from a label with the given text."""
    if control.find_parent("label") is not None:
        return text in control.find_parent("label").get_text()
    if control.has_attr("aria-labelledby"):
        return text in soup.find(id=control["aria-labelledby"]).get_text()
    label = soup.find("label", attrs={"for": control.get("id")})
    return label is not None and text in label.get_text()


# Tag call (without tag_id) and the selector of the labelled control, with "{id}" for the expected id.
FIELDS = [
    pytest.param('{% input_field name="email" label="Label"', "input#{id}", id="input_field"),
    pytest.param('{% textarea name="email" label="Label"', "textarea#{id}", id="textarea"),
    pytest.param('{% select name="email" label="Label" options=options', "select#{id}", id="select"),
    pytest.param('{% checkbox name="email" label="Label"', "input#{id}", id="checkbox"),
    pytest.param('{% toggle name="email" label="Label"', "input#{id}", id="toggle"),
    pytest.param('{% toggle name="email" label="Label" switch=True', "input#{id}", id="toggle-switch"),
    pytest.param('{% slider name="email" label="Label"', "input#{id}", id="slider"),
    pytest.param('{% multiselect name="email" label="Label" options=options', "input#{id}-search", id="multiselect"),
]


@pytest.mark.parametrize(("tag", "selector"), FIELDS)
def test_fields_without_tag_id_take_their_id_from_the_name(tag: str, selector: str) -> None:
    """The label is associated with the control even without a tag_id."""
    soup = render(tag + " %}")
    control = soup.select_one(selector.format(id="email"))

    assert control is not None
    assert is_labelled(soup, control, "Label")
    assert soup.find(id="None") is None
    assert soup.find(attrs={"for": "None"}) is None


@pytest.mark.parametrize(("tag", "selector"), FIELDS)
def test_tag_id_takes_precedence_over_the_name(tag: str, selector: str) -> None:
    """Two fields with the same name can coexist on one page through their tag_id."""
    soup = render(tag + ' tag_id="billing-email" %}')
    control = soup.select_one(selector.format(id="billing-email"))

    assert control is not None
    assert is_labelled(soup, control, "Label")
    assert soup.find(id="email") is None


@pytest.mark.parametrize(("tag", "selector"), [field for field in FIELDS if field.id != "multiselect"])
def test_the_name_stays_the_request_parameter(tag: str, selector: str) -> None:
    """The tag_id only changes the id; the form still submits under the name."""
    control = render(tag + ' tag_id="billing-email" %}').select_one(selector.format(id="billing-email"))

    assert control["name"] == "email"


def test_multiselect_ids_build_on_the_tag_id() -> None:
    """The listbox, its options and the status region use the tag_id; the hidden inputs keep the name."""
    soup = render('{% multiselect tag_id="billing-tags" name="tags" label="Tags" options=options %}')
    search = soup.find(id="billing-tags-search")

    assert soup.find(id=search["aria-controls"]) is not None
    assert soup.find(id="billing-tags-listbox") is not None
    assert soup.find(id="billing-tags-opt-1") is not None
    assert soup.find(id="billing-tags-aria-status") is not None
    assert not soup.select('[id^="tags-"]')


def test_slider_derives_its_ids_from_the_name() -> None:
    """The min and max labels of a slider without tag_id do not collide as "None"."""
    soup = render('{% slider name="volume" label="Volume" %}')
    ids = [element["id"] for element in soup.find_all(id=True)]

    assert "volume" in ids
    assert all(element_id.startswith("volume") for element_id in ids)
