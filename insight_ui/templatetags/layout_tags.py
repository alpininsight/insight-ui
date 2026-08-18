"""
Layout block tags for Insight UI.

Provides block-level layout components for consistent spacing and alignment.
All layout tags are **mobile-first and responsive by default**.

Responsive Behavior
-------------------
Layout tags automatically adapt to screen size:

**Spacing (gap, padding):**
    - ``xs``, ``s``, ``m`` remain constant across all screen sizes
    - ``l`` becomes ``m`` on mobile, ``l`` from md breakpoint
    - ``xl`` becomes ``l`` on mobile, ``xl`` from md breakpoint

**HBox direction:**
    - Stacks vertically (column) on mobile by default
    - Switches to horizontal (row) from md breakpoint
    - Use ``inline=True`` for icon+text combos that should never stack

Spacing System
--------------
All spacing parameters (gap, padding, size, spacing) use a fixed scale:

    xs  = 0.25rem (4px)   -> Tailwind: gap-1, p-1
    s   = 0.5rem  (8px)   -> Tailwind: gap-2, p-2
    m   = 1rem   (16px)   -> Tailwind: gap-4, p-4  [default]
    l   = 1.5rem (24px)   -> Tailwind: gap-6, p-6  (responsive: m on mobile)
    xl  = 2rem   (32px)   -> Tailwind: gap-8, p-8  (responsive: l on mobile)

Available Tags
--------------
Block tags (require closing tag):

    {% section id="intro" gap="m" aria_label="Introduction" %}...{% endsection %}
        Semantic section container for content groupings (renders <section>).

    {% page padding="m" height="full" %}...{% endpage %}
        Full-width page container with consistent padding and optional height.

    {% hbox gap="s" v_align="center" h_align="between" full_height=True %}...{% endhbox %}
        Horizontal flex container. Stacks vertically on mobile, horizontal from md.
        Use inline=True for icon+text combos that should never stack.

    {% vbox gap="m" v_align="center" full_height=True %}...{% endvbox %}
        Vertical flex container (column direction).

    {% grid cols=3 gap="m" %}...{% endgrid %}
        CSS Grid container with responsive columns.

    {% surface padding="m" variant="surface" radius="m" %}...{% endsurface %}
        Styled container with background, border, and optional shadow.
        When href is provided, renders as clickable <a> with hover effects.

    {% collapsible summary="Show details" open=False icon=True %}...{% endcollapsible %}
        Expandable/collapsible section with toggle button.

    {% tabs id="my-tabs" label="Tab Label" %}
        {% tab id="tab1" label="Tab 1" active=True %}...{% endtab %}
        {% tab id="tab2" label="Tab 2" %}...{% endtab %}
    {% endtabs %}
        Tabbed interface with static content or HTMX loading.

    {% tabs config=tabs_config %}{% endtabs %}
        Tabbed interface using a TabsConfig object (HTMX mode).

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
    When set (except "fit" and "full"), container is also centered (mx-auto).

inline : True | False
    Prevent responsive stacking (hbox only). Default: False
    Use for icon+text combinations that should stay horizontal on all screens.

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

variant : surface | raised | outline
    Surface visual style. Default: "surface"
    - surface: Light background with border
    - raised: Light background with border and shadow
    - outline: Border only, transparent background

radius : xs | s | m | l | xl | none
    Border radius for surface. Default: "m"

href : str
    URL for link_surface. Required for link_surface.

external : True | False
    Open link in new tab (link_surface only). Default: False

summary : str
    Text displayed on the collapsible trigger button.

open : True | False
    Whether the collapsible is initially expanded. Default: False

icon : True | False
    Show chevron icon on trigger button. Default: True

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

import uuid
from typing import TYPE_CHECKING

from django import template
from django.template.base import Node, NodeList, TokenType, token_kwargs
from django.template.loader import get_template
from django.utils.safestring import mark_safe

if TYPE_CHECKING:
    from django.template.base import FilterExpression, Parser, Token
    from django.template.context import Context

register = template.Library()


# =============================================================================
# Type Definitions & Constants
# =============================================================================

VALID_SPACING: frozenset[str] = frozenset({"xs", "s", "m", "l", "xl"})
VALID_SPACING_WITH_NONE: frozenset[str] = frozenset({"none", "xs", "s", "m", "l", "xl"})
VALID_ALIGN: frozenset[str] = frozenset({"start", "center", "end", "stretch", "baseline"})
VALID_JUSTIFY: frozenset[str] = frozenset({"start", "center", "end", "between", "around", "evenly"})
VALID_DIRECTION: frozenset[str] = frozenset({"horizontal", "vertical"})
VALID_HEIGHT: frozenset[str] = frozenset({"auto", "full", "peek"})
VALID_MAX_WIDTH: frozenset[str] = frozenset({"xs", "s", "m", "l", "xl", "fit", "full"})
VALID_SURFACE_VARIANT: frozenset[str] = frozenset({"surface", "raised", "outline"})
VALID_RADIUS: frozenset[str] = frozenset({"xs", "s", "m", "l", "xl", "none"})
VALID_SIDE: frozenset[str] = frozenset({"left", "right"})
VALID_WIDTH: frozenset[str] = frozenset({"narrow", "normal", "wide"})
VALID_MOBILE_BEHAVIOR: frozenset[str] = frozenset({"hidden", "drawer"})

# Class mappings (classes are defined in input.css or are tailwind classes)
# Note: l and xl are responsive - smaller on mobile, full size from md breakpoint
GAP_CLASSES: dict[str, str] = {
    "xs": "gap-insight-xs",
    "s": "gap-insight-s",
    "m": "gap-insight-m",
    "l": "gap-insight-m md:gap-insight-l",
    "xl": "gap-insight-l md:gap-insight-xl",
}
PADDING_CLASSES: dict[str, str] = {
    "xs": "p-insight-xs",
    "s": "p-insight-s",
    "m": "p-insight-m",
    "l": "p-insight-m md:p-insight-l",
    "xl": "p-insight-l md:p-insight-xl",
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
    "xs": "mx-auto max-w-sm",  # 24rem (384px), centered
    "s": "mx-auto max-w-xl",  # 36rem (576px), centered
    "m": "mx-auto max-w-3xl",  # 48rem (768px), centered
    "l": "mx-auto max-w-5xl",  # 64rem (1024px), centered
    "xl": "mx-auto max-w-7xl",  # 80rem (1280px), centered
    "fit": "max-w-fit",
    "full": "",  # No max-width constraint
}
HEIGHT_CLASSES: dict[str, str] = {
    "auto": "",  # No height constraint
    "full": "min-h-screen",  # Full viewport height
    "peek": "page-peek",  # Shows next section peeking
}

# Surface variant classes (using combined CSS classes from input.css)
SURFACE_VARIANT_CLASSES: dict[str, str] = {
    "surface": "insight-surface",
    "raised": "insight-raised",
    "outline": "border border-insight-surface",  # outline has no bg/shadow
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

# Sidebar width classes (direct Tailwind classes)
SIDEBAR_WIDTH_CLASSES: dict[str, str] = {
    "narrow": "w-56",  # 14rem (224px)
    "normal": "w-72",  # 18rem (288px) - default
    "wide": "w-156",  # 24rem (384px)
}


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
            var = value.var
            # Check if it's a literal (number, True, False, None, or quoted string)
            if hasattr(var, "literal") and var.literal is not None:
                # Numeric or boolean literal
                resolved[key] = var.literal
            elif hasattr(var, "var") and var.var is not None:
                # It's a variable reference, keep FilterExpression for runtime
                resolved[key] = value
            else:
                # String literal (var contains the unquoted string value)
                resolved[key] = str(var)
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
    Subclasses set :attr:`flex_direction` to "row" or "col" and :attr:`responsive_stack`
    to control mobile behavior.

    For flex-row (hbox): h_align controls main-axis (justify), v_align controls cross-axis (items).
    For flex-col (vbox): v_align controls main-axis (justify), h_align controls cross-axis (items).

    Note:
        HBox is responsive by default - stacks vertically on mobile, horizontal from md breakpoint.
        Use inline=True for compact layouts (icon+text) that should never stack.
    """

    flex_direction: str = "row"  # Override in subclass
    responsive_stack: bool = False  # If True, stack on mobile (flex-col md:flex-row)

    def build_classes(self, kwargs: dict[str, object]) -> list[str]:
        """Build flex container CSS classes with gap, padding, max_width, h_align, and v_align."""
        # inline=True forces row layout on all screen sizes (for icon+text combos)
        is_inline = kwargs.get("inline", False)

        if self.responsive_stack and not is_inline:
            # Mobile-first: stack vertically, horizontal from md
            classes = ["flex", "flex-col", "md:flex-row"]
        else:
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


class SectionNode(LayoutNode):
    """
    Semantic section container for content groupings.

    Renders a ``<section>`` element for proper document semantics and accessibility.
    Combines vertical flex layout with semantic HTML structure.

    Parameters:
        id: Optional anchor ID (adds scroll-mt-24 for fixed navbar offset).
        gap: Space between children (xs, s, m, l, xl). Default: "m"
        aria_label: Accessible label for the section.
        aria_labelledby: ID of element that labels this section.
        class: Additional CSS classes to append.

    Example::

        {% section id="installation" gap="m" %}
            <h2>Installation</h2>
            <p>Instructions here...</p>
        {% endsection %}

    """

    def build_classes(self, kwargs: dict[str, object]) -> list[str]:
        """Build section container CSS classes."""
        classes = ["flex", "flex-col"]

        # Add scroll margin if section has an ID (for fixed navbar offset)
        if kwargs.get("id"):
            classes.append("scroll-mt-24")

        # Gap between children
        gap = str(kwargs.get("gap", "m"))
        _validate(gap, VALID_SPACING, "gap", self.tag_name)
        classes.append(GAP_CLASSES[gap])

        return classes

    def render(self, context: Context) -> str:
        """Render the section element with semantic HTML."""
        resolved = self.resolve_kwargs(context)
        classes = self.build_classes(resolved)

        # Append user-provided extra classes
        extra_classes = resolved.get("class", "")
        if extra_classes:
            classes.append(str(extra_classes))

        content = self.nodelist.render(context)
        class_str = " ".join(classes)

        # Build attributes
        attrs = [f'class="{class_str}"']

        section_id = resolved.get("id")
        if section_id:
            attrs.append(f'id="{section_id}"')

        aria_label = resolved.get("aria_label")
        if aria_label:
            attrs.append(f'aria-label="{aria_label}"')

        aria_labelledby = resolved.get("aria_labelledby")
        if aria_labelledby:
            attrs.append(f'aria-labelledby="{aria_labelledby}"')

        attrs_str = " ".join(attrs)
        return f"<section {attrs_str}>{content}</section>"


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
    """
    Horizontal flex container (flex-row).

    Responsive by default: stacks vertically on mobile, horizontal from md breakpoint.
    To force horizontal on all screens, add class="flex-row".
    """

    flex_direction = "row"
    responsive_stack = True


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
        classes = ["grid", "w-full"]

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
    When ``href`` is provided, renders as a clickable ``<a>`` element with hover effects.

    Parameters:
        variant: Visual style (surface|raised|outline). Default: "surface"
        padding: Inner padding (xs|s|m|l|xl). Default: "m"
        radius: Border radius override (xs|s|m|l|xl|none). Default: uses variant's radius.
        id: HTML id attribute for anchor links and JavaScript targeting.
        href: URL for clickable surface (renders as <a> instead of <div>).
        external: Open link in new tab (only when href is set).
        class: Additional CSS classes to append.

    Example::

        {# Static container (renders as <div>) #}
        {% surface padding="l" variant="raised" %}
            {% vbox gap="m" %}
                <h3>Title</h3>
                <p>Content goes here</p>
            {% endvbox %}
        {% endsurface %}

        {# Clickable surface (renders as <a>) #}
        {% surface href="/components" padding="m" %}
            <span class="group-hover:text-insight-primary">Browse Components</span>
        {% endsurface %}

    Note:
        When ``href`` is set, the container has ``class="group"`` so children
        can use ``group-hover:`` utilities for hover effects.

    """

    def build_classes(self, kwargs: dict[str, object], is_link: bool = False) -> list[str]:
        """Build surface container CSS classes."""
        variant = str(kwargs.get("variant", "surface"))
        _validate(variant, VALID_SURFACE_VARIANT, "variant", self.tag_name)
        classes = [SURFACE_VARIANT_CLASSES[variant]]

        # Padding
        padding = str(kwargs.get("padding", "m"))
        _validate(padding, VALID_SPACING, "padding", self.tag_name)
        classes.append(PADDING_CLASSES[padding])

        # Border radius (only add if explicitly set, otherwise use variant's default)
        if "radius" in kwargs:
            radius = str(kwargs.get("radius"))
            _validate(radius, VALID_RADIUS, "radius", self.tag_name)
            if RADIUS_CLASSES[radius]:
                classes.append(RADIUS_CLASSES[radius])

        # Add hover effects and group class for clickable surfaces
        if is_link:
            classes.append(LINK_SURFACE_HOVER_CLASSES)

        return classes

    def render(self, context: Context) -> str:
        """Render the surface as either <div> or <a> based on href."""
        resolved = self.resolve_kwargs(context)

        href = resolved.get("href", "")
        is_link = bool(href)

        classes = self.build_classes(resolved, is_link=is_link)

        # Append user-provided extra classes
        extra_classes = resolved.get("class", "")
        if extra_classes:
            classes.append(str(extra_classes))

        content = self.nodelist.render(context)
        class_str = " ".join(classes)

        # Build id attribute if provided
        element_id = resolved.get("id", "")
        id_attr = f' id="{element_id}"' if element_id else ""

        if is_link:
            # Render as anchor element
            external = resolved.get("external", False)
            attrs = f'href="{href}"{id_attr} class="{class_str}"'
            if external:
                attrs += ' target="_blank" rel="noopener noreferrer"'
            return f"<a {attrs}>{content}</a>"

        # Render as div element
        return f'<div{id_attr} class="{class_str}">{content}</div>'


class CollapsibleNode(LayoutNode):
    """
    Collapsible container with toggle button.

    Creates an expandable/collapsible section using the existing
    insight-ui-collapsible.js module. The trigger button toggles
    the visibility of the content.

    Example::

        {% collapsible summary="Show more details" %}
            <p>Hidden content that can be revealed.</p>
        {% endcollapsible %}

        {% collapsible summary="Advanced options" open=True icon=False %}
            <p>Initially visible content.</p>
        {% endcollapsible %}

    """

    def render(self, context: Context) -> str:
        """Render the collapsible container."""
        resolved = self.resolve_kwargs(context)

        template_context = {
            "summary": resolved.get("summary", "Details"),
            "is_open": resolved.get("open", False),
            "show_icon": resolved.get("icon", True),
            "collapsible_id": f"collapsible-{uuid.uuid4().hex[:8]}",
            "wrapper_class": str(resolved.get("class", "")),
            "content": self.nodelist.render(context),
        }

        tpl = get_template("insight_ui/components/layout/collapsible.html")
        return tpl.render(template_context)


# =============================================================================
# Tabs Component
# =============================================================================


class SidebarNode(LayoutNode):
    """
    Sidebar layout container.

    A flexible container for sidebar content that can be positioned on either side,
    with configurable width and mobile behavior.

    Parameters:
        side: Position of sidebar ("left" or "right"). Auto-detected from block context
            when used inside ``{% block sidebar_left %}`` or ``{% block sidebar_right %}``.
            Falls back to "right" if not specified and not in a sidebar block.
        static: If True, sidebar is sticky; if False, it's a drawer. Default: True
        width: Sidebar width ("narrow", "normal", "wide"). Default: "normal"
        mobile_behavior: How to behave on mobile ("hidden", "drawer"). Default: "hidden"
        class: Additional CSS classes to append.

    Example::

        {# Inside sidebar blocks, side is auto-detected - no need to specify #}
        {% block sidebar_left %}
            {% sidebar %}
                {% include "components/sidebar_nav.html" %}
            {% endsidebar %}
        {% endblock %}

        {% block sidebar_right %}
            {% sidebar width="wide" mobile_behavior="drawer" %}
                <h2>Table of Contents</h2>
            {% endsidebar %}
        {% endblock %}

        {# Outside blocks, specify side explicitly #}
        {% sidebar width="wide" %}
            <h2>Custom Title</h2>
            <nav>...</nav>
        {% endsidebar %}

    """

    def render(self, context: Context) -> str:
        """Render the sidebar container."""
        resolved = self.resolve_kwargs(context)

        # Get side from explicit parameter, context variable, or default
        # Context variable _sidebar_side is set by base.html when using sidebar blocks
        side_default = context.get("_sidebar_side", "right")
        side = str(resolved.get("side", side_default))
        _validate(side, VALID_SIDE, "side", self.tag_name)

        static = resolved.get("static", True)
        if isinstance(static, str):
            static = static.lower() == "true"

        width = str(resolved.get("width", "normal"))
        _validate(width, VALID_WIDTH, "width", self.tag_name)

        mobile_behavior = str(resolved.get("mobile_behavior", "hidden"))
        _validate(mobile_behavior, VALID_MOBILE_BEHAVIOR, "mobile_behavior", self.tag_name)

        # Get navbar_fixed from context (set by context processor)
        navbar_fixed = context.get("navbar_fixed", False)

        # Build template context
        template_context = {
            "side": side,
            "static": static,
            "width": width,
            "width_class": SIDEBAR_WIDTH_CLASSES[width],
            "mobile_behavior": mobile_behavior,
            "navbar_fixed": navbar_fixed,
            "wrapper_class": str(resolved.get("class", "")),
            "content": self.nodelist.render(context),
        }

        tpl = get_template("insight_ui/components/layout/sidebar.html")
        return tpl.render(template_context)


class TabNode(Node):
    """
    Single tab within a tabs container.

    Used internally by TabsNode to collect tab definitions.
    """

    def __init__(  # noqa: PLR0913
        self,
        nodelist: NodeList,
        *,
        tab_id: str,
        label: str,
        active: bool = False,
        url: str = "",
        icon: str = "",
    ) -> None:
        """Initialize the tab node."""
        self.nodelist = nodelist
        self.tab_id = tab_id
        self.label = label
        self.active = active
        self.url = url
        self.icon = icon

    def render(self, context: Context) -> str:
        """Render the tab content (used for static tabs)."""
        return self.nodelist.render(context)


class TabsNode(Node):
    """
    Tabbed interface with support for both static content and HTMX loading.

    Supports two modes:

    1. **Block mode** - Define tabs inline with content::

        {% tabs id="install" label="Installation" %}
            {% tab id="uv" label="uv (recommended)" active=True %}
                <p>uv content here</p>
            {% endtab %}
            {% tab id="pip" label="pip" %}
                <p>pip content here</p>
            {% endtab %}
        {% endtabs %}

    2. **Config mode** - Use a TabsConfig object (HTMX)::

        {% tabs config=my_tabs_config %}{% endtabs %}

    3. **HTMX mode** - Tabs with URLs load content via HTMX::

        {% tabs id="settings" label="Settings" %}
            {% tab id="general" label="General" url="/settings/general" active=True %}{% endtab %}
            {% tab id="security" label="Security" url="/settings/security" %}{% endtab %}
        {% endtabs %}

    """

    def __init__(
        self,
        tab_nodes: list[TabNode],
        *,
        tag_id: str = "",
        label: str = "",
        config: object | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize the tabs container."""
        self.tab_nodes = tab_nodes
        self.tag_id = tag_id
        self.label = label
        self.config = config
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

    def render(self, context: Context) -> str:
        """Render the tabs container."""
        resolved = self.resolve_kwargs(context)
        config = resolved.get("config") or self.config

        # Resolve config if it's a variable
        if config is not None and hasattr(config, "resolve"):
            config = config.resolve(context)

        # Determine mode and build tabs list
        if config is not None:
            # Config mode (HTMX) - data comes from TabsConfig object
            tag_id = config.tag_id
            label = config.label
            is_htmx = True
            tabs_data = [
                {
                    "id": tab.tag_id,
                    "label": tab.title,
                    "active": tab.active,
                    "url": tab.url,
                    "icon": getattr(tab, "icon", ""),
                    "panel_id": f"{tag_id}-{tab.tag_id}",
                    "content": None,
                }
                for tab in config.tabs
            ]
        else:
            # Block mode - data comes from inline {% tab %} blocks
            tag_id = str(resolved.get("id", f"tabs-{uuid.uuid4().hex[:8]}"))
            label = str(resolved.get("label", ""))
            is_htmx = any(tab.url for tab in self.tab_nodes)

            # Ensure at least one tab is active
            has_active = any(tab.active for tab in self.tab_nodes)
            if not has_active and self.tab_nodes:
                self.tab_nodes[0].active = True

            tabs_data = [
                {
                    "id": tab.tab_id,
                    "label": tab.label,
                    "active": tab.active,
                    "url": tab.url if is_htmx else "",
                    "icon": tab.icon,
                    "panel_id": f"{tag_id}-{tab.tab_id}",
                    # Content comes from internal template rendering, not user input
                    "content": mark_safe(tab.render(context)) if not is_htmx else None,  # noqa: S308  # nosec B308 B703
                }
                for tab in self.tab_nodes
            ]

        template_context = {
            "tag_id": tag_id,
            "label": label,
            "is_htmx": is_htmx,
            "tabs": tabs_data,
        }

        tpl = get_template("insight_ui/components/layout/tabs.html")
        return tpl.render(template_context)


def do_tabs(parser: Parser, token: Token) -> TabsNode:
    """
    Parse the {% tabs %} block tag.

    Collects all {% tab %}...{% endtab %} blocks within.
    """
    bits = token.split_contents()
    remaining_bits = bits[1:]

    # Parse kwargs for the tabs container
    kwargs = token_kwargs(remaining_bits, parser) if remaining_bits else {}
    parsed_kwargs = _parse_kwargs(kwargs)

    # Collect tab nodes
    tab_nodes: list[TabNode] = []
    nodelist = NodeList()

    while True:
        token = parser.next_token()

        if token.token_type == TokenType.BLOCK:
            tag_name = token.split_contents()[0]

            if tag_name == "endtabs":
                break
            if tag_name == "tab":
                # Parse the tab tag
                tab_node = do_tab(parser, token)
                tab_nodes.append(tab_node)
            else:
                # Other block tag, add to nodelist
                nodelist.append(parser.compile_filter(token.contents))
        else:
            # Text or variable, ignore (whitespace between tabs)
            pass

    return TabsNode(
        tab_nodes,
        tag_id=str(parsed_kwargs.get("id", "")),
        label=str(parsed_kwargs.get("label", "")),
        config=parsed_kwargs.get("config"),
        **{k: v for k, v in parsed_kwargs.items() if k not in ("id", "label", "config")},
    )


def do_tab(parser: Parser, token: Token) -> TabNode:
    """Parse a single {% tab %} block."""
    bits = token.split_contents()
    remaining_bits = bits[1:]

    kwargs = token_kwargs(remaining_bits, parser) if remaining_bits else {}
    parsed_kwargs = _parse_kwargs(kwargs)

    # Parse content until {% endtab %}
    nodelist = parser.parse(("endtab",))
    parser.delete_first_token()

    return TabNode(
        nodelist,
        tab_id=str(parsed_kwargs.get("id", f"tab-{uuid.uuid4().hex[:8]}")),
        label=str(parsed_kwargs.get("label", "Tab")),
        active=bool(parsed_kwargs.get("active", False)),
        url=str(parsed_kwargs.get("url", "")),
        icon=str(parsed_kwargs.get("icon", "")),
    )


# =============================================================================
# Tag Registration
# =============================================================================


register.tag("section", _make_block_tag(SectionNode))
register.tag("page", _make_block_tag(PageNode))
register.tag("hbox", _make_block_tag(HBoxNode))
register.tag("vbox", _make_block_tag(VBoxNode))
register.tag("grid", _make_block_tag(GridNode))
register.tag("surface", _make_block_tag(SurfaceNode))
register.tag("collapsible", _make_block_tag(CollapsibleNode))
register.tag("sidebar", _make_block_tag(SidebarNode))
register.tag("tabs", do_tabs)


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
        spacing: Margin spacing (none, xs, s, m, l, xl). Default: "m"

    Returns:
        HTML div element styled as a divider.

    Example:
        {% divider %}
        {% divider direction="vertical" %}
        {% divider spacing="l" %}

    """
    _validate(spacing, VALID_SPACING_WITH_NONE, "spacing", "divider")
    _validate(direction, VALID_DIRECTION, "direction", "divider")

    # Margin classes based on direction
    margin_map = {
        ("horizontal", "none"): "",
        ("horizontal", "xs"): "my-1",
        ("horizontal", "s"): "my-2",
        ("horizontal", "m"): "my-4",
        ("horizontal", "l"): "my-6",
        ("horizontal", "xl"): "my-8",
        ("vertical", "none"): "",
        ("vertical", "xs"): "mx-1",
        ("vertical", "s"): "mx-2",
        ("vertical", "m"): "mx-4",
        ("vertical", "l"): "mx-6",
        ("vertical", "xl"): "mx-8",
    }
    margin = margin_map[(direction, spacing)]
    base_classes = "w-px self-stretch bg-gray-200" if direction == "vertical" else "h-px w-full bg-gray-200"
    classes = f"{base_classes} {margin}".strip()

    return mark_safe(f'<div class="{classes}"></div>')  # noqa: S308, # nosec B308, B703
