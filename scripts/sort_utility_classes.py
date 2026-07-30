#!/usr/bin/env python3
"""Sort Tailwind CSS classes in HTML files.

Sorts classes in class="..." attributes following Tailwind's recommended order:
Layout -> Flexbox/Grid -> Spacing -> Sizing -> Typography -> Backgrounds -> Borders -> Effects -> States

Also fixes nested quotes in Django template tags within attributes:
  class="{% if x == "y" %}" -> class="{% if x == 'y' %}"
"""

import logging
import re
import sys
from pathlib import Path

# Configure logging for CLI output
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
)
logger = logging.getLogger(__name__)

# Priority order for Tailwind class prefixes (lower = earlier)
# Based on Tailwind's recommended class order
CLASS_ORDER: list[tuple[str, int]] = [
    # Layout
    ("container", 10),
    ("block", 11),
    ("inline-block", 12),
    ("inline", 13),
    ("flex", 14),
    ("inline-flex", 15),
    ("grid", 16),
    ("inline-grid", 17),
    ("hidden", 18),
    ("contents", 19),
    ("flow-root", 20),
    # Position
    ("static", 30),
    ("fixed", 31),
    ("absolute", 32),
    ("relative", 33),
    ("sticky", 34),
    ("inset", 35),
    ("top-", 36),
    ("right-", 37),
    ("bottom-", 38),
    ("left-", 39),
    ("ltr:", 40),
    ("rtl:", 41),
    # Z-index
    ("z-", 50),
    # Flexbox
    ("basis-", 60),
    ("flex-row", 61),
    ("flex-col", 62),
    ("flex-wrap", 63),
    ("flex-nowrap", 64),
    ("flex-1", 65),
    ("flex-auto", 66),
    ("flex-initial", 67),
    ("flex-none", 68),
    ("grow", 69),
    ("shrink", 70),
    ("order-", 71),
    # Grid
    ("grid-cols-", 80),
    ("grid-rows-", 81),
    ("col-", 82),
    ("row-", 83),
    ("auto-cols-", 84),
    ("auto-rows-", 85),
    ("gap-", 86),
    # Alignment
    ("justify-", 90),
    ("items-", 91),
    ("content-", 92),
    ("place-", 93),
    ("self-", 94),
    # Spacing
    ("p-", 100),
    ("px-", 101),
    ("py-", 102),
    ("ps-", 103),
    ("pe-", 104),
    ("pt-", 105),
    ("pr-", 106),
    ("pb-", 107),
    ("pl-", 108),
    ("m-", 110),
    ("mx-", 111),
    ("my-", 112),
    ("ms-", 113),
    ("me-", 114),
    ("mt-", 115),
    ("mr-", 116),
    ("mb-", 117),
    ("ml-", 118),
    ("-m", 119),
    ("space-", 120),
    # Sizing
    ("w-", 130),
    ("min-w-", 131),
    ("max-w-", 132),
    ("h-", 133),
    ("min-h-", 134),
    ("max-h-", 135),
    ("size-", 136),
    # Typography
    ("font-", 140),
    ("text-", 141),
    ("leading-", 142),
    ("tracking-", 143),
    ("whitespace-", 144),
    ("break-", 145),
    ("truncate", 146),
    ("uppercase", 147),
    ("lowercase", 148),
    ("capitalize", 149),
    ("italic", 150),
    ("not-italic", 151),
    ("underline", 152),
    ("overline", 153),
    ("line-through", 154),
    ("no-underline", 155),
    # Backgrounds
    ("bg-", 160),
    ("from-", 161),
    ("via-", 162),
    ("to-", 163),
    # Borders
    ("border", 170),
    ("border-", 171),
    ("rounded", 172),
    ("rounded-", 173),
    ("outline", 174),
    ("outline-", 175),
    ("ring", 176),
    ("ring-", 177),
    # Effects
    ("shadow", 180),
    ("shadow-", 181),
    ("opacity-", 182),
    ("blur", 183),
    ("blur-", 184),
    ("brightness-", 185),
    ("contrast-", 186),
    ("grayscale", 187),
    ("invert", 188),
    ("saturate-", 189),
    ("sepia", 190),
    ("backdrop-", 191),
    # Filters
    ("filter", 195),
    # Transitions
    ("transition", 200),
    ("transition-", 201),
    ("duration-", 202),
    ("ease-", 203),
    ("delay-", 204),
    # Transforms
    ("transform", 210),
    ("scale-", 211),
    ("rotate-", 212),
    ("translate-", 213),
    ("skew-", 214),
    ("origin-", 215),
    # Interactivity
    ("cursor-", 220),
    ("select-", 221),
    ("resize", 222),
    ("scroll-", 223),
    ("snap-", 224),
    ("touch-", 225),
    ("pointer-events-", 226),
    # Overflow
    ("overflow-", 230),
    # Visibility
    ("visible", 240),
    ("invisible", 241),
    ("collapse", 242),
    # Tables
    ("table", 250),
    # SVG
    ("fill-", 260),
    ("stroke-", 261),
    # Accessibility
    ("sr-only", 270),
    ("not-sr-only", 271),
    # State variants (should come last)
    ("group", 900),
    ("peer", 901),
    ("hover:", 910),
    ("focus:", 911),
    ("focus-within:", 912),
    ("focus-visible:", 913),
    ("active:", 914),
    ("visited:", 915),
    ("disabled:", 916),
    ("checked:", 917),
    ("first:", 920),
    ("last:", 921),
    ("odd:", 922),
    ("even:", 923),
    ("dark:", 930),
    ("sm:", 940),
    ("md:", 941),
    ("lg:", 942),
    ("xl:", 943),
    ("2xl:", 944),
]


def get_class_priority(class_name: str) -> int:
    """Get sort priority for a Tailwind class.

    Custom (non-Tailwind) classes get priority 0, so they appear first.
    Tailwind classes are sorted according to their category in CLASS_ORDER.

    Args:
        class_name: The CSS class name to get priority for.

    Returns:
        Integer priority value. Lower values sort first.
        Custom classes return 0, Tailwind classes return 10-944.

    """
    for prefix, priority in CLASS_ORDER:
        if class_name == prefix.rstrip("-:") or class_name.startswith(prefix):
            return priority
    # Custom/unknown classes come first (priority 0)
    return 0


def fix_nested_quotes(content: str) -> str:  # noqa: C901
    r"""Fix nested double quotes in Django template tags within double-quoted attributes.

    When an HTML attribute uses double quotes and contains Django template tags
    that also use double quotes, this creates invalid HTML. This function
    converts the inner quotes to single quotes.

    Args:
        content: The full HTML file content to process.

    Returns:
        The content with nested quotes fixed.

    Examples:
        >>> fix_nested_quotes('class="{% if x == "y" %}foo{% endif %}"')
        'class="{% if x == \\'y\\' %}foo{% endif %}"'
        >>> fix_nested_quotes('placeholder="{% trans "Hello" %}"')
        'placeholder="{% trans \\'Hello\\' %}"'

    """

    def fix_template_tag(tag_match: re.Match) -> str:
        """Replace double quotes with single quotes inside a template tag.

        Args:
            tag_match: Regex match object containing the template tag.

        Returns:
            The template tag with double quotes replaced by single quotes.

        """
        tag = tag_match.group(0)
        return tag.replace('"', "'")

    def fix_attribute_value(value: str) -> str:
        """Fix all template tags within an attribute value.

        Args:
            value: The attribute value (without surrounding quotes).

        Returns:
            The value with template tag quotes fixed.

        """
        if "{%" not in value:
            return value
        # Replace double quotes with single quotes inside all template tags
        return re.sub(r"\{%.*?%\}", fix_template_tag, value)

    # Match any attribute="value" where value might span multiple lines
    # Use a character-by-character approach to handle nested template tags
    result: list[str] = []
    pos = 0
    # Pattern to find start of double-quoted attribute
    attr_pattern = re.compile(r'(\w+)="')

    while pos < len(content):
        match = attr_pattern.search(content, pos)
        if not match:
            result.append(content[pos:])
            break

        # Add content before this attribute
        result.append(content[pos : match.start()])

        attr_name = match.group(1)
        value_start = match.end()

        # Find the closing quote, accounting for template tags
        # We need to handle {% ... %} which may contain "
        i = value_start
        in_template = False
        while i < len(content):
            if content[i : i + 2] == "{%":
                in_template = True
                i += 2
            elif content[i : i + 2] == "%}":
                in_template = False
                i += 2
            elif content[i] == '"' and not in_template:
                # Found closing quote
                break
            else:
                i += 1

        if i >= len(content):
            # No closing quote found, append rest and break
            result.append(content[match.start() :])
            break

        attr_value = content[value_start:i]
        fixed_value = fix_attribute_value(attr_value)
        result.append(f'{attr_name}="{fixed_value}"')
        pos = i + 1  # Skip the closing quote

    return "".join(result)


def sort_classes(class_string: str) -> str:
    """Sort space-separated CSS classes according to Tailwind conventions.

    Classes are sorted with custom classes first, followed by Tailwind
    utility classes in their recommended order. Django template tags
    within the class string are preserved in their original position.

    Whitespace is normalized: multiple spaces become one, leading/trailing
    whitespace is removed. However, the presence or absence of whitespace
    at template tag boundaries is preserved to maintain class concatenation
    patterns like `btn-{% if x %}outline-{% endif %}`.

    Args:
        class_string: Space-separated CSS class names, may include
            Django template tags like {% if %} or {{ variable }}.

    Returns:
        The sorted class string with normalized whitespace.

    Examples:
        >>> sort_classes("mt-4 flex custom-class bg-red-500")
        'custom-class flex mt-4 bg-red-500'
        >>> sort_classes("flex {% if x %}hidden{% endif %} mt-4")
        'flex {% if x %}hidden{% endif %} mt-4'
        >>> sort_classes("flex  mt-4")  # double space normalized
        'flex mt-4'

    """
    # Check if there are any Django template constructs
    if "{%" not in class_string and "{{" not in class_string:
        classes = class_string.split()
        sorted_classes = sorted(classes, key=get_class_priority)
        return " ".join(sorted_classes)

    # Split into template tags/variables and static parts, preserving delimiters
    # Match both {% ... %} and {{ ... }}
    parts = re.split(r"(\{%.*?%\}|\{\{.*?\}\})", class_string)

    result: list[str] = []
    for part in parts:
        if part.startswith(("{%", "{{")):
            # Template tag or variable - preserve as-is
            result.append(part)
        elif part:
            # Static text - normalize whitespace while preserving boundary presence
            has_leading_ws = part[0].isspace()
            has_trailing_ws = part[-1].isspace()

            # Sort the classes
            classes = part.split()
            if classes:
                sorted_part = " ".join(sorted(classes, key=get_class_priority))
                # Add single space if original had whitespace at boundary
                if has_leading_ws:
                    sorted_part = " " + sorted_part
                if has_trailing_ws:
                    sorted_part = sorted_part + " "
                result.append(sorted_part)
            elif has_leading_ws or has_trailing_ws:
                # Only whitespace - normalize to single space
                result.append(" ")

    return "".join(result).strip()


def process_file(filepath: Path) -> bool:
    """Process a single HTML file, sorting classes and fixing quotes.

    This function performs two operations:
    1. Fixes nested double quotes in Django template tags within attributes
    2. Sorts CSS classes in class="..." attributes

    Args:
        filepath: Path to the HTML file to process.

    Returns:
        True if the file was modified, False otherwise.

    """
    content = filepath.read_text(encoding="utf-8")
    original = content

    # First, fix nested quotes in all attributes (not just class)
    content = fix_nested_quotes(content)

    # Match class="..." attributes (handles multi-line with re.DOTALL)
    def replace_class(match: re.Match) -> str:
        """Replace callback for class attribute regex.

        Args:
            match: Regex match containing quote char and class string.

        Returns:
            The class attribute with sorted classes.

        """
        quote = match.group(1)
        classes = match.group(2)
        sorted_classes = sort_classes(classes)
        return f"class={quote}{sorted_classes}{quote}"

    # Handle both single and double quotes
    content = re.sub(r'class=(["\'])(.*?)\1', replace_class, content, flags=re.DOTALL)

    if content != original:
        filepath.write_text(content, encoding="utf-8")
        return True
    return False


def main() -> int:
    """Main entry point for the CLI.

    Processes HTML files passed as command line arguments, sorting
    Tailwind classes and fixing nested quotes in template tags.

    Returns:
        Exit code: 0 if no files modified, 1 if files were modified
        (for pre-commit compatibility).

    """
    if len(sys.argv) < 2:  # noqa: PLR2004
        logger.error("Usage: sort_tailwind_classes.py <file1.html> [file2.html ...]")
        return 1

    modified_count = 0
    for filepath in sys.argv[1:]:
        path = Path(filepath)
        if not path.exists():
            logger.warning("File not found: %s", filepath)
            continue
        if process_file(path):
            logger.info("Sorted: %s", filepath)
            modified_count += 1

    # Return 1 if files were modified (for pre-commit)
    return 1 if modified_count > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
