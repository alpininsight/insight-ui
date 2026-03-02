from dataclasses import dataclass

from insight_ui.component_details.component_context import component


@dataclass
class ParameterDetails:
    """Describes a component parameter, with a 'name', 'type', 'description' and the 'default' value."""

    name: str
    type: str
    description: str
    default: str


@dataclass
class ParameterDoc:
    """Represents the documentation of a component parameter."""

    details: ParameterDetails
    params_table: list[ParameterDetails]
    example_data: str


@component("page_header")
def get_page_header_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the page_header component."""
    main_params = [
        ParameterDetails("title", "str", "Der Titel der Seite, wird als h1 in weißer Schrift angezeigt.", "''"),
        ParameterDetails("description", "str", "Eine optionale Beschreibung unterhalb des Titels.", "''"),
    ]

    return {"params": [main_params]}


@component("article")
def get_article_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the article component."""
    main_params = [
        ParameterDetails("content", "str", "Der Textinhalt des Artikels (kann HTML enthalten).", "''"),
        ParameterDetails("columns", "int", "Die Anzahl der Spalten für das CSS-Columns-Layout.", "2"),
        ParameterDetails("column_gap", "str", "Der Abstand zwischen den Spalten (CSS-Einheit).", "'2rem'"),
        ParameterDetails("title", "str", "Ein optionaler Titel über dem Artikel.", "''"),
    ]

    return {"params": [main_params]}


@component("hero")
def get_hero_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the hero component."""
    cta_param = ParameterDoc(
        ParameterDetails("cta_primary", "dict[str, str]", "Primärer 'Call-to-Action' Button", "{}"),
        [
            ParameterDetails("url", "str", "URL, welche beim klick des Buttons aufgerufen werden soll.", "''"),
            ParameterDetails("text", "str", "Beschriftung des Buttons.", "''"),
        ],
        """
            {"url": "/newsletter", "content": "Subscribe to Newsletter"}
        """,
    )

    badge_param = ParameterDoc(
        ParameterDetails("badge", "dict[str, str]", "Eine Badge mit Icon und Text.", "{}"),
        [
            ParameterDetails("text", "str", "Beschriftung des Badge.", "''"),
            ParameterDetails(
                "icon", "dict[str, str]", "Ein optionales Icon, welches vor dem Text angezeigt wird.", "{}"
            ),
        ],
        """
            {"url": "/newsletter", "content": "Subscribe to Newsletter"}
        """,
    )

    main_params = [
        ParameterDetails("title", "str", "Titel der Hero-Section.", "''"),
        ParameterDetails(
            "subtitle", "int", "Untertitel der Hero-Section, welche unter dem Titel angezeigt wird.", "''"
        ),
        ParameterDetails(
            "description",
            "str",
            "Beschreibung der Hero-Section, welche unter dem Titel zw. Untertitel angezeigt wird.",
            "''",
        ),
        cta_param.details,
        ParameterDetails("cta_secondary", "dict[str, str]", "Sekundärer 'Call-to-Action' Button", "{}"),
        ParameterDetails("background_image_url", "str", "URL des Hintergrundbildes.", "''"),
        badge_param.details,
    ]

    return {"params": [main_params, cta_param, badge_param]}


@component("navbar")
def get_navbar_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the navbar component."""
    logo_param = ParameterDoc(
        ParameterDetails(
            "logo", "dict[str, str]", "Beschreibt das Logo, welches neben dem Titel angezeigt wird.", "{}"
        ),
        [
            ParameterDetails("url", "str", "Pfad zu der Logo Datei für das helle Theme.", "insight_ui/svg/ai-logo.svg"),
            ParameterDetails(
                "url_dark", "str", "Pfad zu der Logo Datei für das dunkle Theme.", "insight_ui/svg/ai-logo-dark.svg"
            ),
            ParameterDetails("alt", "str", "Alternativtext des Logos.", "Insight UI Logo"),
            ParameterDetails("height", "str", "Dieser Wert bestimmt die Größe des Logos.", "2rem"),
        ],
        """""",
    )

    brand_param = ParameterDoc(
        ParameterDetails(
            "brand", "dict[str, Any]", "Beschreibt den Titel und das Logo der Anwendung in der Navbar.", "{}"
        ),
        [
            ParameterDetails("title", "str", "Der Titel der Anwendung.", "''"),
            ParameterDetails(
                "view_name", "str", "Name der URL welche beim klick auf den Titel aufgerufen werden soll.", "''"
            ),
            ParameterDetails(
                "gap", "str", "Dieser Wert bestimmt den Abstand zwischen dem Logo und dem Titel.", "0.5rem"
            ),
            logo_param.details,
        ],
        """""",
    )

    links_param = ParameterDoc(
        ParameterDetails("links", "list[dict]", "Enthält/Beschreibt die Navigationspunkte der Navbar.", "[]"),
        [
            ParameterDetails("text", "str", "Beschriftung des Links.", "''"),
            ParameterDetails(
                "icon", "dict[str, str]", "Ein optionales Icon, welches vor dem Text angezeigt wird.", "{}"
            ),
            ParameterDetails(
                "view_name", "str", "Name der URL welche beim Klick auf den Link aufgerufen werden soll.", "''"
            ),
            ParameterDetails(
                "open_modal", "str", "ID des Modal-Dialogs welche beim Klick auf den Link angezeigt werden soll.", "''"
            ),
            ParameterDetails(
                "active",
                "bool",
                "Hebt den Link stilistisch von den anderen ab um zu zeigen, dass der Nutzer auf der entsprechenden Seite ist.",
                "True",
            ),
            ParameterDetails("need_auth", "bool", "Der Link wird nur für angemeldete Nutzer angezeigt.", "False"),
            ParameterDetails("staff_only", "bool", "Der Link wird nur für Administratoren angezeigt.", "False"),
        ],
        """""",
    )

    config_param = ParameterDoc(
        ParameterDetails(
            "config", "dict[str, Any]", "Ein Dictionary mit der gesamten Konfiguration der Navigationsleiste.", "{}"
        ),
        [
            brand_param.details,
            links_param.details,
            ParameterDetails(
                "searchbar_request_view",
                "str",
                "Name der URL welche bei der Suche aufgerufen werden soll (wenn leer wird keine Suchzeile angezeigt).",
                "''",
            ),
            ParameterDetails(
                "show_usermenu", "bool", "Zeigt ein Dropdown-Menü mit mindestens einem Logout-Button.", "False"
            ),
            ParameterDetails(
                "show_language_selector",
                "bool",
                "Zeigt ein Dropdown-Menü zum Auswählen der Anzeigesprache (sofern definiert).",
                "False",
            ),
            ParameterDetails(
                "show_theme_toggle",
                "bool",
                "Zeigt ein Button zum wechsel zwischen der hellen und der dunklen Darstellung der Seite.",
                "False",
            ),
        ],
        """
        {
            "brand": {
                "title": "Insight UI",
                "view_name": "storybook_view",
                "gap": "0.5rem",
                "logo": {
                    "url": "insight_ui/svg/ai-logo.svg",
                    "url_dark": "insight_ui/svg/ai-logo-dark.svg",
                    "alt": "Insight UI Logo",
                    "height": "2rem",
                },
            },
            "links": [
                {
                    "text": _("Startseite"),
                    "icon": {"name": "home", "size": "small"},
                    "view_name": "storybook_view",
                    "active": True,
                    "need_auth": False,
                    "staff_only": False,
                },
                {
                    "text": _("Über"),
                    "open_modal": "about-modal",
                    "active": False,
                    "need_auth": False,
                    "staff_only": False,
                },
            ],
            "searchbar_request_view": "search_view",
            "show_usermenu": True,
            "show_language_selector": True,
            "show_theme_toggle": True,
        }
        """,
    )

    main_params = [
        config_param.details,
        ParameterDetails(
            "user", "User", "Das <i>user</i> Objekt des Requests (i.d.R. über <i>request.user</i> verfügbar).", "None"
        ),
        ParameterDetails(
            "user_dropdown_links",
            "list",
            "Eine Liste mit den Links welche in dem Benutzermenü angezeigt werden sollen.",
            "[]",
        ),
        ParameterDetails(
            "show_login", "bool", "<b>True</b> wenn ein Button zum Anmelden angezeigt werden soll.", "false"
        ),
        ParameterDetails("search_query", "str", "Suchstring für die Suchleiste.", "''"),
    ]

    return {"params": [main_params, config_param, brand_param, logo_param, links_param]}


@component("sidebar")
def get_sidebar_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the sidebar component."""
    main_params = [
        ParameterDetails(
            "sidebar_data", "dict[str, Any]", "Inhalt der Sidebar (Titel und Navigations-Elemente).", "None"
        ),
        ParameterDetails("side", "str", "Bestimmt, auf welcher Seite die Sidebar platziert werden soll.", "right"),
        ParameterDetails("static", "bool", "<b>True</b> wenn die Sidebar nicht einklappbar sein soll.", "True"),
        ParameterDetails(
            "auto_close", "bool", "Bei <b>True</b> schließt sich die Sidebar sobald der Cursor diese verlässt.", "False"
        ),
        ParameterDetails(
            "mobile_hidden",
            "bool",
            "Bei <b>True</b> wird eine statische Sidebar auf einem kleineren Viewport ausgeblendet.",
            "False",
        ),
        ParameterDetails(
            "navbar_fixed",
            "bool",
            "Bei <b>True</b> wird die Position des Inhalts angepasst. (NUR FÜR CUSTOM-SIDEBAR!) ",
            "False",
        ),
    ]

    return {"params": [main_params]}


@component("footer")
def get_footer_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the footer component."""
    image_param = ParameterDoc(
        ParameterDetails(
            "image", "dict[str, str]", "Optionales Bild, welches unter dem Text der Beschreibung angezeigt wird.", "{}"
        ),
        [
            ParameterDetails("url", "str", "Pfad zu der Bilddatei für das helle Theme.", "insight_ui/svg/ai-logo.svg"),
            ParameterDetails(
                "url_dark", "str", "Pfad zu der Bilddatei für das dunkle Theme.", "insight_ui/svg/ai-logo-dark.svg"
            ),
            ParameterDetails("alt", "str", "Alternativtext des Logos.", "Insight UI Logo"),
            ParameterDetails("height", "str", "Dieser Wert bestimmt die Größe des Logos.", "2rem"),
        ],
        """""",
    )

    description_param = ParameterDoc(
        ParameterDetails("description", "dict[str, Any]", "Kurzbeschreibung der Anwendung mit optionalen Bild.", "{}"),
        [
            ParameterDetails("title", "str", "Überschrift der Beschreibung.", "''"),
            ParameterDetails("text", "str", "Kurze Zusammenfassung der Anwendung.", "''"),
            image_param.details,
        ],
        """""",
    )

    links_param = ParameterDoc(
        ParameterDetails("links", "list[dict[str, Any]]", "Liste der Hauptnavigationspunkte der Anwendung.", "[]"),
        [
            ParameterDetails("text", "str", "Beschriftung des Links.", "''"),
            ParameterDetails(
                "icon", "dict[str, str]", "Ein optionales Icon, welches vor dem Text angezeigt wird.", "{}"
            ),
            ParameterDetails(
                "view_name", "str", "Name der URL welche beim Klick auf den Link aufgerufen werden soll.", "''"
            ),
            ParameterDetails(
                "open_modal", "str", "ID des Modal-Dialogs welche beim Klick auf den Link angezeigt werden soll.", "''"
            ),
            ParameterDetails(
                "active",
                "bool",
                "Hebt den Link stilistisch von den anderen ab um zu zeigen, dass der Nutzer auf der entsprechenden Seite ist.",
                "True",
            ),
            ParameterDetails("need_auth", "bool", "Der Link wird nur für angemeldete Nutzer angezeigt.", "False"),
            ParameterDetails("staff_only", "bool", "Der Link wird nur für Administratoren angezeigt.", "False"),
        ],
        """""",
    )

    contact_param = ParameterDoc(
        ParameterDetails(
            "contact",
            "dict[str, Any]",
            "Kontaktinformationen, Link zum Impressum, Datenschutz und eine Kontaktmailadresse.",
            "{}",
        ),
        [
            ParameterDetails("mail_url", "str", "URL einer Kontaktmailadresse.", "''"),
            ParameterDetails("imprint", "str", "Verlinkung zu einem Impressum.", "''"),
            ParameterDetails("privacy", "str", "Verlinkung zu einer Datenschutzerklärung.", "''"),
        ],
        """""",
    )

    copyright_param = ParameterDoc(
        ParameterDetails(
            "copyright", "dict[str, str]", "Copyright Informationen, wie das Jahr und der geschützte Name.", "{}"
        ),
        [
            ParameterDetails("year", "int", "I.d.R das aktuelle Jahr (ist nicht zwingend erforderlich). ", "undefined"),
            ParameterDetails("app_name", "str", "Der geschützte Name der Anwendung.", "''"),
        ],
        """""",
    )

    data_param = ParameterDoc(
        ParameterDetails("data", "dict[str, Any]", "Daten welche im Footer angezeigt werden sollen.", "{}"),
        [description_param.details, links_param.details, contact_param.details, copyright_param.details],
        """""",
    )

    main_params = [data_param.details]

    return {
        "params": [main_params, data_param, description_param, image_param, links_param, contact_param, copyright_param]
    }


@component("breadcrumbs")
def get_breadcrumb_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the breadcrumb component."""
    links_param = ParameterDoc(
        ParameterDetails("items", "list[dict]", "Liste der Navigationspunkte.", "[]"),
        [
            ParameterDetails("text", "str", "Beschriftung des Links.", "''"),
            ParameterDetails(
                "icon", "dict[str, str]", "Ein optionales Icon, welches vor dem Text angezeigt wird.", "{}"
            ),
            ParameterDetails(
                "view_name", "str", "Name der URL welche beim Klick auf den Link aufgerufen werden soll.", "''"
            ),
            ParameterDetails(
                "query_params", "str", "Ein optionaler Parameter, falls die aufzurufende View einen benötigt.", "''"
            ),
        ],
        """""",
    )

    main_params = [links_param.details]

    return {"params": [main_params, links_param]}


@component("step_bar")
def get_step_bar_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the step bar component."""
    step_param = ParameterDoc(
        ParameterDetails("items", "list[dict]", "Liste der Prozessschritte.", "[]"),
        [
            ParameterDetails("title", "str", "Titel des Schritts.", "''"),
            ParameterDetails("description", "str", "Zusätzliche Beschreibung des Schritts unter dem Titel.", "''"),
            ParameterDetails("completed", "bool", "Zeigt statt der Schrittzahl ein Haken an.", "False"),
            ParameterDetails(
                "current", "bool", "Hebt den Titel farblich hervor und lässt den Text pulsieren.", "False"
            ),
        ],
        """""",
    )

    main_params = [step_param.details]

    return {"params": [main_params, step_param]}


@component("minimal_step_bar")
def get_minimal_step_bar_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the minimal step bar component."""
    config_param = ParameterDoc(
        ParameterDetails("config", "dict[str, Any]", "Konfiguration der Step Bar.", "{}"),
        [
            ParameterDetails(
                "items",
                "list[str]",
                "Liste der Zustände der Prozessschritte. Mögliche Werte: 'success', 'failed', 'active' und '' für Inaktiv. ",
                "[]",
            ),
            ParameterDetails(
                "step_count", "int", "(Nur wenn 'items' nicht gesetzt ist!) Anzahl der Prozessschritte.", "0"
            ),
            ParameterDetails(
                "current_step", "int", "(Nur wenn 'items' nicht gesetzt ist!) Aktueller Schritt des Prozesses.", "0"
            ),
            ParameterDetails("icon_size", "str", "Größe der Icons auf der Fortschrittsanzeige.", "xs"),
        ],
        """""",
    )

    main_params = [config_param.details]

    return {"params": [main_params, config_param]}


@component("bullet_point_list")
def get_bullet_point_list_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the bullet point list component."""
    step_param = ParameterDoc(
        ParameterDetails("items", "list[dict]", "Liste der einzelnen Punkte.", "[]"),
        [
            ParameterDetails("title", "str", "Titel des Schritts.", "''"),
            ParameterDetails("description", "str", "Zusätzliche Beschreibung des Schritts unter dem Titel.", "''"),
            ParameterDetails(
                "bullet_icon",
                "dict[str, str]",
                "Ein optionales Icon, welches statt dem normalen Punkt angezeigt wird.",
                "''",
            ),
            ParameterDetails(
                "bullet_text", "str", "Ein optionaler Text, welcher statt dem normalen Punkt angezeigt wird.", "''"
            ),
            ParameterDetails(
                "view_name",
                "str",
                "Name der URL welche beim Klick auf den jeweiligen Punkt aufgerufen werden soll.",
                "''",
            ),
            ParameterDetails("completed", "bool", "Zeigt statt dem Punkt ein Haken an.", "False"),
            ParameterDetails("current", "bool", "Hebt den Titel farblich hervor.", "False"),
        ],
        """""",
    )

    main_params = [step_param.details]

    return {"params": [main_params, step_param]}


@component("accordion")
def get_accordion_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the accordion component."""
    item_param = ParameterDoc(
        ParameterDetails("items", "list[dict]", "Liste der einzelnen Abschnitte.", "[]"),
        [
            ParameterDetails("title", "str", "Titel des Abschnitts.", "''"),
            ParameterDetails("content", "str", "Inhalt des Abschnitts.", "''"),
        ],
        """
        [
            {"title": "Was ist Django?", "content": "Django ist ein Web-Framework für Python."},
            {"title": "Was ist Tailwind?", "content": "Tailwind ist ein CSS-Utility-Framework."},
            {"title": "Was ist ARIA?", "content": "ARIA steht für Accessible Rich Internet Applications."},
        ]
        """,
    )

    main_params = [
        ParameterDetails("id", "str", "Eindeutige Tag-ID für die Identifizierung des Elements im JavaScript.", "''"),
        item_param.details,
        ParameterDetails(
            "exclusive", "bool", "Bei <b>True</b> kann immer nur ein Abschnitt gleichzeitig geöffnet sein.", "False"
        ),
    ]

    return {"params": [main_params, item_param]}


@component("tabs")
def get_tabs_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the tabs component."""
    tabs_param = ParameterDoc(
        ParameterDetails("tabs", "list[dict]", "Liste der Tab-Buttons.", "[]"),
        [
            ParameterDetails(
                "id", "str", "Eindeutige Tag-ID für die Identifizierung des Elements im JavaScript.", "''"
            ),
            ParameterDetails("url", "str", "Die URL welche beim Klick auf den Tab aufgerufen werden soll.", "''"),
            ParameterDetails("title", "str", "Beschriftung des Tab-Button.", "''"),
            ParameterDetails(
                "icon", "dict[str, str]", "Ein optionales Icon, welches vor der Beschriftung angezeigt wird.", "{}"
            ),
        ],
        """""",
    )

    config_param = ParameterDoc(
        ParameterDetails(
            "config",
            "dict[str, Any]",
            "Beschreibt die Buttons, welche zum wechseln der einzelnen Tabs verwendet werden.",
            "{}",
        ),
        [
            ParameterDetails(
                "id", "str", "Eindeutige Tag-ID für die Identifizierung des Elements im JavaScript.", "''"
            ),
            ParameterDetails(
                "label",
                "str",
                "Zusätzlicher, nicht sichtbarer Titel, welcher nur von Screenreadern vorgelesen wird.",
                "''",
            ),
            tabs_param.details,
        ],
        """""",
    )

    main_params = [config_param.details]

    return {"params": [main_params, config_param, tabs_param]}


@component("button")
def get_button_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the button component."""
    main_params = [ParameterDetails("", "", "", "")]

    return {"params": [main_params]}


@component("input_field")
def get_input_field_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the input field component."""
    main_params = [
        ParameterDetails(
            "tag_id", "str", "Optionale, eindeutige Tag-ID für die Identifizierung des Elements im JavaScript.", "''"
        ),
        ParameterDetails(
            "name",
            "str",
            "Wird für eine <span class='inline-tag'>&lt;form&gt;</span> benötigt, als Name des Request-Parameters.",
            "''",
        ),
        ParameterDetails(
            "input_type", "str", "Der Type des Input-Feldes bspw.: 'text', 'password', 'date', etc..", "''"
        ),
        ParameterDetails(
            "placeholder",
            "str",
            "Platzhalter Text, wird in dem Feld angezeigt, solange es nicht selektiert wurde.",
            "''",
        ),
        ParameterDetails("value", "str", "Der Wert des Input-Feldes.", "''"),
        ParameterDetails("minimum", "int", "Kleinster numerischer Wert (für input_type='number').", "undefined"),
        ParameterDetails("maximum", "int", "Größter numerischer Wert (für input_type='number').", "undefined"),
        ParameterDetails("min_length", "int", "Minimale Anzahl an Zeichen in einem Textfeld.", "undefined"),
        ParameterDetails("max_length", "int", "Maximale Anzahl an Zeichen in einem Textfeld.", "undefined"),
        ParameterDetails(
            "checked",
            "bool",
            "<b>True</b>, wenn <span class='inline-tag'>input_type='checkbox'</span> und die Checkbox ausgewählt sein soll.",
            "False",
        ),
        ParameterDetails("required", "bool", "<b>True</b> wenn das Feld ausgefüllt werden muss.", "False"),
        ParameterDetails("disabled", "bool", "<b>True</b>, wenn das Feld deaktiviert sein soll.", "False"),
        ParameterDetails("label", "str", "Ein Label-Text welcher über dem Input-Feld angezeigt wird.", "''"),
        ParameterDetails(
            "config",
            "dict[str, Any]",
            "Eine alternative Konfiguration mit Keys entsprechend den vorherigen Parametern.",
            "{}",
        ),
    ]

    return {"params": [main_params]}


@component("checkbox")
def get_checkbox_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the checkbox component."""
    main_params = [
        ParameterDetails(
            "tag_id", "str", "Optionale, eindeutige Tag-ID für die Identifizierung des Elements im JavaScript.", "''"
        ),
        ParameterDetails(
            "name",
            "str",
            "Wird für eine <span class='inline-tag'>&lt;form&gt;</span> benötigt, als Name des Request-Parameters.",
            "''",
        ),
        ParameterDetails(
            "value",
            "str",
            "Der Wert der Checkbox (Dabei handelt es sich nicht um den Zustand, siehe dafür 'checked').",
            "''",
        ),
        ParameterDetails("label", "str", "Ein Label-Text welcher über der Checkbox angezeigt wird.", "''"),
        ParameterDetails("checked", "bool", "<b>True</b>, wenn die Checkbox ausgewählt sein soll.", "False"),
        ParameterDetails("disabled", "bool", "<b>True</b>, wenn die Checkbox deaktiviert sein soll.", "False"),
        ParameterDetails(
            "config",
            "dict[str, Any]",
            "Eine alternative Konfiguration mit Keys entsprechend den vorherigen Parametern.",
            "{}",
        ),
    ]

    return {"params": [main_params]}


@component("checkbox_group")
def get_checkbox_group_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the checkbox group component."""
    config_param = ParameterDoc(
        ParameterDetails(
            "config", "dict[str, Any]", "Beschreibt die Checkbox Gruppe und die einzelnen Checkbox-Elemente.", "{}"
        ),
        [
            ParameterDetails(
                "name",
                "str",
                "Wird für eine <span class='inline-tag'>&lt;form&gt;</span> benötigt, als Name des Request-Parameters.",
                "''",
            ),
            ParameterDetails("label", "str", "Label-Text welcher über den Checkbox-Elementen angezeigt wird.", "''"),
            ParameterDetails(
                "as_row",
                "bool",
                "<b>True</b>, wenn die Checkbox-Elemente nebeneinander angezeigt werden sollen.",
                "False",
            ),
            ParameterDetails(
                "minimum_checked",
                "int",
                "Anzahl der Checkbox-Elemente welche mindestens ausgewählt sein müssen.",
                "undefined",
            ),
            ParameterDetails(
                "maximum_checked",
                "int",
                "Anzahl der Checkbox-Elemente welche gleichzeitig ausgewählt sein dürfen.",
                "undefined",
            ),
            ParameterDetails("items", "list[dict[str, Any]]", "Liste der Checkbox-Elemente.", "[]"),
        ],
        """""",
    )

    main_params = [config_param.details]

    return {"params": [main_params, config_param]}


@component("dropdown")
def get_dropdown_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the dropdown component."""
    item_param = ParameterDoc(
        ParameterDetails("items", "list[dict[str, Any]]", "Eine Liste der Menüelemente.", "[]"),
        [
            ParameterDetails("text", "str", "Beschriftung des Dropdown-Elements.", "''"),
            ParameterDetails(
                "view_name",
                "str",
                "Name der URL welche beim Klick auf den jeweiligen Punkt aufgerufen werden soll.",
                "''",
            ),
            ParameterDetails(
                "icon", "dict[str, str]", "Ein optionales Icon, welches vor der Beschriftung angezeigt wird.", "{}"
            ),
        ],
        """""",
    )

    dropdown_menu_param = ParameterDoc(
        ParameterDetails(
            "dropdown_menu", "dict[str, Any]", "Beschreibt den Dropdown-Button und die Menüelemente.", "{}"
        ),
        [
            ParameterDetails(
                "tag_id",
                "str",
                "Optionale, eindeutige Tag-ID für die Identifizierung des Elements im JavaScript.",
                "''",
            ),
            ParameterDetails("title", "str", "Beschriftung des Dropdown-Buttons.", "''"),
            ParameterDetails("show_arrow", "bool", "<b>True</b> zeigt einen Pfeil hinter em Titel an.", "False"),
            item_param.details,
        ],
        """""",
    )

    main_params = [dropdown_menu_param.details]

    return {"params": [main_params, dropdown_menu_param, item_param]}


@component("radio_group")
def get_radio_group_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the radio_group component."""
    items_param = ParameterDoc(
        ParameterDetails("items", "list[dict[str, Any]]", "Eine Liste der Radio-Elemente.", "[]"),
        [
            ParameterDetails(
                "tag_id",
                "str",
                "Optionale, eindeutige Tag-ID für die Identifizierung des Elements im JavaScript.",
                "''",
            ),
            ParameterDetails("value", "str", "Wert des jeweiligen Radio-Buttons.", "''"),
            ParameterDetails("text", "str", "Beschriftung des jeweiligen Radio-Buttons.", "''"),
            ParameterDetails(
                "icon",
                "dict[str, str]",
                "Optionales Icon, welches vor der Beschriftung angezeigt wird (nur für die Radio-Block Variante).",
                "{}",
            ),
            ParameterDetails("disabled", "bool", "<b>True</b>, wenn der Radio-Button deaktiviert sein soll.", "False"),
        ],
        """""",
    )

    config_param = ParameterDoc(
        ParameterDetails(
            "config", "dict[str, Any]", "Beschreibt die Radio-Button Gruppe und die einzelnen Radio-Elemente.", "{}"
        ),
        [
            ParameterDetails(
                "name", "str", "Optionale, eindeutige Tag-ID für die Identifizierung des Elements im JavaScript.", "''"
            ),
            ParameterDetails("label", "str", "Ein Label-Text welcher über den Radio-Elementen angezeigt wird.", "''"),
            ParameterDetails(
                "as_row", "bool", "<b>True</b>, wenn die Radio-Elemente nebeneinander angezeigt werden sollen.", "False"
            ),
            items_param.details,
        ],
        """""",
    )

    main_params = [
        config_param.details,
        ParameterDetails("current_value", "str", "Der Wert des aktuell ausgewählten Radio-Buttons.", "''"),
        # Block only
        ParameterDetails(
            "view_name",
            "str",
            "Name der URL an welchen der Request beim Klick auf einen der Radio-Button, gesendet werden soll.",
            "''",
        ),
        ParameterDetails(
            "query_params",
            "str",
            "Ein String von Query-Parametern, welche bei dem Request mit gesendet werden sollen.",
            "''",
        ),
        ParameterDetails(
            "target_id",
            "str",
            "Die ID des HTML-Tags, welches bei wechseln des Radio-Buttons ausgetauscht werden soll.",
            "''",
        ),
        ParameterDetails(
            "method",
            "str",
            "Name der JavaScript Methode welche beim Klick auf einen der Radio-Button ausgeführt werden soll.",
            "''",
        ),
        ParameterDetails(
            "integrated",
            "bool",
            "<b>True</b> wenn sich die Gruppe in einer &lt;form&gt; befindet, bei <b>False</b> bekommt die Gruppe ihre eigene &lt;form&gt;.",
            "False",
        ),
    ]

    return {"params": [main_params, config_param, items_param]}


@component("range_slider")
def get_rangle_slider_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the range slider component."""
    main_params = [
        ParameterDetails(
            "tag_id", "str", "Optionale, eindeutige Tag-ID für die Identifizierung des Elements im JavaScript.", "''"
        ),
        ParameterDetails(
            "name",
            "str",
            "Wird für eine <span class='inline-tag'>&lt;form&gt;</span> benötigt, als Name des Request-Parameters.",
            "''",
        ),
        ParameterDetails("label", "str", "Ein Label-Text welcher über dem Range-Slider angezeigt wird.", "''"),
        ParameterDetails("value", "int", "Der Wert des Range-Sliders.", "0"),
        ParameterDetails("minimum", "int", "Kleinster einzustellender Wert des Range-Sliders.", "undefined"),
        ParameterDetails("maximum", "int", "Größter einzustellender Wert des Range-Sliders.", "undefined"),
        ParameterDetails(
            "step_size",
            "int",
            "Die Größe der Schritte um welche sich der Wert, beim Bewegen des Range-Sliders verändert.",
            "1",
        ),
        ParameterDetails("disabled", "bool", "<b>True</b>, wenn der Range-Slider deaktiviert sein soll.", "False"),
        ParameterDetails(
            "items", "list[str]", "Eine Liste von Texten, welche als Legende unter dem Slider angezeigt werden.", "[]"
        ),
        ParameterDetails(
            "config",
            "dict[str, Any]",
            "Eine alternative Konfiguration mit Keys entsprechend den vorherigen Parametern.",
            "{}",
        ),
    ]

    return {"params": [main_params]}


@component("toggle")
def get_toggle_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the toggle component."""
    main_params = [
        ParameterDetails(
            "tag_id", "str", "Optionale, eindeutige Tag-ID für die Identifizierung des Elements im JavaScript.", "''"
        ),
        ParameterDetails(
            "name",
            "str",
            "Wird für eine <span class='inline-tag'>&lt;form&gt;</span> benötigt, als Name des Request-Parameters.",
            "''",
        ),
        ParameterDetails("label", "str", "Ein Label-Text welcher über dem Toggle-Button angezeigt wird.", "''"),
        ParameterDetails("value", "str", "Der Wert des Toggle-Buttons.", "''"),
        ParameterDetails(
            "switch",
            "bool",
            "<b>True</b>, wenn der Toggle-Button wie ein typischer Switch-Select aussehen soll.",
            "False",
        ),
        ParameterDetails("checked", "bool", "<b>True</b>, wenn der Toggle-Button ausgewählt sein soll.", "False"),
        ParameterDetails("disabled", "bool", "<b>True</b>, wenn der Toggle-Button deaktiviert sein soll.", "False"),
        ParameterDetails(
            "method",
            "str",
            "Name der JavaScript Methode welche beim Klick auf den Toggle-Button ausgeführt werden soll.",
            "''",
        ),
        ParameterDetails(
            "config",
            "dict[str, Any]",
            "Eine alternative Konfiguration mit Keys entsprechend den vorherigen Parametern.",
            "{}",
        ),
    ]

    return {"params": [main_params]}


@component("select")
def get_select_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the select component."""
    main_params = [
        ParameterDetails(
            "name",
            "str",
            "Wird für eine <span class='inline-tag'>&lt;form&gt;</span> benötigt, als Name des Request-Parameters.",
            "''",
        ),
        ParameterDetails("label", "str", "Ein Label-Text welcher über dem Select angezeigt wird.", "''"),
        ParameterDetails(
            "options", "list[str] oder dict[str, str]", "Liste von Werten welche ausgewählt werden können.", "[]"
        ),
        ParameterDetails(
            "selected_option",
            "str",
            "Wert (Der Key-Wert, falls die Optionen als Dict übergeben wurden) der aktuell ausgewählten Option.",
            "''",
        ),
        ParameterDetails(
            "config",
            "dict[str, Any]",
            "Eine alternative Konfiguration mit Keys entsprechend den vorherigen Parametern.",
            "{}",
        ),
    ]

    return {"params": [main_params]}


@component("multiselect")
def get_multiselect_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the multiselect component."""
    main_params = [
        ParameterDetails(
            "name",
            "str",
            "Wird für eine <span class='inline-tag'>&lt;form&gt;</span> benötigt, als Name des Request-Parameters.",
            "''",
        ),
        ParameterDetails("label", "str", "Ein Label-Text welcher über dem Select angezeigt wird.", "''"),
        ParameterDetails("maximum", "int", "Anzahl der maximal ausgewählten Optionen.", "undefined"),
        ParameterDetails(
            "show_buttons",
            "bool",
            "zusätzliche Buttons für 'Alle Auswählen' und 'Alle Abwählen' Buttons anzeigen.",
            "False",
        ),
        ParameterDetails(
            "options", "list[str] oder dict[str, str]", "Liste von Werten welche ausgewählt werden können.", "[]"
        ),
        ParameterDetails("selected_options", "list[str]", "Liste der aktuell ausgewählten Optionen.", "[]"),
        ParameterDetails(
            "config",
            "dict[str, Any]",
            "Eine alternative Konfiguration mit Keys entsprechend den vorherigen Parametern.",
            "{}",
        ),
    ]

    return {"params": [main_params]}


@component("chat")
def get_chat_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the chat component."""
    main_params = [
        ParameterDetails(
            "view_name",
            "str",
            "Name der URL an welchen der Request beim absenden einer Nachricht, gesendet werden soll.",
            "''",
        )
    ]

    return {"params": [main_params]}


@component("alert")
def get_alert_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the alert component."""
    main_params = [
        ParameterDetails(
            "tag_id", "str", "Optionale, eindeutige Tag-ID für die Identifizierung des Elements im JavaScript.", "''"
        ),
        ParameterDetails("message", "str", "Nachricht welche in dem Alert angezeigt wird.", "''"),
        ParameterDetails(
            "type", "str", "Typ des Alerts. Möglich Werte sind 'info', 'success', 'warning' und 'error'.", "info"
        ),
        ParameterDetails(
            "dismissible", "bool", "Zeigt ein Button zum schließen des Alerts am Ende des Alert-Containers an.", "False"
        ),
    ]

    return {"params": [main_params]}


@component("modal")
def get_modal_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the modal component."""
    action_button_param = ParameterDoc(
        ParameterDetails(
            "actions",
            "Sequence[Mapping[str, str]]",
            "Liste von Buttons, welche um unteren Ende des Dialogs angezeigt werden.",
            "[]",
        ),
        [
            ParameterDetails("text", "str", "Beschriftung des Buttons.", "''"),
            ParameterDetails(
                "type",
                "str",
                "Beschreibt die Wichtigkeit des Buttons (rein visuell). Mögliche Werte sind: 'primary' und 'secondary'.",
                "''",
            ),
            ParameterDetails("onclick", "str", "Aufruf einer JavaScript Funktion, bspw.: alert('Confirmed!')", "''"),
            ParameterDetails("dismiss", "bool", "Schließt den Dialog beim Klick.", "False"),
        ],
        """""",
    )

    main_params = [
        ParameterDetails(
            "tag_id", "str", "Optionale, eindeutige Tag-ID für die Identifizierung des Elements im JavaScript.", "''"
        ),
        ParameterDetails("title", "str", "Überschrift des Modal Dialogs.", "''"),
        ParameterDetails("description", "str", "Text welcher direkt unter dem Titel angezeigt wird.", "''"),
        ParameterDetails(
            "additional_content",
            "str",
            "Zusätzlicher Text, welcher unter der Kopfzeile, welche aus Titel und Description besteht, angezeigt wird.",
            "''",
        ),
        action_button_param.details,
    ]

    return {"params": [main_params, action_button_param]}


@component("popover")
def get_popover_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the popover component."""
    main_params = [
        ParameterDetails(
            "data-popover='<target-id>'",
            "str",
            "Bestimmt das Popover Objekt, welches beim Hovern angezeigt werden soll.",
            "''",
        ),
        ParameterDetails(
            "data-position='<position>'",
            "str",
            "Bestimmt wo im Bezug auf das Element, der Popover angezeigt werden soll. Mögliche Werte sind: 'top', 'bottom', 'right', und 'left'.",
            "''",
        ),
        ParameterDetails(
            "data-show-arrow", "bool", "Zeigt ein Pfeil am Rand des Popovers, hin zum auslösenden Objekt an.", "False"
        ),
    ]

    return {"params": [main_params]}


@component("tooltip")
def get_tooltip_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the tooltip component."""
    main_params = [
        ParameterDetails(
            "data-popover='<text>'",
            "str",
            "Zeigt beim Hovern über das Element, ein Tooltip mit dem angegeben Text an.",
            "''",
        ),
        ParameterDetails(
            "data-position='<position>'",
            "str",
            "Bestimmt wo im Bezug auf das Element, der Tooltip angezeigt werden soll. Mögliche Werte sind: 'top', 'bottom', 'right', und 'left'.",
            "''",
        ),
        ParameterDetails(
            "data-show-arrow", "bool", "Zeigt ein Pfeil am Rand des Tooltips, hin zum auslösenden Objekt an.", "False"
        ),
    ]

    return {"params": [main_params]}


@component("code_block")
def get_code_block_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the code block component."""
    main_params = [
        ParameterDetails(
            "id", "str", "Optionale, eindeutige Tag-ID für die Identifizierung des Elements im JavaScript.", "''"
        ),
        ParameterDetails(
            "data-insight-code-block",
            "str",
            "Identifiziert dieses Objekt als Code Block und um welche Sprache es sich handelt.",
            "''",
        ),
        ParameterDetails(
            "data-insight-code-block-filename",
            "str",
            "Zeigt den Text, als Hinweis für den Nutzer in der Kopfzeile des Code Blocks an.",
            "''",
        ),
    ]

    return {"params": [main_params]}


@component("differentiator")
def get_differentiator_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the differentiator component."""
    main_params = [
        ParameterDetails("textA", "str", "Erste bzw. ältere Version des Textes.", "''"),
        ParameterDetails("textB", "str", "Zweite bzw. neuere Version des Textes.", "''"),
    ]

    return {"params": [main_params]}


@component("progress_bar")
def get_progress_bar_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the progress bar component."""
    main_params = [ParameterDetails("", "", "", "")]

    return {"params": [main_params]}


@component("geo_map")
def get_geo_map_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the geo map component."""
    data_param = ParameterDoc(
        ParameterDetails("data", "list[dict]", "Liste der Dateneinträge.", "-"),
        [
            ParameterDetails("lat", "double", "Breitengrad (Latitude) des Dateneintrags.", "-"),
            ParameterDetails("lon", "double", "Längengrad (Longitude) des Dateneintrags.", "-"),
            ParameterDetails("title", "str", "Wird als Überschrift in dem Popover des Dateneintrags angezeigt.", "-"),
            ParameterDetails(
                "description", "str", "Wird unter dem Title in dem Popover des Dateneintrags angezeigt.", "-"
            ),
            ParameterDetails(
                "value",
                "int",
                "Wird nur für 'circle' Dateneinträge verwenden und definiert die Größe/Farbe des Kreises.",
                "-",
            ),
        ],
        """""",
    )

    datasets_param = ParameterDoc(
        ParameterDetails(
            "datasets", "dict[str, Any]", "Datensätze welche auf der Karte dargestellt werden sollen.", "{}"
        ),
        [
            ParameterDetails("name", "str", "Der Name des Datensatzes, wird intern zur Benennung verwendet.", "-"),
            ParameterDetails(
                "type",
                "str",
                "Die Art und Weise wie die Daten dargestellt werden sollen. Mögliche Werte sind: 'marker' und 'circle'.",
                "-",
            ),
            data_param.details,
        ],
        """""",
    )

    config_param = ParameterDoc(
        ParameterDetails(
            "data",
            "dict[str, Any]",
            "Beschreibt die Karte und die Daten welche auf der Karte dargestellt werden sollen.",
            "{}",
        ),
        [
            ParameterDetails(
                "initial_coords", "set(int, int)", "Startposition auf der Karte, beim Seitenaufruf.", "undefined"
            ),
            ParameterDetails("initial_zoom", "int", " Zoom auf der Karte, beim Seitenaufruf", "undefined"),
            datasets_param.details,
        ],
        """""",
    )

    main_params = [config_param.details, ParameterDetails("map_height", "int", "Höhe der Karte in 'rem'.", "36")]

    return {"params": [main_params, config_param, datasets_param, data_param]}


@component("chart")
def get_charts_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the charts component."""
    chart_param = ParameterDoc(
        ParameterDetails("chart", "dict[str, Any]", "Informationen und Daten des Diagramms.", "{}"),
        [
            ParameterDetails("title", "str", "Wird über dem Diagramm als Überschrift angezeigt.", "-"),
            ParameterDetails("x_axis_legend", "list[str]", "Beschriftung der X-Achse.", "-"),
            ParameterDetails("series", "list[str]", "Namen der einzelnen Datensätze.", "-"),
            ParameterDetails("data", "list[list[int]]", "Die Daten der einzelnen Datensätze.", "-"),
        ],
        """""",
    )

    main_params = [
        ParameterDetails(
            "chart_id", "str", "Eindeutige Tag-ID für die Identifizierung des Elements im JavaScript.", "''"
        ),
        chart_param.details,
    ]

    return {"params": [main_params, chart_param]}


@component("live_content")
def get_live_content_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the live content component."""
    main_params = [
        ParameterDetails(
            "tag_id", "str", "Optionale, eindeutige Tag-ID für die Identifizierung des Elements im JavaScript.", "''"
        ),
        ParameterDetails("url", "str", "URL des API Endpunkts zum abfragen der Daten.", "''"),
        ParameterDetails("interval", "int", "Intervall des Datenabrufs in Sekunden.", "10"),
        ParameterDetails("initial_content", "str", "Optionaler, initialer Inhalt.", "''"),
    ]

    return {"params": [main_params]}


@component("web_socket")
def get_web_socket_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the web socket component."""
    main_params = [
        ParameterDetails(
            "tag_id", "str", "Optionale, eindeutige Tag-ID für die Identifizierung des Elements im JavaScript.", "''"
        ),
        ParameterDetails("url", "str", "URL des Websocket-API Endpunkts.", "''"),
        ParameterDetails("initial_content", "str", "Optionaler, initialer Inhalt.", "''"),
    ]

    return {"params": [main_params]}


@component("infinite_scroll")
def get_infinite_scroll_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the infinite scroll component."""
    main_params = [
        ParameterDetails(
            "tag_id", "str", "Optionale, eindeutige Tag-ID für die Identifizierung des Elements im JavaScript.", "''"
        ),
        ParameterDetails("view_name", "str", "Name der URL, an welche der Request zum laden weitere Elemente.", "''"),
        ParameterDetails("items", "list[dict]", "Liste der bereits geladenen Elemente.", "[]"),
        ParameterDetails(
            "auto_fetch",
            "bool",
            "<b>True</b>, neue Einträge werden, sobald der angegebenen Threshold beim Scrollen überschritten wird, geladen. <b>False</b>, am Ende der Liste wird ein Button zum Abfragen weiterer Einträge angezeigt.",
            "True",
        ),
        ParameterDetails(
            "threshold",
            "int",
            "Der Pixel-Schwellenwert für das Laden weiterer Elemente (nur wenn <b>auto_fetch=False</b>).",
            "100",
        ),
    ]

    return {"params": [main_params]}


@component("pagination")
def get_pagination_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the pagination component."""
    main_params = [
        ParameterDetails(
            "current_page", "Page", "Ein von Django erzeugtes Pagination-Objekt der aktuellen Seite.", "None"
        ),
        ParameterDetails("surrounding_pages", "list[str]", "Liste der benachbarten Seiten.", "[]"),
    ]

    return {"params": [main_params]}


@component("table")
def get_table_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the table component."""
    data_param = ParameterDoc(
        ParameterDetails(
            "data",
            "dict[str, Any]",
            "Beschreibt die Tabelle und die Daten welche in dieser dargestellt werden sollen.",
            "{}",
        ),
        [
            ParameterDetails("caption", "str", "Überschrift der Tabelle.", "''"),
            ParameterDetails(
                "empty_msg", "str", "Wird angezeigt, wenn keine Einträge vorhanden sind (wenn 'rows=[]').", "''"
            ),
            ParameterDetails("headers", "list[str]", "Liste der Überschriften der einzelnen Spalten.", "[]"),
            ParameterDetails("rows", "list[list[str]]", "Liste der Daten der einzelnen Zeilen.", "[]"),
        ],
        """""",
    )

    main_params = [data_param.details]

    return {"params": [main_params, data_param]}


@component("generic_filter")
def get_generic_filter_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the generic filter component."""
    main_params = [
        ParameterDetails(
            "view_name",
            "str",
            "Name der URL an welchen der Request beim ändern eines Filters, gesendet werden soll.",
            "''",
        ),
        ParameterDetails(
            "hx_target",
            "str",
            "ID des HTML-Containers, dessen Inhalt beim Response ausgetauscht werden soll (zum Beispiel eine Liste von Daten, welche gefiltert wird).",
            "''",
        ),
        ParameterDetails(
            "hx_push_url",
            "bool",
            "<b>True</b> wenn die ausgewählten Filterwerte in der URL angezeigt werden sollen.",
            "True",
        ),
        ParameterDetails("filters", "list[dict[str, Any]]", "Definition der einzelnen Filter.", "[]"),
        ParameterDetails(
            "vertical", "bool", "<b>True</b> wenn die Filter übereinander angeordnet sein sollen.", "False"
        ),
        ParameterDetails(
            "query_params",
            "dict[str, str]",
            "Enthält die aktuell ausgewählten Werte der einzelnen Filter, um diese nach dem Request wiederherzustellen.",
            "''",
        ),
    ]

    return {"params": [main_params]}


@component("search_bar")
def get_search_bar_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the search bar component."""
    main_params = [
        ParameterDetails(
            "request_view",
            "str",
            "Name der URL an welchen der Request beim absenden der Suche, gesendet werden soll.",
            "''",
        ),
        ParameterDetails(
            "simple", "bool", "<b>True</b> wenn die Suchleiste ohne Button und kleiner angezeigt werden soll.", "False"
        ),
        ParameterDetails(
            "search_query", "str", "Optionaler Wert der automatisch in dem Textfeld angezeigt wird.", "''"
        ),
    ]

    return {"params": [main_params]}


@component("query_builder")
def get_query_builder_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the query builder component."""
    main_params = [ParameterDetails("", "", "", "")]

    return {"params": [main_params]}


@component("card")
def get_card_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the card component."""
    image_param = ParameterDoc(
        ParameterDetails(
            "image",
            "dict[str]",
            "Beschreibt ein Bild, welches als Hintergrund für den Title und dem Subtitle angezeigt wird.",
            "{}",
        ),
        [
            ParameterDetails("url", "str", "URL zu der Bild-Resource.", "''"),
            ParameterDetails(
                "alt",
                "str",
                "Alternativtext der angezeigt wird, falls das Bild nicht geladen werden kann und für Screenreader verwendet wird.",
                "''",
            ),
        ],
        """""",
    )

    action_button_param = ParameterDoc(
        ParameterDetails(
            "actions",
            "list[dict[str, str]]",
            "Liste von Buttons, welche am unteren Rand der Karte angezeigt werden.",
            "[]",
        ),
        [
            ParameterDetails("text", "str", "Beschriftung des Buttons.", "''"),
            ParameterDetails(
                "type",
                "str",
                "Beschreibt die Wichtigkeit des Buttons (rein visuell). Mögliche Werte sind: 'primary' und 'secondary'.",
                "''",
            ),
            ParameterDetails("url", "str", "URL welche beim Klick auf den Button aufgerufen werden soll.", "''"),
        ],
        """""",
    )

    main_params = [
        ParameterDetails("title", "str", "Überschrift der Karte.", "''"),
        ParameterDetails(
            "subtitle", "str", "Optionaler Untertitel, welcher direkt unter dem Title angezeigt wird.", "''"
        ),
        ParameterDetails(
            "content", "str", "Textinhalt der Karte. Wird unter dem Title bzw. unter dem Subtitle angezeigt.", "''"
        ),
        image_param.details,
        action_button_param.details,
    ]

    return {"params": [main_params, image_param, action_button_param]}


@component("card_carousel")
def get_card_carousel_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the card carousel component."""
    main_params = [
        ParameterDetails(
            "carousel_items",
            "list[dict]",
            "Daten welche innerhalb des Karussell angezeigt werden sollen (frei definierbar).",
            "[]",
        ),
        ParameterDetails(
            "show_index",
            "bool",
            "<b>True</b>, wenn in der unteren rechten Ecke die aktuelle Seite angezeigt werden soll.",
            "False",
        ),
        ParameterDetails(
            "show_dots",
            "bool",
            "<b>True</b>, wenn unter dem Karussell-Inhalt eine einfache Pagination angezeigt werden soll.",
            "True",
        ),
        ParameterDetails(
            "autoplay", "bool", "<b>True</b>, wenn das Karussell von alleine durch den Inhalt iterieren soll.", "False"
        ),
        ParameterDetails("items_per_slide", "int", "Anzahl an 'carousel_items' pro Seite.", "1"),
    ]

    return {"params": [main_params]}


@component("image_carousel")
def get_image_carousel_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the image carousel component."""
    image_param = ParameterDoc(
        ParameterDetails(
            "images", "list[dict]", "Bilder welche innerhalb des Karussell angezeigt werden sollen.", "[]"
        ),
        [
            ParameterDetails(
                "description",
                "str",
                "Optionale Beschreibung des Bildes, welche am oberen Rand des Bildes angezeigt wird.",
                "''",
            ),
            ParameterDetails("url", "str", "URL zu der Bild-Resource.", "''"),
            ParameterDetails(
                "alt",
                "str",
                "Alternativtext der angezeigt wird, falls das Bild nicht geladen werden kann und für Screenreader verwendet wird.",
                "''",
            ),
        ],
        """""",
    )

    main_params = [
        image_param.details,
        ParameterDetails(
            "show_index",
            "bool",
            "<b>True</b>, wenn in der unteren rechten Ecke die aktuelle Seite angezeigt werden soll.",
            "False",
        ),
        ParameterDetails(
            "show_dots",
            "bool",
            "<b>True</b>, wenn unter dem Karussell-Inhalt eine einfache Pagination angezeigt werden soll.",
            "True",
        ),
        ParameterDetails(
            "autoplay", "bool", "<b>True</b>, wenn das Karussell von alleine durch den Inhalt iterieren soll.", "False"
        ),
        ParameterDetails("items_per_slide", "int", "Anzahl der Bilder pro Seite.", "1"),
    ]

    return {"params": [main_params, image_param]}


@component("3d_carousel")
def get_3d_carousel_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the 3D carousel component."""
    main_params = [
        ParameterDetails(
            "tag_id", "str", "Optionale, eindeutige Tag-ID für die Identifizierung des Elements im JavaScript.", "''"
        ),
        ParameterDetails("velocity", "int", "Geschwindigkeit mit welcher sich das Karussell dreht.", "1000"),
        ParameterDetails("tilt", "int", "Vertikale Neigung des Karussell zur Camera.", "0"),
        ParameterDetails(
            "face_camera",
            "bool",
            "<b>True</b> wenn alle Karten immer in Richtung der Kamera ausgerichtet sein sollen.",
            "False",
        ),
        ParameterDetails(
            "carousel_items",
            "list[dict]",
            "Daten welche innerhalb des Karussell angezeigt werden sollen (frei definierbar).",
            "[]",
        ),
    ]

    return {"params": [main_params]}


@component("toggle_view")
def get_toggle_view_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the toggle view component."""
    items_param = ParameterDoc(
        ParameterDetails("items", "list[dict]", "Eine Liste der Radio-Elemente.", "[]"),
        [
            ParameterDetails(
                "tag_id",
                "str",
                "Optionale, eindeutige Tag-ID für die Identifizierung des Elements im JavaScript.",
                "''",
            ),
            ParameterDetails("value", "str", "Wert des jeweiligen Radio-Buttons.", "''"),
            ParameterDetails("text", "str", "Beschriftung des jeweiligen Radio-Buttons.", "''"),
            ParameterDetails(
                "icon", "dict[str, str]", "Optionales Icon, welches vor der Beschriftung angezeigt wird.", "{}"
            ),
            ParameterDetails("disabled", "bool", "<b>True</b>, wenn der Radio-Button deaktiviert sein soll.", "False"),
        ],
        """""",
    )

    view_radio_config_param = ParameterDoc(
        ParameterDetails(
            "view_radio_config", "dict[str, Any]", "Konfiguration der Radio-Group, zum wechseln der Ansichtsart.", "{}"
        ),
        [
            ParameterDetails(
                "name", "str", "Optionale, eindeutige Tag-ID für die Identifizierung des Elements im JavaScript.", "''"
            ),
            items_param.details,
        ],
        """""",
    )

    main_params = [
        ParameterDetails(
            "tag_id",
            "str",
            "Eindeutige Tag-ID für die Identifizierung des Elements im JavaScript (wird für den wechsel der Ansicht benötigt).",
            "''",
        ),
        ParameterDetails("data", "list[dict]", "Daten, welche angezeigt werden sollen.", "[]"),
        view_radio_config_param.details,
        ParameterDetails("current_view", "str", "Name der aktuell ausgewählten View-Variante.", "''"),
    ]

    return {"params": [main_params, view_radio_config_param, items_param]}


@component("form")
def get_form_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the form component."""
    htmx_config_param = ParameterDoc(
        ParameterDetails(
            "htmx_config", "dict[str, str]", "Konfiguration des HTMX Request, für asynchrone Requests.", "{}"
        ),
        [
            ParameterDetails(
                "target", "str", "ID des HTML-Containers, dessen Inhalt beim Response ausgetauscht werden soll.", "''"
            ),
            ParameterDetails(
                "swap",
                "str",
                "Die Art wie das Target ausgetauscht werden soll, nur der Inhalt mit 'innerHTML' oder der Container selbst mit 'outerHTML'.",
                "innerHTML",
            ),
        ],
        """""",
    )

    main_params = [
        ParameterDetails(
            "tag_id", "str", "Optionale, eindeutige Tag-ID für die Identifizierung des Elements im JavaScript.", "''"
        ),
        ParameterDetails("title", "str", "Überschrift des Formulars.", "''"),
        ParameterDetails(
            "description", "str", "Beschreibung des Formulars, welche direkt unter dem Title angezeigt wird.", "''"
        ),
        ParameterDetails("fields", "list[dict[str, str]]", "Liste der einzelnen Formular-Felder.", "[]"),
        ParameterDetails(
            "show_reset_button",
            "bool",
            "<b>True</b>, wenn neben dem 'Absenden' Button ein 'Zurücksetzen' Button angezeigt werden soll",
            "False",
        ),
        ParameterDetails(
            "view_name",
            "str",
            "Name der URL, an welche beim absenden des Formulars, der Request gesendet werden soll.",
            "''",
        ),
        htmx_config_param.details,
    ]

    return {"params": [main_params, htmx_config_param]}
