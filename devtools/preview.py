# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Render a single trusted local component manifest without a docs dependency."""

from __future__ import annotations

import re
from pathlib import PurePosixPath
from typing import TYPE_CHECKING

from django.conf import settings
from django.contrib.staticfiles import finders
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render
from django.template import engines
from django.templatetags.static import static
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_safe
from insight_ui.component_manifest import build_example_config, load_manifest, manifest_path

if TYPE_CHECKING:
    from insight_ui.component_manifest import ComponentManifest

SLUG = re.compile(r"[a-z][a-z0-9]*(?:_[a-z0-9]+)*\Z")


def selected_manifest(slug: str) -> ComponentManifest:
    """Require a validated package manifest matching the selected template tag."""
    if not SLUG.fullmatch(slug):
        message = "Use a component slug such as example_panel."
        raise ValueError(message)
    manifest = load_manifest(manifest_path(slug))
    if manifest.slug != slug:
        message = "The selected manifest does not match its component slug."
        raise ValueError(message)
    return manifest


def _module_url(module: str | None) -> str:
    """Restrict optional component JavaScript to the package's local static tree."""
    if not module:
        return ""
    path = PurePosixPath(module.removeprefix("static/"))
    if (
        path.is_absolute()
        or ".." in path.parts
        or path.parts[:2] != ("insight_ui", "js")
        or path.suffix != ".js"
        or not finders.find(str(path))
    ):
        message = "The preview JavaScript module must be an existing local insight_ui/js/*.js asset."
        raise ValueError(message)
    return static(str(path))


def _component_modules(manifest: ComponentManifest, seen: set[str] | None = None) -> list[str]:
    """Initialize manifested children before their parent, without looping on cycles."""
    visited = set() if seen is None else seen
    if manifest.slug in visited:
        return []
    visited.add(manifest.slug)
    modules = []
    for child in manifest.uses:
        # Built-in components predate manifests; their existing classes load below.
        if manifest_path(child).is_file():
            modules.extend(_component_modules(selected_manifest(child), visited))
    if manifest.js_module:
        modules.append(_module_url(manifest.js_module))
    return modules


@require_safe
@never_cache
def preview(request: HttpRequest) -> HttpResponse:
    """Display only the CLI-selected component and one of its declared examples."""
    # Also check the host when this view is exercised outside CommonMiddleware.
    request.get_host()
    try:
        manifest = selected_manifest(settings.INSIGHT_UI_PREVIEW_COMPONENT)
    except (FileNotFoundError, ValueError, TypeError) as error:
        message = "No valid component was selected for this preview."
        raise Http404(message) from error
    example_name = request.GET.get("example", "default")
    if example_name not in {example.name for example in manifest.examples}:
        message = "This component does not declare the requested example."
        raise Http404(message)

    component_config = build_example_config(manifest, example_name)
    template = engines["django"].from_string(
        "{% load insight_tags %}{% " + manifest.slug + " config=component_config %}"
    )
    component_html = template.render({"component_config": component_config}, request)
    response = render(
        request,
        "devtools/preview.html",
        {
            "manifest": manifest,
            "component_html": component_html,
            "example_name": example_name,
            "component_modules": _component_modules(manifest),
        },
    )
    response["Content-Security-Policy"] = (
        "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data:; font-src 'self'; connect-src 'self'; "
        "object-src 'none'; base-uri 'none'; frame-ancestors 'none'; form-action 'none'"
    )
    response["Referrer-Policy"] = "no-referrer"
    response["X-Content-Type-Options"] = "nosniff"
    return response
