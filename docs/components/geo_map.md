# Geo-Map-Komponente (Version 0.1.0)

Mit der `geo_map` Komponente wird eine geografische Karte mittels [leaflet](https://leafletjs.com) dargestellt. Auf dieser lassen sich mühelos geografische Informationen darstellen.

## Abhängigkeiten

- **[leaflet](https://leafletjs.com)**: Wird für das Einbinden der Karte verwendet.

## Verwendung

```django
{% load insight_tags %}

{% geo_map data=geo_map_data %}
```

## Parameter

- **data** (_dict_): Die Daten welche auf der Karte dargestellt werden sollen.

### data

Die Daten welche auf der Karte dargestellt werden sollen.

```py
{
    "initial_coords": [52.5200, 13.4050],
    "initial_zoom": 8,
    "datasets": [
        {
            "name": "population",
            "type": "circle",
            "data": [
                {"title": "Berlin", "value": 3769000, "lat": 52.5200, "lon": 13.4050},
                {"title": "Hamburg", "value": 1850000, "lat": 53.5511, "lon": 9.9937},
                {"title": "München", "value": 1488000, "lat": 48.1351, "lon": 11.5820},
                ...
            ],
        },
        {
            "name": "hanseatic_cities",
            "type": "marker",
            "data": [
                {
                    "title": "Lübeck",
                    "lat": 53.8655,
                    "lon": 10.6866,
                    "description": "Hauptstadt der Hanse („Königin der Hanse“); Sitz der Hansetage und Zentrum des Ostseehandels.",  # noqa: E501
                },
                ...
            ],
        }
    ],
}
```

- **initial_coords** (_set_): Die Startposition auf der Karte, beim Seitenaufruf.
- **initial_zoom** (_int_): Der Zoom auf der Karte, beim Seitenaufruf.
- **datasets** (_dict_): Die Datensätze welche auf der Karte dargestellt werden sollen.
    - **name** (_str_): Der Name des Datensatzes, wird im Hintergrund zur Benennung verwendet.
    - **type** (_str_): Die Art und Weise wie die Daten dargestellt werden sollen ("marker", "circle")
    - **data** (_list_): Die eigentlichen Daten. Jeder Eintrage braucht folgende Werte "lat", "lon", "title" und "description". Daten welche mittels "circle" dargestellt werden sollen, benötigen noch einen Wert "value".

## Barrierefreiheit

- _Todo_

## Verwandte Themen

- _Todo_
