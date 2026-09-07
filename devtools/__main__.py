# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Scaffold and preview one component from an Insight UI source checkout."""

import argparse
import os
import sys

from django.core.management import execute_from_command_line
from django.core.management.base import CommandError

MAX_PORT = 65535


def _port(value: str) -> int:
    """Accept a TCP port, not a runserver address or extra command arguments."""
    try:
        number = int(value)
    except ValueError as error:
        message = "The port must be an integer between 1 and 65535."
        raise argparse.ArgumentTypeError(message) from error
    if not 1 <= number <= MAX_PORT:
        message = "The port must be between 1 and 65535."
        raise argparse.ArgumentTypeError(message)
    return number


def main(argv: list[str] | None = None) -> None:
    """Dispatch generation to Django and constrain the preview to loopback."""
    arguments = list(sys.argv[1:] if argv is None else argv)
    parser = argparse.ArgumentParser(description=__doc__, prog="python -m devtools")
    parser.add_argument("command", choices=("create_component", "preview"))
    if not arguments or arguments[0] in ("-h", "--help"):
        parser.parse_args(arguments)
        return
    command = parser.parse_args(arguments[:1]).command
    os.environ["DJANGO_SETTINGS_MODULE"] = "devtools.settings"

    if command == "create_component":
        if any(arg.split("=", 1)[0] in ("--settings", "--pythonpath") for arg in arguments[1:]):
            parser.error("Contributor commands always use the local devtools.settings host.")
        execute_from_command_line(["devtools", command, *arguments[1:], "--settings=devtools.settings"])
        return

    preview_parser = argparse.ArgumentParser(prog="python -m devtools preview")
    preview_parser.add_argument("component", help="Slug of a component with a contributor manifest.")
    preview_parser.add_argument("--port", type=_port, default=8010)
    preview_parser.add_argument("--no-reload", action="store_true", help="Disable Django's source autoreloader.")
    options = preview_parser.parse_args(arguments[1:])

    from devtools.preview import selected_manifest  # noqa: PLC0415

    try:
        selected_manifest(options.component)
    except (FileNotFoundError, ValueError, TypeError) as error:
        message = f"Cannot preview {options.component!r}: {error}"
        raise CommandError(message) from error

    os.environ["INSIGHT_UI_PREVIEW_COMPONENT"] = options.component
    server_args = ["devtools", "runserver", f"127.0.0.1:{options.port}", "--settings=devtools.settings"]
    if options.no_reload:
        server_args.append("--noreload")
    execute_from_command_line(server_args)


if __name__ == "__main__":
    try:
        main()
    except CommandError as error:
        sys.stderr.write(f"{error}\n")
        raise SystemExit(1) from error
