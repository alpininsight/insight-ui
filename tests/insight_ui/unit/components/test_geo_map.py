# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Tests for the geo_map component."""

import json

import pytest
from bs4 import BeautifulSoup
from django.test import override_settings
from insight_ui.configs import GeoMapConfig, GeoMapDatasetConfig, GeoMapMarkerConfig

from tests.insight_ui.unit.components.test_template_tags import TemplateTagsTestCase

OSM_MAX_ZOOM = 19
ZOOM = 6


def map_data(rendered: str, tag_id: str = "map") -> dict:
    """Read the JSON the map script works with."""
    script = BeautifulSoup(rendered, "html.parser").find("script", id=f"{tag_id}-data")
    assert script is not None
    return json.loads(script.string)


class TestGeoMap(TemplateTagsTestCase):
    """Test suite for the geo_map component."""

    def render_map(self, config: GeoMapConfig) -> str:
        """Render a map from a config."""
        return self.render_template("{% load insight_tags %}{% geo_map config=map %}", {"map": config})

    def test_default_ids_and_accessible_description(self) -> None:
        """Without tag_id the map keeps its ids and points to the screen-reader list."""
        soup = BeautifulSoup(self.render_map(GeoMapConfig()), "html.parser")

        element = soup.find(id="map")
        assert element["role"] == "application"
        assert element["aria-describedby"] == "map-locations-list"
        assert soup.find(id="map-locations-list") is not None

    def test_two_maps_on_one_page_have_their_own_ids(self) -> None:
        """Each map renders its element, list and data under its own tag_id."""
        rendered = self.render_template(
            "{% load insight_tags %}{% geo_map tag_id='offices' %}{% geo_map tag_id='stores' %}"
        )
        soup = BeautifulSoup(rendered, "html.parser")

        for tag_id in ("offices", "stores"):
            assert soup.find(id=tag_id)["aria-describedby"] == f"{tag_id}-locations-list"
            assert soup.find(id=f"{tag_id}-locations-list") is not None
            assert map_data(rendered, tag_id)["datasets"] == []
        assert soup.find(id="map") is None

    def test_empty_tag_id_is_rejected(self) -> None:
        """A map needs an element id for Leaflet."""
        with pytest.raises(ValueError, match="tag_id"):
            GeoMapConfig(tag_id="")

    def test_default_tiles_follow_the_openstreetmap_policy(self) -> None:
        """The default tile URL has no a/b/c subdomain and names OpenStreetMap."""
        tiles = map_data(self.render_map(GeoMapConfig()))["tiles"]

        assert tiles["url"] == "https://tile.openstreetmap.org/{z}/{x}/{y}.png"
        assert "openstreetmap.org/copyright" in tiles["attribution"]
        assert tiles["max_zoom"] == OSM_MAX_ZOOM

    def test_tiles_come_from_the_setting(self) -> None:
        """A host can switch the tile service; unset keys keep their defaults."""
        with override_settings(INSIGHT_UI={"map_tiles": {"url": "https://tiles.example.com/{z}/{x}/{y}.png"}}):
            tiles = map_data(self.render_map(GeoMapConfig()))["tiles"]

        assert tiles["url"] == "https://tiles.example.com/{z}/{x}/{y}.png"
        assert tiles["max_zoom"] == OSM_MAX_ZOOM

    def test_datasets_from_configs_and_dicts_give_the_same_data(self) -> None:
        """Config objects and plain dicts, also mixed, reach the script as the same JSON."""
        from_configs = GeoMapConfig(
            initial_coords=[48.1, 11.6],
            initial_zoom=ZOOM,
            datasets=[
                GeoMapDatasetConfig(
                    name="Offices",
                    data=[GeoMapMarkerConfig(title="HQ", lat=48.1, lon=11.6, description="Main office")],
                )
            ],
        )
        from_dicts = GeoMapConfig(
            initial_coords=[48.1, 11.6],
            initial_zoom=ZOOM,
            datasets=[
                {
                    "name": "Offices",
                    "type": "marker",
                    "data": [GeoMapMarkerConfig(title="HQ", lat=48.1, lon=11.6, description="Main office")],
                    "min": 0,
                    "max": 100,
                }
            ],
        )

        data = map_data(self.render_map(from_configs))

        assert data == map_data(self.render_map(from_dicts))
        assert data["center"] == [48.1, 11.6]
        assert data["zoom"] == ZOOM
        assert data["datasets"][0]["data"][0] == {
            "title": "HQ",
            "lat": 48.1,
            "lon": 11.6,
            "description": "Main office",
            "value": None,
        }

    def test_marker_text_cannot_end_the_script(self) -> None:
        """Marker texts are data: a closing script tag stays inside the JSON."""
        text = "</script><img src=x onerror=alert(1)>"
        config = GeoMapConfig(
            datasets=[GeoMapDatasetConfig(name=text, data=[GeoMapMarkerConfig(title=text, lat=0, lon=0)])]
        )

        rendered = self.render_map(config)
        soup = BeautifulSoup(rendered, "html.parser")

        assert soup.find("img") is None
        assert map_data(rendered)["datasets"][0]["data"][0]["title"] == text
        assert soup.find(id="map-locations-list").find("li").get_text() == text

    def test_control_labels_are_translated_data(self) -> None:
        """The labels of the zoom and layer controls reach the script as data."""
        labels = map_data(self.render_map(GeoMapConfig()))["labels"]

        assert labels == {"zoom_in": "Zoom in", "zoom_out": "Zoom out", "layers": "Map layers"}
