"""Configuration classes for layout components."""

from dataclasses import dataclass, field
from typing import Literal

from django.utils.translation import gettext_lazy as _

from insight_ui.configs.base import ActionConfig, IconConfig


@dataclass
class PageHeaderConfig:
    """
    Configuration for the page_header component.

    Renders a page header with title and optional description.

    Attributes:
        title: The page title, displayed as h1 in white text.
        description: An optional description below the title.

    """

    __example__ = """
        PageHeaderConfig(
            title="Dashboard",
            description="Welcome to your personal dashboard.",
        )
        """

    title: str = field(metadata={"doc": _("The page title, displayed as h1 in white text.")})
    description: str | list[str] = field(default="", metadata={"doc": _("An optional description below the title.")})


@dataclass
class HeadingDecorationConfig:
    """
    Configuration for the heading_decoration component.

    Renders the decorative transition between header and content.

    Attributes:
        style: Decoration style: 'waves', 'image', 'gradient', or 'none'. Unknown values fall back to 'waves'.
        color: Optional CSS color override. By default the component follows --color-insight-primary.
        image_url: Background image URL used when style is 'image'.
        height: Decoration height in pixels.

    """

    __example__ = """
        HeadingDecorationConfig(
            style="gradient",
            color="var(--color-insight-primary)",
            height=72,
        )
        """

    style: Literal["waves", "image", "gradient", "none"] = field(
        default="waves",
        metadata={
            "doc": _("Decoration style: 'waves', 'image', 'gradient', or 'none'. Unknown values fall back to 'waves'.")
        },
    )
    color: str = field(
        default="var(--color-insight-primary, #3b82f6)",
        metadata={"doc": _("Optional CSS color override. By default the component follows --color-insight-primary.")},
    )
    image_url: str = field(default="", metadata={"doc": _("Background image URL used when style is 'image'.")})
    height: int = field(default=90, metadata={"doc": _("Decoration height in pixels.")})

    def __post_init__(self) -> None:
        """Validate height is positive."""
        self.height = max(self.height, 1)


@dataclass
class ArticleConfig:
    """
    Configuration for the article component.

    Renders text in newspaper-style multi-column layout.

    Attributes:
        content: The text content of the article (can contain HTML).
        columns: The number of columns for the CSS columns layout.
        column_gap: The gap between the columns (CSS unit).
        title: An optional title above the article.

    """

    __example__ = """
        ArticleConfig(
            title="About Us",
            content="<p>Our company was founded in...</p>",
            columns=2,
            column_gap="2rem",
        )
        """

    content: str = field(metadata={"doc": _("The text content of the article (can contain HTML).")})
    columns: int = field(default=2, metadata={"doc": _("The number of columns for the CSS columns layout.")})
    column_gap: str = field(default="2rem", metadata={"doc": _("The gap between the columns (CSS unit).")})
    title: str = field(default="", metadata={"doc": _("An optional title above the article.")})


@dataclass
class BadgeConfig:
    """
    Configuration for a badge element.

    Used in hero sections and other components.

    Attributes:
        text: Badge label.
        icon: An optional icon displayed before the text.

    """

    __example__ = """
        BadgeConfig("/newsletter", "Subscribe to Newsletter")
    """

    text: str = field(metadata={"doc": _("Badge label.")})
    icon: IconConfig | None = field(default=None, metadata={"doc": _("An optional icon displayed before the text.")})


@dataclass
class HeroConfig:
    """
    Configuration for the hero component.

    Renders a prominent banner section.

    Attributes:
        title: Title of the Hero section.
        subtitle: Subtitle of the Hero section, displayed below the title.
        description: Description of the Hero section, displayed below the title and subtitle.
        cta_primary: Primary 'Call-to-Action' button.
        cta_secondary: Secondary 'Call-to-Action' button.
        background_image_url: URL of the background image.
        badge: A badge with icon and text.

    """

    __example__ = """
        HeroConfig(
            title="Welcome to Our Platform",
            subtitle="The Future of Web Development",
            description="Build amazing applications with modern tools.",
            cta_primary=ActionConfig(text="Get Started", url="/signup/", type="primary"),
            cta_secondary=ActionConfig(text="Learn More", url="/docs/", type="secondary"),
            badge=BadgeConfig(text="New!", icon=IconConfig(name="sparkles")),
        )
        """

    title: str = field(default="", metadata={"doc": _("Title of the Hero section.")})
    subtitle: str = field(default="", metadata={"doc": _("Subtitle of the Hero section, displayed below the title.")})
    description: str = field(
        default="", metadata={"doc": _("Description of the Hero section, displayed below the title and subtitle.")}
    )
    cta_primary: ActionConfig | None = field(default=None, metadata={"doc": _("Primary 'Call-to-Action' button.")})
    cta_secondary: ActionConfig | None = field(default=None, metadata={"doc": _("Secondary 'Call-to-Action' button.")})
    background_image_url: str = field(default="", metadata={"doc": _("URL of the background image.")})
    badge: BadgeConfig | None = field(default=None, metadata={"doc": _("A badge with icon and text.")})
