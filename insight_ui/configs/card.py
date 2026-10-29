# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Configuration classes for card components."""

from dataclasses import dataclass, field
from typing import Any

from django.utils.translation import gettext_lazy as _

from insight_ui.configs.base import ImageConfig
from insight_ui.configs.input import ButtonConfig, RadioBlockConfig
from insight_ui.configs.list import TableConfig
from insight_ui.configs.types import (
    HeadingLevel,
    ToggleViewType,
    validate_heading_level,
    validate_not_empty,
    validate_toggle_view_type,
    validate_urls,
)
from insight_ui.configs.utils import BadgeConfig


@dataclass
class CardConfig:
    """Configuration for the card component.

    Renders a card with 16:9 aspect ratio (business card style).

    Attributes:
        title: Card title.
        content: Main card content.
        subtitle: Optional subtitle.
        image: Optional card image.
        actions: List of action buttons.
        heading_level: Heading level of the title.

    """

    __example__ = """
        CardConfig(
            title="Welcome",
            subtitle="Getting Started",
            content="Learn how to use our platform.",
            actions=[
                ButtonConfig(label="Learn More", request_url="/docs/", color="primary"),
            ],
        )
        """

    title: str = field(metadata={"doc": _("Card title.")})
    content: str = field(metadata={"doc": _("Main card content.")})
    subtitle: str = field(default="", metadata={"doc": _("Optional subtitle.")})
    image: ImageConfig | None = field(default=None, metadata={"doc": _("Optional card image.")})
    actions: list[ButtonConfig] = field(default_factory=list, metadata={"doc": _("List of action buttons.")})
    heading_level: HeadingLevel = field(default=3, metadata={"doc": _("Heading level of the title.")})

    def __post_init__(self) -> None:
        """Validate heading_level after initialization."""
        validate_heading_level(self.heading_level)


@dataclass
class AppCardConfig:
    """Configuration for the app_card component.

    Renders a vertically-oriented card ideal for app/product listings.

    Attributes:
        title: Card title.
        content: Card description.
        request_url: The URL to be called when title is clicked.
        image: Card image (displayed as square at top).
        tags: List of badge configurations for tags.
        actions: List of action buttons.
        heading_level: Heading level of the title.

    """

    __example__ = """
        AppCardConfig(
            title="Analytics Dashboard",
            content="Real-time metrics and insights.",
            request_url="/apps/analytics/",
            image=ImageConfig(url="img/analytics.png", alt="Analytics"),
            tags=[BadgeConfig(label="New", color="success"), BadgeConfig(label="Featured", color="primary")],
            actions=[ButtonConfig(label="Open", request_url="/apps/analytics/", color="primary")],
        )
        """

    title: str = field(metadata={"doc": _("Card title.")})
    content: str = field(metadata={"doc": _("Card description.")})
    request_url: str = field(default="", metadata={"doc": _("The URL to be called when title is clicked.")})
    image: ImageConfig | None = field(default=None, metadata={"doc": _("Card image (displayed as square at top).")})
    tags: list[BadgeConfig] = field(default_factory=list, metadata={"doc": _("List of badge configurations for tags.")})
    actions: list[ButtonConfig] = field(default_factory=list, metadata={"doc": _("List of action buttons.")})
    heading_level: HeadingLevel = field(default=3, metadata={"doc": _("Heading level of the title.")})

    def __post_init__(self) -> None:
        """Validate heading_level after initialization."""
        validate_urls(self)
        validate_heading_level(self.heading_level)


@dataclass
class FlipCardConfig:
    """Configuration for the flip_card component.

    Renders a card that rotates 180° via button click to show back content.

    Attributes:
        title: Card title.
        content: Front side content.
        back_title: Back side title.
        back_content: Back side content.
        back_actions: Back side action buttons.
        request_url: The URL to be called when title is clicked.
        image: Front side image.
        tags: List of badge configurations for tags.
        actions: Front side action buttons.
        heading_level: Heading level of the front and back titles.

    """

    __example__ = """
        FlipCardConfig(
            title="Product Name",
            content="Short description on the front.",
            back_title="Details",
            back_content="Extended product information and specs.",
            back_actions=[ButtonConfig(label="Contact", request_url="/contact/", variant="outline")],
            image=ImageConfig(url="img/product.png", alt="Product"),
            tags=[BadgeConfig(label="Sale", color="danger"), BadgeConfig(label="-20%", color="warning")],
            actions=[ButtonConfig(label="Buy", request_url="/buy/", color="primary")],
        )
        """

    title: str = field(metadata={"doc": _("Card title.")})
    content: str = field(metadata={"doc": _("Front side content.")})
    back_title: str = field(default="", metadata={"doc": _("Back side title.")})
    back_content: str = field(default="", metadata={"doc": _("Back side content.")})
    back_actions: list[ButtonConfig] = field(default_factory=list, metadata={"doc": _("Back side action buttons.")})
    request_url: str = field(default="", metadata={"doc": _("The URL to be called when title is clicked.")})
    image: ImageConfig | None = field(default=None, metadata={"doc": _("Front side image.")})
    tags: list[BadgeConfig] = field(default_factory=list, metadata={"doc": _("List of badge configurations for tags.")})
    actions: list[ButtonConfig] = field(default_factory=list, metadata={"doc": _("Front side action buttons.")})
    heading_level: HeadingLevel = field(default=3, metadata={"doc": _("Heading level of the front and back titles.")})

    def __post_init__(self) -> None:
        """Validate heading_level after initialization."""
        validate_urls(self)
        validate_heading_level(self.heading_level)


@dataclass
class CarouselConfig:
    """Configuration for the carousel component.

    Renders any items as pages that can be browsed. Each item is rendered with item_template;
    the default shows CardConfig items as cards.

    Attributes:
        items: Items to display, e.g. CardConfig, CarouselImageConfig or model instances.
        item_template: Template that renders one item; gets item and the page context.
        tag_id: Optional unique ID of the carousel.
        label: Accessible name of the carousel.
        autoplay: Auto-advance pages every 5 seconds.
        show_dots: Show a dot per page.
        show_index: Show the current and total page.
        items_per_slide: Maximum number of items visible per page.
        min_item_width: Minimum width of an item, e.g. "16rem"; narrow screens then show fewer items per page.

    """

    __example__ = """
        CarouselConfig(
            items=Product.objects.filter(featured=True),
            item_template="shop/product_slide.html",
            label="Featured products",
            items_per_slide=3,
            min_item_width="16rem",
        )
        """

    items: list[Any] = field(
        default_factory=list,
        metadata={"doc": _("Items to display, e.g. CardConfig, CarouselImageConfig or model instances.")},
    )
    item_template: str = field(
        default="insight_ui/components/items/card_item.html",
        metadata={"doc": _("Template that renders one item; gets item and the page context.")},
    )
    tag_id: str = field(default="", metadata={"doc": _("Optional unique ID of the carousel.")})
    label: str = field(default="", metadata={"doc": _("Accessible name of the carousel.")})
    autoplay: bool = field(default=False, metadata={"doc": _("Auto-advance pages every 5 seconds.")})
    show_dots: bool = field(default=True, metadata={"doc": _("Show a dot per page.")})
    show_index: bool = field(default=False, metadata={"doc": _("Show the current and total page.")})
    items_per_slide: int = field(default=1, metadata={"doc": _("Maximum number of items visible per page.")})
    min_item_width: str = field(
        default="",
        metadata={"doc": _('Minimum width of an item, e.g. "16rem"; narrow screens then show fewer items per page.')},
    )

    def __post_init__(self) -> None:
        """Require a template and at least one item per page."""
        validate_not_empty(self, "item_template")
        if self.items_per_slide < 1:
            msg = f"CarouselConfig needs items_per_slide of at least 1, got {self.items_per_slide}."
            raise ValueError(msg)


@dataclass
class CarouselImageConfig:
    """An image shown by the carousel with the image item template.

    Attributes:
        url: Image URL.
        alt: Alternative text; empty for a decorative image.
        caption: Optional caption below the image.
        center_caption: Center the caption; suits short captions.

    """

    __example__ = """
        CarouselConfig(
            items=[CarouselImageConfig(url="/img/photo1.jpg", alt="Lake at dawn", caption="Lake Constance")],
            item_template="insight_ui/components/items/image_item.html",
        )
        """

    url: str = field(metadata={"doc": _("Image URL.")})
    alt: str = field(metadata={"doc": _("Alternative text; empty for a decorative image.")})
    caption: str = field(default="", metadata={"doc": _("Optional caption below the image.")})
    center_caption: bool = field(default=False, metadata={"doc": _("Center the caption; suits short captions.")})

    def __post_init__(self) -> None:
        """Reject an empty URL and a URL with a scheme that is not allowed."""
        validate_urls(self)
        validate_not_empty(self, "url")


@dataclass
class RingCarouselConfig:
    """Configuration for the ring_carousel component.

    Arranges any items on a turning ring. Each item is rendered with item_template; the default shows
    CardConfig items as cards.

    Attributes:
        tag_id: Unique ID for the carousel.
        items: Items to display, e.g. CardConfig or model instances.
        item_template: Template that renders one item; gets item and the page context.
        label: Accessible name of the carousel.
        duration: Duration of a turn in milliseconds.
        tilt: Camera tilt in degrees; the ring is seen from above.
        face_camera: Turn every item towards the camera; otherwise items tilt with the ring.

    """

    __example__ = """
        RingCarouselConfig(
            tag_id="product-showcase",
            items=Product.objects.filter(featured=True),
            item_template="shop/product_slide.html",
            tilt=15,
        )
        """

    tag_id: str = field(metadata={"doc": _("Unique ID for the carousel.")})
    items: list[Any] = field(
        default_factory=list, metadata={"doc": _("Items to display, e.g. CardConfig or model instances.")}
    )
    item_template: str = field(
        default="insight_ui/components/items/card_item.html",
        metadata={"doc": _("Template that renders one item; gets item and the page context.")},
    )
    label: str = field(default="", metadata={"doc": _("Accessible name of the carousel.")})
    duration: int = field(default=600, metadata={"doc": _("Duration of a turn in milliseconds.")})
    tilt: int = field(default=0, metadata={"doc": _("Camera tilt in degrees; the ring is seen from above.")})
    face_camera: bool = field(
        default=False,
        metadata={"doc": _("Turn every item towards the camera; otherwise items tilt with the ring.")},
    )

    def __post_init__(self) -> None:
        """Require an ID and a template, and reject a negative duration."""
        validate_not_empty(self, "tag_id", "item_template")
        if self.duration < 0:
            msg = f"RingCarouselConfig needs a duration of at least 0, got {self.duration}."
            raise ValueError(msg)


@dataclass
class ToggleViewConfig:
    """Configuration for the toggle_view component.

    Allows switching between different data views (cards, table, carousel).

    Attributes:
        tag_id: Unique ID for the component.
        cards: The cards to be displayed.
        table: Configuration of the table view.
        view_switch: Radio block for switching the view.
        current_view: Currently active view ('card', 'table', 'carousel').

    """

    __example__ = """
        ToggleViewConfig(
            tag_id="products-view",
            cards=products_list,
            table=TableConfig(headers, rows),
            view_switch=RadioBlockConfig(
                name="view",
                items=[
                    RadioItemConfig(tag_id="card", value="card", icon=IconConfig(name="squares-2x2")),
                    RadioItemConfig(tag_id="table", value="table", icon=IconConfig(name="list-bullet")),
                ],
            ),
            current_view="card",
        )
        """

    tag_id: str = field(metadata={"doc": _("Unique ID for the component.")})
    cards: list[CardConfig] = field(default_factory=list, metadata={"doc": _("The cards to be displayed.")})
    table: TableConfig | None = field(default=None, metadata={"doc": _("Configuration of the table view.")})
    view_switch: RadioBlockConfig | None = field(
        default=None, metadata={"doc": _("Radio block for switching the view.")}
    )
    current_view: ToggleViewType = field(
        default="card", metadata={"doc": _("Currently active view ('card', 'table', 'carousel').")}
    )

    def __post_init__(self) -> None:
        """Require a tag_id and validate current_view after initialization."""
        validate_not_empty(self, "tag_id")
        validate_toggle_view_type(self.current_view, "current_view")
