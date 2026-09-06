"""Check the built public wheel and sdist, not just packaging configuration."""

import sys
import tarfile
import zipfile
from pathlib import Path, PurePosixPath

FORBIDDEN = {"core", "documentation", "enterprise", "docs", ".github", "Dockerfile", "docker", "manage.py"}
DOC_ASSETS = {"insight-ui-demo-container", "insight-ui-demo-sandbox", "insight-ui-mockup-toc"}
REQUIRED = {
    "insight_ui/__init__.py",
    "insight_ui/templates/insight_ui/base.html",
    "insight_ui/utils/input.css",
    "insight_ui/static/insight_ui/css/tailwind.css",
    "insight_ui/static/insight_ui/js/insight-ui-init.js",
}


def check_archive(archive: Path) -> None:
    """Fail if app/enterprise files leaked or required public assets are absent."""
    if archive.suffix == ".whl":
        with zipfile.ZipFile(archive) as wheel:
            names = {PurePosixPath(name) for name in wheel.namelist()}
    else:
        with tarfile.open(archive) as sdist:
            names = {PurePosixPath(*PurePosixPath(name).parts[1:]) for name in sdist.getnames()}
    leaked = sorted(
        str(name)
        for name in names
        if FORBIDDEN.intersection(name.parts) or any(name.name.startswith(asset) for asset in DOC_ASSETS)
    )
    missing = sorted(REQUIRED - {str(name) for name in names})
    if leaked or missing:
        message = f"{archive.name}: unexpected={leaked}; missing={missing}"
        raise SystemExit(message)


if __name__ == "__main__":
    root = Path(sys.argv[1] if len(sys.argv) > 1 else "dist")
    archives = [*root.glob("*.whl"), *root.glob("*.tar.gz")]
    if not any(p.suffix == ".whl" for p in archives) or not any(p.name.endswith(".tar.gz") for p in archives):
        message = "Build both wheel and sdist before checking distribution boundaries."
        raise SystemExit(message)
    for archive in archives:
        check_archive(archive)
