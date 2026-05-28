"""Configuration classes for layout components."""

from dataclasses import dataclass
from typing import Literal

from insight_ui.configs.base import ActionConfig, IconConfig


@dataclass
class PageHeaderConfig:
    """
    Configuration for the page_header component.

    Renders a page header with title and optional description.

    Attributes:
        title: Page title (rendered as h1).
        description: Optional description (string or list of paragraphs).

    Example:
        >>> header = PageHeaderConfig(
        ...     title="Dashboard",
        ...     description="Welcome to your personal dashboard.",
        ... )

    """

    title: str
    description: str | list[str] = ""


@dataclass
class HeadingDecorationConfig:
    """
    Configuration for the heading_decoration component.

    Renders the decorative transition between header and content.

    Attributes:
        style: Decoration style ('waves', 'image', 'gradient', 'none').
        color: CSS color value.
        image_url: Background image URL (for 'image' style).
        height: Decoration height in pixels.

    Example:
        >>> decoration = HeadingDecorationConfig(
        ...     style="waves",
        ...     color="var(--color-insight-primary)",
        ...     height=90,
        ... )

    """

    style: Literal["waves", "image", "gradient", "none"] = "waves"
    color: str = "var(--color-insight-primary, #3b82f6)"
    image_url: str = ""
    height: int = 90

    def __post_init__(self) -> None:
        """Validate height is positive."""
        self.height = max(self.height, 1)


@dataclass
class ArticleConfig:
    """
    Configuration for the article component.

    Renders text in newspaper-style multi-column layout.

    Attributes:
        content: Article text content (may include HTML).
        columns: Number of columns.
        column_gap: CSS gap between columns.
        title: Optional article title.

    Example:
        >>> article = ArticleConfig(
        ...     title="About Us",
        ...     content="<p>Our company was founded in...</p>",
        ...     columns=2,
        ...     column_gap="2rem",
        ... )

    """

    content: str
    columns: int = 2
    column_gap: str = "2rem"
    title: str = ""


@dataclass
class BadgeConfig:
    """
    Configuration for a badge element.

    Used in hero sections and other components.

    Attributes:
        text: Badge text.
        icon: Optional icon configuration.

    """

    text: str
    icon: IconConfig | None = None


@dataclass
class HeroConfig:
    """
    Configuration for the hero component.

    Renders a prominent banner section.

    Attributes:
        title: Hero title (rendered as h1).
        subtitle: Subtitle below the title.
        description: Description text.
        cta_primary: Primary call-to-action button.
        cta_secondary: Secondary call-to-action button.
        background_image_url: Background image URL.
        badge: Optional badge displayed above the title.

    Example:
        >>> hero = HeroConfig(
        ...     title="Welcome to Our Platform",
        ...     subtitle="The Future of Web Development",
        ...     description="Build amazing applications with modern tools.",
        ...     cta_primary=ActionConfig(text="Get Started", url="/signup/", type="primary"),
        ...     cta_secondary=ActionConfig(text="Learn More", url="/docs/", type="secondary"),
        ...     badge=BadgeConfig(text="New!", icon=IconConfig(name="sparkles")),
        ... )

    """

    title: str = ""
    subtitle: str = ""
    description: str = ""
    cta_primary: ActionConfig | None = None
    cta_secondary: ActionConfig | None = None
    background_image_url: str = ""
    badge: BadgeConfig | None = None
