"""Django Insight UI - Ein auf Barrierefreiheit ausgelegtes UI-Framework für Django."""

from __future__ import annotations

try:  # Prefer generated version file from hatch-vcs at build time
    from ._version import __version__ as __version__  # type: ignore[import-not-found]
except ImportError:  # pragma: no cover - fallback for editable installs
    from importlib.metadata import PackageNotFoundError, version

    try:
        __version__ = version("insight-ui")
    except PackageNotFoundError:
        __version__ = "0.0.0"
