# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for the tabs layout tag."""

import pytest
from bs4 import BeautifulSoup
from django.template import Context, Template, TemplateSyntaxError
from insight_ui.configs import TabConfig, TabsConfig


def render(body: str, context: dict | None = None) -> BeautifulSoup:
    """Render a template snippet with layout_tags loaded."""
    html = Template("{% load layout_tags %}" + body).render(Context(context or {}))
    return BeautifulSoup(html, "html.parser")


def tab_buttons(soup: BeautifulSoup) -> list:
    """Return the tab buttons in order."""
    return soup.find_all(attrs={"role": "tab"})


STATIC = """
{% tabs id="install" label="Installation" %}
    {% tab id="uv" label="uv" %}uv content{% endtab %}
    {% tab id="pip" label="pip" %}pip content{% endtab %}
{% endtabs %}
"""


def test_tab_config_requires_request_url() -> None:
    """TabConfig requires request_url (config mode is HTMX-only)."""
    with pytest.raises(TypeError):
        TabConfig(tag_id="general", title="General")  # type: ignore[call-arg]


def test_id_and_label_name_the_tab_group() -> None:
    """The tablist gets its accessible name, and the id identifies the group and its panels."""
    soup = render(STATIC)

    assert soup.find(attrs={"data-insight-tabs": "install"}) is not None
    assert soup.find(attrs={"role": "tablist"})["aria-label"] == "Installation"
    assert soup.find(id="install-uv")["role"] == "tabpanel"


def test_first_tab_is_active_by_default() -> None:
    """Without active=True the first tab is selected and its panel visible."""
    soup = render(STATIC)
    uv, pip = tab_buttons(soup)

    assert (uv["aria-selected"], pip["aria-selected"]) == ("true", "false")
    assert "hidden" not in soup.find(id="install-uv").get("class", [])
    assert "hidden" in soup.find(id="install-pip")["class"]


def test_only_one_tab_is_active_even_if_several_are_marked() -> None:
    """The first tab marked active wins; there is never more than one selected tab."""
    soup = render(
        """
        {% tabs id="t" %}
            {% tab id="a" label="A" %}A{% endtab %}
            {% tab id="b" label="B" active=True %}B{% endtab %}
            {% tab id="c" label="C" active=True %}C{% endtab %}
        {% endtabs %}
        """
    )

    assert [tab["aria-selected"] for tab in tab_buttons(soup)] == ["false", "true", "false"]


def test_active_tab_follows_the_context_on_every_render() -> None:
    """The active tab is decided per render, so one compiled template serves different requests."""
    template = Template(
        """{% load layout_tags %}{% tabs id="t" %}
        {% for item in items %}{% tab id=item.id label=item.id active=item.active %}x{% endtab %}{% endfor %}
        {% endtabs %}"""
    )

    for current in ("b", "a", "b"):
        items = [{"id": key, "active": key == current} for key in ("a", "b")]
        soup = BeautifulSoup(template.render(Context({"items": items})), "html.parser")
        selected = [tab["id"] for tab in tab_buttons(soup) if tab["aria-selected"] == "true"]
        assert selected == [current]


def test_tabs_can_be_conditional() -> None:
    """{% if %} around a tab works and leaves the tab out when false."""
    body = """
    {% tabs id="t" %}
        {% tab id="a" label="A" %}A{% endtab %}
        {% if show_admin %}{% tab id="admin" label="Admin" %}Admin{% endtab %}{% endif %}
    {% endtabs %}
    """

    assert [tab["id"] for tab in tab_buttons(render(body, {"show_admin": True}))] == ["a", "admin"]
    assert [tab["id"] for tab in tab_buttons(render(body, {"show_admin": False}))] == ["a"]


def test_tabs_can_come_from_a_loop_with_variables() -> None:
    """Tab parameters are resolved from the context, also inside {% for %}."""
    soup = render(
        """
        {% tabs id=group_id label=group_label %}
            {% for item in items %}
                {% tab id=item.id label=item.label %}{{ item.text }}{% endtab %}
            {% endfor %}
        {% endtabs %}
        """,
        {
            "group_id": "langs",
            "group_label": "Languages",
            "items": [
                {"id": "de", "label": "Deutsch", "text": "Hallo"},
                {"id": "en", "label": "English", "text": "Hi"},
            ],
        },
    )

    assert [(tab["id"], tab.get_text(strip=True)) for tab in tab_buttons(soup)] == [
        ("de", "Deutsch"),
        ("en", "English"),
    ]
    assert soup.find(attrs={"role": "tablist"})["aria-label"] == "Languages"
    assert soup.find(id="langs-en").get_text(strip=True) == "Hi"


def test_static_panels_are_labelled_by_their_tab() -> None:
    """Each panel is named by its tab and can receive focus."""
    soup = render(STATIC)
    panel = soup.find(id="install-pip")

    assert panel["aria-labelledby"] == "pip"
    assert panel["tabindex"] == "0"


def test_tab_icon_renders_an_icon_not_its_name() -> None:
    """The icon parameter is an icon name and renders the SVG icon."""
    soup = render('{% tabs id="t" %}{% tab id="a" label="A" icon="rocket-launch" %}A{% endtab %}{% endtabs %}')
    button = tab_buttons(soup)[0]

    assert button.find("svg") is not None
    assert "rocket-launch" not in button.get_text()


def test_htmx_tabs_load_the_active_tab_and_label_the_panel() -> None:
    """The active tab loads its content right away; the shared panel is labelled by it."""
    soup = render(
        """
        {% tabs id="settings" label="Settings" %}
            {% tab id="general" label="General" request_url="/settings/general/" %}{% endtab %}
            {% tab id="security" label="Security" request_url="/settings/security/" %}{% endtab %}
        {% endtabs %}
        """
    )
    general, security = tab_buttons(soup)
    panel = soup.find(id="settings-tab-content")

    assert general["hx-trigger"] == "load, click"
    assert not security.has_attr("hx-trigger")
    assert panel["aria-labelledby"] == "general"


def test_config_mode_renders_the_tabs_of_the_config() -> None:
    """A TabsConfig renders HTMX tabs; id and label arguments override it."""
    config = TabsConfig(
        tag_id="settings",
        label="Settings",
        tabs=[
            TabConfig(tag_id="general", title="General", request_url="/general/"),
            TabConfig(tag_id="security", title="Security", request_url="/security/", active=True),
        ],
    )
    soup = render('{% tabs config=config label="Account" %}{% endtabs %}', {"config": config})

    assert soup.find(attrs={"role": "tablist"})["aria-label"] == "Account"
    assert [tab["aria-selected"] for tab in tab_buttons(soup)] == ["false", "true"]


def test_config_mode_rejects_dicts() -> None:
    """Like the component tags, only dataclass configs are accepted."""
    with pytest.raises(TypeError, match="must be a dataclass instance"):
        render("{% tabs config=config %}{% endtabs %}", {"config": {"tag_id": "x", "tabs": []}})


def test_config_and_tab_blocks_cannot_be_combined() -> None:
    """Either the config or the blocks define the tabs."""
    config = TabsConfig(tag_id="s", tabs=[TabConfig(tag_id="a", title="A", request_url="/a/")])

    with pytest.raises(ValueError, match="either a config or"):
        render('{% tabs config=config %}{% tab id="b" label="B" %}B{% endtab %}{% endtabs %}', {"config": config})


def test_tab_outside_of_tabs_is_an_error() -> None:
    """A lone {% tab %} would otherwise render nothing without notice."""
    with pytest.raises(TemplateSyntaxError, match="must be placed inside"):
        render('{% tab id="a" label="A" %}A{% endtab %}')


@pytest.mark.parametrize(
    ("body", "message"),
    [
        pytest.param('{% tabs id="t" colour="red" %}{% endtabs %}', "Unknown parameter 'colour'", id="tabs"),
        pytest.param(
            '{% tabs id="t" %}{% tab id="a" lable="A" %}A{% endtab %}{% endtabs %}',
            "Unknown parameter 'lable'",
            id="tab",
        ),
    ],
)
def test_unknown_parameters_are_rejected(body: str, message: str) -> None:
    """Typos in parameters fail instead of being ignored."""
    with pytest.raises(ValueError, match=message):
        render(body)


def test_tabs_config_without_tabs_fails_clearly() -> None:
    """An empty tab list has no tab to activate."""
    with pytest.raises(ValueError, match="at least one tab"):
        TabsConfig(tag_id="settings", tabs=[])
