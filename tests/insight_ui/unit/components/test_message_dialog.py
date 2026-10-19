# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for the message_dialog component and the config support of the modal block tag."""

import pytest
from bs4 import BeautifulSoup, Tag
from django.template import Context, Template
from insight_ui.configs import ButtonConfig, MessageDialogConfig, ModalConfig


def render(template: str, context: dict | None = None) -> BeautifulSoup:
    """Render a template string and parse the result."""
    return BeautifulSoup(Template(template).render(Context(context or {})), "html.parser")


def render_dialog(config: MessageDialogConfig) -> Tag:
    """Render a message dialog and return the dialog element."""
    soup = render("{% load insight_tags %}{% message_dialog config %}", {"config": config})
    return soup.find(attrs={"aria-modal": "true"})


# --- message_dialog -----------------------------------------------------


def test_info_dialog_is_a_dialog_with_its_message_described() -> None:
    """An about box is a plain dialog; screen readers read the message when it opens."""
    dialog = render_dialog(MessageDialogConfig(id="about", title="About", message="Insight UI"))

    assert dialog["role"] == "dialog"
    assert dialog["aria-labelledby"] == "about-title"
    assert dialog["aria-describedby"] == "about-message"
    assert dialog.select_one("#about-message").get_text(strip=True) == "Insight UI"


def test_alert_dialog_uses_the_alertdialog_role() -> None:
    """A dialog that asks for a decision is an ARIA alertdialog."""
    dialog = render_dialog(MessageDialogConfig(id="confirm", title="Delete?", message="Sure?", alert=True))

    assert dialog["role"] == "alertdialog"


def test_message_paragraphs_are_rendered_in_order() -> None:
    """A list of strings renders one paragraph each."""
    dialog = render_dialog(MessageDialogConfig(id="about", message=["Insight UI", "Version 1"]))

    assert [p.get_text(strip=True) for p in dialog.select("#about-message p")] == ["Insight UI", "Version 1"]


def test_actions_replace_the_default_close_button() -> None:
    """Configured actions are the footer buttons; without them the footer offers a close button."""
    with_actions = render_dialog(
        MessageDialogConfig(
            id="confirm",
            message="Sure?",
            show_close=False,
            actions=[ButtonConfig(label="Cancel", type="secondary"), ButtonConfig(label="Delete", type="danger")],
        )
    )
    without_actions = render_dialog(MessageDialogConfig(id="about", message="Info", show_close=False))

    assert [b.get_text(strip=True) for b in with_actions.find_all("button")] == ["Cancel", "Delete"]
    close = without_actions.find("button")
    assert close.get_text(strip=True) == "Close"
    assert close["data-insight-dismiss"] == "modal"


def test_dialog_is_opened_like_a_modal() -> None:
    """The dialog uses the modal shell, so data-insight-modal buttons open it by its ID."""
    dialog = render_dialog(MessageDialogConfig(id="about", message="Info"))

    assert dialog["id"] == "about"
    assert "hidden" in dialog["class"]
    assert dialog.select_one('[data-insight-dismiss="modal"]') is not None


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        pytest.param({"id": "about", "message": ""}, "non-empty message", id="empty-message"),
        pytest.param({"id": "", "message": "Info"}, "non-empty id", id="empty-id"),
    ],
)
def test_dialog_requires_id_and_message(kwargs: dict, message: str) -> None:
    """The ID opens the dialog and the message is its content."""
    with pytest.raises(ValueError, match=message):
        MessageDialogConfig(**kwargs)


# --- modal block tag with config ----------------------------------------


def test_modal_block_tag_accepts_a_config() -> None:
    """The modal takes its settings from a ModalConfig, like the tabs."""
    soup = render(
        "{% load layout_tags %}{% modal config=c %}<p>Body</p>{% endmodal %}",
        {"c": ModalConfig(id="settings", title="Settings", show_close=False)},
    )
    modal = soup.find(attrs={"aria-modal": "true"})

    assert modal["id"] == "settings"
    assert modal.find("h2").get_text(strip=True) == "Settings"
    assert modal.find("button") is None
    assert modal.find("p").get_text(strip=True) == "Body"


def test_modal_parameters_override_the_config() -> None:
    """Single parameters win over the config, like the arguments of the component tags."""
    soup = render(
        "{% load layout_tags %}{% modal config=c title='Override' %}Body{% endmodal %}",
        {"c": ModalConfig(id="settings", title="Settings")},
    )

    assert soup.find("h2").get_text(strip=True) == "Override"


def test_modal_rejects_a_dict_config() -> None:
    """The modal follows the same config contract as the component tags."""
    with pytest.raises(TypeError, match="must be a dataclass instance"):
        render("{% load layout_tags %}{% modal config=c %}Body{% endmodal %}", {"c": {"id": "settings"}})
