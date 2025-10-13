# Chart-Komponente (Version 0.1.0)

Mit der `chart` Komponente können ohne JavaScript anpassen zu müssen, Diagramme dargestellt werden. Die Komponente verwendet intern Apache ECharts.

Die Komponente steht bisher in den folgenden Ausführungen zu Verfügung:
- `line_chart`: Ein Linien-Diagramm.
- `bar_chart`: Ein Stacked Balken-Diagramm. 

## Abhängigkeiten

- **[Apache EChart](https://echarts.apache.org/en/index.html)**: Wird für das Einbinden der Karte verwendet.

## Verwendung

```django
    {% bar_chart chart_id="bar_chart_example" chart=chart_data %}
    {% line_chart chart_id="line_chart_example" chart=chart_data %}
```

## Parameter

- **chart_id** (_str_): Eine eindeutige ID für das Diagramm.
- **chart** (_dict_): Die Informationen und Daten des Diagramms.

### chart

Die Informationen und Daten des Diagramms.

```py
{
    "title": "Chart Example",
    "x_axis_legend": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
    "series": ["Email", "Union Ads", "Video Ads", "Direct", "Search Engine"],
    "data": [
        [100, 302, 301, 334, 390, 330, 320],
        [320, 132, 101, 134, 90, 230, 210],
        [220, 182, 191, 234, 290, 330, 310],
        [150, 212, 201, 154, 190, 330, 410],
        [820, 832, 901, 934, 1290, 1330, 1320],
    ],
}
```

- **title** (_str_): Der Titel des Diagramms.
- **x_axis_legend** (_list_): Die Beschriftung der X-Achse.
- **series** (_list_): Die Namen der einzelnen Datensätze.
- **data** (_list_): Die Daten der einzelnen Datensätze.

## Customization

Der Quellcode der Line-Chart Komponente befindet sich in dieser Datei: `insight_ui/templates/insight_ui/components/charts/line_chart.html`.

Der Quellcode der Bar-Chart Komponente befindet sich in dieser Datei: `insight_ui/templates/insight_ui/components/charts/bar_chart.html`.

Das Design kann am einfachsten angepasst werden, indem eine Kopie der Datei in den folgenden Pfad `templates/insight_ui/components/` vom Projektverzeichnis aus gesehen, abgelegt wird. Anschließend wird immer dieses Template anstelle des Originals verwendet werden.

## Barrierefreiheit

- _Todo_

## Verwandte Themen

- _Todo_
