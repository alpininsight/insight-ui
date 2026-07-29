"""
Layout block tags for Insight UI.

Provides block-level layout components for consistent spacing and alignment.

Spacing System
--------------
All spacing parameters (gap, padding, size, spacing) use a fixed scale:

    xs  = 0.25rem (4px)   -> Tailwind: gap-1, p-1
    s   = 0.5rem  (8px)   -> Tailwind: gap-2, p-2
    m   = 1rem   (16px)   -> Tailwind: gap-4, p-4  [default]
    l   = 1.5rem (24px)   -> Tailwind: gap-6, p-6
    xl  = 2rem   (32px)   -> Tailwind: gap-8, p-8

Available Tags
--------------
Block tags (require closing tag):

    {% page padding="m" height="full" %}...{% endpage %}
        Full-width page container with consistent padding and optional height.

    {% hbox gap="s" v_align="center" h_align="between" full_height=True %}...{% endhbox %}
        Horizontal flex container (row direction).

    {% vbox gap="m" v_align="center" full_height=True %}...{% endvbox %}
        Vertical flex container (column direction).

    {% grid cols=3 gap="m" %}...{% endgrid %}
        CSS Grid container with responsive columns.

    {% surface padding="m" variant="subtle" radius="m" %}...{% endsurface %}
        Styled container with background, border, and optional shadow.

    {% link_surface href="/path" padding="m" %}...{% endlink_surface %}
        Clickable surface container with hover effects (renders as <a>).

Simple tags:

    {% spacer size="m" %}
        Fixed-size spacer element.

    {% divider direction="horizontal" spacing="m" %}
        Visual divider line (horizontal or vertical).

Parameter Reference
-------------------
gap : xs | s | m | l | xl
    Space between children. Default: "m"

padding : xs | s | m | l | xl
    Inner padding. Default: "m" for page, optional for hbox/vbox

height : auto | full | peek
    Page height behavior (page only). Default: "auto"
    - auto: Fits content
    - full: Full viewport height (min-h-screen)
    - peek: Almost full, shows next section peeking
    When set to full or peek, page becomes flex-col so children can use class="grow".

max_width : xs | s | m | l | xl | fit | full
    Maximum container width (hbox/vbox only). Default: "full"

full_height : True | False
    Fill available height in parent container (hbox/vbox only). Default: False

size : xs | s | m | l | xl
    Size of spacer. Default: "m"

spacing : xs | s | m | l | xl
    Margin around divider. Default: "m"

h_align : start | center | end | between | around | evenly (hbox) | start | center | end | stretch | baseline (vbox)
    Horizontal alignment. For hbox: main-axis (justify). For vbox: cross-axis (items).

v_align : start | center | end | stretch | baseline (hbox) | start | center | end | between | around | evenly (vbox)
    Vertical alignment. For hbox: cross-axis (items). For vbox: main-axis (justify).

wrap : True | False
    Allow flex items to wrap. Default: False (hbox only)

direction : horizontal | vertical
    Divider orientation. Default: "horizontal"

variant : subtle | raised | outline
    Surface visual style. Default: "subtle"
    - subtle: Light background with border
    - raised: Light background with border and shadow
    - outline: Border only, transparent background

radius : xs | s | m | l | xl | none
    Border radius for surface. Default: "m"

href : str
    URL for link_surface. Required for link_surface.

external : True | False
    Open link in new tab (link_surface only). Default: False

cols : int (2-6)
    Number of grid columns. If not set, uses auto-fit mode.

min : str
    Minimum item width for auto-fit mode. Default: "250px"

fixed : True | False
    Disable responsive breakpoints for grid. Default: False

class : str
    Additional CSS classes to append.

Grid Examples
-------------
::

    {% load layout_tags %}

    {# Auto-fit: items wrap based on available space #}
    {% grid gap="l" %}
        <div>Item 1</div>
        <div>Item 2</div>
        <div>Item 3</div>
    {% endgrid %}

    {# Auto-fit with custom min-width #}
    {% grid min="300px" gap="m" %}
        ...
    {% endgrid %}

    {# Fixed columns with automatic responsive breakpoints #}
    {% grid cols=3 gap="l" %}
        ...
    {% endgrid %}

    {# Fixed columns without responsive behavior #}
    {% grid cols=4 fixed=True %}
        ...
    {% endgrid %}

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from django import template
from django.template.base import Node, NodeList, token_kwargs
from django.utils.safestring import mark_safe

if TYPE_CHECKING:
    from django.template.base import FilterExpression, Parser, Token
    from django.template.context import Context

register = template.Library()


# =============================================================================
# Type Definitions & Constants
# =============================================================================

VALID_SPACING: frozenset[str] = frozenset({"xs", "s", "m", "l", "xl"})
VALID_ALIGN: frozenset[str] = frozenset({"start", "center", "end", "stretch", "baseline"})
VALID_JUSTIFY: frozenset[str] = frozenset({"start", "center", "end", "between", "around", "evenly"})
VALID_DIRECTION: frozenset[str] = frozenset({"horizontal", "vertical"})
VALID_HEIGHT: frozenset[str] = frozenset({"auto", "full", "peek"})
VALID_MAX_WIDTH: frozenset[str] = frozenset({"xs", "s", "m", "l", "xl", "fit", "full"})
VALID_SURFACE_VARIANT: frozenset[str] = frozenset({"subtle", "raised", "outline"})
VALID_RADIUS: frozenset[str] = frozenset({"xs", "s", "m", "l", "xl", "none"})

# Class mappings (classes are defined in input.css or are tailwind classes)
GAP_CLASSES: dict[str, str] = {
    "xs": "gap-insight-xs",
    "s": "gap-insight-s",
    "m": "gap-insight-m",
    "l": "gap-insight-l",
    "xl": "gap-insight-xl",
}
PADDING_CLASSES: dict[str, str] = {
    "xs": "p-insight-xs",
    "s": "p-insight-s",
    "m": "p-insight-m",
    "l": "p-insight-l",
    "xl": "p-insight-xl",
}
SPACER_CLASSES: dict[str, str] = {"xs": "h-1 w-1", "s": "h-2 w-2", "m": "h-4 w-4", "l": "h-6 w-6", "xl": "h-8 w-8"}
ALIGN_CLASSES: dict[str, str] = {
    "start": "items-start",
    "center": "items-center",
    "end": "items-end",
    "stretch": "items-stretch",
    "baseline": "items-baseline",
}
JUSTIFY_CLASSES: dict[str, str] = {
    "start": "justify-start",
    "center": "justify-center",
    "end": "justify-end",
    "between": "justify-between",
    "around": "justify-around",
    "evenly": "justify-evenly",
}
MAX_WIDTH_CLASSES: dict[str, str] = {
    "xs": "max-w-sm",  # 24rem (384px)
    "s": "max-w-xl",  # 36rem (576px)
    "m": "max-w-3xl",  # 48rem (768px)
    "l": "max-w-5xl",  # 64rem (1024px)
    "xl": "max-w-7xl",  # 80rem (1280px)
    "fit": "max-w-fit",
    "full": "",  # No max-width constraint
}
HEIGHT_CLASSES: dict[str, str] = {
    "auto": "",  # No height constraint
    "full": "min-h-screen",  # Full viewport height
    "peek": "page-peek",  # Shows next section peeking
}

# Surface variant classes
SURFACE_VARIANT_CLASSES: dict[str, str] = {
    "subtle": "insight-surface-subtle border insight-border-subtle",
    "raised": "insight-surface-subtle border insight-border-subtle insight-shadow-raised",
    "outline": "border insight-border-subtle",
}

# Surface radius classes
RADIUS_CLASSES: dict[str, str] = {
    "xs": "rounded-sm",
    "s": "rounded",
    "m": "rounded-lg",
    "l": "rounded-xl",
    "xl": "rounded-2xl",
    "none": "",
}

# Link surface hover classes (added to base surface classes)
LINK_SURFACE_HOVER_CLASSES: str = "hover:border-insight-primary transition-colors group"

# Responsive grid column mappings: cols -> (mobile, sm, md, lg)
# These provide sensible defaults so users don't need to think about breakpoints
RESPONSIVE_GRID_CLASSES: dict[int, str] = {
    2: "grid-cols-1 md:grid-cols-2",
    3: "grid-cols-1 md:grid-cols-2 lg:grid-cols-3",
    4: "grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4",
    5: "grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-5",
    6: "grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6",
}

# Fixed grid column classes (no responsive behavior)
FIXED_GRID_CLASSES: dict[int, str] = {
    1: "grid-cols-1",
    2: "grid-cols-2",
    3: "grid-cols-3",
    4: "grid-cols-4",
    5: "grid-cols-5",
    6: "grid-cols-6",
}

VALID_COLS: frozenset[int] = frozenset({1, 2, 3, 4, 5, 6})


# =============================================================================
# Validation Helpers
# =============================================================================


def _validate(value: str, valid_values: frozenset[str], param_name: str, tag_name: str) -> str:
    """
    Validate a parameter value against allowed values.

    Args:
        value: The value to validate.
        valid_values: Set of allowed values.
        param_name: Name of the parameter (for error message).
        tag_name: Name of the template tag (for error message).

    Returns:
        The validated value.

    Raises:
        ValueError: If value is not in valid_values.

    """
    if value not in valid_values:
        valid_str = ", ".join(sorted(valid_values))
        msg = f"Invalid {param_name} '{value}' in {{% {tag_name} %}}. Must be one of: {valid_str}"
        raise ValueError(msg)
    return value


def _parse_kwargs(kwargs: dict[str, FilterExpression]) -> dict[str, object]:
    """
    Convert token_kwargs FilterExpressions to usable values.

    Literal values are resolved immediately; variable references are kept
    for runtime resolution.
    """
    resolved: dict[str, object] = {}
    for key, value in kwargs.items():
        if hasattr(value, "var"):
            # FilterExpression - check if it's a literal
            if hasattr(value.var, "literal") and value.var.literal is not None:
                resolved[key] = value.var.literal
            else:
                # Variable reference, keep for runtime
                resolved[key] = value
        else:
            resolved[key] = value
    return resolved


def _make_block_tag(node_class: type[LayoutNode]) -> callable:
    """Create a block tag parser function for the given node class."""

    def tag_func(parser: Parser, token: Token) -> LayoutNode:
        bits = token.split_contents()
        tag_name = bits[0]
        remaining_bits = bits[1:]

        kwargs = token_kwargs(remaining_bits, parser) if remaining_bits else {}
        nodelist = parser.parse((f"end{tag_name}",))
        parser.delete_first_token()

        return node_class(nodelist, tag_name=tag_name, **_parse_kwargs(kwargs))

    return tag_func


# =============================================================================
# Base Layout Node
# =============================================================================


class LayoutNode(Node):
    """
    Base class for layout block tags.

    Subclasses must implement :meth:`build_classes` to define the CSS classes
    for the rendered element.

    Attributes:
        nodelist: The template nodes contained within the block.
        tag_name: The name of the tag (for error messages).
        kwargs: Parsed keyword arguments from the template tag.

    """

    def __init__(self, nodelist: NodeList, *, tag_name: str = "layout", **kwargs: object) -> None:
        """Initialize the layout node with content and parameters."""
        self.nodelist = nodelist
        self.tag_name = tag_name
        self.kwargs = kwargs

    def resolve_kwargs(self, context: Context) -> dict[str, object]:
        """Resolve any template variables in kwargs."""
        resolved: dict[str, object] = {}
        for key, value in self.kwargs.items():
            if hasattr(value, "resolve"):
                resolved[key] = value.resolve(context)
            else:
                resolved[key] = value
        return resolved

    def build_classes(self, kwargs: dict[str, object]) -> list[str]:  # noqa: ARG002
        """Build CSS classes from resolved kwargs. Override in subclasses."""
        return []

    def render(self, context: Context) -> str:
        """Render the layout node to HTML."""
        resolved = self.resolve_kwargs(context)
        classes = self.build_classes(resolved)

        # Append user-provided extra classes
        extra_classes = resolved.get("class", "")
        if extra_classes:
            classes.append(str(extra_classes))

        content = self.nodelist.render(context)
        class_str = " ".join(classes)

        return f'<div class="{class_str}">{content}</div>'


# =============================================================================
# Flex Container Base (shared by HBox/VBox)
# =============================================================================


class FlexNode(LayoutNode):
    """
    Base class for flex containers (hbox, vbox).

    Provides shared validation and class building for gap, padding, h_align, v_align.
    Subclasses set :attr:`flex_direction` to "row" or "col".

    For flex-row (hbox): h_align controls main-axis (justify), v_align controls cross-axis (items).
    For flex-col (vbox): v_align controls main-axis (justify), h_align controls cross-axis (items).
    """

    flex_direction: str = "row"  # Override in subclass

    def build_classes(self, kwargs: dict[str, object]) -> list[str]:
        """Build flex container CSS classes with gap, padding, max_width, h_align, and v_align."""
        classes = ["flex", f"flex-{self.flex_direction}"]

        # Optional full height (flex-grow: 1)
        if kwargs.get("full_height", False):
            classes.append("grow")

        # Optional max width
        max_width = str(kwargs.get("max_width", "full"))
        _validate(max_width, VALID_MAX_WIDTH, "max_width", self.tag_name)
        if MAX_WIDTH_CLASSES[max_width]:
            classes.append(MAX_WIDTH_CLASSES[max_width])

        # Optional padding
        padding = kwargs.get("padding")
        if padding:
            _validate(str(padding), VALID_SPACING, "padding", self.tag_name)
            classes.append(PADDING_CLASSES[str(padding)])

        gap = kwargs.get("gap", "m")
        if gap:
            _validate(str(gap), VALID_SPACING, "gap", self.tag_name)
            classes.append(GAP_CLASSES[str(gap)])

        h_align = str(kwargs.get("h_align", "stretch" if self.flex_direction == "col" else "start"))
        v_align = str(kwargs.get("v_align", "stretch" if self.flex_direction == "row" else "start"))

        if self.flex_direction == "row":
            # flex-row: h_align = main-axis (justify), v_align = cross-axis (items)
            _validate(h_align, VALID_JUSTIFY, "h_align", self.tag_name)
            _validate(v_align, VALID_ALIGN, "v_align", self.tag_name)
            classes.append(JUSTIFY_CLASSES[h_align])
            classes.append(ALIGN_CLASSES[v_align])
        else:
            # flex-col: v_align = main-axis (justify), h_align = cross-axis (items)
            _validate(v_align, VALID_JUSTIFY, "v_align", self.tag_name)
            _validate(h_align, VALID_ALIGN, "h_align", self.tag_name)
            classes.append(JUSTIFY_CLASSES[v_align])
            classes.append(ALIGN_CLASSES[h_align])

        if kwargs.get("wrap"):
            classes.append("flex-wrap")

        return classes


# =============================================================================
# Component Nodes
# =============================================================================


class PageNode(LayoutNode):
    """Page container with full width, consistent padding, and optional height control."""

    def build_classes(self, kwargs: dict[str, object]) -> list[str]:
        """Build page container CSS classes."""
        classes = ["w-full"]

        padding = str(kwargs.get("padding", "m"))
        _validate(padding, VALID_SPACING, "padding", self.tag_name)
        classes.append(PADDING_CLASSES[padding])

        height = str(kwargs.get("height", "auto"))
        _validate(height, VALID_HEIGHT, "height", self.tag_name)
        if HEIGHT_CLASSES[height]:
            classes.append(HEIGHT_CLASSES[height])
            # Enable flex layout so children can use grow/flex-1
            classes.extend(["flex", "flex-col"])

        return classes


class HBoxNode(FlexNode):
    """Horizontal flex container (flex-row)."""

    flex_direction = "row"


class VBoxNode(FlexNode):
    """Vertical flex container (flex-col)."""

    flex_direction = "col"


class GridNode(LayoutNode):
    """
    CSS Grid container with responsive or auto-fit columns.

    Modes:
        - Auto-fit (default): Items wrap based on available space.
          Use `min` parameter to set minimum item width.
        - Fixed columns: Set `cols` parameter for specific column count.
          Automatically applies responsive breakpoints unless `fixed=True`.
    """

    def build_classes(self, kwargs: dict[str, object]) -> list[str]:
        """Build grid container CSS classes."""
        classes = ["grid"]

        # Gap
        gap = kwargs.get("gap", "m")
        if gap:
            _validate(str(gap), VALID_SPACING, "gap", self.tag_name)
            classes.append(GAP_CLASSES[str(gap)])

        return classes

    def render(self, context: Context) -> str:
        """Render the grid node to HTML."""
        resolved = self.resolve_kwargs(context)
        classes = self.build_classes(resolved)

        cols = resolved.get("cols")
        min_width = resolved.get("min", "250px")
        fixed = resolved.get("fixed", False)

        style = ""

        if cols is not None:
            # Fixed column mode
            cols_int = int(cols)
            if cols_int not in VALID_COLS:
                valid_str = ", ".join(str(c) for c in sorted(VALID_COLS))
                msg = f"Invalid cols '{cols}' in {{% grid %}}. Must be one of: {valid_str}"
                raise ValueError(msg)

            if fixed or cols_int == 1:
                # No responsive behavior
                classes.append(FIXED_GRID_CLASSES[cols_int])
            else:
                # Responsive breakpoints
                classes.append(RESPONSIVE_GRID_CLASSES[cols_int])
        else:
            # Auto-fit mode: items wrap based on available space
            style = f"grid-template-columns: repeat(auto-fit, minmax({min_width}, 1fr));"

        # Append user-provided extra classes
        extra_classes = resolved.get("class", "")
        if extra_classes:
            classes.append(str(extra_classes))

        content = self.nodelist.render(context)
        class_str = " ".join(classes)

        if style:
            return f'<div class="{class_str}" style="{style}">{content}</div>'
        return f'<div class="{class_str}">{content}</div>'


class SurfaceNode(LayoutNode):
    """
    Surface container with background, border, and optional shadow.

    A styled container for grouping content with consistent visual treatment.
    Combine with vbox/hbox inside for layout control.

    Example::

        {% surface padding="l" variant="raised" %}
            {% vbox gap="m" %}
                <h3>Title</h3>
                <p>Content goes here</p>
            {% endvbox %}
        {% endsurface %}

    """

    def build_classes(self, kwargs: dict[str, object]) -> list[str]:
        """Build surface container CSS classes."""
        variant = str(kwargs.get("variant", "subtle"))
        _validate(variant, VALID_SURFACE_VARIANT, "variant", self.tag_name)
        classes = [SURFACE_VARIANT_CLASSES[variant]]

        # Padding
        padding = str(kwargs.get("padding", "m"))
        _validate(padding, VALID_SPACING, "padding", self.tag_name)
        classes.append(PADDING_CLASSES[padding])

        # Border radius
        radius = str(kwargs.get("radius", "m"))
        _validate(radius, VALID_RADIUS, "radius", self.tag_name)
        if RADIUS_CLASSES[radius]:
            classes.append(RADIUS_CLASSES[radius])

        return classes


class LinkSurfaceNode(LayoutNode):
    """
    Clickable surface container that renders as an anchor element.

    A styled link container with hover effects for navigation cards.
    Content is fully customizable - combine with hbox/vbox for layout.

    Example::

        {% link_surface href="/components" %}
            {% hbox gap="m" v_align="center" %}
                {% icon name="grid" size="l" %}
                {% vbox gap="xs" %}
                    <span class="font-semibold group-hover:text-insight-primary">Browse Components</span>
                    <span class="text-sm text-secondary">60+ components</span>
                {% endvbox %}
            {% endhbox %}
        {% endlink_surface %}

    Note:
        The container has ``class="group"`` so children can use ``group-hover:`` utilities.

    """

    def build_classes(self, kwargs: dict[str, object]) -> list[str]:
        """Build link surface container CSS classes."""
        variant = str(kwargs.get("variant", "subtle"))
        _validate(variant, VALID_SURFACE_VARIANT, "variant", self.tag_name)
        classes = [SURFACE_VARIANT_CLASSES[variant]]

        # Padding
        padding = str(kwargs.get("padding", "m"))
        _validate(padding, VALID_SPACING, "padding", self.tag_name)
        classes.append(PADDING_CLASSES[padding])

        # Border radius
        radius = str(kwargs.get("radius", "m"))
        _validate(radius, VALID_RADIUS, "radius", self.tag_name)
        if RADIUS_CLASSES[radius]:
            classes.append(RADIUS_CLASSES[radius])

        # Add hover effects and group class
        classes.append(LINK_SURFACE_HOVER_CLASSES)

        return classes

    def render(self, context: Context) -> str:
        """Render the link surface as an anchor element."""
        resolved = self.resolve_kwargs(context)
        classes = self.build_classes(resolved)

        href = resolved.get("href", "#")
        external = resolved.get("external", False)

        # Append user-provided extra classes
        extra_classes = resolved.get("class", "")
        if extra_classes:
            classes.append(str(extra_classes))

        content = self.nodelist.render(context)
        class_str = " ".join(classes)

        # Build attributes
        attrs = f'href="{href}" class="{class_str}"'
        if external:
            attrs += ' target="_blank" rel="noopener noreferrer"'

        return f"<a {attrs}>{content}</a>"


# =============================================================================
# Tag Registration
# =============================================================================


register.tag("page", _make_block_tag(PageNode))
register.tag("hbox", _make_block_tag(HBoxNode))
register.tag("vbox", _make_block_tag(VBoxNode))
register.tag("grid", _make_block_tag(GridNode))
register.tag("surface", _make_block_tag(SurfaceNode))
register.tag("link_surface", _make_block_tag(LinkSurfaceNode))


# =============================================================================
# Simple Tags
# =============================================================================


@register.simple_tag
def spacer(size: str = "m") -> str:
    """
    Insert a fixed-size spacer element.

    Args:
        size: Spacing size (xs, s, m, l, xl). Default: "m"

    Returns:
        HTML div element with appropriate size classes.

    Example:
        {% spacer %}
        {% spacer size="l" %}

    """
    _validate(size, VALID_SPACING, "size", "spacer")
    return mark_safe(f'<div class="flex-shrink-0 {SPACER_CLASSES[size]}"></div>')  # noqa: S308, # nosec B308, B703


@register.simple_tag
def divider(direction: str = "horizontal", spacing: str = "m") -> str:
    """
    Insert a visual divider line.

    Args:
        direction: "horizontal" or "vertical". Default: "horizontal"
        spacing: Margin spacing (xs, s, m, l, xl). Default: "m"

    Returns:
        HTML div element styled as a divider.

    Example:
        {% divider %}
        {% divider direction="vertical" %}
        {% divider spacing="l" %}

    """
    _validate(spacing, VALID_SPACING, "spacing", "divider")
    _validate(direction, VALID_DIRECTION, "direction", "divider")

    # Margin classes based on direction
    margin_map = {
        ("horizontal", "xs"): "my-1",
        ("horizontal", "s"): "my-2",
        ("horizontal", "m"): "my-4",
        ("horizontal", "l"): "my-6",
        ("horizontal", "xl"): "my-8",
        ("vertical", "xs"): "mx-1",
        ("vertical", "s"): "mx-2",
        ("vertical", "m"): "mx-4",
        ("vertical", "l"): "mx-6",
        ("vertical", "xl"): "mx-8",
    }
    margin = margin_map[(direction, spacing)]
    classes = (
        f"w-px self-stretch bg-gray-200 {margin}" if direction == "vertical" else f"h-px w-full bg-gray-200 {margin}"
    )

    return mark_safe(f'<div class="{classes}"></div>')  # noqa: S308, # nosec B308, B703
