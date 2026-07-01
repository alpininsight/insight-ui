"""Configuration classes for layout components."""

from dataclasses import dataclass, field

from django.utils.translation import gettext_lazy as _

from insight_ui.configs.input import ButtonConfig
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
class PageConfig:
    """
    Configuration for the page block tag.

    Block-level page container with consistent padding.

    Attributes:
        padding: Inner padding size (xs|s|m|l|xl).
        full_height: Fill the viewport height (min-h-screen).
        v_align: Vertical alignment (start|center|end|between|around|evenly). Enables flex layout.

    """

    __example__ = """
        {% load layout_tags %}
        {% page padding="l" class="bg-primary" %}
            <h1>Hero</h1>
        {% endpage %}

        {# Centered content (useful with full_height) #}
        {% page full_height=True v_align="center" %}
            <div>Centered on page</div>
        {% endpage %}

        {# Content at bottom #}
        {% page full_height=True v_align="end" %}
            <footer>Footer</footer>
        {% endpage %}

        {# Space between elements #}
        {% page full_height=True v_align="between" %}
            <header>Top</header>
            <footer>Bottom</footer>
        {% endpage %}
        """

    padding: str = field(default="m", metadata={"doc": _("Inner padding size (xs|s|m|l|xl).")})
    full_height: bool = field(default=False, metadata={"doc": _("Fill the viewport height (min-h-screen).")})
    v_align: str = field(
        default="",
        metadata={"doc": _("Vertical alignment (start|center|end|between|around|evenly). Enables flex layout.")},
    )


@dataclass
class HBoxConfig:
    """
    Configuration for the hbox block tag.

    Horizontal flex container (row direction).

    Attributes:
        gap: Space between children (xs|s|m|l|xl).
        h_align: Horizontal alignment (start|center|end|between|around|evenly).
        v_align: Vertical alignment (start|center|end|stretch|baseline).
        wrap: Allow flex items to wrap.

    """

    __example__ = """
        {% load layout_tags %}
        {% hbox gap="s" v_align="center" h_align="between" %}
            <span>Left</span>
            <span>Right</span>
        {% endhbox %}
        """

    gap: str = field(default="m", metadata={"doc": _("Space between children (xs|s|m|l|xl).")})
    h_align: str = field(
        default="start", metadata={"doc": _("Horizontal alignment (start|center|end|between|around|evenly).")}
    )
    v_align: str = field(
        default="stretch", metadata={"doc": _("Vertical alignment (start|center|end|stretch|baseline).")}
    )
    wrap: bool = field(default=False, metadata={"doc": _("Allow flex items to wrap.")})


@dataclass
class VBoxConfig:
    """
    Configuration for the vbox block tag.

    Vertical flex container (column direction).

    Attributes:
        gap: Space between children (xs|s|m|l|xl).
        h_align: Horizontal alignment (start|center|end|stretch|baseline).
        v_align: Vertical alignment (start|center|end|between|around|evenly).

    """

    __example__ = """
        {% load layout_tags %}
        {% vbox gap="m" h_align="stretch" %}
            <div>Top</div>
            <div>Bottom</div>
        {% endvbox %}
        """

    gap: str = field(default="m", metadata={"doc": _("Space between children (xs|s|m|l|xl).")})
    h_align: str = field(
        default="stretch", metadata={"doc": _("Horizontal alignment (start|center|end|stretch|baseline).")}
    )
    v_align: str = field(
        default="start", metadata={"doc": _("Vertical alignment (start|center|end|between|around|evenly).")}
    )


@dataclass
class CenterConfig:
    """
    Configuration for the center block tag.

    Centers content horizontally and vertically.

    Attributes:
        padding: Optional inner padding (xs|s|m|l|xl).

    """

    __example__ = """
        {% load layout_tags %}
        {% center padding="m" %}
            <p>Centered content</p>
        {% endcenter %}
        """

    padding: str | None = field(default=None, metadata={"doc": _("Optional inner padding (xs|s|m|l|xl).")})


@dataclass
class StackConfig:
    """
    Configuration for the stack block tag.

    Overlapping elements using CSS Grid.

    Attributes:
        h_align: Horizontal alignment (start|center|end).
        v_align: Vertical alignment (start|center|end).

    """

    __example__ = """
        {% load layout_tags %}
        {% stack v_align="center" h_align="center" %}
            <div class="[grid-area:1/1]">Background</div>
            <div class="[grid-area:1/1]">Foreground</div>
        {% endstack %}
        """

    h_align: str = field(default="center", metadata={"doc": _("Horizontal alignment (start|center|end).")})
    v_align: str = field(default="center", metadata={"doc": _("Vertical alignment (start|center|end).")})


@dataclass
class SpacerConfig:
    """
    Configuration for the spacer simple tag.

    Fixed-size spacer element.

    Attributes:
        size: Spacer size (xs|s|m|l|xl).

    """

    __example__ = """
        {% load layout_tags %}
        {% spacer size="l" %}
        """

    size: str = field(default="m", metadata={"doc": _("Spacer size (xs|s|m|l|xl).")})


@dataclass
class DividerConfig:
    """
    Configuration for the divider simple tag.

    Visual divider line.

    Attributes:
        direction: Orientation (horizontal|vertical).
        size: Margin size (xs|s|m|l|xl).

    """

    __example__ = """
        {% load layout_tags %}
        {% divider direction="horizontal" size="m" %}
        """

    direction: str = field(default="horizontal", metadata={"doc": _("Orientation (horizontal|vertical).")})
    size: str = field(default="m", metadata={"doc": _("Margin size (xs|s|m|l|xl).")})


@dataclass
class GridConfig:
    """
    Configuration for the grid block tag.

    CSS Grid container with responsive or auto-fit columns.

    Attributes:
        cols: Number of columns (1-6). If not set, uses auto-fit mode.
        gap: Space between grid items (xs|s|m|l|xl).
        min: Minimum item width for auto-fit mode.
        fixed: Disable responsive breakpoints.

    """

    __example__ = """
        {% load layout_tags %}

        {# Auto-fit mode #}
        {% grid gap="l" %}
            <div>Item 1</div>
            <div>Item 2</div>
        {% endgrid %}

        {# Fixed columns with responsive breakpoints #}
        {% grid cols=3 gap="m" %}
            ...
        {% endgrid %}
        """

    cols: int | None = field(
        default=None, metadata={"doc": _("Number of columns (1-6). If not set, uses auto-fit mode.")}
    )
    gap: str = field(default="m", metadata={"doc": _("Space between grid items (xs|s|m|l|xl).")})
    min: str = field(default="250px", metadata={"doc": _("Minimum item width for auto-fit mode.")})
    fixed: bool = field(default=False, metadata={"doc": _("Disable responsive breakpoints.")})


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
            cta_primary=ButtonConfig(label="Get Started", request_url="/signup/", type="primary"),
            cta_secondary=ButtonConfig(label="Learn More", request_url="/docs/", type="secondary"),
            badge_config=BadgeConfig(text="New!", icon=IconConfig(name="sparkles")),
        )
        """

    title: str = field(default="", metadata={"doc": _("Title of the Hero section.")})
    subtitle: str = field(default="", metadata={"doc": _("Subtitle of the Hero section, displayed below the title.")})
    description: str = field(
        default="", metadata={"doc": _("Description of the Hero section, displayed below the title and subtitle.")}
    )
    cta_primary: ButtonConfig | None = field(default=None, metadata={"doc": _("Primary 'Call-to-Action' button.")})
    cta_secondary: ButtonConfig | None = field(default=None, metadata={"doc": _("Secondary 'Call-to-Action' button.")})
    background_image_url: str = field(default="", metadata={"doc": _("URL of the background image.")})
    badge_config: BadgeConfig | None = field(default=None, metadata={"doc": _("A badge with icon and text.")})
