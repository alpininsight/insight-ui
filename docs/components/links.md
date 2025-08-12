# Links (Version 0.1.0)

Hierbei handelt es sich um keine Komponente, sondern um eine Sammlung der in diversen Komponenten verwendeten Links und ihren Attributen. 

## Parameter

```py
"link" = {
    "text": _("Startseite"),
    "icon": {"name": "home", "size": "small"}}
    "view_name": "storybook_view",
    "open_modal": "about-modal",
    "active": False,
    "need_auth": False,
    "staff_only": False,
```

Jeder Link bekommt ein Anzeigetext, einen **view_name** oder eine Tag-ID mit der Variable **open_modal**, welche die ID des zu öffnenden Modal-Dialogs enthält. Ein Link kann auf _aktiv/aktuell_ gesetzt werden mit der Variable **active**. Wenn ein Link als _aktiv_ eingestellt ist, wird dieser hervorgehoben dargestellt (Betrifft nur die Navbar). Zusätzlich kann ein Link auch ein Icon enthalten, dieses wird über den entsprechenden Namen angegeben (siehe [Icons](../guides/icons.md)) und kann in unterschiedlichen Größen angegeben werden.

Die letzten beiden Variablen regeln, wer den jeweiligen Link sehen darf. **need_auth** wenn nur angemeldete Benutzer ihn sehen sollen und **staff_only** wenn der Link nur von Administratoren gesehen werden soll.

## Verwandte Themen

- [Navbar](navbar.md)
- [Footer](footer.md)
- [Benutzermenü](usermenu.md)
