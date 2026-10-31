# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for the text_diff and code_diff components."""

import json

import pytest
from bs4 import BeautifulSoup
from django.template import Context, Template
from insight_ui.configs import CodeDiffConfig, TextDiffConfig


def render(body: str, context: dict | None = None) -> BeautifulSoup:
    """Render a template snippet with insight_tags loaded."""
    html = Template("{% load insight_tags %}" + body).render(Context(context or {}))
    return BeautifulSoup(html, "html.parser")


# --- text_diff --------------------------------------------------------------------


def text_diff(before: str, after: str, **kwargs: object) -> BeautifulSoup:
    """Render a text diff for two texts."""
    return render("{% text_diff config=c %}", {"c": TextDiffConfig(before=before, after=after, **kwargs)})


def test_text_diff_marks_removed_and_added_words() -> None:
    """Removed words are in <del>, added words in <ins>, unchanged text stays plain."""
    soup = text_diff("The meeting is on Monday.", "The meeting is on Tuesday at noon.")
    text = soup.select_one(".insight-text-diff p")

    assert [element.get_text() for element in text.find_all("del")] == ["Removed: Monday"]
    assert [element.get_text() for element in text.find_all("ins")] == ["Added: Tuesday at noon"]
    assert text.get_text().startswith("The meeting is on ")


def test_text_diff_announces_changes_to_screen_readers() -> None:
    """Each change starts with a visually hidden label, so the meaning does not rely on styling."""
    soup = text_diff("red", "blue")

    assert soup.select_one("del .sr-only").get_text().strip() == "Removed:"
    assert soup.select_one("ins .sr-only").get_text().strip() == "Added:"


def test_text_diff_marks_punctuation_separately() -> None:
    """A changed punctuation mark does not mark the whole word."""
    text = text_diff("Hello, world", "Hello world").select_one(".insight-text-diff p")

    assert [element.get_text() for element in text.find_all("del")] == ["Removed: ,"]
    assert text.find("ins") is None


def test_text_diff_keeps_line_breaks() -> None:
    """Paragraph breaks survive and are shown as line breaks."""
    soup = text_diff("First line.\nSecond line.", "First line.\nThird line.")
    paragraph = soup.select_one(".insight-text-diff p")

    assert "\n" in paragraph.get_text()
    assert "whitespace-pre-line" in paragraph["class"]


def test_text_diff_escapes_both_texts() -> None:
    """Markup in the texts is shown as text, never rendered."""
    soup = text_diff("<b>old</b>", '<img src=x onerror="alert(1)">')

    assert soup.find("img") is None
    assert soup.find("b") is None
    assert 'onerror="alert(1)"' in soup.get_text()


def test_text_diff_legend_can_be_hidden() -> None:
    """The legend explains the markings and is hidden from assistive technology."""
    legend = text_diff("a", "b").select_one(".insight-text-diff p[aria-hidden='true']")

    assert legend.get_text(" ", strip=True) == "removed added"
    assert text_diff("a", "b", show_legend=False).select_one("p[aria-hidden='true']") is None


def test_text_diff_accepts_tag_arguments() -> None:
    """Before and after can be passed directly to the tag."""
    soup = render('{% text_diff before="one" after="two" show_legend=False %}')

    assert soup.find("del").get_text() == "Removed: one"


# --- code_diff --------------------------------------------------------------------


def code_diff(before: str, after: str, **kwargs: object) -> BeautifulSoup:
    """Render a code diff for two snippets."""
    return render("{% code_diff config=c %}", {"c": CodeDiffConfig(before=before, after=after, **kwargs)})


def test_code_diff_marks_every_line() -> None:
    """Unchanged lines start with a space, removed with "-" and added with "+"; nothing is collapsed."""
    before = """
        def greet(name):
            return "Hi " + name
    """
    after = """
        def greet(name):
            return f"Hello, {name}!"
    """
    pre = code_diff(before, after, language="python").pre

    assert pre.get_text().splitlines() == [
        " def greet(name):",
        '-    return "Hi " + name',
        '+    return f"Hello, {name}!"',
    ]


def test_code_diff_renders_a_code_block_in_diff_mode() -> None:
    """The code block script turns the element into a highlighted diff without a copy button."""
    pre = code_diff("a = 1", "a = 2", language="python", filename="settings.py", tag_id="example").pre

    assert pre["data-insight-code-block"] == "python"
    assert pre.has_attr("data-diff")
    assert pre["data-filename"] == "settings.py"
    assert pre["id"] == "example"
    assert not pre.has_attr("data-copy")


def test_code_diff_escapes_the_code() -> None:
    """Code is shown as text; markup in it is not rendered."""
    pre = code_diff("<div>old</div>", "<script>alert(1)</script>", language="html").pre

    assert pre.find("script") is None
    assert "+<script>alert(1)</script>" in pre.get_text()


def test_code_diff_requires_a_language() -> None:
    """An empty language would leave the code block without a grammar."""
    with pytest.raises(ValueError, match="language"):
        CodeDiffConfig(before="a", after="b", language="")


def test_code_diff_accepts_tag_arguments() -> None:
    """before, after and language can be passed directly to the tag."""
    pre = render('{% code_diff before="x = 1" after="x = 2" language="python" %}').pre

    assert pre.get_text().splitlines() == ["-x = 1", "+x = 2"]


def test_code_diff_marks_the_changed_part_of_a_similar_line() -> None:
    """Only the changed attribute name is marked, in the removed and in the added line."""
    pre = code_diff(
        '<button class="btn" type="primary">Save</button>',
        '<button class="btn" color="primary">Save</button>',
        language="html",
    ).pre
    text = pre.get_text()
    marks = json.loads(pre["data-diff-marks"])

    assert [text[start:end] for start, end in marks] == ["type", "color"]


def test_code_diff_does_not_mark_rewritten_lines() -> None:
    """A line that shares little with its counterpart is only marked as a whole by its background."""
    pre = code_diff("x = compute(a, b)", 'print("done")', language="python").pre

    assert not pre.has_attr("data-diff-marks")


def test_code_diff_without_changes_inside_lines_has_no_marks() -> None:
    """Added and removed lines without a counterpart get no marks."""
    pre = code_diff("a = 1", "a = 1\nb = 2", language="python").pre

    assert pre.get_text().splitlines() == [" a = 1", "+b = 2"]
    assert not pre.has_attr("data-diff-marks")


def test_code_diff_marks_count_from_the_start_of_the_diff() -> None:
    """Marks of later lines include the lines before them, so they point at the right characters."""
    pre = code_diff("a = 1\nx = f(1)", "a = 1\nx = f(2)", language="python").pre
    text = pre.get_text()

    assert [text[start:end] for start, end in json.loads(pre["data-diff-marks"])] == ["1", "2"]
