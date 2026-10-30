# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
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

    {% modal id="my-modal" title="Dialog Title" width=32 %}...{% endmodal %}
        Modal dialog container with customizable content.

    {% list gap="m" %}
        {% listitem %}First item{% endlistitem %}
        {% listitem %}Second item{% endlistitem %}
    {% endlist %}
        Semantic list container (<ul> or <ol>) with flexible layout.
        Use `horizontal` flag for horizontal layout: {% list horizontal %}...{% endlist %}

Simple tags:

    {% spacer size="m" %}
        Fixed-size spacer element.

    {% divider direction="horizontal" spacing="m" weight="thin" style="solid" %}
        Visual divider line (horizontal or vertical).

Parameter Reference
-------------------
gap : none | xs | s | m | l | xl
    Space between children. Default: "m". Use "none" for zero gap.

padding : none | xs | s | m | l | xl
    Inner padding. Default: "m" for page, optional for hbox/vbox. Use "none" for zero padding.

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

weight : thin | medium | thick
    Divider line thickness. Default: "thin"

style : solid | dashed | dotted
    Divider line style. Default: "solid"

label : str
    Optional text label displayed in the center of the divider.
    For vertical dividers, the text is rotated 90°.

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
from typing import TYPE_CHECKING, cast

from django import template
from django.template.base import Node, NodeList, token_kwargs
from django.template.exceptions import TemplateSyntaxError
from django.template.loader import get_template
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.translation import gettext

from insight_ui.configs import HtmxConfig, ModalConfig, TabsConfig
from insight_ui.configs.types import LINK_URL_SCHEMES, url_scheme
from insight_ui.templatetags.insight_tags import build_config

if TYPE_CHECKING:
    from collections.abc import Callable

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
VALID_WIDTH: frozenset[str] = frozenset({"narrow", "normal", "wide", "fit"})
VALID_WIDTH_LIMIT: frozenset[str] = frozenset({"narrow", "normal", "wide"})
VALID_MOBILE_BEHAVIOR: frozenset[str] = frozenset({"hidden", "drawer"})
VALID_WEIGHT: frozenset[str] = frozenset({"thin", "medium", "thick"})
VALID_LINE_STYLE: frozenset[str] = frozenset({"solid", "dashed", "dotted"})

# Class mappings (classes are defined in input.css or are tailwind classes)
# Note: l and xl are responsive - smaller on mobile, full size from md breakpoint
GAP_CLASSES: dict[str, str] = {
    "none": "gap-0",
    "xs": "gap-insight-xs",
    "s": "gap-insight-s",
    "m": "gap-insight-m",
    "l": "gap-insight-m md:gap-insight-l",
    "xl": "gap-insight-l md:gap-insight-xl",
}
PADDING_CLASSES: dict[str, str] = {
    "none": "p-0",
    "xs": "p-insight-xs",
    "s": "p-insight-s",
    "m": "p-insight-m",
    "l": "p-insight-m md:p-insight-l",
    "xl": "p-insight-l md:p-insight-xl",
}
# Pages pad vertically; the content box provides the horizontal gutter.
PAGE_PADDING_CLASSES: dict[str, str] = {
    "none": "py-0",
    "xs": "py-insight-xs",
    "s": "py-insight-s",
    "m": "py-insight-m",
    "l": "py-insight-m md:py-insight-l",
    "xl": "py-insight-l md:py-insight-xl",
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
    "xs": "rounded-insight-xs",
    "s": "rounded-insight-s",
    "m": "rounded-insight-m",
    "l": "rounded-insight-l",
    "xl": "rounded-insight-xl",
    "none": "rounded-none",
}

# Link surface hover classes (added to base surface classes)
LINK_SURFACE_HOVER_CLASSES: str = "hover:border-insight-primary transition-colors group"

# Fixed grid column classes (no responsive behavior)
FIXED_GRID_CLASSES: dict[int, str] = {
    1: "grid-cols-1",
    2: "grid-cols-2",
    3: "grid-cols-3",
    4: "grid-cols-4",
    5: "grid-cols-5",
    6: "grid-cols-6",
}

# Responsive grid column classes (breakpoints based on container width)
# Uses @container queries for true component isolation - grid adapts to available space
RESPONSIVE_GRID_CLASSES: dict[int, str] = {
    2: "grid-cols-1 @md:grid-cols-2",
    3: "grid-cols-1 @md:grid-cols-2 @lg:grid-cols-3",
    4: "grid-cols-1 @sm:grid-cols-2 @md:grid-cols-3 @lg:grid-cols-4",
    5: "grid-cols-1 @sm:grid-cols-2 @md:grid-cols-3 @lg:grid-cols-5",
    6: "grid-cols-2 @sm:grid-cols-3 @md:grid-cols-4 @lg:grid-cols-6",
}

VALID_COLS: frozenset[int] = frozenset({1, 2, 3, 4, 5, 6})

# Sidebar width classes (direct Tailwind classes)
SIDEBAR_WIDTH_CLASSES: dict[str, str] = {
    "narrow": "w-56",  # 14rem (224px)
    "normal": "w-72",  # 18rem (288px) - default
    "wide": "w-96",  # 24rem (384px)
    "fit": "w-fit",  # content width, limited by min_width and max_width
}
SIDEBAR_WIDTH_ORDER: tuple[str, ...] = ("narrow", "normal", "wide")
SIDEBAR_MIN_WIDTH_CLASSES: dict[str, str] = {"narrow": "min-w-56", "normal": "min-w-72", "wide": "min-w-96"}
SIDEBAR_MAX_WIDTH_CLASSES: dict[str, str] = {"narrow": "max-w-56", "normal": "max-w-72", "wide": "max-w-96"}


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


def _validate_unknown_params(
    kwargs: dict[str, object],
    valid_params: frozenset[str],
    tag_name: str,
) -> None:
    """
    Validate that no unknown parameters were passed to a layout tag.

    Args:
        kwargs: The resolved keyword arguments.
        valid_params: Set of valid parameter names for this tag.
        tag_name: Name of the template tag (for error message).

    Raises:
        ValueError: If unknown parameters are found, with suggestions for typos.

    """
    from difflib import get_close_matches  # noqa: PLC0415

    unknown = set(kwargs) - valid_params
    if not unknown:
        return

    unknown_param = next(iter(unknown))
    suggestions = get_close_matches(unknown_param, list(valid_params), n=3, cutoff=0.5)

    if suggestions:
        suggestion_text = ", ".join(f"'{s}'" for s in suggestions)
        msg = f"Unknown parameter '{unknown_param}' in {{% {tag_name} %}}. Did you mean: {suggestion_text}?"
    else:
        valid_str = ", ".join(sorted(valid_params))
        msg = f"Unknown parameter '{unknown_param}' in {{% {tag_name} %}}. Valid parameters: {valid_str}"

    raise ValueError(msg)


def _validate_href(href: str, tag_name: str) -> str:
    """
    Allow relative URLs and the link schemes the component configs allow.

    Other schemes are rejected. Escaping an attribute does not change which
    scheme the browser follows.

    Args:
        href: Candidate URL from the layout tag.
        tag_name: Name of the template tag, used in the error message.

    Returns:
        The original URL when its scheme is allowed.

    Raises:
        ValueError: If the URL uses a scheme outside the allowlist.

    """
    scheme = url_scheme(href)
    if scheme and scheme not in LINK_URL_SCHEMES:
        allowed = ", ".join(LINK_URL_SCHEMES)
        msg = (
            f"Invalid href in {{% {tag_name} %}}: the scheme '{scheme}:' is not allowed. "
            f"Use a relative URL or {allowed}."
        )
        raise ValueError(msg)
    return href


# Context key under which {% tab %} nodes register with the surrounding {% tabs %}.
_TABS_CONTEXT_KEY = "_insight_tabs"


def _make_block_tag(node_class: type[LayoutNode]) -> Callable[[Parser, Token], LayoutNode]:
    """Create a block tag parser function for the given node class."""

    def tag_func(parser: Parser, token: Token) -> LayoutNode:
        bits = token.split_contents()
        tag_name = bits[0]
        remaining_bits = bits[1:]

        # Separate boolean flags from key=value pairs BEFORE calling token_kwargs
        flags = []
        kwarg_bits = []
        for bit in remaining_bits:
            if "=" not in bit and not bit.startswith(('"', "'")):
                flags.append(bit)
            else:
                kwarg_bits.append(bit)

        kwargs: dict[str, object] = dict(token_kwargs(kwarg_bits, parser)) if kwarg_bits else {}

        # Add boolean flags
        for flag in flags:
            kwargs[flag] = True

        nodelist = parser.parse((f"end{tag_name}",))
        parser.delete_first_token()

        # Values stay template expressions and are resolved per render (variables, filters, _() translations).
        return node_class(nodelist, tag_name=tag_name, **kwargs)

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
        valid_params: Frozenset of valid parameter names for this tag.

    """

    # Override in subclasses with the set of valid parameters
    valid_params: frozenset[str] = frozenset({"id", "class"})

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

    def wrap_content(self, content: str, classes: list[str]) -> str:  # noqa: ARG002
        """Wrap the rendered children. Override in subclasses that need an inner element."""
        return content

    def render(self, context: Context) -> str:
        """Render the layout node to HTML."""
        resolved = self.resolve_kwargs(context)

        # Validate no unknown parameters
        _validate_unknown_params(resolved, self.valid_params, self.tag_name)

        classes = self.build_classes(resolved)

        # Append user-provided extra classes
        extra_classes = resolved.get("class", "")
        if extra_classes:
            classes.append(str(extra_classes))

        content = self.wrap_content(self.nodelist.render(context), classes)
        class_str = " ".join(classes)

        # Optional id attribute
        element_id = resolved.get("id", "")
        id_attr = f' id="{escape(element_id)}"' if element_id else ""

        return f'<div{id_attr} class="{escape(class_str)}">{content}</div>'


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
    valid_params: frozenset[str] = frozenset(
        {
            "id",
            "gap",
            "padding",
            "h_align",
            "v_align",
            "max_width",
            "full_height",
            "inline",
            "wrap",
            "class",
        }
    )

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
            _validate(str(padding), VALID_SPACING_WITH_NONE, "padding", self.tag_name)
            classes.append(PADDING_CLASSES[str(padding)])

        gap = kwargs.get("gap", "m")
        if gap:
            _validate(str(gap), VALID_SPACING_WITH_NONE, "gap", self.tag_name)
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

    valid_params: frozenset[str] = frozenset({"id", "gap", "aria_label", "aria_labelledby", "class"})

    def build_classes(self, kwargs: dict[str, object]) -> list[str]:
        """Build section container CSS classes."""
        classes = ["flex", "flex-col"]

        # Add scroll margin if section has an ID (for fixed navbar offset)
        if kwargs.get("id"):
            classes.append("scroll-mt-24")

        # Gap between children
        gap = str(kwargs.get("gap", "m"))
        _validate(gap, VALID_SPACING_WITH_NONE, "gap", self.tag_name)
        classes.append(GAP_CLASSES[gap])

        return classes

    def render(self, context: Context) -> str:
        """Render the section element with semantic HTML."""
        resolved = self.resolve_kwargs(context)

        # Validate no unknown parameters
        _validate_unknown_params(resolved, self.valid_params, self.tag_name)

        classes = self.build_classes(resolved)

        # Append user-provided extra classes
        extra_classes = resolved.get("class", "")
        if extra_classes:
            classes.append(str(extra_classes))

        content = self.nodelist.render(context)
        class_str = " ".join(classes)

        # Build attributes
        attrs = [f'class="{escape(class_str)}"']

        section_id = resolved.get("id")
        if section_id:
            attrs.append(f'id="{escape(section_id)}"')

        aria_label = resolved.get("aria_label")
        if aria_label:
            attrs.append(f'aria-label="{escape(aria_label)}"')

        aria_labelledby = resolved.get("aria_labelledby")
        if aria_labelledby:
            attrs.append(f'aria-labelledby="{escape(aria_labelledby)}"')

        attrs_str = " ".join(attrs)
        return f"<section {attrs_str}>{content}</section>"


class PageNode(LayoutNode):
    """Full-width page band with vertical padding and optional height control.

    The band carries background and height and spans the full width of the content area when it is a
    direct child of #content. Its own content sits in the shared content box, so it lines up with the page
    header and the rest of the content. Nested deeper, the band stays in the content column.
    """

    valid_params: frozenset[str] = frozenset({"id", "padding", "height", "class"})

    def build_classes(self, kwargs: dict[str, object]) -> list[str]:
        """Build page container CSS classes."""
        classes = ["w-full", "insight-full-bleed"]

        padding = str(kwargs.get("padding", "m"))
        _validate(padding, VALID_SPACING_WITH_NONE, "padding", self.tag_name)
        classes.append(PAGE_PADDING_CLASSES[padding])

        height = str(kwargs.get("height", "auto"))
        _validate(height, VALID_HEIGHT, "height", self.tag_name)
        if HEIGHT_CLASSES[height]:
            classes.append(HEIGHT_CLASSES[height])
            # Enable flex layout so children can use grow/flex-1
            classes.extend(["flex", "flex-col"])

        return classes

    def wrap_content(self, content: str, classes: list[str]) -> str:
        """Put the content in the shared content box; a page with a height keeps the box stretching."""
        inner = "insight-content-box flex flex-col grow" if "flex-col" in classes else "insight-content-box"
        return f'<div class="{inner}">{content}</div>'


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
          Use `min` parameter to set minimum item width (supports any CSS unit: px, rem, em, etc.).
        - Fixed columns: Set `cols` parameter for specific column count.
          Automatically applies responsive breakpoints based on container width
          unless `fixed=True`.

    The grid uses CSS Container Queries for responsive behavior, meaning breakpoints
    are based on the grid's container width, not the viewport. This ensures the grid
    adapts correctly regardless of where it's placed (sidebar, modal, card, etc.).
    """

    valid_params: frozenset[str] = frozenset({"id", "cols", "gap", "min", "fixed", "class"})

    def build_classes(self, kwargs: dict[str, object]) -> list[str]:
        """Build grid container CSS classes."""
        classes = ["grid", "w-full"]

        # Gap
        gap = kwargs.get("gap", "m")
        if gap:
            _validate(str(gap), VALID_SPACING_WITH_NONE, "gap", self.tag_name)
            classes.append(GAP_CLASSES[str(gap)])

        return classes

    def render(self, context: Context) -> str:
        """Render the grid node to HTML."""
        resolved = self.resolve_kwargs(context)

        # Validate no unknown parameters
        _validate_unknown_params(resolved, self.valid_params, self.tag_name)

        classes = self.build_classes(resolved)

        cols = resolved.get("cols")
        min_width = resolved.get("min", "250px")
        fixed = resolved.get("fixed", False)

        style = ""
        needs_container_wrapper = False

        if cols is not None:
            # Fixed column mode; cols may arrive as a number literal, a string or a context value.
            valid_str = ", ".join(str(c) for c in sorted(VALID_COLS))
            msg = f"Invalid cols '{cols}' in {{% grid %}}. Must be one of: {valid_str}"
            try:
                cols_int = int(cast("int | str", cols))
            except (TypeError, ValueError):
                raise ValueError(msg) from None
            if cols_int not in VALID_COLS:
                raise ValueError(msg)

            if fixed or cols_int == 1:
                # No responsive behavior
                classes.append(FIXED_GRID_CLASSES[cols_int])
            else:
                # Container query responsive breakpoints
                classes.append(RESPONSIVE_GRID_CLASSES[cols_int])
                needs_container_wrapper = True
        else:
            # Auto-fit mode: items wrap based on available space
            style = f"grid-template-columns: repeat(auto-fit, minmax({min_width}, 1fr));"

        # Get user-provided extra classes
        extra_classes = str(resolved.get("class", "")).strip()

        # Optional id attribute
        element_id = resolved.get("id", "")
        id_attr = f' id="{escape(element_id)}"' if element_id else ""

        content = self.nodelist.render(context)

        # Wrap in container element for container query support
        # Container queries require @container on a parent element
        if needs_container_wrapper:
            # Apply extra classes to the wrapper (for sizing/centering)
            # The inner grid stays w-full to fill the container
            grid_class_str = " ".join(classes)
            wrapper_classes = "@container w-full"
            if extra_classes:
                wrapper_classes = f"@container w-full {extra_classes}"
            if style:
                grid_html = f'<div class="{grid_class_str}" style="{escape(style)}">{content}</div>'
            else:
                grid_html = f'<div class="{grid_class_str}">{content}</div>'
            return f'<div{id_attr} class="{escape(wrapper_classes)}">{grid_html}</div>'

        # No wrapper needed - apply extra classes directly to grid
        if extra_classes:
            classes.append(extra_classes)
        class_str = " ".join(classes)

        if style:
            return f'<div{id_attr} class="{escape(class_str)}" style="{escape(style)}">{content}</div>'
        return f'<div{id_attr} class="{escape(class_str)}">{content}</div>'


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
            <span class="group-hover:text-insight-primary-text">Browse Components</span>
        {% endsurface %}

    Note:
        When ``href`` is set, the container has ``class="group"`` so children
        can use ``group-hover:`` utilities for hover effects.

    """

    valid_params: frozenset[str] = frozenset({"variant", "padding", "radius", "id", "href", "external", "class"})

    def build_classes(self, kwargs: dict[str, object], is_link: bool = False) -> list[str]:
        """Build surface container CSS classes."""
        variant = str(kwargs.get("variant", "surface"))
        _validate(variant, VALID_SURFACE_VARIANT, "variant", self.tag_name)
        classes = [SURFACE_VARIANT_CLASSES[variant]]

        # Padding
        padding = str(kwargs.get("padding", "m"))
        _validate(padding, VALID_SPACING_WITH_NONE, "padding", self.tag_name)
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

        # Validate no unknown parameters
        _validate_unknown_params(resolved, self.valid_params, self.tag_name)

        href = _validate_href(str(resolved.get("href") or ""), self.tag_name)
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
        id_attr = f' id="{escape(element_id)}"' if element_id else ""

        if is_link:
            # Render as anchor element
            external = resolved.get("external", False)
            attrs = f'href="{escape(href)}"{id_attr} class="{escape(class_str)}"'
            new_tab_hint = ""
            if external:
                attrs += ' target="_blank" rel="noopener noreferrer"'
                # A new tab is a change of context; say so to screen readers.
                new_tab_hint = f'<span class="sr-only"> {escape(gettext("(opens in a new tab)"))}</span>'
            return f"<a {attrs}>{content}{new_tab_hint}</a>"

        # Render as div element
        return f'<div{id_attr} class="{escape(class_str)}">{content}</div>'


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

    valid_params: frozenset[str] = frozenset({"id", "summary", "open", "icon", "class"})

    def render(self, context: Context) -> str:
        """Render the collapsible container."""
        resolved = self.resolve_kwargs(context)

        # Validate no unknown parameters
        _validate_unknown_params(resolved, self.valid_params, self.tag_name)

        template_context = {
            "element_id": resolved.get("id", ""),
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
        width: Sidebar width ("narrow", "normal", "wide", "fit"). "fit" follows the content. Default: "normal"
        min_width: Lower limit for width="fit" ("narrow", "normal", "wide"). Default: none
        max_width: Upper limit for width="fit" ("narrow", "normal", "wide"). Default: "wide"
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

        {# Content width between narrow and wide #}
        {% sidebar width="fit" min_width="narrow" %}
            <nav>...</nav>
        {% endsidebar %}

        {# Outside blocks, specify side explicitly #}
        {% sidebar width="wide" %}
            <h2>Custom Title</h2>
            <nav>...</nav>
        {% endsidebar %}

    """

    valid_params: frozenset[str] = frozenset(
        {"side", "static", "width", "min_width", "max_width", "mobile_behavior", "class"}
    )

    def render(self, context: Context) -> str:
        """Render the sidebar container.

        Raises:
            ValueError: If min_width or max_width is set without width="fit", or min_width exceeds max_width.

        """
        resolved = self.resolve_kwargs(context)

        # Validate no unknown parameters
        _validate_unknown_params(resolved, self.valid_params, self.tag_name)

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
        width_class = SIDEBAR_WIDTH_CLASSES[width]
        if width == "fit":
            min_width = str(resolved.get("min_width") or "")
            max_width = str(resolved.get("max_width") or "wide")
            _validate(max_width, VALID_WIDTH_LIMIT, "max_width", self.tag_name)
            if min_width:
                _validate(min_width, VALID_WIDTH_LIMIT, "min_width", self.tag_name)
                if SIDEBAR_WIDTH_ORDER.index(min_width) > SIDEBAR_WIDTH_ORDER.index(max_width):
                    msg = f"min_width '{min_width}' is wider than max_width '{max_width}' in {{% {self.tag_name} %}}"
                    raise ValueError(msg)
                width_class += f" {SIDEBAR_MIN_WIDTH_CLASSES[min_width]}"
            width_class += f" {SIDEBAR_MAX_WIDTH_CLASSES[max_width]}"
        elif "min_width" in resolved or "max_width" in resolved:
            msg = f'min_width and max_width only apply to width="fit" in {{% {self.tag_name} %}}'
            raise ValueError(msg)

        mobile_behavior = str(resolved.get("mobile_behavior", "hidden"))
        _validate(mobile_behavior, VALID_MOBILE_BEHAVIOR, "mobile_behavior", self.tag_name)

        # Get navbar_fixed from INSIGHT_UI config (set by context processor)
        insight_ui_config = context.get("INSIGHT_UI", {})
        navbar_fixed = insight_ui_config.get("navbar_fixed", False) if isinstance(insight_ui_config, dict) else False

        # Build template context
        template_context = {
            "side": side,
            "static": static,
            "width": width,
            "width_class": width_class,
            "mobile_behavior": mobile_behavior,
            "navbar_fixed": navbar_fixed,
            "wrapper_class": str(resolved.get("class", "")),
            "content": self.nodelist.render(context),
        }

        tpl = get_template("insight_ui/components/layout/sidebar.html")
        return tpl.render(template_context)


class ModalNode(LayoutNode):
    """
    Modal dialog container with customizable content.

    A flexible modal that allows arbitrary content inside. The modal structure
    (backdrop, centering, close button) is handled automatically while the user
    provides the actual content.

    Parameters:
        config: Optional ModalConfig; the single parameters below override its values.
        id: Required unless set in config. Unique ID for JavaScript targeting (data-insight-modal).
        title: Optional heading displayed in the modal header.
        width: Maximum width in rem units. Default: 32
        show_close: Show the close button in the header. Default: True
        class: Additional CSS classes to append.

    Example::

        {# Basic modal with title #}
        {% modal id="confirm-delete" title="Confirm Deletion" %}
            <p>Are you sure you want to delete this item?</p>
            {% hbox gap="s" h_align="end" %}
                {% button label="Cancel" color="secondary" data_insight_dismiss="modal" %}
                {% button label="Delete" color="danger" on_click="deleteItem()" %}
            {% endhbox %}
        {% endmodal %}

        {# Modal without title (custom header) #}
        {% modal id="custom-modal" width=48 %}
            <div class="text-center">
                <h2>Custom Header</h2>
                <p>Full control over content</p>
            </div>
        {% endmodal %}

        {# Trigger button elsewhere in page #}
        {% button label="Open Modal" data_insight_modal="confirm-delete" %}

    Note:
        The modal is initially hidden and must be triggered using a button with
        ``data-insight-modal="modal-id"`` attribute. Close buttons inside the
        modal should have ``data-insight-dismiss="modal"`` attribute.

    """

    valid_params: frozenset[str] = frozenset({"config", "id", "title", "width", "show_close", "class"})

    def render(self, context: Context) -> str:
        """Render the modal container."""
        resolved = self.resolve_kwargs(context)

        # Validate no unknown parameters
        _validate_unknown_params(resolved, self.valid_params, self.tag_name)

        # build_config rejects anything that is not a dataclass instance.
        config = cast("ModalConfig | None", resolved.get("config"))
        if config is None and not resolved.get("id"):
            msg = "{% modal %} requires an 'id' parameter or a ModalConfig"
            raise ValueError(msg)
        # Single parameters override the config, like the arguments of the component tags.
        overrides = {key: resolved[key] for key in ("id", "title", "width", "show_close") if key in resolved}
        modal_config = build_config(ModalConfig, config, **overrides)

        template_context = {
            "modal_id": modal_config.id,
            "title": modal_config.title,
            "width": modal_config.width,
            "show_close": modal_config.show_close,
            "wrapper_class": str(resolved.get("class", "")),
            "content": self.nodelist.render(context),
        }

        tpl = get_template("insight_ui/components/layout/modal.html")
        return tpl.render(template_context)


# =============================================================================
# List Components
# =============================================================================

VALID_MARKER: frozenset[str] = frozenset({"none", "disc", "circle", "square", "decimal", "decimal-leading-zero"})
VALID_MARKER_POSITION: frozenset[str] = frozenset({"inside", "outside"})

MARKER_CLASSES: dict[str, str] = {
    "none": "list-none",
    "disc": "list-disc",
    "circle": "list-[circle]",
    "square": "list-[square]",
    "decimal": "list-decimal",
    "decimal-leading-zero": "list-[decimal-leading-zero]",
}


class ListNode(LayoutNode):
    """
    Semantic list container with flexible layout options.

    Creates accessible `<ul>` or `<ol>` elements with consistent styling.
    Use with `{% listitem %}` tags for each list entry.

    Parameters:
        horizontal: Use horizontal layout instead of vertical (default).
        gap: Spacing between items (xs, s, m, l, xl). Default: "m"
        ordered: Use `<ol>` instead of `<ul>`. Default: False
        marker: List marker style (none, disc, circle, square, decimal). Default: "none"
        marker_position: Marker position (inside, outside). Default: "inside"
        aria_label: Accessible label for the list.
        class: Additional CSS classes.

    Example::

        {% list gap="m" %}
            {% for item in items %}
                {% listitem %}
                    {% surface %}{{ item.name }}{% endsurface %}
                {% endlistitem %}
            {% endfor %}
        {% endlist %}

        {# Horizontal list with markers #}
        {% list horizontal gap="s" marker="disc" %}
            {% listitem %}First{% endlistitem %}
            {% listitem %}Second{% endlistitem %}
        {% endlist %}

        {# Ordered list #}
        {% list ordered marker="decimal" marker_position="outside" %}
            {% listitem %}Step one{% endlistitem %}
            {% listitem %}Step two{% endlistitem %}
        {% endlist %}

    """

    valid_params: frozenset[str] = frozenset(
        {"id", "horizontal", "gap", "ordered", "marker", "marker_position", "aria_label", "class"}
    )

    def render(self, context: Context) -> str:
        """Render the list container."""
        resolved = self.resolve_kwargs(context)

        # Validate no unknown parameters
        _validate_unknown_params(resolved, self.valid_params, self.tag_name)

        # Horizontal flag (default: vertical)
        horizontal = resolved.get("horizontal", False)

        # Gap
        gap = str(resolved.get("gap", "m"))
        _validate(gap, VALID_SPACING_WITH_NONE, "gap", self.tag_name)

        # Marker
        marker = str(resolved.get("marker", "none"))
        _validate(marker, VALID_MARKER, "marker", self.tag_name)

        # Marker position
        marker_position = str(resolved.get("marker_position", "inside"))
        _validate(marker_position, VALID_MARKER_POSITION, "marker_position", self.tag_name)

        # Build classes
        classes = ["flex"]

        if horizontal:
            classes.append("flex-row")
            classes.append("flex-wrap")
        else:
            classes.append("flex-col")

        classes.append(GAP_CLASSES[gap])
        classes.append(MARKER_CLASSES[marker])

        if marker != "none":
            classes.append(f"list-{marker_position}")

        # Extra classes
        extra_classes = resolved.get("class", "")
        if extra_classes:
            classes.append(str(extra_classes))

        class_str = " ".join(classes)

        # Element type
        tag = "ol" if resolved.get("ordered", False) else "ul"

        # Optional id attribute
        element_id = resolved.get("id", "")
        id_attr = f' id="{escape(element_id)}"' if element_id else ""

        # Aria label
        aria_label = resolved.get("aria_label", "")
        aria_attr = f' aria-label="{escape(aria_label)}"' if aria_label else ""

        content = self.nodelist.render(context)

        return f'<{tag}{id_attr} class="{escape(class_str)}"{aria_attr}>{content}</{tag}>'


class ListItemNode(LayoutNode):
    """
    Single item within a list container.

    Wraps content in a semantic `<li>` element.

    Parameters:
        class: Additional CSS classes for the list item.

    Example::

        {% list %}
            {% listitem %}First item{% endlistitem %}
            {% listitem class="font-bold" %}Highlighted item{% endlistitem %}
        {% endlist %}

    """

    valid_params: frozenset[str] = frozenset({"id", "class"})

    def render(self, context: Context) -> str:
        """Render the list item."""
        resolved = self.resolve_kwargs(context)

        # Validate no unknown parameters
        _validate_unknown_params(resolved, self.valid_params, self.tag_name)

        content = self.nodelist.render(context)

        # Build attributes
        element_id = resolved.get("id", "")
        extra_classes = resolved.get("class", "")

        attrs = []
        if element_id:
            attrs.append(f'id="{escape(element_id)}"')
        if extra_classes:
            attrs.append(f'class="{escape(extra_classes)}"')

        if attrs:
            attrs_str = " ".join(attrs)
            return f"<li {attrs_str}>{content}</li>"

        return f"<li>{content}</li>"


class TabNode(Node):
    """
    Single tab within a tabs container.

    Renders nothing itself: it registers its resolved values with the surrounding
    {% tabs %}, so tabs can come from {% if %} and {% for %} and from variables.
    """

    valid_params: frozenset[str] = frozenset({"id", "label", "active", "request_url", "icon"})

    def __init__(self, nodelist: NodeList, kwargs: dict[str, FilterExpression]) -> None:
        """Initialize the tab node."""
        self.nodelist = nodelist
        self.kwargs = kwargs

    def render(self, context: Context) -> str:
        """Register this tab with the surrounding {% tabs %}.

        Raises:
            TemplateSyntaxError: If the tab is not inside a {% tabs %} block.

        """
        collected = context.get(_TABS_CONTEXT_KEY)
        if collected is None:
            msg = "{% tab %} must be placed inside {% tabs %}"
            raise TemplateSyntaxError(msg)

        resolved = {key: value.resolve(context) for key, value in self.kwargs.items()}
        _validate_unknown_params(resolved, self.valid_params, "tab")
        collected.append(
            {
                "id": str(resolved.get("id") or f"tab-{uuid.uuid4().hex[:8]}"),
                "label": str(resolved.get("label", "Tab")),
                "active": bool(resolved.get("active", False)),
                "url": str(resolved.get("request_url", "")),
                "icon": str(resolved.get("icon", "")),
                "content": self.nodelist.render(context),
            }
        )
        return ""


class TabsNode(Node):
    """
    Tabbed interface with support for both static content and HTMX loading.

    Supports three modes:

    1. **Block mode** - Define tabs inline with content::

        {% tabs id="install" label="Installation" %}
            {% tab id="uv" label="uv (recommended)" active=True %}
                <p>uv content here</p>
            {% endtab %}
            {% tab id="pip" label="pip" %}
                <p>pip content here</p>
            {% endtab %}
        {% endtabs %}

       Tabs may be wrapped in {% if %} or created in a {% for %} loop, and their
       parameters may be template variables.

    2. **Config mode** - Use a TabsConfig object (HTMX); ``id`` and ``label`` override it::

        {% tabs config=my_tabs_config %}{% endtabs %}

    3. **HTMX mode** - Tabs with URLs load content via HTMX; ``htmx`` takes an HtmxConfig
       for shared request options. Target, swap and trigger stay fixed by the tabs::

        {% tabs id="settings" label="Settings" htmx=htmx %}
            {% tab id="general" label="General" request_url="/settings/general" active=True %}{% endtab %}
            {% tab id="security" label="Security" request_url="/settings/security" %}{% endtab %}
        {% endtabs %}

    The active tab is the first one with ``active=True``, otherwise the first tab.
    """

    valid_params: frozenset[str] = frozenset({"id", "label", "config", "htmx"})

    def __init__(self, nodelist: NodeList, kwargs: dict[str, FilterExpression]) -> None:
        """Initialize the tabs container."""
        self.nodelist = nodelist
        self.kwargs = kwargs

    def render(self, context: Context) -> str:
        """Render the tabs container.

        Raises:
            ValueError: If both a config and {% tab %} blocks are given.
            TypeError: If htmx is not an HtmxConfig.

        """
        resolved = {key: value.resolve(context) for key, value in self.kwargs.items()}
        _validate_unknown_params(resolved, self.valid_params, "tabs")

        collected: list[dict[str, object]] = []
        with context.push({_TABS_CONTEXT_KEY: collected}):
            self.nodelist.render(context)

        config = resolved.get("config")
        if config is not None:
            if collected:
                msg = "{% tabs %} takes either a config or {% tab %} blocks, not both"
                raise ValueError(msg)
            # build_config rejects anything that is not a dataclass instance.
            overrides = {
                target: resolved[key]
                for key, target in (("id", "tag_id"), ("label", "label"), ("htmx", "htmx"))
                if key in resolved
            }
            tabs_config = build_config(TabsConfig, cast("TabsConfig", config), **overrides)
            tag_id = tabs_config.tag_id
            label = tabs_config.label
            htmx = tabs_config.htmx
            collected = [
                {"id": tab.tag_id, "label": tab.title, "active": tab.active, "url": tab.request_url, "icon": ""}
                for tab in tabs_config.tabs
            ]
        else:
            tag_id = str(resolved.get("id") or f"tabs-{uuid.uuid4().hex[:8]}")
            label = str(resolved.get("label", ""))
            htmx = resolved.get("htmx")
        if htmx is not None and not isinstance(htmx, HtmxConfig):
            msg = f"{{% tabs %}} htmx must be an HtmxConfig, got {type(htmx).__name__}"
            raise TypeError(msg)

        is_htmx = any(tab["url"] for tab in collected)
        # Exactly one active tab per render: the first marked one, otherwise the first tab.
        active_index = next((i for i, tab in enumerate(collected) if tab["active"]), 0)
        tabs_data = [
            {
                **tab,
                "active": index == active_index,
                "url": tab["url"] if is_htmx else "",
                "panel_id": f"{tag_id}-{tab['id']}",
                # Content comes from internal template rendering, not user input
                "content": None if is_htmx else mark_safe(str(tab.get("content", ""))),  # noqa: S308  # nosec B308 B703
            }
            for index, tab in enumerate(collected)
        ]

        template_context = {
            "tag_id": tag_id,
            "label": label,
            "is_htmx": is_htmx,
            "htmx": htmx or HtmxConfig(),
            "panel_target": f"#{tag_id}-tab-content",
            "tabs": tabs_data,
            "active_tab_id": tabs_data[active_index]["id"] if tabs_data else "",
        }

        tpl = get_template("insight_ui/components/layout/tabs.html")
        return tpl.render(template_context)


def _parse_tag_kwargs(parser: Parser, token: Token) -> dict[str, FilterExpression]:
    """Parse the key=value arguments of a tag into unresolved filter expressions.

    Raises:
        TemplateSyntaxError: If an argument is not of the form key=value.

    """
    bits = token.split_contents()
    kwargs = token_kwargs(bits[1:], parser)
    if len(kwargs) != len(bits) - 1:
        msg = f"{{% {bits[0]} %}} only accepts key=value arguments"
        raise TemplateSyntaxError(msg)
    return kwargs


def do_tabs(parser: Parser, token: Token) -> TabsNode:
    """Parse the {% tabs %} block tag; its content is parsed like any other template content."""
    kwargs = _parse_tag_kwargs(parser, token)
    nodelist = parser.parse(("endtabs",))
    parser.delete_first_token()
    return TabsNode(nodelist, kwargs)


def do_tab(parser: Parser, token: Token) -> TabNode:
    """Parse a single {% tab %} block."""
    kwargs = _parse_tag_kwargs(parser, token)
    nodelist = parser.parse(("endtab",))
    parser.delete_first_token()
    return TabNode(nodelist, kwargs)


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
register.tag("modal", _make_block_tag(ModalNode))
register.tag("list", _make_block_tag(ListNode))
register.tag("listitem", _make_block_tag(ListItemNode))
register.tag("tabs", do_tabs)
register.tag("tab", do_tab)


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
def divider(
    direction: str = "horizontal",
    spacing: str = "m",
    weight: str = "thin",
    style: str = "solid",
    label: str = "",
) -> str:
    """
    Insert a visual divider line.

    Args:
        direction: "horizontal" or "vertical". Default: "horizontal"
        spacing: Margin spacing (none, xs, s, m, l, xl). Default: "m"
        weight: Line thickness (thin, medium, thick). Default: "thin"
        style: Line style (solid, dashed, dotted). Default: "solid"
        label: Optional text label displayed in the center of the divider.

    Returns:
        HTML div element styled as a divider.

    Example:
        {% divider %}
        {% divider direction="vertical" %}
        {% divider spacing="l" %}
        {% divider weight="thick" style="dashed" %}
        {% divider label="or" %}

    """
    _validate(spacing, VALID_SPACING_WITH_NONE, "spacing", "divider")
    _validate(direction, VALID_DIRECTION, "direction", "divider")
    _validate(weight, VALID_WEIGHT, "weight", "divider")
    _validate(style, VALID_LINE_STYLE, "style", "divider")

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

    # Build line classes based on style and weight
    # Note: All class names must be written out fully for Tailwind to detect them
    if style == "solid":
        weight_h = {"thin": "h-px", "medium": "h-0.5", "thick": "h-1"}
        weight_v = {"thin": "w-px", "medium": "w-0.5", "thick": "w-1"}
        if direction == "vertical":
            line_classes = f"{weight_v[weight]} flex-1 bg-insight-divider"
        else:
            line_classes = f"{weight_h[weight]} flex-1 bg-insight-divider"
    else:
        border_style = {"dashed": "border-dashed", "dotted": "border-dotted"}[style]
        border_h = {"thin": "border-t", "medium": "border-t-2", "thick": "border-t-4"}
        border_v = {"thin": "border-l", "medium": "border-l-2", "thick": "border-l-4"}
        if direction == "vertical":
            line_classes = f"flex-1 {border_v[weight]} {border_style} border-insight-divider"
        else:
            line_classes = f"flex-1 {border_h[weight]} {border_style} border-insight-divider"

    # Without label: simple divider
    if not label:
        if direction == "vertical":
            base_classes = line_classes.replace("flex-1", "self-stretch")
        else:
            base_classes = line_classes.replace("flex-1", "w-full")
        classes = f"{base_classes} {margin}".strip()
        return mark_safe(f'<div class="{classes}"></div>')  # noqa: S308, # nosec B308, B703

    # With label: flex container with two lines and text
    escaped_label = escape(label)

    if direction == "vertical":
        container_classes = f"flex flex-col items-center gap-2 self-stretch {margin}".strip()
        label_classes = "text-sm text-insight-text-muted -rotate-90"
    else:
        container_classes = f"flex items-center gap-4 {margin}".strip()
        label_classes = "text-sm text-insight-text-muted whitespace-nowrap"

    return mark_safe(  # noqa: S308, # nosec B308, B703
        f'<div class="{container_classes}">'
        f'<div class="{line_classes}"></div>'
        f'<span class="{label_classes}">{escaped_label}</span>'
        f'<div class="{line_classes}"></div>'
        f"</div>"
    )
