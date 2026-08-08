"""Configuration classes for layout components."""

from dataclasses import dataclass, field

from django.utils.translation import gettext_lazy as _

from insight_ui.configs.input import ButtonConfig
from insight_ui.configs.utils import BadgeConfig


@dataclass
class PageHeaderConfig:
    """Configuration for the page_header component.

    Renders a page header with title and optional description.

    Attributes:
        title: The main page title, displayed prominently in primary color.
        chapter: Optional chapter displayed before the title in muted style.
        description: An optional description below the title.
        badges: Optional list of badges displayed below the description.
        buttons: Optional list of action buttons displayed below the badges.

    """

    __example__ = """
        PageHeaderConfig(
            title="Page Header",
            chapter="Insight UI",
            description="A header component for documentation pages.",
            badges=[BadgeConfig(label="New", type="success")],
            buttons=[ButtonConfig(label="Get Started", href="/start")],
        )
        """

    title: str = field(metadata={"doc": _("The main page title, displayed prominently in primary color.")})
    chapter: str = field(default="", metadata={"doc": _("Optional chapter displayed before the title in muted style.")})
    description: str | list[str] = field(default="", metadata={"doc": _("An optional description below the title.")})
    badges: list[BadgeConfig] = field(
        default_factory=list, metadata={"doc": _("Optional list of badges displayed below the description.")}
    )
    buttons: list[ButtonConfig] = field(
        default_factory=list, metadata={"doc": _("Optional list of action buttons displayed below the badges.")}
    )


@dataclass
class ArticleConfig:
    """Configuration for the article component.

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

    Block-level page container with consistent padding and optional height control.

    Attributes:
        padding: Inner padding size (xs|s|m|l|xl).
        height: Height behavior (auto|full|peek).

    """

    __example__ = """
        {% load layout_tags %}

        {# Standard - fits content #}
        {% page padding="l" %}
            <h1>Welcome</h1>
        {% endpage %}

        {# Full viewport height with centered content #}
        {% page height="full" %}
            {% vbox v_align="center" full_height=True %}
                <div>Vertically centered</div>
            {% endvbox %}
        {% endpage %}

        {# Peek - shows next section is coming #}
        {% page height="peek" %}
            <h1>Hero Section</h1>
        {% endpage %}
        """

    padding: str = field(default="m", metadata={"doc": _("Inner padding size (xs|s|m|l|xl).")})
    height: str = field(default="auto", metadata={"doc": _("Height behavior (auto|full|peek).")})


@dataclass
class HBoxConfig:
    """
    Configuration for the hbox block tag.

    Horizontal flex container (row direction).

    Attributes:
        gap: Space between children (xs|s|m|l|xl).
        padding: Inner padding (xs|s|m|l|xl). Optional.
        max_width: Maximum width (xs|s|m|l|xl|fit|full).
        full_height: Fill available height in parent container.
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

        {# Fill parent height - useful inside page with height="full" #}
        {% hbox full_height=True %}
            {% vbox %}Column 1{% endvbox %}
            {% vbox %}Column 2{% endvbox %}
        {% endhbox %}

        {# With max width #}
        {% hbox max_width="m" class="mx-auto" %}
            <div>Centered container</div>
        {% endhbox %}
        """

    gap: str = field(default="m", metadata={"doc": _("Space between children (xs|s|m|l|xl).")})
    padding: str | None = field(default=None, metadata={"doc": _("Inner padding (xs|s|m|l|xl). Optional.")})
    max_width: str = field(default="full", metadata={"doc": _("Maximum width (xs|s|m|l|xl|fit|full).")})
    full_height: bool = field(default=False, metadata={"doc": _("Fill available height in parent container.")})
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
        padding: Inner padding (xs|s|m|l|xl). Optional.
        max_width: Maximum width (xs|s|m|l|xl|fit|full).
        full_height: Fill available height in parent container.
        h_align: Horizontal alignment (start|center|end|stretch|baseline).
        v_align: Vertical alignment (start|center|end|between|around|evenly).

    """

    __example__ = """
        {% load layout_tags %}
        {% vbox gap="m" h_align="stretch" %}
            <div>Top</div>
            <div>Bottom</div>
        {% endvbox %}

        {# Fill parent height and center content vertically #}
        {% vbox full_height=True v_align="center" %}
            <div>Vertically centered</div>
        {% endvbox %}

        {# With max width #}
        {% vbox max_width="l" class="mx-auto" %}
            <article>Content</article>
        {% endvbox %}
        """

    gap: str = field(default="m", metadata={"doc": _("Space between children (xs|s|m|l|xl).")})
    padding: str | None = field(default=None, metadata={"doc": _("Inner padding (xs|s|m|l|xl). Optional.")})
    max_width: str = field(default="full", metadata={"doc": _("Maximum width (xs|s|m|l|xl|fit|full).")})
    full_height: bool = field(default=False, metadata={"doc": _("Fill available height in parent container.")})
    h_align: str = field(
        default="stretch", metadata={"doc": _("Horizontal alignment (start|center|end|stretch|baseline).")}
    )
    v_align: str = field(
        default="start", metadata={"doc": _("Vertical alignment (start|center|end|between|around|evenly).")}
    )


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
        spacing: Spacing size (none|xs|s|m|l|xl).

    """

    __example__ = """
        {% load layout_tags %}
        {% divider direction="horizontal" spacing="m" %}
        """

    direction: str = field(default="horizontal", metadata={"doc": _("Orientation (horizontal|vertical).")})
    spacing: str = field(default="m", metadata={"doc": _("Spacing size (none|xs|s|m|l|xl).")})


@dataclass
class SectionConfig:
    """
    Configuration for the section block tag.

    Semantic section container for content groupings.
    Renders a ``<section>`` element for proper document semantics and accessibility.

    Attributes:
        id: Anchor ID for navigation (adds scroll-mt-24 for fixed navbar offset).
        gap: Space between children (xs|s|m|l|xl).
        aria_label: Accessible label for the section.
        aria_labelledby: ID of element that labels this section.

    """

    __example__ = """
        {% load layout_tags %}

        {% section id="installation" gap="m" %}
            <h2>Installation</h2>
            <p>Follow these steps...</p>
        {% endsection %}

        {# With accessibility label #}
        {% section id="features" aria_label="Product features" %}
            ...
        {% endsection %}
        """

    id: str = field(
        default="", metadata={"doc": _("Anchor ID for navigation (adds scroll-mt-24 for fixed navbar offset).")}
    )
    gap: str = field(default="m", metadata={"doc": _("Space between children (xs|s|m|l|xl).")})
    aria_label: str = field(default="", metadata={"doc": _("Accessible label for the section.")})
    aria_labelledby: str = field(default="", metadata={"doc": _("ID of element that labels this section.")})


@dataclass
class SurfaceConfig:
    """
    Configuration for the surface block tag.

    Styled container with background, border, and optional shadow.
    When ``href`` is provided, renders as a clickable ``<a>`` element with hover effects.

    Attributes:
        variant: Visual style (surface|raised|outline).
        padding: Inner padding (xs|s|m|l|xl).
        radius: Border radius (xs|s|m|l|xl|none).
        id: HTML id attribute for anchor links and JavaScript targeting.
        href: URL for clickable surface (renders as <a> instead of <div>).
        external: Open link in new tab (only when href is set).

    """

    __example__ = """
        {% load layout_tags %}

        {# Static container #}
        {% surface variant="raised" padding="l" %}
            <h3>Card Title</h3>
            <p>Content here</p>
        {% endsurface %}

        {# Clickable surface (renders as <a>) #}
        {% surface href="/components" padding="m" %}
            <span class="group-hover:text-insight-primary">Browse Components</span>
        {% endsurface %}

        {# External link #}
        {% surface href="https://example.com" external=True %}
            External Resource
        {% endsurface %}
        """

    variant: str = field(default="surface", metadata={"doc": _("Visual style (surface|raised|outline).")})
    padding: str = field(default="m", metadata={"doc": _("Inner padding (xs|s|m|l|xl).")})
    radius: str = field(default="m", metadata={"doc": _("Border radius (xs|s|m|l|xl|none).")})
    id: str = field(default="", metadata={"doc": _("HTML id attribute for anchor links and JavaScript targeting.")})
    href: str = field(default="", metadata={"doc": _("URL for clickable surface (renders as <a> instead of <div>).")})
    external: bool = field(default=False, metadata={"doc": _("Open link in new tab (only when href is set).")})


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
    """Configuration for the hero component.

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
