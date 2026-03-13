from django.utils.translation import gettext as _

from insight_ui.component_details.component_context import register_component
from insight_ui.component_details.components import Component


@register_component(Component.PAGE_HEADER)
def get_page_header_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the page hader component."""
    return {
        "description": [
            _(
                "Die `Page-Header`-Komponente rendert den Seitenkopf innerhalb der blauen Kopfzeile des Base-Templates. Sie zeigt einen Titel und optional eine Beschreibung an."
            )
        ]
    }


@register_component(Component.ARTICLE)
def get_article_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the article component."""
    return {
        "description": [
            _(
                "Die Article-Komponente rendert Textinhalte im Zeitungsstil mit mehrspaltigen CSS-Columns. Der Text fließt automatisch von einer Spalte in die nächste."
            )
        ]
    }


@register_component(Component.HERO)
def get_hero_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the hero component."""
    return {
        "description": [
            _(
                "Die Hero-Komponente rendert einen prominenten Banner-Abschnitt mit Titel, Untertitel, Beschreibung und Call-to-Action Buttons."
            )
        ]
    }


@register_component(Component.NAVBAR)
def get_navbar_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the navbar component."""
    return {
        "description": [
            _(
                "Die navbar Komponente stellt eine anpassbare Navigationsleiste mit verschiedenen Komponenten zur Verfügung. Die Navigation ist fixiert am oberen Rand des Browserfenstern und bewegt sich beim nach unten Scrollen mit. Die Navigationsleiste besteht aus den folgenden Komponenten: "
            ),
            _(
                "Brand: Logo und Titel am linken Rand. Navigationslinks: Hauptnavigation, rechts neben dem Logo und Titel. Suchleiste: Eine optionale Suchleiste, rechts neben der Hauptnavigation. Login/Benutzermenü: Ein optionales, anpassbares Benutzermenü bzw. ein Anmeldebutton wenn der Nutzer nicht angemeldet ist. Sprachauswahl: Ein optionales Menü zum auswählen der Sprache, in welcher die Webseite angezeigt werden soll. Theme-Toggle Button: Ein optionaler Button zum wechseln wischen dem hellen und dem dunklen Design."
            ),
        ]
    }


@register_component(Component.SIDEBAR)
def get_sidebar_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the sidebar component."""
    return {
        "description": [
            _(
                "Die sidebar Komponente fügt einen Bereich an der Fensterseite hinzu. Die Sidebar kann sowohl auf der linken oder auf der rechten Seite sowie auch auf beiden Seiten gleichzeitig angewendet werden. Die Sidebar kann auch als Drawer verwendet werden, in diesem Fall kann sie geschlossen werden."
            )
        ]
    }


@register_component(Component.FOOTER)
def get_footer_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the footer component."""
    return {
        "description": [
            _(
                "Ein einfacher Footer bestehend aus drei Spalten mit anpassbaren Inhalt. Der Footer ist ein wichtiger Bestandteil einer jeden Webseite, er dient jedoch nicht nur dazu, die Webseite optisch abzuschließen. Er enthält i.d.R. mindestens eine Verlinkung zum Impressum und der Datenschutzerklärung. Oft befindet sich im Footer noch einmal eine Navigation zu den wichtigsten Seiten der Webseite und eine Copyright Angabe."
            )
        ]
    }


@register_component(Component.BREADCRUMBS)
def get_breadcrumb_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the breadcrumbs component."""
    return {
        "description": [
            _(
                "Breadcrumbs sind eine sekundäre Navigation, welche dazu verwendet werden, dem Nutzer Klarheit über die hierarchische Struktur einer Webseite zu verschaffen. Dies ist vor allem bei Webseiten mit einer tiefen Struktur, also mit vielen Unterseiten sinnvoll. Webseiten mit einer Tiefe von maximal zwei Stufen bspw. Übersicht -> Produkt Details sollten auf Breadcrumbs verzichten."
            ),
            _(
                "Für eine gute Konsistenz sollten Breadcrumbs, wenn sie verwendet werden, überall verwendet werden und nicht nur sporadisch."
            ),
        ]
    }


@register_component(Component.STEP_BAR)
def get_step_bar_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the step bar component."""
    return {
        "description": [
            _(
                "Diese Komponente kann dazu verwendet werden, dem Nutzer den Fortschritt eines manuellen Prozesses anzuzeigen. Damit ist zum Beispiel ein typischer Bezahlvorgang gemeint. Dieser besteht i.d.R. aus mehreren Schritten, wie die Adresse anzugeben, eine Zahlungsmethode auszuwählen und im Anschluss nochmal die Eingaben zu überprüfen. Die Komponente zeigt dem Nutzer an, wo er sich gerade befindet und wie viele Schritte noch folgen."
            )
        ]
    }


@register_component(Component.MINIMAL_STEP_BAR)
def get_minimal_step_bar_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the minimal step bar component."""
    return {
        "description": [
            _(
                "Mit der minimal_step_bar Komponente lässt sich der Fortschritt in einem mehrstufigen Prozess auf einem simple Art und Weise, graphisch darstellen."
            )
        ]
    }


@register_component(Component.BULLET_POINT_LIST)
def get_bullet_point_list_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the bullet point list component."""
    return {
        "description": [
            _(
                "Die bullet_point_list Komponente kann dazu verwendet werden, eine Abfolge von Tasks, Prozessschritten, o.ä darzustellen. Die einzelnen Schritte können eine Verlinkung enthalten, um diese beispielsweise mit einer konkreten Seite für jeden Tasks, o.ä. zu verlinken."
            )
        ]
    }


@register_component(Component.ACCORDION)
def get_accordion_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the accordion component."""
    return {
        "description": [
            _(
                "Mit der accordion Komponente lassen sich ausklappbare Bereiche für weitere Informationen hinzufügen. Ein Accordion kann entweder ein oder mehrere Bereiche gleichzeitig geöffnet haben. Beim öffnen eines Accordion-Abschnitts wird automatisch ein URL-Anchor gesetzt. Dadurch lassen sich über die URL bestimmte Bereiche beim aufrufen der Seite automatisch aufklappen und die Ansicht scrollt automatisch bis zu dem geöffneten Bereich."
            )
        ]
    }


@register_component(Component.TABS)
def get_tabs_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the tabs component."""
    return {
        "description": [
            _(
                "Mit der tabs Komponente lassen sich Tabs bzw. Registrierkarten hinzufügen. Diese Komponente besteht aus einer Reihe von Buttons, welche per HTMX-Request den Hauptinhalt der Komponente austauschen. Dadurch kann zwischen den einzelnen Tabs gewechselt werden, ohne dass die Seite neu geladen werden muss."
            )
        ]
    }


@register_component(Component.BUTTON)
def get_button_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the button component."""
    return {
        "description": [
            _(
                "Für einen gewöhnlichen Button stellt unser UI-Framework eine Reihe von CSS-Klassen zur Verfügung. Damit lassen sich Buttons für unterschiedliche Szenarien ohne großen Aufwand mit gängigen CSS-Klassen einbauen."
            )
        ]
    }


@register_component(Component.INPUT_FIELD)
def get_input_field_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the input field component."""
    return {"description": [_("Mit der input_field Komponente lassen sich einzelne <input>-Elemente einbauen.")]}


@register_component(Component.CHECKBOX)
def get_checkbox_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the checkbox component."""
    return {
        "description": [
            _(
                "Mit der checkbox Komponente lassen sich einzelne Checkbox-Elemente einbauen. Für eine Gruppe von miteinander verbundenen Checkbox-Elementen siehe Checkbox-Group."
            )
        ]
    }


@register_component(Component.CHECKBOX_GROUP)
def get_checkbox_group_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the checkbox group component."""
    return {
        "description": [
            _(
                "Mit der checkbox_group Komponente lassen sich Gruppen von Checkbox-Elementen einbauen, welche miteinander verknüpft sind. Das erlaubt es eine Beschränkung einzuschalten, welche es zum Beispiel nicht erlaubt, dass kein Checkbox-Element ausgewählt ist."
            )
        ]
    }


@register_component(Component.DROPDOWN)
def get_dropdown_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the dropdown component."""
    return {
        "description": [
            _(
                "Ein Dropdown-Menü bietet die Möglichkeit eine Gruppe von Buttons in einem sich ein- und ausklappbaren Menü zu verstauen. Das ist immer dann sehr nützlich, wenn entweder nur wenig Platz zu Verfügung steht oder die Anzahl der Elemente sonst zu groß und unübersichtlich wäre."
            ),
            _(
                "Bei der Verwendung von Dropdown-Menüs ist dennoch zu beachten, das diese nicht überladen werden. In der Regel sollte ein Menü nicht mehr als sieben Elemente besitzen und auch verschachtelte Menüs, also ein Dropdown-Menü in einem Dropdown-Menü sollten vermieden werden."
            ),
        ]
    }


@register_component(Component.RADIO_GROUP)
def get_radio_group_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the radio_group component."""
    return {
        "description": [
            _(
                "Mit der radio_group Komponente lassen sich Gruppen von Radio-Buttons einbauen. Bei der radio_group Variante handelt es sich um eine Variante mit normalen Radio-Buttons für ein Formular o.ä.."
            )
        ]
    }


@register_component(Component.RADIO_BLOCK)
def get_radio_group_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the radio_block component."""
    return {
        "description": [
            _(
                "Mit der radio_block Komponente lassen sich Gruppen von Radio-Buttons einbauen. Die radio_block Variante der Radio-Buttons wird als Block von Buttons dargestellt und kann dazu verwendet werden, einen Request beim wechsel des ausgewählten Wertes zu starten."
            )
        ]
    }


@register_component(Component.RANGE_SLIDER)
def get_rangle_slider_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the range slider component."""
    return {
        "description": [
            _(
                "Mit der slider-Komponente kann ein Range-Slider in das Frontend eingebaut werden, mit welchem sich ein Wert innerhalb eines begrenzten Intervall auswählen lässt."
            )
        ]
    }


@register_component(Component.TOGGLE)
def get_toggle_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the toggle component."""
    return {
        "description": [
            _(
                "Mit der toggle Komponente lässt sich ein Toggle-Button einbauen. Dieser funktioniert im Grunde wie eine einzelne Checkbox."
            )
        ]
    }


@register_component(Component.SELECT)
def get_select_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the select component."""
    return {"description": [_("Die select Komponente stellt eine einfache Auswahlbox zur Verfügung.")]}


@register_component(Component.MULTISELECT)
def get_multiselect_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the multiselect component."""
    return {
        "description": [
            _(
                "Die multiselect Komponente stellt eine Auswahlbox zur Verfügung, welche die Auswahl mehrere Werte erlaubt. Zusätzlich hat das Multiselect eine Suchleiste integriert um schnell nach bestimmten Werten suchen zu können."
            )
        ]
    }


@register_component(Component.CHAT)
def get_chat_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the chat component."""
    return {
        "description": [
            _(
                "Die Chat Komponente bietet ein einfaches Frontend für eine Chat-Anwendung. Die Komponente besteht aus einem Text-Input und einem Bereich für die Nachrichten. Der Inhalt des Nachrichtenbereichs wird mittels HTMX bei jedem Response erweitert, ohne dass die Seite neu geladen wird."
            )
        ]
    }


@register_component(Component.ALERT)
def get_alert_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the alert component."""
    return {
        "description": [
            _(
                "Die Alert-Komponente bietet eine Möglichkeit, Benutzern wichtige Informationen, Warnungen oder Erfolgsmeldungen anzuzeigen."
            )
        ]
    }


@register_component(Component.MODAL)
def get_modal_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the modal component."""
    return {
        "description": [
            _(
                "Mit der Modal Komponente lassen sich anpassbare Dialoge einbauen. Diese können verwendet werden um dem Nutzer zusätzliche Informationen anzuzeigen oder als Bestätigungsdialoge für diverse Aktionen verwendet werden."
            )
        ]
    }


@register_component(Component.POPOVER)
def get_popover_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the popover component."""
    return {
        "description": [
            _(
                "In manchen Fällen ist es notwendig weitere jedoch eher optionale Informationen anzuzeigen, welche jedoch das gesamtbild stören würden oder für welche einfach nicht genug Platz vorhanden ist. Für diesen Fall sind _Popover_ eine nützliche Komponente. Ähnlich wie ein _Tooltip_ werden auch Popover getrennt vom restlichen Layout dargestellt und stören insofern nicht den Fluss des Layouts. Bei einem Popover handelt es sich um eine Bereich für zusätzliche Informationen, welcher nur angezeigt wird, wenn der Nutzer sich mit dem Mauszeiger über einem bestimmten Element befindet. Im gegensatz zum Tooltip, kann der Nutzer mit dem Mauszeiger auf das Popover gehen, ohne das dieses sich schließt. Dadurch können mit einem Popover auch interaktive Elemente angezeigt werden."
            ),
            _(
                "Wenn nur ein kurzer Informationstext angezeigt werden soll, um ein Element mit ein, zwei Wörter zu erklären, sollte stattdessen die Tooltip-Komponente verwendet werden."
            ),
        ]
    }


@register_component(Component.TOOLTIP)
def get_tooltip_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the tooltip component."""
    return {
        "description": [
            _(
                "Manchmal ist die Beschriftung oder das Icon eines Buttons o.ä. nicht eindeutig genug und lässt Raum für Interpretationen, was im schlimmsten Fall zu Verwirrung führen kann. In solchen Fällen ist es hilfreich und wichtig, zusätzliche Informationen anzuzeigen. Um nicht den Fluss der Weboberfläche zu stören, eignen sich _Tooltips_. Diese werden nur angezeigt, wenn der Nutzer sich mit dem Mauszeiger über dem entsprechenden Element befindet. Der Tooltip wird getrennt wom restlichen Layout über allen anderen Elementen angezeigt und ist damit immer sichtbar und stört nicht das gesamtbild."
            ),
            _(
                "Ein Tooltip sollte nur für kurze Informationstexte (meist nur ein Wort) verwendet werden, wenn mehr Informationen angezeigt werden sollen, sollte stattdessen die Popover-Komponente verwendet werden."
            ),
        ]
    }


@register_component(Component.CODE_BLOCK)
def get_code_block_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the code block component."""
    return {
        "description": [
            _(
                "Diese Komponente bietet die Möglichkeit, Quellcode mit Syntax-Highlighting darzustellen. Darüber hinaus gibt es Möglichkeit, den dargestellten Quellcode, über einen Button in den Zwischenspeicher zu kopieren. Das Syntax-Highlighting umfasst so ziemlich alle gängigen und auch die meisten nicht sehr geläufigen Programmiersprachen."
            )
        ]
    }


@register_component(Component.DIFFERENTIATOR)
def get_differentiator_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the differentiator component."""
    return {
        "description": [
            _(
                "Mit dem Differentiator lassen sich Unterschiede zwischen zwei Texten grafisch darstellen, was vor allem bei längeren Texten mit nur kleinen Änderungen, eine sehr gute Hilfe bieten kann. Für Texte welche sich mehr oder weniger komplett voneinander unterscheiden, ist diese Komponente wahrscheinlich weniger nützlich."
            )
        ]
    }


@register_component(Component.PROGRESS_BAR)
def get_progress_bar_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the progress bar component."""
    return {
        "description": [
            _(
                "Die progress_bar Komponente wird dafür verwendet dem Nutzer den Fortschritt eines im Hintergrund laufenden Prozesses visuell darzustellen. Ein gängiges Szenario für solche Komponenten sind zum Beispiel Downloads."
            ),
            _(
                "Für eine Fortschrittsanzeige wo der Fortschritt durch aktives Zutun des Nutzers entsteht, eignet sich unsere Step Bar Komponente."
            ),
        ]
    }


@register_component(Component.GEO_MAP)
def get_geo_map_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the geo map component."""
    return {
        "description": [
            _(
                "Mit der geo_map Komponente wird eine geografische Karte mittels leaflet dargestellt. Auf dieser lassen sich mühelos geografische Informationen darstellen."
            )
        ]
    }


@register_component(Component.CHART)
def get_charts_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the charts component."""
    return {
        "description": [
            _(
                "Mit der chart Komponente können ohne JavaScript anpassen zu müssen, Diagramme dargestellt werden. Die Komponente verwendet intern Apache ECharts."
            ),
            _(
                "Die Komponente steht bisher in den folgenden Ausführungen zu Verfügung: line_chart: Ein Linien-Diagramm. bar_chart: Ein Stacked Balken-Diagramm."
            ),
        ]
    }


@register_component(Component.LIVE_CONTENT)
def get_live_content_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the live content component."""
    return {
        "description": [
            _(
                "Die live_content Komponente aktualisiert ein Fragment regelmäßig mithilfe von HTMX-Abfragen. Sie eignet sich ideal für Dashboards oder Statusansichten, die häufig aktualisiert werden müssen, ohne dass die gesamte Seite neu geladen werden muss."
            )
        ]
    }


@register_component(Component.WEB_SOCKET)
def get_web_socket_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the web socket component."""
    return {
        "description": [
            _(
                "Mit der websocket kann eine Verbindung mit einem anderen Websocket aufgebaut werden, um automatisch Daten zu empfangen. Die empfangenen Daten werden mittels HTMX in dem Container der Komponente eingesetzt. Es wird kein Neuladen der Seite oder irgendeine andere Form von Interaktion benötigt."
            )
        ]
    }


@register_component(Component.INFINITE_SCROLL)
def get_infinite_scroll_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the infinite scroll component."""
    return {
        "description": [
            _(
                "Die infinite_scroll Komponente stellt eine Alternative zu einer Pagination dar und kann dazu verwendet werden, eine große Menge Daten darzustellen. Anstatt von Seite zu Seite zu wechseln, lädt der Infinite Scroll nach dem ein bestimmter Schwellwert beim Scrollen erreicht wurde, weitere Daten aus dem Backend und fügt diese mittels HTMX an das Ende an."
            ),
            _(
                "Die Komponente wird in zwei Varianten zur Verfügung gestellt, eine mit automatischer Erweiterung und eine zweite, wobei zum Laden neuer Elemente aktiv ein Button Lade weitere geklickt werden muss."
            ),
        ]
    }


@register_component(Component.PAGINATION)
def get_pagination_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the pagination component."""
    return {
        "description": [
            _(
                "Mit der pagination Komponente lässt sich eine Liste auf mehrere Seiten aufteilen, welche mittels der durch diese Komponente dargestellte Pagination am Ende der Liste gewechselt werden kann. Dies ist praktisch für große Datenmengen und bietet eine alternative zur infinite_scroll Komponente."
            )
        ]
    }


@register_component(Component.TABLE)
def get_table_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the table component."""
    return {
        "description": [
            _(
                "Mit der table Komponente lässt sich eine einfache Tabelle für beliebige Daten darstellen. Das Layout ist responsive Gestaltet, sollte der Platz nicht ausreichen wird eine horizontale Scrollbar eingeblendet."
            )
        ]
    }


@register_component(Component.GENERIC_FILTER)
def get_generic_filter_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the generic filter component."""
    return {
        "description": [
            _(
                "Mit der generic_filter Komponente lassen sich relativ einfach standard Filter, bestehend aus <select>-Tags, bauen. Der Filter macht bei einer Änderung automatisch einen Request an den entsprechenden Endpunkt und aktualisiert den Datenbereich mittels HTMX."
            ),
            _("Eine alternative hierzu stellt der flexiblere, aber auch kompliziertere Query Builder dar."),
        ]
    }


@register_component(Component.SEARCH_BAR)
def get_search_bar_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the search bar component."""
    return {
        "description": [
            _(
                "Ein einfaches Textinput-Feld mit einem großen Button am rechten Ende. Beim absenden wird ein Request an den angegebenen Endpunkt geschickt. Die search_bar Komponente unterstützt auch HTMX Requests."
            )
        ]
    }


@register_component(Component.QUERY_BUILDER)
def get_query_builder_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the query builder component."""
    return {
        "description": [
            _("Diese Komponente stellt eine Alternative zur Generic Filter Komponente dar."),
            _(
                "Der Query Builder ist weitaus flexibler aber auch komplexer in der Nutzung als übliche Filter Methoden. Der Query Builder ist im Grunde eine Art grafische Darstellung einer SQL-Query. Der Query Builder bekommt eine Liste der Modell-Felder in welchen gesucht werden kann und zu jedem Feld eine Liste der erlaubten Operationen. Bspw.: { 'field': 'name', 'type': 'text', 'operations': ['iexact', 'icontains']}."
            ),
            _(
                "In speziellen Fällen können auch wie bei der anderen Variante, vordefinierte Werte angegeben werden. Dieser Aspekt macht diese Art der Filterung, u.u. wesentlich flexibler, da auf fest definierte Werte verzichtet wird."
            ),
            _(
                "Ähnlich wie bei der anderen Filter Variante, wird hier auch lediglich ein Dictionary mit den gewünschten Eigenschaften benötigt."
            ),
        ]
    }


@register_component(Component.CARD)
def get_card_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the card component."""
    return {
        "description": [
            _(
                "Die card Komponenten werden dazu verwendet Informationsgruppen zu erstellen. Jede Karte besteht aus einer Überschrift und ihren Hauptinhalt. Dazu gibt es noch weitere Optionen, wie ein Hintergrundbild oder ein Untertitel und Aktion-Buttons."
            ),
            _(
                "Für die Card Komponente gibt es unterschiedliche Varianten zur Auswahl: Card: Standard Karte im 16:9 Format. App Card: Das Layout dieser Karte ist vertikal ausgerichtet wodurch dieses länger ist. Flip Card: Diese Karte dreht sich um 180° und hält auf ihrer Rückseite weiteren Inhalt bereit."
            ),
        ]
    }


@register_component(Component.CARD_CAROUSEL)
def get_card_carousel_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the card carousel component."""
    return {
        "description": [
            _(
                "Mit der carousel Komponente können Bilder, aber auch alle möglichen anderen Sachen, Platzsparend und interaktiv angezeigt werden und es befindet sich immer ein Objekt im Fokus. Daher eignet sich die Komponente vor allem für Bilder."
            )
        ]
    }


@register_component(Component.IMAGE_CAROUSEL)
def get_image_carousel_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the image carousel component."""
    return {
        "description": [
            _(
                "Die image_carousel Komponente ist eine auf die Darstellung von Bildern angepasste Variante der carousel Komponente."
            )
        ]
    }


@register_component(Component.THREE_D_CAROUSEL)
def get_3d_carousel_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the 3D carousel component."""
    return {
        "description": [
            _(
                "Mit der three_d_carousel Komponente können beliebige Inhalte auf einzigartige Weise dargestellt werden. Die Inhalte werden in einem Kreis angeordnet dargestellt."
            )
        ]
    }


@register_component(Component.TOGGLE_VIEW)
def get_toggle_view_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the toggle view component."""
    return {
        "description": [
            _(
                "Die toggle-view Komponente kombiniert die Tabellen und die Karten-Ansicht, sowie die Karussell-Komponente. Die Komponente wird dazu verwendet, die selben Daten auf komplett unterschiedliche Art und Weise darzustellen."
            )
        ]
    }


@register_component(Component.FORM)
def get_form_description_context() -> dict[str, list[str]]:
    """Serve description documentation for the form component."""
    return {
        "description": [
            _("Mit der form Komponente lässt sich ohne selbst HTML-Code editieren zu müssen, Formulare bauen.")
        ]
    }
