"""Configuration classes for utility components (differentiator, charts, maps, etc.)."""

from dataclasses import dataclass, field
from typing import Literal

from django.utils.translation import gettext_lazy as _

from insight_ui.configs.base import IconConfig


@dataclass
class InfoboxConfig:
    """
    Configuration for the infobox component.

    Renders a bordered information box (less prominent than alert).

    Attributes:
        message: Descriptive message.
        info_type: Importance level of the message. Possible values are 'info', 'success', 'warn' or 'danger'.

    """

    __example__ = """
        InfoboxConfig(
            message="Tip: You can drag and drop files here.",
            info_type="info",
        )
        """

    message: str = field(metadata={"doc": _("Descriptive message.")})
    info_type: Literal["info", "warn", "danger"] = field(
        default="info",
        metadata={
            "doc": _("Importance level of the message. Possible values are 'info', 'success', 'warn' or 'danger'.")
        },
    )


@dataclass
class CopyrightNoticeConfig:
    """
    Configuration for the copyright_notice component.

    Renders a compact copyright and legal notice line.

    Attributes:
        year: Typically the current year (not strictly required).
        holder: The copyright holder.
        source_label: Optional source model label, for example Open Source.
        license_text: Optional license label, for example AGPL-3.0.
        license_url: Optional URL for the license label.
        separator: Separator between legal metadata parts.
        rights_text: Optional rights statement.

    """

    __example__ = """
        CopyrightNoticeConfig(
            year=2026,
            holder="Alpin Insight Solutions GmbH",
            source_label="Open Source",
            license_text="AGPL-3.0",
            license_url="https://github.com/org/repo/blob/main/LICENSE",
        )
        """

    year: int | str = field(default="", metadata={"doc": _("Typically the current year (not strictly required).")})
    holder: str = field(default="", metadata={"doc": _("The copyright holder.")})
    source_label: str = field(default="", metadata={"doc": _("Optional source model label, for example Open Source.")})
    license_text: str = field(default="", metadata={"doc": _("Optional license label, for example AGPL-3.0.")})
    license_url: str = field(default="", metadata={"doc": _("Optional URL for the license label.")})
    separator: str = field(
        default="\u00b7", metadata={"doc": _("Separator between legal metadata parts.")}
    )  # Middle dot
    rights_text: str = field(default="", metadata={"doc": _("Optional rights statement.")})


@dataclass
class LogoConfig:
    """
    Configuration for the logo component.

    Renders a brand logo as an image, SVG, or icon.

    Attributes:
        url: Static, absolute, root-relative, or data URL for image/svg logos.
        url_dark: Optional dark-theme URL for image/svg logos.
        alt: Accessible text. Empty values make image/svg logos decorative.
        icon: Icon configuration used when type is 'icon'.
        icon_name: Icon name (alternative to icon config).
        icon_size: Icon size (alternative to icon config).
        height: CSS height for image/svg logos.
        width: Optional CSS width for image/svg logos.

    """

    __example__ = """
        LogoConfig(
            url="img/logo.svg",
            url_dark="img/logo-dark.svg",
            alt="Company Logo",
            height="2rem",
        )
        """

    url: str = field(
        default="", metadata={"doc": _("Static, absolute, root-relative, or data URL for image/svg logos.")}
    )
    url_dark: str = field(default="", metadata={"doc": _("Optional dark-theme URL for image/svg logos.")})
    alt: str = field(default="", metadata={"doc": _("Accessible text. Empty values make image/svg logos decorative.")})
    icon: IconConfig | None = field(default=None, metadata={"doc": _("Icon configuration used when type is 'icon'.")})
    icon_name: str = field(default="", metadata={"doc": _("Icon name (alternative to icon config).")})
    icon_size: str = field(default="", metadata={"doc": _("Icon size (alternative to icon config).")})
    height: str = field(default="2rem", metadata={"doc": _("CSS height for image/svg logos.")})
    width: str = field(default="", metadata={"doc": _("Optional CSS width for image/svg logos.")})


@dataclass
class CornerRibbonConfig:
    """
    Configuration for the corner_ribbon component.

    Renders a decorative diagonal ribbon in a browser corner.

    Attributes:
        text: The text displayed in the ribbon.
        position: Corner position: 'top-right', 'top-left', 'bottom-right', 'bottom-left'. Invalid values fall back to 'top-right'.
        color: Color variant: 'primary', 'success', 'warning', 'danger', 'info'. Invalid values fall back to 'primary'.

    """

    __example__ = """
        CornerRibbonConfig(
            text="Beta",
            position="top-right",
            color="warning",
        )
        """

    text: str = field(metadata={"doc": _("The text displayed in the ribbon.")})
    position: Literal["top-right", "top-left", "bottom-right", "bottom-left"] = field(
        default="top-right",
        metadata={
            "doc": _(
                "Corner position: 'top-right', 'top-left', 'bottom-right', 'bottom-left'. Invalid values fall back to 'top-right'."
            )
        },
    )
    color: Literal["primary", "success", "warning", "danger", "info"] = field(
        default="primary",
        metadata={
            "doc": _(
                "Color variant: 'primary', 'success', 'warning', 'danger', 'info'. Invalid values fall back to 'primary'."
            )
        },
    )


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

    title: str = field(metadata={"doc": _("Marker title/label.")})
    lat: float = field(metadata={"doc": _("Latitude coordinate.")})
    lon: float = field(metadata={"doc": _("Longitude coordinate.")})
    description: str = field(default="", metadata={"doc": _("Optional popup description.")})
    value: int | float | None = field(default=None, metadata={"doc": _("Optional numeric value (for circle markers).")})


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

    """

    __example__ = """
        GeoMapDatasetConfig(
            name="population",
            type="circle",
            min=100000,
            max=5000000,
            data=[
                GeoMapMarkerConfig(title="Berlin", lat=52.52, lon=13.405, value=3769000),
                GeoMapMarkerConfig(title="Munich", lat=48.135, lon=11.582, value=1488000),
            ],
        )
        """

    name: str = field(metadata={"doc": _("Dataset name.")})
    type: Literal["marker", "circle"] = field(
        default="marker", metadata={"doc": _("Marker type ('marker' or 'circle').")}
    )
    data: list[GeoMapMarkerConfig] = field(default_factory=list, metadata={"doc": _("List of marker configurations.")})
    min: int | float = field(default=0, metadata={"doc": _("Minimum value for circle scaling.")})
    max: int | float = field(default=100, metadata={"doc": _("Maximum value for circle scaling.")})


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

    """

    __example__ = """
        GeoMapConfig(
            initial_coords=[52.52, 13.405],
            initial_zoom=10,
            datasets=[
                GeoMapDatasetConfig(
                    name="offices",
                    type="marker",
                    data=[
                        GeoMapMarkerConfig(title="HQ", lat=52.52, lon=13.405),
                    ],
                ),
            ],
        )
        """

    initial_coords: list[float] = field(
        default_factory=lambda: [52.52, 13.405], metadata={"doc": _("Starting map center [lat, lon].")}
    )
    initial_zoom: int = field(default=8, metadata={"doc": _("Starting zoom level.")})
    map_height: int = field(default=36, metadata={"doc": _("The height of the map in 'rem'.")})
    datasets: list[GeoMapDatasetConfig] = field(
        default_factory=list, metadata={"doc": _("List of data layers to display.")}
    )


@dataclass
class ChartSeriesConfig:
    """
    Configuration for a chart data series.

    Attributes:
        name: Series name (shown in legend).
        data: Data points for this series.

    """

    name: str = field(metadata={"doc": _("Series name (shown in legend).")})
    data: list[int | float] = field(metadata={"doc": _("Data points for this series.")})


@dataclass
class ChartConfig:
    """
    Configuration for chart components (bar_chart, line_chart).

    Attributes:
        title: Chart title.
        x_axis_legend: Labels for X-axis categories.
        series: Series names (for legend).
        data: Data for each series (list of lists).

    """

    __example__ = """
        ChartConfig(
            title="Weekly Sales",
            x_axis_legend=["Mon", "Tue", "Wed", "Thu", "Fri"],
            series=["Online", "In-Store"],
            data=[
                [120, 150, 180, 130, 200],  # Online
                [80, 90, 110, 100, 120],    # In-Store
            ],
        )
        """

    title: str = field(default="", metadata={"doc": _("Chart title.")})
    x_axis_legend: list[str] = field(default_factory=list, metadata={"doc": _("Labels for X-axis categories.")})
    series: list[str] = field(default_factory=list, metadata={"doc": _("Series names (for legend).")})
    data: list[list[int | float]] = field(
        default_factory=list, metadata={"doc": _("Data for each series (list of lists).")}
    )


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

    """

    __example__ = """
        LiveContentConfig(
            tag_id="live-stats",
            request_url="/api/stats/",
            interval=30,
            initial_content="Loading...",
        )
        """

    tag_id: str = field(default="", metadata={"doc": _("Unique ID for JavaScript/CSS targeting.")})
    request_url: str = field(default="", metadata={"doc": _("URL for content updates.")})
    interval: int = field(default=10, metadata={"doc": _("Update interval in seconds.")})
    initial_content: str = field(default="", metadata={"doc": _("Initial content before first update.")})


@dataclass
class WebSocketConfig:
    """
    Configuration for the insight_websocket component.

    Renders a WebSocket-connected container using HTMX ws extension.

    Attributes:
        tag_id: Container ID.
        request_url: WebSocket endpoint URL.
        initial_content: Initial content.

    """

    __example__ = """
        WebSocketConfig(
            tag_id="chat-stream",
            request_url="/ws/chat/",
            initial_content="Connecting...",
        )
        """

    tag_id: str = field(default="", metadata={"doc": _("Container ID.")})
    request_url: str = field(default="", metadata={"doc": _("WebSocket endpoint URL.")})
    initial_content: str = field(default="", metadata={"doc": _("Initial content.")})
