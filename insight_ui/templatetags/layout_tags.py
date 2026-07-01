"""
Layout block tags for Insight UI.

Provides block-level layout components for consistent spacing and alignment.

Spacing System
--------------
All spacing parameters (gap, padding, size) use a fixed scale:

    xs  = 0.25rem (4px)   -> Tailwind: gap-1, p-1
    s   = 0.5rem  (8px)   -> Tailwind: gap-2, p-2
    m   = 1rem   (16px)   -> Tailwind: gap-4, p-4  [default]
    l   = 1.5rem (24px)   -> Tailwind: gap-6, p-6
    xl  = 2rem   (32px)   -> Tailwind: gap-8, p-8

Available Tags
--------------
Block tags (require closing tag):

    {% page padding="m" %}...{% endpage %}
        Full-width page container with consistent padding.

    {% hbox gap="s" v_align="center" h_align="between" wrap=True %}...{% endhbox %}
        Horizontal flex container (row direction).

    {% vbox gap="m" h_align="stretch" v_align="start" %}...{% endvbox %}
        Vertical flex container (column direction).

    {% grid cols=3 gap="m" %}...{% endgrid %}
        CSS Grid container with responsive columns.

Simple tags:

    {% spacer size="m" %}
        Fixed-size spacer element.

    {% divider direction="horizontal" size="m" %}
        Visual divider line (horizontal or vertical).

Parameter Reference
-------------------
gap : xs | s | m | l | xl
    Space between children. Default: "m"

padding : xs | s | m | l | xl
    Inner padding of container. Default: "m" (page)

size : xs | s | m | l | xl
    Size of spacer/divider margin. Default: "m"

align : start | center | end | stretch | baseline
    Cross-axis alignment (items-*). Default: "stretch" (hbox/vbox)

justify : start | center | end | between | around | evenly
    Main-axis alignment (justify-*). Default: "start" (hbox/vbox)

wrap : True | False
    Allow flex items to wrap. Default: False (hbox only)

direction : horizontal | vertical
    Divider orientation. Default: "horizontal"

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

# Class mappings (classes are defined in input.css or are tailwind classes)
GAP_CLASSES: dict[str, str] = {"xs": "gap-xs", "s": "gap-s", "m": "gap-m", "l": "gap-l", "xl": "gap-xl"}
PADDING_CLASSES: dict[str, str] = {"xs": "p-xs", "s": "p-s", "m": "p-m", "l": "p-l", "xl": "p-xl"}
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

    Provides shared validation and class building for gap, h_align, v_align.
    Subclasses set :attr:`flex_direction` to "row" or "col".

    For flex-row (hbox): h_align controls main-axis (justify), v_align controls cross-axis (items).
    For flex-col (vbox): v_align controls main-axis (justify), h_align controls cross-axis (items).
    """

    flex_direction: str = "row"  # Override in subclass

    def build_classes(self, kwargs: dict[str, object]) -> list[str]:
        """Build flex container CSS classes with gap, h_align, and v_align."""
        classes = ["flex", f"flex-{self.flex_direction}"]

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
    """Page container with full width and optional min-height."""

    def build_classes(self, kwargs: dict[str, object]) -> list[str]:
        """Build page container CSS classes."""
        classes = ["w-full"]

        # Optional full viewport height
        if kwargs.get("full_height", False):
            classes.append("min-h-screen")

        # Optional vertical alignment (enables flex layout)
        v_align = str(kwargs.get("v_align", ""))
        if v_align:
            _validate(v_align, VALID_JUSTIFY, "v_align", self.tag_name)
            classes.extend(["flex", "flex-col", JUSTIFY_CLASSES[v_align]])

        padding = str(kwargs.get("padding", "m"))
        _validate(padding, VALID_SPACING, "padding", self.tag_name)
        classes.append(PADDING_CLASSES[padding])

        return classes

    def render(self, context: Context) -> str:
        """Render the page node."""
        resolved = self.resolve_kwargs(context)
        classes = self.build_classes(resolved)

        # Append user-provided extra classes
        extra_classes = resolved.get("class", "")
        if extra_classes:
            classes.append(str(extra_classes))

        content = self.nodelist.render(context)
        class_str = " ".join(classes)

        return f'<div class="{class_str}">{content}</div>'


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


# =============================================================================
# Tag Registration
# =============================================================================


register.tag("page", _make_block_tag(PageNode))
register.tag("hbox", _make_block_tag(HBoxNode))
register.tag("vbox", _make_block_tag(VBoxNode))
register.tag("grid", _make_block_tag(GridNode))


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
def divider(direction: str = "horizontal", size: str = "m") -> str:
    """
    Insert a visual divider line.

    Args:
        direction: "horizontal" or "vertical". Default: "horizontal"
        size: Margin size (xs, s, m, l, xl). Default: "m"

    Returns:
        HTML div element styled as a divider.

    Example:
        {% divider %}
        {% divider direction="vertical" %}
        {% divider size="l" %}

    """
    _validate(size, VALID_SPACING, "size", "divider")
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
    margin = margin_map[(direction, size)]
    classes = (
        f"w-px self-stretch bg-gray-200 {margin}" if direction == "vertical" else f"h-px w-full bg-gray-200 {margin}"
    )

    return mark_safe(f'<div class="{classes}"></div>')  # noqa: S308, # nosec B308, B703
