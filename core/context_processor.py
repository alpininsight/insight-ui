import importlib
import tomllib
from functools import lru_cache
from pathlib import Path

import structlog
from django.conf import settings
from django.http import HttpRequest

_PYPROJECT_PATH = Path(settings.BASE_DIR) / "pyproject.toml"


logger = structlog.getLogger(__name__)


@lru_cache(maxsize=1)
def get_app_version() -> str:
    """
    Return the application version string (e.g. 'v1.1.0').

    Resolution order:

    1. ``APP_VERSION`` environment variable — set at build time in Docker images
       (e.g. via ``ARG APP_VERSION`` + ``ENV APP_VERSION``). Preferred source in
       production images where the project is not installed as a package.
    2. Installed distribution metadata via ``importlib.metadata`` — used when
       the project is installed as an editable package (local dev with
       ``uv sync``).
    3. ``pyproject.toml`` at ``BASE_DIR`` — fallback for runtime environments
       where the project runs from source and the env var was not set.
    4. Literal ``dev`` — last-resort fallback.

    Cached for the lifetime of the process (``lru_cache``).
    """
    env_version = getattr(settings, "APP_VERSION", "") or ""
    if env_version:
        return env_version if env_version.startswith("v") else f"v{env_version}"

    version = importlib.metadata.version("insight-ui")
    if not version and _PYPROJECT_PATH.is_file():
        try:
            with _PYPROJECT_PATH.open("rb") as fh:
                data = tomllib.load(fh)
            version = data.get("project", {}).get("version", "") or ""
        except (OSError, tomllib.TOMLDecodeError) as exc:
            logger.warning("Could not read version from pyproject.toml: %s", exc)

    return f"v{version}" if version else "dev"


def project_context(request: HttpRequest) -> dict:
    """Contains information of the project."""
    return {}
