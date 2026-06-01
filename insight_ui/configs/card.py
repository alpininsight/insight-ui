"""Configuration classes for card components."""

from dataclasses import dataclass, field
from typing import Literal

from insight_ui.configs.base import ActionConfig, ImageConfig
from insight_ui.configs.input import RadioBlockConfig
from insight_ui.configs.list import TableConfig


@dataclass
class CardConfig:
    """
    Configuration for the card component.

    Renders a card with 16:9 aspect ratio (business card style).

    Attributes:
        title: Card title.
        subtitle: Optional subtitle.
        content: Main card content.
        image: Optional card image.
        actions: List of action buttons.

    Example:
        >>> card = CardConfig(
        ...     title="Welcome",
        ...     subtitle="Getting Started",
        ...     content="Learn how to use our platform.",
        ...     actions=[
        ...         ActionConfig(text="Learn More", url="/docs/", type="primary"),
        ...     ],
        ... )

    """

    title: str
    content: str
    subtitle: str = ""
    image: ImageConfig | None = None
    actions: list[ActionConfig] = field(default_factory=list)


@dataclass
class AppCardConfig:
    """
    Configuration for the app_card component.

    Renders a vertically-oriented card ideal for app/product listings.

    Attributes:
        title: Card title.
        content: Card description.
        request_url: URL when title is clicked.
        image: Card image (displayed as square at top).
        tags: List of tag labels.
        actions: List of action buttons.

    Example:
        >>> app = AppCardConfig(
        ...     title="Analytics Dashboard",
        ...     content="Real-time metrics and insights.",
        ...     request_url="/apps/analytics/",
        ...     image=ImageConfig(url="img/analytics.png", alt="Analytics"),
        ...     tags=["New", "Featured"],
        ...     actions=[ActionConfig(text="Open", url="/apps/analytics/", type="primary")],
        ... )

    """

    title: str
    content: str
    request_url: str = ""
    image: ImageConfig | None = None
    tags: list[str] = field(default_factory=list)
    actions: list[ActionConfig] = field(default_factory=list)


@dataclass
class FlipCardConfig:
    """
    Configuration for the flip_card component.

    Renders a card that rotates 180° on hover to show back content.

    Attributes:
        title: Card title.
        content: Back side content.
        request_url: URL when title is clicked.
        image: Front side image.
        tags: List of tag labels.
        actions: List of action buttons.

    Example:
        >>> flip_card = FlipCardConfig(
        ...     title="Product Name",
        ...     content="Detailed description shown on hover.",
        ...     image=ImageConfig(url="img/product.png", alt="Product"),
        ...     tags=["Sale", "-20%"],
        ...     actions=[ActionConfig(text="Buy", url="/buy/", type="primary")],
        ... )

    """

    title: str
    content: str
    request_url: str = ""
    image: ImageConfig | None = None
    tags: list[str] = field(default_factory=list)
    actions: list[ActionConfig] = field(default_factory=list)


@dataclass
class CarouselItemConfig:
    """
    Configuration for a carousel item.

    Attributes:
        title: Item title.
        content: Item content/description.
        image: Optional image configuration.
        url: Optional link URL.

    """

    title: str = ""
    content: str = ""
    image: ImageConfig | None = None
    url: str = ""


@dataclass
class CardCarouselConfig:
    """
    Configuration for the carousel (card carousel) component.

    Renders a card carousel with navigation.

    Attributes:
        carousel_items: List of items to display.
        autoplay: Auto-advance slides every 5 seconds.
        show_dots: Show pagination dots.
        show_index: Show current/total index.
        items_per_slide: Number of items visible per slide.

    Example:
        >>> carousel = CardCarouselConfig(
        ...     carousel_items=[
        ...         CarouselItemConfig(title="Item 1", content="Description 1"),
        ...         CarouselItemConfig(title="Item 2", content="Description 2"),
        ...     ],
        ...     autoplay=True,
        ...     show_dots=True,
        ...     items_per_slide=3,
        ... )

    """

    carousel_items: list[CardConfig] = field(default_factory=list)
    autoplay: bool = False
    show_dots: bool = True
    show_index: bool = False
    items_per_slide: int = 1


@dataclass
class ImageCarouselItemConfig:
    """
    Configuration for an image carousel item.

    Attributes:
        url: Image URL.
        alt: Image alt text.
        description: Optional caption/description.

    """

    url: str
    alt: str = ""
    description: str = ""


@dataclass
class ImageCarouselConfig:
    """
    Configuration for the image_carousel component.

    Renders an image-focused carousel.

    Attributes:
        carousel_items: List of image configurations.
        autoplay: Auto-advance slides.
        show_dots: Show pagination dots.
        show_index: Show current/total index.
        items_per_slide: Images visible per slide.

    Example:
        >>> gallery = ImageCarouselConfig(
        ...     carousel_items=[
        ...         ImageCarouselItemConfig(url="/img/photo1.jpg", alt="Photo 1"),
        ...         ImageCarouselItemConfig(url="/img/photo2.jpg", alt="Photo 2"),
        ...     ],
        ...     autoplay=True,
        ... )

    """

    carousel_items: list[ImageCarouselItemConfig] = field(default_factory=list)
    autoplay: bool = False
    show_dots: bool = True
    show_index: bool = False
    items_per_slide: int = 1


@dataclass
class ThreeDCarouselConfig:
    """
    Configuration for the three_d_carousel component.

    Renders items in a 3D circular arrangement.

    Attributes:
        tag_id: Unique ID for the carousel.
        carousel_items: List of items to display.
        velocity: Rotation speed.
        tilt: Camera tilt angle.
        face_camera: If True, items always face the camera.

    Example:
        >>> carousel_3d = ThreeDCarouselConfig(
        ...     tag_id="product-showcase",
        ...     carousel_items=[...],
        ...     velocity=1000,
        ...     tilt=15,
        ...     face_camera=True,
        ... )

    """

    tag_id: str
    carousel_items: list[CarouselItemConfig] = field(default_factory=list)
    velocity: int = 1000
    tilt: int = 0
    face_camera: bool = False


@dataclass
class ToggleViewConfig:
    """
    Configuration for the toggle_view component.

    Allows switching between different data views (cards, table, carousel).

    Attributes:
        tag_id: Unique ID for the component.
        cards: The cards to be displayed.
        table_config: Configuration of the table view.
        view_radio_config: Radio block config for view switching.
        current_view: Currently active view ('card', 'table', 'carousel').

    Example:
        >>> toggle = ToggleViewConfig(
        ...     tag_id="products-view",
        ...     cards=products_list,
        ...     table_config=TableConfig(headers, rows),
        ...     view_radio_config=RadioBlockConfig(
        ...         name="view",
        ...         items=[
        ...             RadioItemConfig(tag_id="card", value="card", icon=IconConfig(name="cards")),
        ...             RadioItemConfig(tag_id="table", value="table", icon=IconConfig(name="list")),
        ...         ],
        ...     ),
        ...     current_view="card",
        ... )

    """

    tag_id: str
    cards: list[CardConfig] = field(default_factory=list)
    table_config: TableConfig | None = None
    view_radio_config: RadioBlockConfig | None = None
    current_view: Literal["card", "table", "carousel"] = "card"
