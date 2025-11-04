"""Django Insight UI - Ein barrierefreies UI-Framework für Django."""

from __future__ import annotations

try:  # Prefer generated version file from hatch-vcs at build time
    from ._version import __version__ as __version__  # type: ignore
except Exception:  # pragma: no cover - fallback for editable installs
    try:
        from importlib.metadata import PackageNotFoundError, version

        __version__ = version("django-insight-ui")
    except Exception:
        __version__ = "0.0.0"
