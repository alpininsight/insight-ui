# UI-Komponenten (Version 0.1.0)

Das UI-Framework bietet für den schnellen Start in ein neues Projekt, vorgefertigte UI-Elemente sog. Komponenten. Diese können über Template-Tags direkt in den Projekt-Templates eingebunden werden.

## Verfügbare Komponenten

- [Navbar](navbar.md): Eine Navigationsleiste mit Branding (Name, Logo), Links, einer Suchzeile, Sprachauswahl und Theme-Toggle
- [Usermenu](usermenu.md): Ein Dropdown-Menü mit Benutzer spezifischen Navigationselementen 
- [Alert](alert.md): Benachrichtigungen und Warnmeldungen in verschiedenen Stilen
- [Breadcrumbs](breadcrumbs.md): Eine Art Mini-Navigation, um dem Nutzer zu zeigen, wo er sich grade befindet
- [Carousel](carousel.md): Ein Karussell für Kacheln (Später auch für Bilder und andere Container, etc.)
- [Footer](footer.md): Ein einfacher Footer, mit einem Beschreibungstext, Links, Kontaktinformationen und Copyright Angabe
- [Form](form.md): Beispiele für Form-Elemente
- [Infinite Scroll](infinite_scroll.md): Eine sich kontinuierlich erweiternde Liste
- [Eingabeelemente](inputs.md): Eine Sammlung einfacher Input-Elemente wie Buttons, Checkboxen, etc.
- [Modal](modal.md): Dialoge
- [Searchbar](search_bar.md): Eine einfache Suchzeile

Jede Komponente ist:

- **Barrierefrei**: Entspricht den WCAG 2.1 AA-Richtlinien
- **Responsiv**: Passt sich der Bildschirmgröße an und funktioniert auch auf mobilen Endgeräten
- **Themenfähig**: Unterstützt ein helles und dunkles Farbschema
- **Anpassbar**: Kann über die Parameter der Template-Tags angepasst

## Verwendung

Alle Komponenten können über Template-Tags verwendet werden oder mittels des `{% include %}` Tags eingefügt werden:

```django
{% load insight_tags %}

{% navbar brand="Meine App" %}

{% alert message="Operation erfolgreich!" type="success" %}
```

## Komponenten anpassen

Es besteht die Möglichkeit die vorgefertigten Komponenten anzupassen. Weitere Informationen dazu befinden sich im Abschnitt [Anpassung](../guides/customization.md).
