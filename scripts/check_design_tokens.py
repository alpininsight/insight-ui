#!/usr/bin/env python3
"""Check for hardcoded Tailwind utilities that should use design tokens.

This script detects direct Tailwind utilities that should be replaced with
design tokens from input.css:
- Colors: bg-gray-300 -> bg-insight-bg-base
- Radii: rounded-lg -> rounded-insight-surface
- Shadows: shadow-md -> shadow-insight-surface
- Verbose tokens: text-insight-text-body -> text-body

Exceptions can be marked with a Django template comment on the same line:
    <div class="rounded-lg {# tw-token-ok: special case #}">

Or suppress all warnings for a file by adding at the top:
    {# tw-token-ok-file: legacy template #}
"""

import logging
import re
import subprocess  # nosec B404 - needed for git diff in pre-commit hook
import sys
from dataclasses import dataclass, field
from pathlib import Path

# Configure logging for CLI output
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
)
logger = logging.getLogger(__name__)


# =============================================================================
# Configuration: Token Types
# =============================================================================


@dataclass
class TokenConfig:
    """Configuration for a design token type.

    Attributes:
        name: Human-readable name for this token type (e.g., "color").
        pattern: Compiled regex to match hardcoded values.
        suggestions: Mapping of pattern prefixes to suggested replacements.
        whitelist: Set of class patterns that are always allowed.

    """

    name: str
    pattern: re.Pattern
    suggestions: dict[str, str] = field(default_factory=dict)
    whitelist: set[str] = field(default_factory=set)


# State/responsive prefixes that may come before utility classes
STATE_PREFIXES: list[str] = [
    "hover:",
    "focus:",
    "focus-within:",
    "focus-visible:",
    "active:",
    "visited:",
    "disabled:",
    "checked:",
    "first:",
    "last:",
    "odd:",
    "even:",
    "group-hover:",
    "group-focus:",
    "peer-hover:",
    "peer-focus:",
    "dark:",
    "sm:",
    "md:",
    "lg:",
    "xl:",
    "2xl:",
]

STATE_PATTERN = "(?:" + "|".join(re.escape(p) for p in STATE_PREFIXES) + ")?"


# =============================================================================
# Color Token Configuration
# =============================================================================

TAILWIND_COLORS: set[str] = {
    "slate",
    "gray",
    "zinc",
    "neutral",
    "stone",
    "red",
    "orange",
    "amber",
    "yellow",
    "lime",
    "green",
    "emerald",
    "teal",
    "cyan",
    "sky",
    "blue",
    "indigo",
    "violet",
    "purple",
    "fuchsia",
    "pink",
    "rose",
}

TAILWIND_SHADES: set[str] = {
    "50",
    "100",
    "200",
    "300",
    "400",
    "500",
    "600",
    "700",
    "800",
    "900",
    "950",
}

COLOR_PREFIXES: list[str] = [
    "bg",
    "text",
    "border",
    "border-t",
    "border-r",
    "border-b",
    "border-l",
    "border-x",
    "border-y",
    "border-s",
    "border-e",
    "ring",
    "from",
    "via",
    "to",
    "divide",
    "placeholder",
    "outline",
    "decoration",
    "accent",
    "caret",
    "fill",
    "stroke",
]

# Colors that are universally acceptable without tokens
WHITELISTED_COLORS: set[str] = {"white", "black", "transparent", "current"}


def build_color_config() -> TokenConfig:
    """Build configuration for color token checking.

    Returns:
        TokenConfig for detecting hardcoded color classes.

    """
    prefix_pattern = "(?:" + "|".join(re.escape(p) for p in COLOR_PREFIXES) + ")"
    color_pattern = "(?:" + "|".join(TAILWIND_COLORS) + ")"
    shade_pattern = "(?:" + "|".join(TAILWIND_SHADES) + ")"

    # Match: [state:]prefix-color-shade[/opacity]
    pattern = re.compile(rf"\b({STATE_PATTERN}{prefix_pattern}-{color_pattern}-{shade_pattern}(?:/\d+)?)\b")

    # Build whitelist pattern for white/black/transparent
    whitelist_colors = "(?:" + "|".join(WHITELISTED_COLORS) + ")"
    whitelist_pattern = re.compile(rf"^{STATE_PATTERN}{prefix_pattern}-{whitelist_colors}(?:/\d+)?$")

    return TokenConfig(
        name="color",
        pattern=pattern,
        suggestions={
            "bg-gray-": "bg-insight-*-background",
            "bg-slate-": "bg-insight-*-background",
            "bg-red-": "bg-insight-danger[-soft]",
            "bg-green-": "bg-insight-success[-soft]",
            "bg-yellow-": "bg-insight-warning[-soft]",
            "bg-blue-": "bg-insight-primary[-soft] or bg-insight-info[-soft]",
            "text-gray-": "text-insight-text-headline or text-insight-text-body",
            "text-red-": "text-insight-danger",
            "text-green-": "text-insight-success",
            "text-yellow-": "text-insight-warning",
            "text-blue-": "text-insight-primary or text-insight-info",
            "border-gray-": "border-insight-*-border",
            "ring-blue-": "ring-insight-primary",
            "focus:ring-blue-": "focus:ring-insight-primary",
            "focus:border-blue-": "focus:border-insight-primary",
        },
        whitelist={whitelist_pattern},
    )


# =============================================================================
# Radius Token Configuration
# =============================================================================

# Standard Tailwind rounded values (without insight- prefix)
# Note: "none" is excluded - removing radius is always allowed
TAILWIND_RADII: set[str] = {
    "sm",
    "md",
    "lg",
    "xl",
    "2xl",
    "3xl",
    "full",
}

# Rounded positions
ROUNDED_POSITIONS: list[str] = [
    "",  # rounded-{size}
    "t-",
    "r-",
    "b-",
    "l-",  # sides
    "tl-",
    "tr-",
    "bl-",
    "br-",  # corners
    "s-",
    "e-",  # logical sides
    "ss-",
    "se-",
    "es-",
    "ee-",  # logical corners
]


def build_radius_config() -> TokenConfig:
    """Build configuration for radius token checking.

    Returns:
        TokenConfig for detecting hardcoded rounded classes.

    """
    # Build explicit list of hardcoded Tailwind rounded classes
    # This is more reliable than trying to exclude insight- with lookahead
    hardcoded_variants: list[str] = ["rounded"]

    # rounded-{size}: rounded-sm, rounded-md, rounded-lg, etc.
    hardcoded_variants.extend(f"rounded-{size}" for size in TAILWIND_RADII)

    # rounded-{position}-{size}: rounded-t-lg, rounded-tl-md, etc.
    hardcoded_variants.extend(
        f"rounded-{pos}{size}"
        for pos in ROUNDED_POSITIONS
        if pos  # skip empty position
        for size in TAILWIND_RADII
    )

    # Build alternation pattern (sort by length descending so longer matches are tried first)
    hardcoded_variants.sort(key=len, reverse=True)
    variants_pattern = "(?:" + "|".join(re.escape(v) for v in hardcoded_variants) + ")"

    pattern = re.compile(rf"\b({STATE_PATTERN}{variants_pattern})\b")

    return TokenConfig(
        name="radius",
        pattern=pattern,
        suggestions={
            "rounded-sm": "rounded-insight-s",
            "rounded-md": "rounded-insight-m",
            "rounded-lg": "rounded-insight-l",
            "rounded-xl": "rounded-insight-xl",
            "rounded-2xl": "rounded-insight-xl (or custom)",
            "rounded-3xl": "rounded-insight-xl (or custom)",
            "rounded-full": "rounded-insight-full",
            "rounded": "rounded-insight-control or rounded-insight-surface",
        },
        whitelist=set(),
    )


# =============================================================================
# Shadow Token Configuration
# =============================================================================

# Standard Tailwind shadow values (without insight- prefix)
# Note: "none" is excluded - removing shadow is always allowed
TAILWIND_SHADOWS: set[str] = {
    "sm",
    "md",
    "lg",
    "xl",
    "2xl",
    "inner",
}


def build_shadow_config() -> TokenConfig:
    """Build configuration for shadow token checking.

    Returns:
        TokenConfig for detecting hardcoded shadow classes.

    """
    # Build explicit list of hardcoded Tailwind shadow classes
    hardcoded_variants: list[str] = ["shadow"]  # bare shadow

    # shadow-{size}: shadow-sm, shadow-md, shadow-lg, etc.
    hardcoded_variants.extend(f"shadow-{size}" for size in TAILWIND_SHADOWS)

    # shadow-{color}-{shade}: shadow-blue-500, etc.
    hardcoded_variants.extend(f"shadow-{color}-{shade}" for color in TAILWIND_COLORS for shade in TAILWIND_SHADES)

    # Build alternation pattern (sort by length descending so longer matches are tried first)
    hardcoded_variants.sort(key=len, reverse=True)
    variants_pattern = "(?:" + "|".join(re.escape(v) for v in hardcoded_variants) + ")"

    pattern = re.compile(rf"\b({STATE_PATTERN}{variants_pattern})\b")

    return TokenConfig(
        name="shadow",
        pattern=pattern,
        suggestions={
            "shadow-sm": "shadow-insight-subtle",
            "shadow-md": "shadow-insight-surface",
            "shadow-lg": "shadow-insight-raised",
            "shadow-xl": "shadow-insight-overlay",
            "shadow-2xl": "shadow-insight-overlay",
            "shadow-inner": "(no direct equivalent)",
            "shadow": "shadow-insight-subtle or shadow-insight-surface",
        },
        whitelist=set(),
    )


# =============================================================================
# Verbose Token Configuration
# =============================================================================

# Mapping of verbose token patterns to their shorthand equivalents
# These are custom utilities defined in @layer utilities of input.css
VERBOSE_TOKEN_MAPPINGS: dict[str, str] = {
    # Text utilities - use semantic shorthand
    "text-insight-text-headline": "text-insight-headline",
    "text-insight-text-body": "text-insight-body",
    "text-insight-text-muted": "text-insight-muted",
    "text-insight-text-disabled": "text-insight-disabled",
    # Background utilities - drop redundant "bg-" in token name
    "bg-insight-bg-base": "bg-insight-base",
    "bg-insight-bg-surface": "bg-insight-surface",
    "bg-insight-bg-raised": "bg-insight-raised",
    "bg-insight-bg-overlay": "bg-insight-overlay",
    # Border utilities - drop redundant "border-" in token name
    "border-insight-border-surface": "border-insight-surface",
    "border-insight-border-raised": "border-insight-raised",
    "border-insight-border-overlay": "border-insight-overlay",
}


def build_verbose_config() -> TokenConfig:
    """Build configuration for verbose token checking.

    Detects verbose token names that have shorter equivalents defined
    in @layer utilities of input.css.

    Note: Verbose tokens with opacity modifiers (e.g., bg-insight-bg-raised/50)
    are intentionally allowed because shorthand utilities don't support
    Tailwind's opacity modifier syntax.

    Returns:
        TokenConfig for detecting verbose token classes.

    """
    # Build pattern matching all verbose tokens with optional state prefixes
    # Use negative lookahead to exclude tokens followed by /opacity modifier
    verbose_tokens = list(VERBOSE_TOKEN_MAPPINGS.keys())
    verbose_tokens.sort(key=len, reverse=True)  # Longer matches first
    tokens_pattern = "(?:" + "|".join(re.escape(t) for t in verbose_tokens) + ")"

    # Negative lookahead (?!/\d) ensures we don't match tokens with opacity modifiers
    pattern = re.compile(rf"\b({STATE_PATTERN}{tokens_pattern})(?!/\d)\b")

    return TokenConfig(
        name="verbose",
        pattern=pattern,
        suggestions=VERBOSE_TOKEN_MAPPINGS,
        whitelist=set(),
    )


# =============================================================================
# Violation Detection
# =============================================================================

# Exception markers in Django template comments
EXCEPTION_MARKER = "tw-token-ok"
FILE_EXCEPTION_MARKER = "tw-token-ok-file"


@dataclass
class TokenViolation:
    """Represents a hardcoded token violation.

    Attributes:
        filepath: Path to the file containing the violation.
        line_number: Line number where the violation was found.
        class_name: The hardcoded class that was detected.
        token_type: Type of token (color, radius, shadow).
        suggestion: Suggested replacement if available.

    """

    filepath: Path
    line_number: int
    class_name: str
    token_type: str
    suggestion: str | None = None


def has_exception_marker(line: str) -> bool:
    """Check if a line has an exception marker comment.

    Args:
        line: The line content to check.

    Returns:
        True if the line contains {# tw-token-ok ... #}.

    """
    return EXCEPTION_MARKER in line


def has_file_exception(content: str) -> bool:
    """Check if a file has a file-level exception marker.

    Args:
        content: The full file content.

    Returns:
        True if the file contains {# tw-token-ok-file ... #}.

    """
    return FILE_EXCEPTION_MARKER in content


def is_whitelisted(class_name: str, config: TokenConfig) -> bool:
    """Check if a class is whitelisted for a token type.

    Args:
        class_name: The CSS class to check.
        config: Token configuration with whitelist patterns.

    Returns:
        True if the class matches any whitelist pattern.

    """
    return any(pattern.match(class_name) for pattern in config.whitelist)


def get_suggestion(class_name: str, config: TokenConfig) -> str | None:
    """Get a replacement suggestion for a hardcoded class.

    Args:
        class_name: The hardcoded class (e.g., 'bg-gray-300' or 'hover:bg-gray-300').
        config: Token configuration with suggestions.

    Returns:
        Suggested replacement or None if no suggestion available.
        Preserves state prefixes (hover:, focus:, dark:, etc.) in the suggestion.

    """
    # Extract state prefix if present (e.g., "hover:" from "hover:bg-gray-300")
    state_prefix = ""
    base_class = class_name
    for prefix in STATE_PREFIXES:
        if class_name.startswith(prefix):
            state_prefix = prefix
            base_class = class_name[len(prefix) :]
            break

    # Find suggestion for the base class
    for pattern, suggestion in config.suggestions.items():
        if pattern in base_class or pattern == base_class:
            # Prepend state prefix to suggestion if present
            if state_prefix:
                return f"{state_prefix}{suggestion}"
            return suggestion
    return None


def extract_class_attributes(line: str) -> list[tuple[int, int, str]]:
    """Extract all class attribute values from a line.

    Args:
        line: The line content to parse.

    Returns:
        List of tuples (start_pos, end_pos, class_value) for each class attribute.

    """
    # Match class="..." or class='...'
    # Also handles Django template syntax like class="foo {{ bar }}"
    class_pattern = re.compile(r'\bclass\s*=\s*(["\'])([^"\']*)\1')
    results = []
    for match in class_pattern.finditer(line):
        start = match.start(2)  # Start of the class value
        end = match.end(2)  # End of the class value
        value = match.group(2)
        results.append((start, end, value))
    return results


def find_violations(  # noqa: C901
    filepath: Path,
    configs: list[TokenConfig],
) -> list[TokenViolation]:
    """Find all token violations in a file.

    Args:
        filepath: Path to the HTML file to check.
        configs: List of token configurations to check against.

    Returns:
        List of TokenViolation objects for each violation found.

    """
    content = filepath.read_text(encoding="utf-8")

    # Check for file-level exception
    if has_file_exception(content):
        logger.debug("Skipping %s (file-level exception)", filepath)
        return []

    violations: list[TokenViolation] = []
    lines = content.splitlines()

    for line_number, line in enumerate(lines, start=1):
        # Skip lines with exception marker
        if has_exception_marker(line):
            continue

        # Only search within class="..." attributes
        class_attrs = extract_class_attributes(line)
        if not class_attrs:
            continue

        # Check each token type within each class attribute
        for _start, _end, class_value in class_attrs:
            for config in configs:
                for match in config.pattern.finditer(class_value):
                    class_name = match.group(1)
                    match_end = match.end()

                    # Skip if this is part of an insight- token
                    # e.g., "rounded" in "rounded-insight-surface"
                    # or "rounded" in "rounded-t-insight-control"
                    remaining = class_value[match_end:]
                    # Check if -insight appears before the next space or end of attribute
                    next_space = remaining.find(" ")
                    end_pos = next_space if next_space != -1 else len(remaining)
                    rest_of_class = remaining[:end_pos]
                    if "-insight" in rest_of_class:
                        continue

                    # Skip if this ends with -none (removing styles is always allowed)
                    # e.g., "rounded" in "rounded-ee-none" or "shadow" in "shadow-none"
                    if rest_of_class.endswith("-none"):
                        continue

                    # Skip whitelisted classes
                    if is_whitelisted(class_name, config):
                        continue

                    suggestion = get_suggestion(class_name, config)
                    violations.append(
                        TokenViolation(
                            filepath=filepath,
                            line_number=line_number,
                            class_name=class_name,
                            token_type=config.name,
                            suggestion=suggestion,
                        )
                    )

    return violations


# =============================================================================
# CLI
# =============================================================================


def find_template_files(base_path: Path) -> list[Path]:
    """Find all HTML template files in the given directory.

    Args:
        base_path: Base directory to search in.

    Returns:
        List of paths to HTML files in templates directories.

    """
    templates_dir = base_path / "insight_ui" / "templates"
    if not templates_dir.exists():
        return []
    return sorted(templates_dir.rglob("*.html"))


def find_staged_template_files() -> list[Path]:
    """Find staged HTML template files via git.

    Returns:
        List of paths to staged HTML files in templates directories.

    """
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],  # noqa: S607
        capture_output=True,
        text=True,
        check=False,
    )  # nosec B603 B607 - git is a trusted command with static arguments
    if result.returncode != 0:
        return []

    files = []
    for line in result.stdout.strip().splitlines():
        path = Path(line)
        if path.suffix == ".html" and "templates" in path.parts:
            files.append(path)
    return sorted(files)


def print_usage() -> None:
    """Print CLI usage information."""
    logger.error(
        "Usage: check_design_tokens.py [--all | --staged] [file1.html ...]\n\n"
        "Checks for hardcoded Tailwind utilities that should use design tokens:\n"
        "  - Colors: bg-gray-300 -> bg-insight-*\n"
        "  - Radii: rounded-lg -> rounded-insight-*\n"
        "  - Shadows: shadow-md -> shadow-insight-*\n"
        "  - Verbose: text-insight-text-body -> text-body\n\n"
        "Options:\n"
        "  --all     Scan all template files in insight_ui/templates/\n"
        "  --staged  Scan only staged template files (for pre-commit)\n\n"
        "To suppress warnings, add a comment on the same line:\n"
        '  <div class="rounded-lg {# tw-token-ok: reason #}">\n\n'
        "To suppress all warnings in a file, add at the top:\n"
        "  {# tw-token-ok-file: reason #}"
    )


def collect_files_to_check(
    args: list[str],
    scan_all: bool,
    scan_staged: bool,
) -> list[Path] | None:
    """Collect files to check based on CLI arguments.

    Args:
        args: Remaining CLI arguments (file paths).
        scan_all: Whether to scan all template files.
        scan_staged: Whether to scan only staged files.

    Returns:
        List of paths to check, or None if --staged with no staged files.

    """
    if scan_all:
        return find_template_files(Path.cwd())
    if scan_staged:
        files = find_staged_template_files()
        return files or None
    return [Path(f) for f in args]


def print_violations(violations: list[TokenViolation]) -> None:
    """Print violations grouped by file with summary.

    Args:
        violations: List of violations to print.

    """
    current_file: Path | None = None
    for violation in violations:
        if violation.filepath != current_file:
            current_file = violation.filepath
            logger.info("\n%s:", current_file)

        if violation.suggestion:
            logger.info(
                "  %d: [%s] %s -> %s",
                violation.line_number,
                violation.token_type,
                violation.class_name,
                violation.suggestion,
            )
        else:
            logger.info(
                "  %d: [%s] %s",
                violation.line_number,
                violation.token_type,
                violation.class_name,
            )

    # Summary by type
    by_type: dict[str, int] = {}
    for v in violations:
        by_type[v.token_type] = by_type.get(v.token_type, 0) + 1

    logger.info("\nSummary:")
    for token_type, count in sorted(by_type.items()):
        logger.info("  %s: %d violation(s)", token_type, count)
    logger.info("  Total: %d", len(violations))
    logger.info("\nAdd {# tw-token-ok: reason #} to suppress individual warnings")


def main() -> int:
    """Main entry point for the CLI.

    Returns:
        Exit code: 0 if no violations, 1 if violations found.

    """
    args = sys.argv[1:]
    scan_all = "--all" in args
    scan_staged = "--staged" in args
    args = [a for a in args if a not in ("--all", "--staged")]

    if not args and not scan_all and not scan_staged:
        print_usage()
        return 1

    configs = [
        build_color_config(),
        build_radius_config(),
        build_shadow_config(),
        build_verbose_config(),
    ]

    files_to_check = collect_files_to_check(args, scan_all, scan_staged)
    if files_to_check is None:
        return 0  # --staged with no staged files

    all_violations: list[TokenViolation] = []
    for path in files_to_check:
        if not path.exists():
            logger.warning("File not found: %s", path)
            continue
        all_violations.extend(find_violations(path, configs))

    if not all_violations:
        return 0

    print_violations(all_violations)
    return 1


if __name__ == "__main__":
    sys.exit(main())
