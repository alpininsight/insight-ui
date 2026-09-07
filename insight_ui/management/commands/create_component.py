# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Scaffold a public component without importing the documentation app."""

from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING, Any

from django.core.management.base import BaseCommand, CommandError

from insight_ui.component_manifest import CATEGORIES, LEVELS
from insight_ui.scaffolding import ComponentScaffold, apply_component, plan_component

if TYPE_CHECKING:
    from argparse import ArgumentParser


class Command(BaseCommand):
    """Create a component source skeleton, tests and reusable example inputs."""

    help = "Create an atom, molecule or organism in the local insight-ui source checkout."

    def add_arguments(self, parser: ArgumentParser) -> None:
        """Preserve the existing name/category flags and add explicit composition."""
        parser.add_argument("--name", required=True, help="Component name, for example 'Example Panel'.")
        parser.add_argument("--category", required=True, choices=CATEGORIES)
        parser.add_argument("--level", choices=LEVELS, default="atom")
        parser.add_argument("--compose", default="", help="Comma-separated existing component tag names.")
        parser.add_argument("--js", action="store_true", help="Add lifecycle-ready JS and its tests.")
        parser.add_argument("--package-root", type=Path, default=Path.cwd())
        parser.add_argument("--example-config", type=Path, help="JSON object with the default Config values.")
        parser.add_argument("--dry-run", action="store_true", help="Validate and list changes without writing.")

    def handle(self, *_args: object, **options: Any) -> None:  # noqa: ANN401 - Django command option interface
        """Generate only source files; the downstream docs importer is separate."""
        spec = ComponentScaffold(
            name=options["name"],
            category=options["category"],
            level=options["level"],
            compose=tuple(item.strip() for item in options["compose"].split(",") if item.strip()),
            javascript=options["js"],
        )
        try:
            example = None
            if options["example_config"]:
                example = json.loads(options["example_config"].read_text(encoding="utf-8"))
            changes = plan_component(options["package_root"], spec, example)
            if not options["dry_run"]:
                apply_component(changes)
        except (OSError, ValueError, TypeError) as exc:
            raise CommandError(str(exc)) from exc
        for change in changes:
            self.stdout.write(f"{'Would write' if options['dry_run'] else 'Wrote'} {change.path}")
        if not options["dry_run"]:
            self.stdout.write(
                self.style.SUCCESS(f"Created {spec.slug} ({spec.level}). This is a scaffold, not finished behavior.")
            )
            self.stdout.write("Next: npm run build:static-all; uv run pytest; then preview the component.")
            self.stdout.write(f"Preview: uv run python -m devtools preview {spec.slug} --port 8010")
