from insight_ui.component_details.component_context import register_component
from insight_ui.component_details.components import Component


@register_component(Component.PAGE_HEADER)
def get_page_header_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the page header component."""
    return {
        "a11y": [
            "Der Titel wird als semantisches h1-Element gerendert.",
            "Die Beschreibung verwendet ein p-Element mit ausreichendem Farbkontrast (grau auf blau).",
        ]
    }


@register_component(Component.ARTICLE)
def get_article_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the article component."""
    return {
        "a11y": [
            "Der Artikel verwendet das semantische article-Element.",
            "Die Spaltenstruktur ist rein visuell und beeinflusst nicht die Lesereihenfolge für Screenreader.",
            "Die Spaltentrennung wird mit column-rule visuell dargestellt.",
        ]
    }


@register_component(Component.HERO)
def get_hero_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the hero component."""
    return {
        "a11y": [
            "Der Titel wird als semantisches h1-Element gerendert.",
            "CTA-Buttons sind als Link-Elemente mit klarer Beschriftung implementiert.",
            "Hintergrundbilder werden mit aria-hidden markiert.",
        ]
    }


@register_component(Component.NAVBAR)
def get_navbar_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the navbar component."""
    return {"a11y": ["Die Navbar-Komponente enthält einen Skip-Link zum Hauptinhalt."]}


@register_component(Component.SIDEBAR)
def get_sidebar_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the sidebar component."""
    return {
        "a11y": [
            "Die Sidebar verwendet für eine semantische Korrektheit das <aside>-Tag und das Attribute role='complementary'.",
            "Die Drawer Variante verwendet Focus-Trapping und besitzt ein Schließen-Button, um diese auch per Tastatur verwenden zu können.",
        ]
    }


@register_component(Component.FOOTER)
def get_footer_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the footer component."""
    return {
        "a11y": [
            "Die Überschriften der drei Spalten verwenden <h4>-Tags wodurch ein Screenreader zwischen den Spalten wechseln kann.",
            "Die Auflistung der Links verwendet ein semantisch korrektes <ul>-Tag mit entsprechenden <li>-Tags.",
        ]
    }


@register_component(Component.BREADCRUMBS)
def get_breadcrumb_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the breadcrumbs component."""
    return {
        "a11y": [
            "Die Komponente verwendet ein <nav>-Tag mit dem entsprechenden aria-label='Breadcrumb'.",
            "Das aktive Element besitzt das Attribute aria-current='page'.",
        ]
    }


@register_component(Component.STEP_BAR)
def get_step_bar_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the step bar component."""
    return {
        "a11y": [
            "Das grafische Element zu Beginn jedes Eintrags, sollte es keine Zahl sein, wird von Screenreadern mittels aria-hidden ignoriert, da es rein dekorativ ist."
        ]
    }


@register_component(Component.MINIMAL_STEP_BAR)
def get_minimal_step_bar_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the minimal step bar component."""
    return {"a11y": []}


@register_component(Component.BULLET_POINT_LIST)
def get_bullet_point_list_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the bullet point list component."""
    return {
        "a11y": [
            "Das grafische Element zu Beginn jedes Eintrags wird von Screenreadern mittels aria-hidden ignoriert, da es rein dekorativ ist."
        ]
    }


@register_component(Component.ACCORDION)
def get_accordion_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the accordion component."""
    return {
        "a11y": [
            "Das aktuell geöffnete Element wird mit aria-expanded='true' markiert.",
            "Die Kopfzeile ist mit aria-controls ausgestattet, wodurch der Bezug zum dem darunter liegenden Container hergestellt wird.",
            "Der Container besitzt zusätzlich das Attribut aria-labelledby.",
            "Der Container ist mit role='region' ausgestattet, damit dieser leicht ansteuerbar ist.",
            "Die Komponente unterstützt die Navigation über die Tastatur mittels der Pfeiltasten (hoch/runter).",
        ]
    }


@register_component(Component.TABS)
def get_tabs_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the tabs component."""
    return {
        "a11y": [
            "Die Komponente Unterstützt Screenreader durch die entsprechenden Rollen: role='tablist', role='tab', role='tabpanel'.",
            "Zusätzlich werden die Tabs und deren Inhalte mittels aria-selected, aria-controls, aria-labelledby miteinander Verbunden.",
            "Der aktuell fokussierte Tab besitzt das Attribute tabindex='0' alle anderen tabindex='-1'.",
            "Die Komponente unterstützt die Navigation über die Tastatur mittels der Pfeil- (links/rechts) und Home/End-Tasten.",
        ]
    }


@register_component(Component.BUTTON)
def get_button_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the button component."""
    return {
        "a11y": [
            "Buttons welche lediglich ein Icon besitzen und keinen Text, sollten ein beschreibendes aria-label besitzen.",
            "Ein Button sollte so wie der Rest der Webseite, immer auch mit der Tastatur ansteuer- und bedienbar sein.",
            "Für die korrekten Einhaltung der Semantik, ist ein <button> einem interaktivem <div>-Container immer vorzuziehen.",
        ]
    }


@register_component(Component.INPUT_FIELD)
def get_input_field_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the input field component."""
    return {"a11y": ["Das <label> und der dazugehörige <input> sind mit for / id miteinander verknüpft."]}


@register_component(Component.CHECKBOX)
def get_checkbox_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the checkbox component."""
    return {"a11y": ["Das <label> und der dazugehörige <input> sind mit for / id miteinander verknüpft."]}


@register_component(Component.CHECKBOX_GROUP)
def get_checkbox_group_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the checkbox group component."""
    return {"a11y": ["Siehe Checkbox"]}


@register_component(Component.DROPDOWN)
def get_dropdown_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the dropdown component."""
    return {
        "a11y": [
            "Der Pfeil am Ende Dropdown-Buttons wird von Screenreadern mittels aria-hidden ignoriert, da dieser rein dekorativ ist.",
            "Icon welche in den Links bzw. Menüpunkten angezeigt werden, werden ebenfalls von Screenreadern ignoriert.",
            "TODO: Unterstützung für die Navigation mit den Pfeiltasten hinzufügen.",
        ]
    }


@register_component(Component.RADIO_GROUP)
def get_radio_group_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the radio_group component."""
    return {
        "a11y": [
            "Die Komponente unterstützt die Navigation über die Tastatur mittels der Pfeiltasten (hoch/runter, rechts/links).",
            "TODO: Fokus hervorheben.",
        ]
    }


@register_component(Component.RANGE_SLIDER)
def get_rangle_slider_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the range slider component."""
    return {
        "a11y": [
            "Das <label> und der dazugehörige <input> sind mit for / id miteinander verknüpft.",
            "Die Komponente unterstützt die Navigation über die Tastatur mittels der Pfeiltasten (hoch/runter, rechts/links).",
        ]
    }


@register_component(Component.TOGGLE)
def get_toggle_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the toggle component."""
    return {
        "a11y": [
            "Das <label> und der dazugehörige <input> sind mit for / id miteinander verknüpft.",
            "TODO: Fokus bei der Block-Variante hervorheben.",
        ]
    }


@register_component(Component.SELECT)
def get_select_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the select component."""
    return {
        "a11y": [
            "Das <label> und der dazugehörige <input> sind mit for / id miteinander verknüpft.",
            "Die Komponente unterstützt die Navigation über die Tastatur mittels der Pfeiltasten (hoch/runter).",
        ]
    }


@register_component(Component.MULTISELECT)
def get_multiselect_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the multiselect component."""
    return {
        "a11y": [
            "Das <label> und der dazugehörige <input> sind mit for / id miteinander verknüpft.",
            "Die Komponente Unterstützt Screenreader durch die entsprechenden ARIA-Attribute: role='combobox', aria-expanded', aria-selected'.",
            "Die Komponente unterstützt die Navigation über die Tastatur mittels der Pfeiltasten (hoch/runter).",
        ]
    }


@register_component(Component.CHAT)
def get_chat_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the chat component."""
    return {"a11y": ["Das <label> und der dazugehörige <input> sind mit for / id miteinander verknüpft."]}


@register_component(Component.ALERT)
def get_alert_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the alert component."""
    return {
        "a11y": [
            "Die Alert-Box besitzt das Attribute role='alert' für die Unterstützung eines Screenreader.",
            "Der Button zum Schließen ist mit der Tastatur ansteuerbar und besitzt ein entsprechendes aria-label.",
        ]
    }


@register_component(Component.MODAL)
def get_modal_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the modal component."""
    return {
        "a11y": [
            "Das Modal wird semantisch korrekt als Dialogfenster definiert, durch die Attribute role='dialog' und aria-modal='true'.",
            "Für Screenreader bietet das Modal einen Titel und eine (jedoch optionale) Beschreibung, welche mit aria-labelledby und aria-describedby verlinkt werden.",
            "Das Dialogfenster verwendet Focus-Trapping und besitzt ein Schließen-Button, um dieses auch per Tastatur verwenden zu können.",
        ]
    }


@register_component(Component.POPOVER)
def get_popover_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the popover component."""
    return {"a11y": ["TODO: Bedienbarkeit über die Tastatur hinzufügen!"]}


@register_component(Component.TOOLTIP)
def get_tooltip_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the tooltip component."""
    return {"a11y": ["TODO: Bedienbarkeit über die Tastatur hinzufügen!"]}


@register_component(Component.CODE_BLOCK)
def get_code_block_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the code block component."""
    return {"a11y": ["Die Komponente ist mit der Tastatur bedienbar."]}


@register_component(Component.DIFFERENTIATOR)
def get_differentiator_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the differentiator component."""
    return {"a11y": []}


@register_component(Component.PROGRESS_BAR)
def get_progress_bar_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the progress bar component."""
    return {"a11y": ["TODO"]}


@register_component(Component.GEO_MAP)
def get_geo_map_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the geo map component."""
    return {"a11y": ["TODO: leaflet.js a11y anwenden!"]}


@register_component(Component.CHART)
def get_charts_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the charts component."""
    return {"a11y": ["TODO: Apache EChart Web Accessibility anwenden!"]}


@register_component(Component.LIVE_CONTENT)
def get_live_content_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the live content component."""
    return {"a11y": ["TODO"]}


@register_component(Component.WEB_SOCKET)
def get_web_socket_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the web socket component."""
    return {"a11y": ["TODO"]}


@register_component(Component.INFINITE_SCROLL)
def get_infinite_scroll_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the infinite scroll component."""
    return {"a11y": ["TODO"]}


@register_component(Component.PAGINATION)
def get_pagination_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the pagination component."""
    return {
        "a11y": [
            "Die Tasten für die Erste Seite, Letzte Seite, etc. haben einen beschreibenden Text, welcher von Screenreadern vorgelesen wird und auch erklärt warum der Button in manchen Fällen deaktiviert ist.",
            "TODO: Unterstützung für Pfeiltasten-Navigation (rechts/links)",
        ]
    }


@register_component(Component.TABLE)
def get_table_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the table component."""
    return {"a11y": ["TODO"]}


@register_component(Component.GENERIC_FILTER)
def get_generic_filter_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the generic filter component."""
    return {"a11y": ["TODO"]}


@register_component(Component.SEARCH_BAR)
def get_search_bar_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the search bar component."""
    return {"a11y": ["Das Textinput-Feld besitzt ein extra Title ('Suche') für Screenreader."]}


@register_component(Component.QUERY_BUILDER)
def get_query_builder_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the query builder component."""
    return {"a11y": ["TODO"]}


@register_component(Component.CARD)
def get_card_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the card component."""
    return {"a11y": []}


@register_component(Component.CARD_CAROUSEL)
def get_card_carousel_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the card carousel component."""
    return {
        "a11y": [
            "Das Karussell ist mit der Tastatur steuerbar.",
            "TODO: Unterstützung für Pfeiltasten-Navigation (rechts/links)",
        ]
    }


@register_component(Component.IMAGE_CAROUSEL)
def get_image_carousel_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the image carousel component."""
    return {"a11y": ["Siehe Card Carousel"]}


@register_component(Component.THREE_D_CAROUSEL)
def get_3d_carousel_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the 3D carousel component."""
    return {"a11y": ["Das Karussell ist mit der Tastatur steuerbar."]}


@register_component(Component.TOGGLE_VIEW)
def get_toggle_view_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the toggle view component."""
    return {"a11y": ["Siehe Radio-Group"]}


@register_component(Component.FORM)
def get_form_a11y_context() -> dict[str, list[str]]:
    """Serve a11y documentation for the form component."""
    return {"a11y": []}
