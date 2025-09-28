# Geo Map Component (Version 0.1.0)

The geo map component prepares a container for visualising geographic data with libraries such as Leaflet or Mapbox.

## Usage

```django
{% include "insight_ui/components/geo_map.html" with map_id="locations-map" %}
```

- `map_id`: DOM ID used to initialise the map via JavaScript.
- Optional context (e.g. coordinates, markers) can be passed through `options`.

## Integration Tips

- Include the required map library scripts/styles in your base template.
- Use HTMX or Alpine.js to load dynamic marker data.

## Customisation

Override `components/geo_map.html` to adjust the container size, add loading states, or hook into specific map providers.

## Related Components
- [Sidebar](sidebar.en.md) – combine filters with map views.
- [Generic filter](generic_filter.en.md)
