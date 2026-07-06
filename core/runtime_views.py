"""HTTP runtime contract endpoints."""

from __future__ import annotations

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.http import require_GET

from core.runtime_contract import build_runtime_info, check_runtime_readiness


@require_GET
def healthz_view(_request: HttpRequest) -> HttpResponse:
    """Cheap liveness endpoint for container and Kubernetes probes."""
    return HttpResponse("OK", content_type="text/plain")


@require_GET
def readyz_view(_request: HttpRequest) -> JsonResponse:
    """Cheap readiness endpoint for local runtime prerequisites."""
    is_ready, checks = check_runtime_readiness()
    return JsonResponse({"status": "ok" if is_ready else "error", "checks": checks}, status=200 if is_ready else 503)


@require_GET
def api_info_view(_request: HttpRequest) -> JsonResponse:
    """Canonical runtime identity endpoint."""
    return JsonResponse(build_runtime_info())
