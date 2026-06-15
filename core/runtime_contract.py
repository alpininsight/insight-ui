"""Runtime contract helpers for health, readiness, and service identity."""

from __future__ import annotations

import os
from pathlib import Path
from socket import gethostname
from typing import Any

from django.conf import settings
from django.db import connections
from django.db.utils import DatabaseError


def _directory_check(path: Path, *, require_write: bool) -> str:
    """Return a cheap status string for a required runtime directory."""
    if not path.exists():
        return "missing"
    if not path.is_dir():
        return "not-a-directory"
    if require_write and not os.access(path, os.W_OK):
        return "not-writable"
    if not require_write and not os.access(path, os.R_OK):
        return "not-readable"
    return "ok"


def get_runtime_instance_id() -> str:
    """Return a stable runtime instance identifier for the current process."""
    return os.environ.get("SERVICE_INSTANCE_ID", "").strip() or gethostname()


def build_runtime_info() -> dict[str, Any]:
    """Build the canonical runtime identity payload for HTTP callers."""
    deployment: dict[str, Any] = {
        "environment": {"name": settings.DEPLOYMENT_ENVIRONMENT},
        "platform_namespace": settings.PLATFORM_NAMESPACE,
    }
    if settings.DEPLOYMENT_LANE:
        deployment["lane"] = settings.DEPLOYMENT_LANE
    if settings.DEPLOYMENT_SLOT:
        deployment["slot"] = settings.DEPLOYMENT_SLOT

    payload: dict[str, Any] = {
        "service": {
            "namespace": settings.SERVICE_NAMESPACE,
            "name": settings.SERVICE_NAME,
            "version": settings.ARTIFACT_VERSION,
            "instance_id": get_runtime_instance_id(),
        },
        "deployment": deployment,
        "build": {"revision": settings.GIT_COMMIT_SHA},
    }

    if settings.PUBLIC_BASE_URL:
        payload["urls"] = {"public_base": settings.PUBLIC_BASE_URL}

    return payload


def check_runtime_readiness() -> tuple[bool, dict[str, str]]:
    """Validate only cheap local prerequisites needed to serve traffic."""
    checks = {
        "data_dir": _directory_check(settings.DATA_DIR, require_write=True),
        "static_root": _directory_check(settings.STATIC_ROOT, require_write=False),
    }

    try:
        connections["default"].ensure_connection()
    except DatabaseError:
        checks["database"] = "unavailable"
    else:
        checks["database"] = "ok"

    is_ready = all(status == "ok" for status in checks.values())
    return is_ready, checks
