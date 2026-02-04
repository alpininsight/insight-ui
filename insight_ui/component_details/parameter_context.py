def get_navbar_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the navbar component."""
    main_params = [
        ["config", "dict[str, Any]", "Ein Dictionary mit der gesamten Konfiguration der Navigationsleiste.", "{}"],
        ["user", "User", "Das <i>user</i> Objekt des Requests (i.d.R. über <i>request.user</i> verfügbar).", "None"],
        [
            "user_dropdown_links",
            "list",
            "Eine Liste mit den Links welche in dem Benutzermenü angezeigt werden sollen.",
            "[]",
        ],
        ["show_login", "bool", "<b>True</b> wenn ein Button zum Anmelden angezeigt werden soll.", "false"],
        ["search_query", "str", "Suchstring für die Suchleiste.", "''"],
    ]

    config_params = [
        ["brand", "dict[str, Any]", "Beschreibt den Titel und das Logo der Anwendung in der Navbar.", "{}"],
        ["links", "list[dict]", "Enthält/Beschreibt die Navigationspunkte der Navbar.", "[]"],
        [
            "searchbar_request_view",
            "str",
            "Name der URL welche bei der Suche aufgerufen werden soll (wenn leer wird keine Suchzeile angezeigt).",
            "''",
        ],
        ["show_usermenu", "bool", "Zeigt ein Dropdownmenü mit mindestens einem Logout-Button.", "False"],
        [
            "show_language_selector",
            "bool",
            "Zeigt ein Dropdownmenü zum Auswählen der Anzeigesprache (sofern definiert).",
            "False",
        ],
        [
            "show_theme_toggle",
            "bool",
            "Zeigt ein Button zum wechsel zwischen der hellen und der dunklen Darstellung der Seite.",
            "False",
        ],
    ]

    brand_params = [
        ["title", "str", "Der Titel der Anwendung.", "''"],
        ["view_name", "str", "Name der URL welche beim klick auf den Titel aufgerufen werden soll.", "''"],
        ["gap", "str", "Dieser Wert bestimmt den Abstand zwischen dem Logo und dem Titel.", "0.5rem"],
        ["logo", "dict[str, str]", "Beschreibt das Logo, welches neben dem Titel angezeigt wird.", "{}"],
    ]

    logo_params = [
        ["url", "str", "Pfad zu der Logo Datei für das helle Theme.", "insight_ui/svg/ai-logo.svg"],
        ["url_dark", "str", "Pfad zu der Logo Datei für das dunkle Theme.", "insight_ui/svg/ai-logo-dark.svg"],
        ["alt", "str", "Alternativtext des Logos.", "Insight UI Logo"],
        ["height", "str", "Dieser Wert bestimmt die Größe des Logos.", "2rem"],
    ]

    links_params = [
        ["text", "str", "Beschriftung des Links.", "''"],
        ["icon", "dict[str, str]", "Ein optionales Icon, welches vor dem Text angezeigt wird.", "{}"],
        ["view_name", "str", "Name der URL welche beim Klick auf den Link aufgerufen werden soll.", "''"],
        ["open_modal", "str", "ID des Modal-Dialogs welche beim Klick auf den Link angezeigt werden soll.", "''"],
        [
            "active",
            "bool",
            "Hebt den Link stilistisch von den anderen ab um zu zeigen, dass der Nutzer auf der entsprechenden Seite ist.",  # noqa: E501
            "True",
        ],
        ["need_auth", "bool", "Der Link wird nur für angemeldete Nutzer angezeigt.", "False"],
        ["staff_only", "bool", "Der Link wird nur für Administratoren angezeigt.", "False"],
    ]

    return {
        "main_params": main_params,
        "config_params": config_params,
        "brand_params": brand_params,
        "logo_params": logo_params,
        "links_params": links_params,
    }


def get_sidebar_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the sidebar component."""
    main_params = [
        ["sidebar_data", "dict[str, Any]", "Inhalt der Sidebar (Titel und Navigations-Elemente).", "None"],
        ["side", "str", "Bestimmt, auf welcher Seite die Sidebar platziert werden soll.", "right"],
        ["static", "bool", "<b>True</b> wenn die Sidebar nicht einklappbar sein soll.", "True"],
        ["auto_close", "bool", "Bei <b>True</b> schließt sich die Sidebar sobald der Cursor diese verlässt.", "False"],
        [
            "navbar_fixed",
            "bool",
            "Bei <b>True</b> wird die Position des Inhalts angepasst. (NUR FÜR CUSTOM-SIDEBAR!) ",
            "False",
        ],
    ]

    return {"main_params": main_params}


def get_footer_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the footer component."""
    main_params = [["data", "dict[str, Any]", "Daten welche im Footer angezeigt werden sollen.", "{}"]]

    data_params = [
        ["description", "dict[str, Any]", "Kurzbeschreibung der Anwendung mit optionalen Bild.", "{}"],
        ["links", "list[dict[str, Any]]", "Liste der Hauptnavigationspunkte der Anwendung.", "[]"],
        [
            "contact",
            "dict[str, Any]",
            "Kontaktinformationen, Link zum Impressum, Datenschutz und eine Kontaktmailadresse.",
            "{}",
        ],
        ["copyright", "dict[str, str]", "Copyright Informationen, wie das Jahr und der geschützte Name.", "{}"],
    ]

    description_params = [
        ["title", "str", "Überschrift der Beschreibung.", "''"],
        ["text", "str", "Kurze Zusammenfassung der Anwendung.", "''"],
        ["image", "dict[str, str]", "Optionales Bild, welches unter dem Text der Beschreibung angezeigt wird.", "{}"],
    ]

    image_params = [
        ["url", "str", "Pfad zu der Bilddatei für das helle Theme.", "insight_ui/svg/ai-logo.svg"],
        ["url_dark", "str", "Pfad zu der Bilddatei für das dunkle Theme.", "insight_ui/svg/ai-logo-dark.svg"],
        ["alt", "str", "Alternativtext des Logos.", "Insight UI Logo"],
        ["height", "str", "Dieser Wert bestimmt die Größe des Logos.", "2rem"],
    ]

    links_params = [
        ["text", "str", "Beschriftung des Links.", "''"],
        ["icon", "dict[str, str]", "Ein optionales Icon, welches vor dem Text angezeigt wird.", "{}"],
        ["view_name", "str", "Name der URL welche beim Klick auf den Link aufgerufen werden soll.", "''"],
        ["open_modal", "str", "ID des Modal-Dialogs welche beim Klick auf den Link angezeigt werden soll.", "''"],
        [
            "active",
            "bool",
            "Hebt den Link stilistisch von den anderen ab um zu zeigen, dass der Nutzer auf der entsprechenden Seite ist.",  # noqa: E501
            "True",
        ],
        ["need_auth", "bool", "Der Link wird nur für angemeldete Nutzer angezeigt.", "False"],
        ["staff_only", "bool", "Der Link wird nur für Administratoren angezeigt.", "False"],
    ]

    contact_params = [
        ["mail_url", "str", "URL einer Kontaktmailadresse.", "''"],
        ["imprint", "str", "Verlinkung zu einem Impressum.", "''"],
        ["privacy", "str", "Verlinkung zu einer Datenschutzerklärung.", "''"],
    ]

    copyright_params = [
        ["year", "int", "I.d.R das aktuelle Jahr (ist nicht zwingend erforderlich). ", "undefined"],
        ["app_name", "str", "Der geschützte Name der Anwendung.", "''"],
    ]

    return {
        "main_params": main_params,
        "data_params": data_params,
        "description_params": description_params,
        "image_params": image_params,
        "links_params": links_params,
        "contact_params": contact_params,
        "copyright_params": copyright_params,
    }


def get_breadcrumb_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the breadcrumb component."""
    main_params = [["items", "list[dict]", "Liste der Navigationspunkte.", "[]"]]

    links_params = [
        ["text", "str", "Beschriftung des Links.", "''"],
        ["icon", "dict[str, str]", "Ein optionales Icon, welches vor dem Text angezeigt wird.", "{}"],
        ["view_name", "str", "Name der URL welche beim Klick auf den Link aufgerufen werden soll.", "''"],
        ["query_params", "str", "Ein optionaler Parameter, falls die aufzurufende View einen benötigt.", "''"],
    ]

    return {"main_params": main_params, "links_params": links_params}


def get_step_bar_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the step bar component."""
    main_params = [["items", "list[dict]", "Liste der Prozessschritte.", "[]"]]

    step_params = [
        ["title", "str", "Titel des Schritts.", "''"],
        ["description", "str", "Zusätzliche Beschreibung des Schritts unter dem Titel.", "''"],
        ["completed", "bool", "Zeigt statt der Schrittzahl ein Haken an.", "False"],
        ["current", "bool", "Hebt den Titel farblich hervor und lässt den Text pulsieren.", "False"],
    ]

    return {"main_params": main_params, "step_params": step_params}


def get_bullet_point_list_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the bullet point list component."""
    main_params = [["items", "list[dict]", "Liste der einzelnen Punkte.", "[]"]]

    step_params = [
        ["title", "str", "Titel des Schritts.", "''"],
        ["description", "str", "Zusätzliche Beschreibung des Schritts unter dem Titel.", "''"],
        [
            "bullet_icon",
            "dict[str, str]",
            "Ein optionales Icon, welches statt dem normalen Punkt angezeigt wird.",
            "''",
        ],
        ["bullet_text", "str", "Ein optionaler Text, welcher statt dem normalen Punkt angezeigt wird.", "''"],
        ["view_name", "str", "Name der URL welche beim Klick auf den jeweiligen Punkt aufgerufen werden soll.", "''"],
        ["completed", "bool", "Zeigt statt dem Punkt ein Haken an.", "False"],
        ["current", "bool", "Hebt den Titel farblich hervor.", "False"],
    ]

    return {"main_params": main_params, "step_params": step_params}


def get_accordion_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the accordion component."""
    main_params = [
        ["id", "str", "Eindeutige Tag-ID für die Identifizierung des Elements im JavaScript.", "''"],
        ["items", "list[dict]", "Liste der einzelnen Abschnitte.", "[]"],
        ["exclusive", "bool", "Bei <b>True</b> kann immer nur ein Abschnitt gleichzeitig geöffnet sein.", "False"],
    ]

    item_params = [["title", "str", "Titel des Abschnitts.", "''"], ["content", "str", "Inhalt des Abschnitts.", "''"]]

    return {"main_params": main_params, "item_params": item_params}


def get_tabs_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the tabs component."""
    main_params = [
        [
            "config",
            "dict[str, Any]",
            "Beschreibt die Buttons, welche zum wechseln der einzelnen Tabs verwendet werden.",
            "{}",
        ]
    ]

    config_params = [
        ["id", "str", "Eindeutige Tag-ID für die Identifizierung des Elements im JavaScript.", "''"],
        ["label", "str", "Zusätzlicher, nicht sichtbarer Titel, welcher nur von Screenreadern vorgelesen wird.", "''"],
        ["tabs", "list[dict]", "Liste der Tab-Buttons.", "[]"],
    ]

    tabs_params = [
        ["id", "str", "Eindeutige Tag-ID für die Identifizierung des Elements im JavaScript.", "''"],
        ["url", "str", "Die URL welche beim Klick auf den Tab aufgerufen werden soll.", "''"],
        ["title", "str", "Beschriftung des Tab-Button.", "''"],
        ["icon", "dict[str, str]", "Ein optionales Icon, welches vor der Beschriftung angezeigt wird.", "{}"],
    ]

    return {"main_params": main_params, "config_params": config_params, "tabs_params": tabs_params}


def get_button_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the button component."""
    main_params = [["", "", "", ""]]

    return {"main_params": main_params}


def get_input_field_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the input field component."""
    main_params = [
        ["tag_id", "str", "Optionale, eindeutige Tag-ID für die Identifizierung des Elements im JavaScript.", "''"],
        [
            "name",
            "str",
            "Wird für eine <span class='inline-tag'>&lt;form&gt;</span> benötigt, als Name des Request-Parameters.",
            "''",
        ],
        ["input_type", "str", "Der Type des Input-Feldes bspw.: 'text', 'password', 'date', etc..", "''"],
        [
            "placeholder",
            "str",
            "Platzhalter Text, wird in dem Feld angezeigt, solange es nicht selektiert wurde.",
            "''",
        ],
        ["value", "str", "Der Wert des Input-Feldes.", "''"],
        ["minimum", "int", "Kleinster numerischer Wert (für input_type='number').", "undefined"],
        ["maximum", "int", "Größter numerischer Wert (für input_type='number').", "undefined"],
        ["min_length", "int", "Minimale Anzahl an Zeichen in einem Textfeld.", "undefined"],
        ["max_length", "int", "Maximale Anzahl an Zeichen in einem Textfeld.", "undefined"],
        [
            "checked",
            "bool",
            "<b>True</b>, wenn <span class='inline-tag'>input_type='checkbox'</span> und die Checkbox ausgewählt sein soll.",  # noqa: E501
            "False",
        ],
        ["required", "bool", "<b>True</b> wenn das Feld ausgefüllt werden muss.", "False"],
        ["disabled", "bool", "<b>True</b>, wenn das Feld deaktiviert sein soll.", "False"],
        ["label", "str", "Ein Label-Text welcher über dem Input-Feld angezeigt wird.", "''"],
        [
            "config",
            "dict[str, Any]",
            "Eine alternative Konfiguration mit Keys entsprechend den vorherigen Parametern.",
            "{}",
        ],
    ]

    return {"main_params": main_params}


def get_checkbox_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the checkbox component."""
    main_params = [
        ["tag_id", "str", "Optionale, eindeutige Tag-ID für die Identifizierung des Elements im JavaScript.", "''"],
        [
            "name",
            "str",
            "Wird für eine <span class='inline-tag'>&lt;form&gt;</span> benötigt, als Name des Request-Parameters.",
            "''",
        ],
        [
            "value",
            "str",
            "Der Wert der Checkbox (Dabei handelt es sich nicht um den Zustand, siehe dafür 'checked').",
            "''",
        ],
        ["label", "str", "Ein Label-Text welcher über der Checkbox angezeigt wird.", "''"],
        ["checked", "bool", "<b>True</b>, wenn die Checkbox ausgewählt sein soll.", "False"],
        ["disabled", "bool", "<b>True</b>, wenn die Checkbox deaktiviert sein soll.", "False"],
        [
            "config",
            "dict[str, Any]",
            "Eine alternative Konfiguration mit Keys entsprechend den vorherigen Parametern.",
            "{}",
        ],
    ]

    return {"main_params": main_params}


def get_checkbox_group_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the checkbox group component."""
    main_params = [
        ["config", "dict[str, Any]", "Beschreibt die Checkbox Gruppe und die einzelnen Checkbox-Elemente.", "{}"]
    ]

    config_params = [
        [
            "name",
            "str",
            "Wird für eine <span class='inline-tag'>&lt;form&gt;</span> benötigt, als Name des Request-Parameters.",
            "''",
        ],
        ["label", "str", "Label-Text welcher über den Checkbox-Elementen angezeigt wird.", "''"],
        ["as_row", "bool", "<b>True</b>, wenn die Checkbox-Elemente nebeneinander angezeigt werden sollen.", "False"],
        [
            "minimum_checked",
            "int",
            "Anzahl der Checkbox-Elemente welche mindestens ausgewählt sein müssen.",
            "undefined",
        ],
        [
            "maximum_checked",
            "int",
            "Anzahl der Checkbox-Elemente welche gleichzeitig ausgewählt sein dürfen.",
            "undefined",
        ],
        ["items", "list[dict[str, Any]]", "Liste der Checkbox-Elemente.", "[]"],
    ]

    return {"main_params": main_params, "config_params": config_params}


def get_dropdown_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the dropdown component."""
    main_params = [["dropdown_menu", "dict[str, Any]", "Beschreibt den Dropdown-Button und die Menüelemente.", "{}"]]

    dropdown_menu_params = [
        ["tag_id", "str", "Optionale, eindeutige Tag-ID für die Identifizierung des Elements im JavaScript.", "''"],
        ["title", "str", "Beschriftung des Dropdown-Buttons.", "''"],
        ["show_arrow", "bool", "<b>True</b> zeigt einen Pfeil hinter em Titel an.", "False"],
        ["items", "list[dict[str, Any]]", "Eine Liste der Menüelemente.", "[]"],
    ]

    item_params = [
        ["text", "str", "Beschriftung des Dropdown-Elements.", "''"],
        ["view_name", "str", "Name der URL welche beim Klick auf den jeweiligen Punkt aufgerufen werden soll.", "''"],
        ["icon", "dict[str, str]", "Ein optionales Icon, welches vor der Beschriftung angezeigt wird.", "{}"],
    ]

    return {"main_params": main_params, "dropdown_menu_params": dropdown_menu_params, "item_params": item_params}


def get_radio_group_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the radio_group component."""
    main_params = [
        ["config", "dict[str, Any]", "Beschreibt die Radio-Button Gruppe und die einzelnen Radio-Elemente.", "{}"],
        ["current_value", "str", "Der Wert des aktuell ausgewählten Radio-Buttons.", "''"],
        # Block only
        [
            "view_name",
            "str",
            "Name der URL an welchen der Request beim Klick auf einen der Radio-Button, gesendet werden soll.",
            "''",
        ],
        [
            "query_params",
            "str",
            "Ein String von Query-Parametern, welche bei dem Request mit gesendet werden sollen.",
            "''",
        ],
        [
            "target_id",
            "str",
            "Die ID des HTML-Tags, welches bei wechseln des Radio-Buttons ausgetauscht werden soll.",
            "''",
        ],
        [
            "method",
            "str",
            "Name der JavaScript Methode welche beim Klick auf einen der Radio-Button ausgeführt werden soll.",
            "''",
        ],
        [
            "integrated",
            "bool",
            "<b>True</b> wenn sich die Gruppe in einer &lt;form&gt; befindet, bei <b>False</b> bekommt die Gruppe ihre eigene &lt;form&gt;.",  # noqa: E501
            "False",
        ],
    ]

    config_params = [
        ["name", "str", "Optionale, eindeutige Tag-ID für die Identifizierung des Elements im JavaScript.", "''"],
        ["label", "str", "Ein Label-Text welcher über den Radio-Elementen angezeigt wird.", "''"],
        ["as_row", "bool", "<b>True</b>, wenn die Radio-Elemente nebeneinander angezeigt werden sollen.", "False"],
        ["items", "list[dict[str, Any]]", "Eine Liste der Radio-Elemente.", "[]"],
    ]

    items_params = [
        ["tag_id", "str", "Optionale, eindeutige Tag-ID für die Identifizierung des Elements im JavaScript.", "''"],
        ["value", "str", "Wert des jeweiligen Radio-Buttons.", "''"],
        ["text", "str", "Beschriftung des jeweiligen Radio-Buttons.", "''"],
        [
            "icon",
            "dict[str, str]",
            "Optionales Icon, welches vor der Beschriftung angezeigt wird (nur für die Radio-Block Variante).",
            "{}",
        ],
        ["disabled", "bool", "<b>True</b>, wenn der Radio-Button deaktiviert sein soll.", "False"],
    ]

    return {"main_params": main_params, "config_params": config_params, "items_params": items_params}


def get_rangle_slider_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the range slider component."""
    main_params = [
        ["tag_id", "str", "Optionale, eindeutige Tag-ID für die Identifizierung des Elements im JavaScript.", "''"],
        [
            "name",
            "str",
            "Wird für eine <span class='inline-tag'>&lt;form&gt;</span> benötigt, als Name des Request-Parameters.",
            "''",
        ],
        ["label", "str", "Ein Label-Text welcher über dem Range-Slider angezeigt wird.", "''"],
        ["value", "int", "Der Wert des Range-Sliders.", "0"],
        ["minimum", "int", "Kleinster einzustellender Wert des Range-Sliders.", "undefined"],
        ["maximum", "int", "Größter einzustellender Wert des Range-Sliders.", "undefined"],
        [
            "step_size",
            "int",
            "Die Größe der Schritte um welche sich der Wert, beim Bewegen des Range-Sliders verändert.",
            "1",
        ],
        ["disabled", "bool", "<b>True</b>, wenn der Range-Slider deaktiviert sein soll.", "False"],
        ["items", "list[str]", "Eine Liste von Texten, welche als Legende unter dem Slider angezeigt werden.", "[]"],
        [
            "config",
            "dict[str, Any]",
            "Eine alternative Konfiguration mit Keys entsprechend den vorherigen Parametern.",
            "{}",
        ],
    ]

    return {"main_params": main_params}


def get_toggle_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the toggle component."""
    main_params = [
        ["tag_id", "str", "Optionale, eindeutige Tag-ID für die Identifizierung des Elements im JavaScript.", "''"],
        [
            "name",
            "str",
            "Wird für eine <span class='inline-tag'>&lt;form&gt;</span> benötigt, als Name des Request-Parameters.",
            "''",
        ],
        ["label", "str", "Ein Label-Text welcher über dem Toggle-Button angezeigt wird.", "''"],
        ["value", "str", "Der Wert des Toggle-Buttons.", "''"],
        [
            "switch",
            "bool",
            "<b>True</b>, wenn der Toggle-Button wie ein typischer Switch-Select aussehen soll.",
            "False",
        ],
        ["checked", "bool", "<b>True</b>, wenn der Toggle-Button ausgewählt sein soll.", "False"],
        ["disabled", "bool", "<b>True</b>, wenn der Toggle-Button deaktiviert sein soll.", "False"],
        [
            "method",
            "str",
            "Name der JavaScript Methode welche beim Klick auf den Toggle-Button ausgeführt werden soll.",
            "''",
        ],
        [
            "config",
            "dict[str, Any]",
            "Eine alternative Konfiguration mit Keys entsprechend den vorherigen Parametern.",
            "{}",
        ],
    ]

    return {"main_params": main_params}


def get_select_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the select component."""
    main_params = [
        [
            "name",
            "str",
            "Wird für eine <span class='inline-tag'>&lt;form&gt;</span> benötigt, als Name des Request-Parameters.",
            "''",
        ],
        ["label", "str", "Ein Label-Text welcher über dem Select angezeigt wird.", "''"],
        ["options", "list[str] oder dict[str, str]", "Liste von Werten welche ausgewählt werden können.", "[]"],
        [
            "selected_option",
            "str",
            "Wert (Der Key-Wert, falls die Optionen als Dict übergeben wurden) der aktuell ausgewählten Option.",
            "''",
        ],
        [
            "config",
            "dict[str, Any]",
            "Eine alternative Konfiguration mit Keys entsprechend den vorherigen Parametern.",
            "{}",
        ],
    ]

    return {"main_params": main_params}


def get_multiselect_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the multiselect component."""
    main_params = [
        [
            "name",
            "str",
            "Wird für eine <span class='inline-tag'>&lt;form&gt;</span> benötigt, als Name des Request-Parameters.",
            "''",
        ],
        ["label", "str", "Ein Label-Text welcher über dem Select angezeigt wird.", "''"],
        ["maximum", "int", "Anzahl der maximal ausgewählten Optionen.", "undefined"],
        [
            "show_buttons",
            "bool",
            "zusätzliche Buttons für 'Alle Auswählen' und 'Alle Abwählen' Buttons anzeigen.",
            "False",
        ],
        ["options", "list[str] oder dict[str, str]", "Liste von Werten welche ausgewählt werden können.", "[]"],
        ["selected_options", "list[str]", "Liste der aktuell ausgewählten Optionen.", "[]"],
        [
            "config",
            "dict[str, Any]",
            "Eine alternative Konfiguration mit Keys entsprechend den vorherigen Parametern.",
            "{}",
        ],
    ]

    return {"main_params": main_params}


def get_chat_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the chat component."""
    main_params = [
        [
            "view_name",
            "str",
            "Name der URL an welchen der Request beim absenden einer Nachricht, gesendet werden soll.",
            "''",
        ]
    ]

    return {"main_params": main_params}


def get_alert_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the alert component."""
    main_params = [
        ["tag_id", "str", "Optionale, eindeutige Tag-ID für die Identifizierung des Elements im JavaScript.", "''"],
        ["message", "str", "Nachricht welche in dem Alert angezeigt wird.", "''"],
        ["type", "str", "Typ des Alerts. Möglich Werte sind 'info', 'success', 'warning' und 'error'.", "info"],
        ["dismissible", "bool", "Zeigt ein Button zum schließen des Alerts am Ende des Alert-Containers an.", "False"],
    ]

    return {"main_params": main_params}


def get_modal_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the modal component."""
    main_params = [
        ["tag_id", "str", "Optionale, eindeutige Tag-ID für die Identifizierung des Elements im JavaScript.", "''"],
        ["title", "str", "Überschrift des Modal Dialogs.", "''"],
        ["description", "str", "Text welcher direkt unter dem Titel angezeigt wird.", "''"],
        [
            "additional_content",
            "str",
            "Zusätzlicher Text, welcher unter der Kopfzeile, welche aus Titel und Description besteht, angezeigt wird.",
            "''",
        ],
        [
            "actions",
            "Sequence[Mapping[str, str]]",
            "Liste von Buttons, welche um unteren Ende des Dialogs angezeigt werden.",
            "[]",
        ],
    ]

    action_button_params = [
        ["text", "str", "Beschriftung des Buttons.", "''"],
        [
            "type",
            "str",
            "Beschreibt die Wichtigkeit des Buttons (rein visuell). Mögliche Werte sind: 'primary' und 'secondary'.",
            "''",
        ],
        ["onclick", "str", "Aufruf einer JavaScript Funktion, bspw.: alert('Confirmed!')", "''"],
        ["dismiss", "bool", "Schließt den Dialog beim Klick.", "False"],
    ]

    return {"main_params": main_params, "action_button_params": action_button_params}


def get_popover_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the popover component."""
    main_params = [
        [
            "data-popover='<target-id>'",
            "str",
            "Bestimmt das Popover Objekt, welches beim Hovern angezeigt werden soll.",
            "''",
        ],
        [
            "data-position='<position>'",
            "str",
            "Bestimmt wo im Bezug auf das Element, der Popover angezeigt werden soll. Mögliche Werte sind: 'top', 'bottom', 'right', und 'left'.",  # noqa: E501
            "''",
        ],
        ["data-show-arrow", "bool", "Zeigt ein Pfeil am Rand des Popovers, hin zum auslösenden Objekt an.", "False"],
    ]

    return {"main_params": main_params}


def get_tooltip_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the tooltip component."""
    main_params = [
        [
            "data-popover='<text>'",
            "str",
            "Zeigt beim Hovern über das Element, ein Tooltip mit dem angegeben Text an.",
            "''",
        ],
        [
            "data-position='<position>'",
            "str",
            "Bestimmt wo im Bezug auf das Element, der Tooltip angezeigt werden soll. Mögliche Werte sind: 'top', 'bottom', 'right', und 'left'.",  # noqa: E501
            "''",
        ],
        ["data-show-arrow", "bool", "Zeigt ein Pfeil am Rand des Tooltips, hin zum auslösenden Objekt an.", "False"],
    ]

    return {"main_params": main_params}


def get_code_block_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the code block component."""
    main_params = [
        ["id", "str", "Optionale, eindeutige Tag-ID für die Identifizierung des Elements im JavaScript.", "''"],
        [
            "data-insight-code-block",
            "str",
            "Identifiziert dieses Objekt als Code Block und um welche Sprache es sich handelt.",
            "''",
        ],
        [
            "data-insight-code-block-filename",
            "str",
            "Zeigt den Text, als Hinweis für den Nutzer in der Kopfzeile des Code Blocks an.",
            "''",
        ],
    ]

    return {"main_params": main_params}


def get_differentiator_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the differentiator component."""
    main_params = [
        ["textA", "str", "Erste bzw. ältere Version des Textes.", "''"],
        ["textB", "str", "Zweite bzw. neuere Version des Textes.", "''"],
    ]

    return {"main_params": main_params}


def get_progress_bar_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the progress bar component."""
    main_params = [["", "", "", ""]]

    return {"main_params": main_params}


def get_geo_map_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the geo map component."""
    main_params = [
        [
            "data",
            "dict[str, Any]",
            "Beschreibt die Karte und die Daten welche auf der Karte dargestellt werden sollen.",
            "{}",
        ],
        ["map_height", "int", "Höhe der Karte in 'rem'.", "36"],
    ]

    config_params = [
        ["initial_coords", "set(int, int)", "Startposition auf der Karte, beim Seitenaufruf.", "undefined"],
        ["initial_zoom", "int", " Zoom auf der Karte, beim Seitenaufruf", "undefined"],
        ["datasets", "dict[str, Any]", "Datensätze welche auf der Karte dargestellt werden sollen.", "{}"],
    ]

    datasets_params = [
        ["name", "str", "Der Name des Datensatzes, wird intern zur Benennung verwendet.", "-"],
        [
            "type",
            "str",
            "Die Art und Weise wie die Daten dargestellt werden sollen. Mögliche Werte sind: 'marker' und 'circle'.",
            "-",
        ],
        ["data", "list[dict]", "Liste der Dateneinträge.", "-"],
    ]

    data_params = [
        ["lat", "double", "Breitengrad (Latitude) des Dateneintrags.", "-"],
        ["lon", "double", "Längengrad (Longitude) des Dateneintrags.", "-"],
        ["title", "str", "Wird als Überschrift in dem Popover des Dateneintrags angezeigt.", "-"],
        ["description", "str", "Wird unter dem Title in dem Popover des Dateneintrags angezeigt.", "-"],
        [
            "value",
            "int",
            "Wird nur für 'circle' Dateneinträge verwenden und definiert die Größe/Farbe des Kreises.",
            "-",
        ],
    ]

    return {
        "main_params": main_params,
        "config_params": config_params,
        "datasets_params": datasets_params,
        "data_params": data_params,
    }


def get_charts_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the charts component."""
    main_params = [
        ["chart_id", "str", "Eindeutige Tag-ID für die Identifizierung des Elements im JavaScript.", "''"],
        ["chart", "dict[str, Any]", "Informationen und Daten des Diagramms.", "{}"],
    ]

    chart_params = [
        ["title", "str", "Wird über dem Diagramm als Überschrift angezeigt.", "-"],
        ["x_axis_legend", "list[str]", "Beschriftung der X-Achse.", "-"],
        ["series", "list[str]", "Namen der einzelnen Datensätze.", "-"],
        ["data", "list[list[int]]", "Die Daten der einzelnen Datensätze.", "-"],
    ]

    return {"main_params": main_params, "chart_params": chart_params}


def get_live_content_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the live content component."""
    main_params = [
        ["tag_id", "str", "Optionale, eindeutige Tag-ID für die Identifizierung des Elements im JavaScript.", "''"],
        ["url", "str", "URL des API Endpunkts zum abfragen der Daten.", "''"],
        ["interval", "int", "Intervall des Datenabrufs in Sekunden.", "10"],
        ["initial_content", "str", "Optionaler, initialer Inhalt.", "''"],
    ]

    return {"main_params": main_params}


def get_web_socket_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the web socket component."""
    main_params = [
        ["tag_id", "str", "Optionale, eindeutige Tag-ID für die Identifizierung des Elements im JavaScript.", "''"],
        ["url", "str", "URL des Websocket-API Endpunkts.", "''"],
        ["initial_content", "str", "Optionaler, initialer Inhalt.", "''"],
    ]

    return {"main_params": main_params}


def get_infinite_scroll_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the infinite scroll component."""
    main_params = [
        ["tag_id", "str", "Optionale, eindeutige Tag-ID für die Identifizierung des Elements im JavaScript.", "''"],
        ["view_name", "str", "Name der URL, an welche der Request zum laden weitere Elemente.", "''"],
        ["items", "list[dict]", "Liste der bereits geladenen Elemente.", "[]"],
        [
            "auto_fetch",
            "bool",
            "<b>True</b>, neue Einträge werden, sobald der angegebenen Threshold beim Scrollen überschritten wird, geladen. <b>False</b>, am Ende der Liste wird ein Button zum Abfragen weiterer Einträge angezeigt.",  # noqa: E501
            "True",
        ],
        [
            "threshold",
            "int",
            "Der Pixel-Schwellenwert für das Laden weiterer Elemente (nur wenn <b>auto_fetch=False</b>).",
            "100",
        ],
    ]

    return {"main_params": main_params}


def get_pagination_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the pagination component."""
    main_params = [
        ["current_page", "Page", "Ein von Django erzeugtes Pagination-Objekt der aktuellen Seite.", "None"],
        ["surrounding_pages", "list[str]", "Liste der benachbarten Seiten.", "[]"],
    ]

    return {"main_params": main_params}


def get_table_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the table component."""
    main_params = [
        [
            "data",
            "dict[str, Any]",
            "Beschreibt die Tabelle und die Daten welche in dieser dargestellt werden sollen.",
            "{}",
        ]
    ]

    data_params = [
        ["caption", "str", "Überschrift der Tabelle.", "''"],
        ["empty_msg", "str", "Wird angezeigt, wenn keine Einträge vorhanden sind (wenn 'rows=[]').", "''"],
        ["headers", "list[str]", "Liste der Überschriften der einzelnen Spalten.", "[]"],
        ["rows", "list[list[str]]", "Liste der Daten der einzelnen Zeilen.", "[]"],
    ]

    return {"main_params": main_params, "data_params": data_params}


def get_generic_filter_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the generic filter component."""
    main_params = [
        [
            "view_name",
            "str",
            "Name der URL an welchen der Request beim ändern eines Filters, gesendet werden soll.",
            "''",
        ],
        [
            "hx_target",
            "str",
            "ID des HTML-Containers, dessen Inhalt beim Response ausgetauscht werden soll (zum Beispiel eine Liste von Daten, welche gefiltert wird).",  # noqa: E501
            "''",
        ],
        [
            "hx_push_url",
            "bool",
            "<b>True</b> wenn die ausgewählten Filterwerte in der URL angezeigt werden sollen.",
            "True",
        ],
        ["filters", "list[dict[str, Any]]", "Definition der einzelnen Filter.", "[]"],
        ["vertical", "bool", "<b>True</b> wenn die Filter übereinander angeordnet sein sollen.", "False"],
        [
            "query_params",
            "dict[str, str]",
            "Enthält die aktuell ausgewählten Werte der einzelnen Filter, um diese nach dem Request wiederherzustellen.",  # noqa: E501
            "''",
        ],
    ]

    return {"main_params": main_params}


def get_search_bar_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the search bar component."""
    main_params = [
        [
            "request_view",
            "str",
            "Name der URL an welchen der Request beim absenden der Suche, gesendet werden soll.",
            "''",
        ],
        ["simple", "bool", "<b>True</b> wenn die Suchleiste ohne Button und kleiner angezeigt werden soll.", "False"],
        ["search_query", "str", "Optionaler Wert der automatisch in dem Textfeld angezeigt wird.", "''"],
    ]

    return {"main_params": main_params}


def get_query_builder_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the query builder component."""
    main_params = [["", "", "", ""]]

    return {"main_params": main_params}


def get_card_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the card component."""
    main_params = [
        ["title", "str", "Überschrift der Karte.", "''"],
        ["subtitle", "str", "Optionaler Untertitel, welcher direkt unter dem Title angezeigt wird.", "''"],
        ["content", "str", "Textinhalt der Karte. Wird unter dem Title bzw. unter dem Subtitle angezeigt.", "''"],
        [
            "image",
            "dict[str]",
            "Beschreibt ein Bild, welches als Hintergrund für den Title und dem Subtitle angezeigt wird.",
            "{}",
        ],
        [
            "actions",
            "list[dict[str, str]]",
            "Liste von Buttons, welche am unteren Rand der Karte angezeigt werden.",
            "[]",
        ],
    ]
    image_params = [
        ["url", "str", "URL zu der Bild-Resource.", "''"],
        [
            "alt",
            "str",
            "Alternativtext der angezeigt wird, falls das Bild nicht geladen werden kann und für Screenreader verwendet wird.",  # noqa: E501
            "''",
        ],
    ]

    action_button_params = [
        ["text", "str", "Beschriftung des Buttons.", "''"],
        [
            "type",
            "str",
            "Beschreibt die Wichtigkeit des Buttons (rein visuell). Mögliche Werte sind: 'primary' und 'secondary'.",
            "''",
        ],
        ["url", "str", "URL welche beim Klick auf den Button aufgerufen werden soll.", "''"],
    ]

    return {"main_params": main_params, "image_params": image_params, "action_button_params": action_button_params}


def get_card_carousel_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the card carousel component."""
    main_params = [
        [
            "carousel_items",
            "list[dict]",
            "Daten welche innerhalb des Karussell angezeigt werden sollen (frei definierbar).",
            "[]",
        ],
        [
            "show_index",
            "bool",
            "<b>True</b>, wenn in der unteren rechten Ecke die aktuelle Seite angezeigt werden soll.",
            "False",
        ],
        [
            "show_dots",
            "bool",
            "<b>True</b>, wenn unter dem Karussell-Inhalt eine einfache Pagination angezeigt werden soll.",
            "True",
        ],
        ["autoplay", "bool", "<b>True</b>, wenn das Karussell von alleine durch den Inhalt iterieren soll.", "False"],
        ["items_per_slide", "int", "Anzahl an 'carousel_items' pro Seite.", "1"],
    ]

    return {"main_params": main_params}


def get_image_carousel_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the image carousel component."""
    main_params = [
        ["images", "list[dict]", "Bilder welche innerhalb des Karussell angezeigt werden sollen.", "[]"],
        [
            "show_index",
            "bool",
            "<b>True</b>, wenn in der unteren rechten Ecke die aktuelle Seite angezeigt werden soll.",
            "False",
        ],
        [
            "show_dots",
            "bool",
            "<b>True</b>, wenn unter dem Karussell-Inhalt eine einfache Pagination angezeigt werden soll.",
            "True",
        ],
        ["autoplay", "bool", "<b>True</b>, wenn das Karussell von alleine durch den Inhalt iterieren soll.", "False"],
        ["items_per_slide", "int", "Anzahl der Bilder pro Seite.", "1"],
    ]

    image_params = [
        [
            "description",
            "str",
            "Optionale Beschreibung des Bildes, welche am oberen Rand des Bildes angezeigt wird.",
            "''",
        ],
        ["url", "str", "URL zu der Bild-Resource.", "''"],
        [
            "alt",
            "str",
            "Alternativtext der angezeigt wird, falls das Bild nicht geladen werden kann und für Screenreader verwendet wird.",  # noqa: E501
            "''",
        ],
    ]

    return {"main_params": main_params, "image_params": image_params}


def get_3d_carousel_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the 3D carousel component."""
    main_params = [
        ["tag_id", "str", "Optionale, eindeutige Tag-ID für die Identifizierung des Elements im JavaScript.", "''"],
        ["velocity", "int", "Geschwindigkeit mit welcher sich das Karussell dreht.", "1000"],
        ["tilt", "int", "Vertikale Neigung des Karussell zur Camera.", "0"],
        [
            "face_camera",
            "bool",
            "<b>True</b> wenn alle Karten immer in Richtung der Kamera ausgerichtet sein sollen.",
            "False",
        ],
        [
            "carousel_items",
            "list[dict]",
            "Daten welche innerhalb des Karussell angezeigt werden sollen (frei definierbar).",
            "[]",
        ],
    ]

    return {"main_params": main_params}


def get_toggle_view_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the toggle view component."""
    main_params = [
        [
            "tag_id",
            "str",
            "Eindeutige Tag-ID für die Identifizierung des Elements im JavaScript (wird für den wechsel der Ansicht benötigt).",  # noqa: E501
            "''",
        ],
        ["data", "list[dict]", "Daten, welche angezeigt werden sollen.", "[]"],
        ["view_radio_config", "dict[str, Any]", "Konfiguration der Radio-Group, zum wechseln der Ansichtsart.", "{}"],
        ["current_view", "str", "Name der aktuell ausgewählten View-Variante.", "''"],
    ]

    view_radio_config_params = [
        ["name", "str", "Optionale, eindeutige Tag-ID für die Identifizierung des Elements im JavaScript.", "''"],
        ["items", "list[dict]", "Eine Liste der Radio-Elemente.", "[]"],
    ]

    items_params = [
        ["tag_id", "str", "Optionale, eindeutige Tag-ID für die Identifizierung des Elements im JavaScript.", "''"],
        ["value", "str", "Wert des jeweiligen Radio-Buttons.", "''"],
        ["text", "str", "Beschriftung des jeweiligen Radio-Buttons.", "''"],
        ["icon", "dict[str, str]", "Optionales Icon, welches vor der Beschriftung angezeigt wird.", "{}"],
        ["disabled", "bool", "<b>True</b>, wenn der Radio-Button deaktiviert sein soll.", "False"],
    ]

    return {
        "main_params": main_params,
        "view_radio_config_params": view_radio_config_params,
        "items_params": items_params,
    }


def get_form_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the form component."""
    main_params = [
        ["tag_id", "str", "Optionale, eindeutige Tag-ID für die Identifizierung des Elements im JavaScript.", "''"],
        ["title", "str", "Überschrift des Formulars.", "''"],
        ["description", "str", "Beschreibung des Formulars, welche direkt unter dem Title angezeigt wird.", "''"],
        ["fields", "list[dict[str, str]]", "Liste der einzelnen Formular-Felder.", "[]"],
        [
            "show_reset_button",
            "bool",
            "<b>True</b>, wenn neben dem 'Absenden' Button ein 'Zurücksetzen' Button angezeigt werden soll",
            "False",
        ],
        [
            "view_name",
            "str",
            "Name der URL, an welche beim absenden des Formulars, der Request gesendet werden soll.",
            "''",
        ],
        ["htmx_config", "dict[str, str]", "Konfiguration des HTMX Request, für asynchrone Requests.", "{}"],
    ]

    htmx_config_params = [
        ["target", "str", "ID des HTML-Containers, dessen Inhalt beim Response ausgetauscht werden soll.", "''"],
        [
            "swap",
            "str",
            "Die Art wie das Target ausgetauscht werden soll, nur der Inhalt mit 'innerHTML' oder der Container selbst mit 'outerHTML'.",  # noqa: E501
            "innerHTML",
        ],
    ]

    return {"main_params": main_params, "htmx_config_params": htmx_config_params}
