# Das Basis-Template (Version 0.1.0)

Das Basis-Template dient als Grundlage für sämtliche Seiten der Anwendung. Es bietet ein semantisch korrektes Grundgerüst inklusive `<meta>` Tags für Icons, SEO, die Einbindung der internen JavaScript- und CSS-Dateien und ein Grundgerüst für den eigentlichen Inhalt.

```django
{% extends "insight_ui/base.html" %}
```

## Head

Im `<head>` werden alle benötigten JavaScript Bibliotheken verlinkt, sowie die SEO und das Favicon definiert. Der Titel lässt sich problemlos anpassen durch den Block `{% block title %}`. Es können bei Bedarf auch weitere JavaScript Bibliotheken verlinkt werden, durch den `{% block extra_head %}` Block.

> Das Favicon, die SEO Angaben, sowie weitere Meta-Information können über die **INSIGHT_UI** Einstellungen in der `settings.py` angepasst werden.

## Body

Der Body stellt ein Grundgerüst für den Inhalt bereit. Es gibt eine Reihe von vordefinierten Blöcken, wodurch der Inhalt so flexibel wie möglich anpassbar sein soll. Es stehen folgende Blöcke zur Verfügung:

- `{% block background_image %}`
- `{% block navbar %}`
- `{% block drawers %}`
- `{% block sidebar_right %}`
- `{% block sidebar_left %}`
- `{% block content %}`
- `{% block footer %}`
- `{% block extra_scripts %}`

> Diese Blöcke müssen nicht zwangsläufig verwendet werden, allerdings ist es empfehlenswert, da sich ein paar Strukturelle Gegebenheiten mit sich bringen. Theoretisch könnte aber auch alles in den `{% block content %}` gepackt werden.

### background_image

Dieser Block befindet sich sozusagen hinter dem Eigentlichen Inhalt und kann dazu verwendet werden, ein Hintergrundbild einzubinden, welches fixiert ist, also sich bei scrollen mitbewegt.

```django
{% block background_image %}
    <img src="{% static "img/hubble-fiction.webp" %}" alt="Hubble Telescope" class="fixed left-1/4 -z-10 w-full h-dvh object-cover opacity-25">
{% endblock background_image %}
```

### navbar

Die Navigationsleiste hat einen eigenen Bereich. Dieser ist vor dem restlichen Inhalt definiert, wodurch dieser immer als ersten auf der Seite auftaucht.

```django
{% block navbar %}
    {% navbar config=nav_config user=user user_dropdown_links=user_dropdown_links show_login=True search_query=search_query %}
{% endblock navbar %}
```

_Für weitere Information über die Komponente, siehe [navbar](components/navbar.md.md)_.

### drawers

In diesem Block können sog. **Drawer** eingebettet werden. Drawer sind ein- und ausklappbare Sidebars und liegen gewöhnlich über dem Inhalt. Daher haben sie ihren eigenen Block, damit sie nicht mit dem restlichen Layout in Konflikt geraten.

```django
{% block drawers %}
    {% sidebar sidebar_data=left_sidebar side="left" static=False %}
{% endblock drawers %}
```

_Für weitere Information über die Komponente, siehe [sidebar](components/sidebar.md)_.

### sidebar_right und sidebar_left

zusätzlich zu dem `{% block drawers %}` Block gibt es zwei Blöcke für statische **Sidebars**. Einen für eine Sidebar auf der rechten Seite des Hauptinhalt und einen für eine Sidebar auf der linken Seite. In diesem Fall bekommt der Hauptinhalt etwas weniger Platz und die Sidebar bleibt dauerhaft sichtbar.

```django
{% block sidebar_left %}
    {% sidebar sidebar_data=left_sidebar side="left" %}
{% endblock sidebar_left %}
```

_Für weitere Information über die Komponente, siehe [sidebar](components/sidebar.md)_.

### content

Dieser Blöcke ist für den Hauptinhalt der Seite vorgesehen. Hier kommt alles rein was rein soll.

> Der Block nimmt immer die volle Höhe des Fenstern ein, unabhängig vom Inhalt. Dadurch wird sichergestellt, das sich der Footer nicht mitten im Browserfenster hängt.

### footer

Direkt unter dem `{% block content %}` befindet sich der **Footer**. Dieser schließt die Seite ab und befindet sich immer am Ende der Seite.

```django
{% block footer %}
    {% footer data=footer_data %}
{% endblock footer %}
```

_Für weitere Information über die Komponente, siehe [footer](components/footer.md)_.

### extra_scripts

Zuletzt gibt es einen Block um zusätzliche JavaScript Dateien zu verlinken.
