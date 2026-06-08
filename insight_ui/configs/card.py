"""Configuration classes for card components."""

from dataclasses import dataclass, field
from typing import Literal

from django.utils.translation import gettext_lazy as _

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
        content: Main card content.
        subtitle: Optional subtitle.
        image: Optional card image.
        actions: List of action buttons.

    """

    __example__ = """
        CardConfig(
            title="Welcome",
            subtitle="Getting Started",
            content="Learn how to use our platform.",
            actions=[
                ActionConfig(text="Learn More", url="/docs/", type="primary"),
            ],
        )
        """

    title: str = field(metadata={"doc": _("Card title.")})
    content: str = field(metadata={"doc": _("Main card content.")})
    subtitle: str = field(default="", metadata={"doc": _("Optional subtitle.")})
    image: ImageConfig | None = field(default=None, metadata={"doc": _("Optional card image.")})
    actions: list[ActionConfig] = field(default_factory=list, metadata={"doc": _("List of action buttons.")})


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

    """

    __example__ = """
        AppCardConfig(
            title="Analytics Dashboard",
            content="Real-time metrics and insights.",
            request_url="/apps/analytics/",
            image=ImageConfig(url="img/analytics.png", alt="Analytics"),
            tags=["New", "Featured"],
            actions=[ActionConfig(text="Open", url="/apps/analytics/", type="primary")],
        )
        """

    title: str = field(metadata={"doc": _("Card title.")})
    content: str = field(metadata={"doc": _("Card description.")})
    request_url: str = field(default="", metadata={"doc": _("URL when title is clicked.")})
    image: ImageConfig | None = field(default=None, metadata={"doc": _("Card image (displayed as square at top).")})
    tags: list[str] = field(default_factory=list, metadata={"doc": _("List of tag labels.")})
    actions: list[ActionConfig] = field(default_factory=list, metadata={"doc": _("List of action buttons.")})


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

    """

    __example__ = """
        FlipCardConfig(
            title="Product Name",
            content="Detailed description shown on hover.",
            image=ImageConfig(url="img/product.png", alt="Product"),
            tags=["Sale", "-20%"],
            actions=[ActionConfig(text="Buy", url="/buy/", type="primary")],
        )
        """

    title: str = field(metadata={"doc": _("Card title.")})
    content: str = field(metadata={"doc": _("Back side content.")})
    request_url: str = field(default="", metadata={"doc": _("URL when title is clicked.")})
    image: ImageConfig | None = field(default=None, metadata={"doc": _("Front side image.")})
    tags: list[str] = field(default_factory=list, metadata={"doc": _("List of tag labels.")})
    actions: list[ActionConfig] = field(default_factory=list, metadata={"doc": _("List of action buttons.")})


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

    title: str = field(default="", metadata={"doc": _("Item title.")})
    content: str = field(default="", metadata={"doc": _("Item content/description.")})
    image: ImageConfig | None = field(default=None, metadata={"doc": _("Optional image configuration.")})
    url: str = field(default="", metadata={"doc": _("Optional link URL.")})


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

    """

    __example__ = """
        CardCarouselConfig(
            carousel_items=[
                CarouselItemConfig(title="Item 1", content="Description 1"),
                CarouselItemConfig(title="Item 2", content="Description 2"),
            ],
            autoplay=True,
            show_dots=True,
            items_per_slide=3,
        )
        """

    carousel_items: list[CardConfig] = field(default_factory=list, metadata={"doc": _("List of items to display.")})
    autoplay: bool = field(default=False, metadata={"doc": _("Auto-advance slides every 5 seconds.")})
    show_dots: bool = field(default=True, metadata={"doc": _("Show pagination dots.")})
    show_index: bool = field(default=False, metadata={"doc": _("Show current/total index.")})
    items_per_slide: int = field(default=1, metadata={"doc": _("Number of items visible per slide.")})


@dataclass
class ImageCarouselItemConfig:
    """
    Configuration for an image carousel item.

    Attributes:
        url: Image URL.
        alt: Image alt text.
        description: Optional caption/description.

    """

    url: str = field(metadata={"doc": _("Image URL.")})
    alt: str = field(default="", metadata={"doc": _("Image alt text.")})
    description: str = field(default="", metadata={"doc": _("Optional caption/description.")})


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

    """

    __example__ = """
        ImageCarouselConfig(
            carousel_items=[
                ImageCarouselItemConfig(url="/img/photo1.jpg", alt="Photo 1"),
                ImageCarouselItemConfig(url="/img/photo2.jpg", alt="Photo 2"),
            ],
            autoplay=True,
        )
        """

    carousel_items: list[ImageCarouselItemConfig] = field(
        default_factory=list, metadata={"doc": _("List of image configurations.")}
    )
    autoplay: bool = field(default=False, metadata={"doc": _("Auto-advance slides.")})
    show_dots: bool = field(default=True, metadata={"doc": _("Show pagination dots.")})
    show_index: bool = field(default=False, metadata={"doc": _("Show current/total index.")})
    items_per_slide: int = field(default=1, metadata={"doc": _("Images visible per slide.")})


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

    """

    __example__ = """
        ThreeDCarouselConfig(
            tag_id="product-showcase",
            carousel_items=[...],
            velocity=1000,
            tilt=15,
            face_camera=True,
        )
        """

    tag_id: str = field(metadata={"doc": _("Unique ID for the carousel.")})
    carousel_items: list[CarouselItemConfig] = field(
        default_factory=list, metadata={"doc": _("List of items to display.")}
    )
    velocity: int = field(default=1000, metadata={"doc": _("Rotation speed.")})
    tilt: int = field(default=0, metadata={"doc": _("Camera tilt angle.")})
    face_camera: bool = field(default=False, metadata={"doc": _("If True, items always face the camera.")})


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

    """

    __example__ = """
        ToggleViewConfig(
            tag_id="products-view",
            cards=products_list,
            table_config=TableConfig(headers, rows),
            view_radio_config=RadioBlockConfig(
                name="view",
                items=[
                    RadioItemConfig(tag_id="card", value="card", icon=IconConfig(name="cards")),
                    RadioItemConfig(tag_id="table", value="table", icon=IconConfig(name="list")),
                ],
            ),
            current_view="card",
        )
        """

    tag_id: str = field(metadata={"doc": _("Unique ID for the component.")})
    cards: list[CardConfig] = field(default_factory=list, metadata={"doc": _("The cards to be displayed.")})
    table_config: TableConfig | None = field(default=None, metadata={"doc": _("Configuration of the table view.")})
    view_radio_config: RadioBlockConfig | None = field(
        default=None, metadata={"doc": _("Radio block config for view switching.")}
    )
    current_view: Literal["card", "table", "carousel"] = field(
        default="card", metadata={"doc": _("Currently active view ('card', 'table', 'carousel').")}
    )
