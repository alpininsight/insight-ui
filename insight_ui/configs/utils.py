"""Configuration classes for utility components (differentiator, charts, maps, etc.)."""

from dataclasses import dataclass, field
from typing import Literal

from insight_ui.configs.base import IconConfig


@dataclass
class InfoboxConfig:
    """
    Configuration for the infobox component.

    Renders a bordered information box (less prominent than alert).

    Attributes:
        message: Information message.
        info_type: Box type/severity.

    Example:
        >>> hint = InfoboxConfig(
        ...     message="Tip: You can drag and drop files here.",
        ...     info_type="info",
        ... )

    """

    message: str
    info_type: Literal["info", "warn", "danger"] = "info"


@dataclass
class CopyrightNoticeConfig:
    """
    Configuration for the copyright_notice component.

    Renders a compact copyright and legal notice line.

    Attributes:
        year: Copyright year.
        holder: Copyright holder name.
        source_label: Source/distribution label (e.g., "Open Source").
        license_text: License name/text.
        license_url: URL to full license.
        separator: Separator between items (default: middle dot).
        rights_text: Rights statement (default: "All rights reserved.").

    Example:
        >>> copyright = CopyrightNoticeConfig(
        ...     year=2026,
        ...     holder="Alpin Insight Solutions GmbH",
        ...     source_label="Open Source",
        ...     license_text="AGPL-3.0",
        ...     license_url="https://github.com/org/repo/blob/main/LICENSE",
        ... )

    """

    year: int | str = ""
    holder: str = ""
    source_label: str = ""
    license_text: str = ""
    license_url: str = ""
    separator: str = "\u00b7"  # Middle dot
    rights_text: str = ""


@dataclass
class LogoConfig:
    """
    Configuration for the logo component.

    Renders a brand logo as an image, SVG, or icon.

    Attributes:
        url: Static path or URL for image/svg logos.
        url_dark: Optional dark-theme variant.
        alt: Accessible text.
        icon: Icon configuration for icon-type logos.
        icon_name: Icon name (alternative to icon config).
        icon_size: Icon size (alternative to icon config).
        height: CSS height value.
        width: Optional CSS width value.

    Example:
        >>> logo = LogoConfig(
        ...     type="svg",
        ...     url="img/logo.svg",
        ...     url_dark="img/logo-dark.svg",
        ...     alt="Company Logo",
        ...     height="2rem",
        ... )

    """

    url: str = ""
    url_dark: str = ""
    alt: str = ""
    icon: IconConfig | None = None
    icon_name: str = ""
    icon_size: str = ""
    height: str = "2rem"
    width: str = ""


@dataclass
class CornerRibbonConfig:
    """
    Configuration for the corner_ribbon component.

    Renders a decorative diagonal ribbon in a browser corner.

    Attributes:
        text: Ribbon text.
        position: Corner position.
        color: Color variant.

    Example:
        >>> beta_ribbon = CornerRibbonConfig(
        ...     text="Beta",
        ...     position="top-right",
        ...     color="warning",
        ... )

    """

    text: str
    position: Literal["top-right", "top-left", "bottom-right", "bottom-left"] = "top-right"
    color: Literal["primary", "success", "warning", "danger", "info"] = "primary"


@dataclass
class GeoMapMarkerConfig:
    """
    Configuration for a marker on a geo map.

    Attributes:
        title: Marker title/label.
        lat: Latitude coordinate.
        lon: Longitude coordinate.
        description: Optional popup description.
        value: Optional numeric value (for circle markers).

    """

    title: str
    lat: float
    lon: float
    description: str = ""
    value: int | float | None = None


@dataclass
class GeoMapDatasetConfig:
    """
    Configuration for a dataset layer on a geo map.

    Attributes:
        name: Dataset name.
        type: Marker type ('marker' or 'circle').
        data: List of marker configurations.
        min: Minimum value for circle scaling.
        max: Maximum value for circle scaling.

    Example:
        >>> population = GeoMapDatasetConfig(
        ...     name="population",
        ...     type="circle",
        ...     min=100000,
        ...     max=5000000,
        ...     data=[
        ...         GeoMapMarkerConfig(title="Berlin", lat=52.52, lon=13.405, value=3769000),
        ...         GeoMapMarkerConfig(title="Munich", lat=48.135, lon=11.582, value=1488000),
        ...     ],
        ... )

    """

    name: str
    type: Literal["marker", "circle"] = "marker"
    data: list[GeoMapMarkerConfig] = field(default_factory=list)
    min: int | float = 0
    max: int | float = 100


@dataclass
class GeoMapConfig:
    """
    Configuration for the geo_map component.

    Renders an interactive Leaflet map.

    Attributes:
        initial_coords: Starting map center [lat, lon].
        initial_zoom: Starting zoom level.
        map_height: The height of the map in 'rem'.
        datasets: List of data layers to display.

    Example:
        >>> geo_map = GeoMapConfig(
        ...     initial_coords=[52.52, 13.405],
        ...     initial_zoom=10,
        ...     datasets=[
        ...         GeoMapDatasetConfig(
        ...             name="offices",
        ...             type="marker",
        ...             data=[
        ...                 GeoMapMarkerConfig(title="HQ", lat=52.52, lon=13.405),
        ...             ],
        ...         ),
        ...     ],
        ... )

    """

    initial_coords: list[float] = field(default_factory=lambda: [52.52, 13.405])
    initial_zoom: int = 8
    map_height: int = 36
    datasets: list[GeoMapDatasetConfig] = field(default_factory=list)


@dataclass
class ChartSeriesConfig:
    """
    Configuration for a chart data series.

    Attributes:
        name: Series name (shown in legend).
        data: Data points for this series.

    """

    name: str
    data: list[int | float]


@dataclass
class ChartConfig:
    """
    Configuration for chart components (bar_chart, line_chart).

    Attributes:
        title: Chart title.
        x_axis_legend: Labels for X-axis categories.
        series: Series names (for legend).
        data: Data for each series (list of lists).

    Example:
        >>> sales_chart = ChartConfig(
        ...     title="Weekly Sales",
        ...     x_axis_legend=["Mon", "Tue", "Wed", "Thu", "Fri"],
        ...     series=["Online", "In-Store"],
        ...     data=[
        ...         [120, 150, 180, 130, 200],  # Online
        ...         [80, 90, 110, 100, 120],    # In-Store
        ...     ],
        ... )

    """

    title: str = ""
    x_axis_legend: list[str] = field(default_factory=list)
    series: list[str] = field(default_factory=list)
    data: list[list[int | float]] = field(default_factory=list)


@dataclass
class LiveContentConfig:
    """
    Configuration for the live_content component.

    Renders a container that auto-refreshes via HTMX polling.

    Attributes:
        tag_id: Unique ID for JavaScript/CSS targeting.
        request_url: URL for content updates.
        interval: Update interval in seconds.
        initial_content: Initial content before first update.

    Example:
        >>> live_stats = LiveContentConfig(
        ...     tag_id="live-stats",
        ...     request_url="/api/stats/",
        ...     interval=30,
        ...     initial_content="Loading...",
        ... )

    """

    tag_id: str = ""
    request_url: str = ""
    interval: int = 10
    initial_content: str = ""


@dataclass
class WebSocketConfig:
    """
    Configuration for the insight_websocket component.

    Renders a WebSocket-connected container using HTMX ws extension.

    Attributes:
        tag_id: Container ID.
        request_url: WebSocket endpoint URL.
        initial_content: Initial content.

    Example:
        >>> ws = WebSocketConfig(
        ...     tag_id="chat-stream",
        ...     request_url="/ws/chat/",
        ...     initial_content="Connecting...",
        ... )

    """

    tag_id: str = ""
    request_url: str = ""
    initial_content: str = ""
