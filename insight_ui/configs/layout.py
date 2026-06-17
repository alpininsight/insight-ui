"""Configuration classes for layout components."""

from dataclasses import dataclass, field

from django.utils.translation import gettext_lazy as _

from insight_ui.configs.base import ActionConfig
from insight_ui.configs.utils import BadgeConfig


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
        badge_config: A badge with icon and text.

    """

    __example__ = """
        HeroConfig(
            title="Welcome to Our Platform",
            subtitle="The Future of Web Development",
            description="Build amazing applications with modern tools.",
            cta_primary=ActionConfig(text="Get Started", url="/signup/", type="primary"),
            cta_secondary=ActionConfig(text="Learn More", url="/docs/", type="secondary"),
            badge_config=BadgeConfig(text="New!", icon=IconConfig(name="sparkles")),
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
    badge_config: BadgeConfig | None = field(default=None, metadata={"doc": _("A badge with icon and text.")})
