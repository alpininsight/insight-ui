# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Smoke-test every built wheel and sdist: python -I scripts/smoke_distribution.py [dist]."""

import argparse
import importlib
import os
import secrets
import shutil
import subprocess  # nosec B404 - run fixed tools without a shell in disposable environments.
import sys
import tempfile
from pathlib import Path

SOURCE_ROOT = Path(__file__).resolve().parent.parent
REQUIRED_ASSETS = {"insight_ui/css/tailwind.css", "insight_ui/js/insight-ui-init.js"}
PUBLIC_MODULES = ("insight_ui", "django", "markdown", "defusedxml")
STEP_TIMEOUT = 600
urlpatterns = []


def find_archives(directory: Path) -> list[Path]:
    """Require both formats and return every exact artifact in stable order."""
    wheels = sorted(path.resolve() for path in directory.glob("*.whl") if path.is_file())
    sdists = sorted(path.resolve() for path in directory.glob("*.tar.gz") if path.is_file())
    if not wheels or not sdists:
        message = f"{directory}: build both wheel and sdist with uv build first."
        raise ValueError(message)
    return [*wheels, *sdists]


def clean_environment(root: Path) -> dict[str, str]:
    """Keep only platform essentials, with disposable config and credential homes."""
    allowed = {"PATH", "SYSTEMROOT", "SystemRoot", "WINDIR", "COMSPEC", "PATHEXT", "LANG", "LC_ALL"}
    environment = {key: value for key, value in os.environ.items() if key in allowed}
    environment.update(
        HOME=str(root),
        USERPROFILE=str(root),
        XDG_CONFIG_HOME=str(root / "config"),
        XDG_DATA_HOME=str(root / "data"),
        XDG_CACHE_HOME=str(root / "cache"),
        APPDATA=str(root / "config"),
        LOCALAPPDATA=str(root / "data"),
        UV_CREDENTIALS_DIR=str(root / "credentials"),
        NETRC=str(root / ".netrc"),
        TMPDIR=str(root),
        TMP=str(root),
        TEMP=str(root),
    )
    return environment


def require_origin(path: Path, root: Path) -> None:
    """Reject imports and assets resolved outside the disposable installation."""
    if not path.resolve().is_relative_to(root.resolve()):
        message = f"Unexpected origin outside {root}: {path}"
        raise RuntimeError(message)


def check_imports(environment: Path) -> Path:
    """Check dependencies and all loaded package submodules, including symlinks."""
    for name in PUBLIC_MODULES:
        importlib.import_module(name)
    for name, module in tuple(sys.modules.items()):
        if name.split(".")[0] in PUBLIC_MODULES and getattr(module, "__file__", None):
            require_origin(Path(module.__file__), environment)
    return Path(sys.modules["insight_ui"].__file__).resolve().parent


def check_component() -> None:
    """Render the public button tag with the package's host configuration API."""
    from django.template import Context, Template  # noqa: PLC0415
    from insight_ui.config import get_config  # noqa: PLC0415

    rendered = Template(
        '{% load insight_tags %}{% button label="Distribution smoke" type="primary" tag_id="distribution-smoke" %}'
    ).render(Context(get_config()))
    expected = ("<button", 'id="distribution-smoke"', "btn-primary", "Distribution smoke", "</button>")
    if not all(fragment in rendered for fragment in expected):
        message = "Public button component did not render the expected markup."
        raise RuntimeError(message)


def check_assets(package: Path, destination: Path) -> None:
    """Discover installed core assets and compare every collected file's content."""
    from django.contrib.staticfiles import finders  # noqa: PLC0415
    from django.core.management import call_command  # noqa: PLC0415

    static = package / "static"
    assets = {path.relative_to(static).as_posix(): path for path in static.rglob("*") if path.is_file()}
    missing = REQUIRED_ASSETS - assets.keys()
    if missing:
        message = f"Installed package is missing core static assets: {sorted(missing)}"
        raise RuntimeError(message)
    for name, path in assets.items():
        require_origin(path, static)
        discovered = finders.find(name)
        if not discovered or Path(discovered).resolve() != path.resolve():
            message = f"Static discovery did not select the installed asset: {name}"
            raise RuntimeError(message)
    call_command("collectstatic", interactive=False, verbosity=0)
    for name, path in assets.items():
        collected = destination / name
        require_origin(collected, destination)
        if not collected.is_file() or collected.read_bytes() != path.read_bytes():
            message = f"collectstatic did not preserve the installed asset: {name}"
            raise RuntimeError(message)


def probe(environment: Path) -> None:
    """Run a minimal, local-only Django host inside the artifact's environment."""
    if not sys.flags.isolated or Path(sys.prefix).resolve() != environment.resolve() or sys.prefix == sys.base_prefix:
        message = "The runtime probe requires its own virtual environment and Python -I."
        raise RuntimeError(message)
    if Path.cwd().resolve().is_relative_to(SOURCE_ROOT):
        message = "The runtime probe must run outside the source checkout."
        raise RuntimeError(message)
    package = check_imports(environment)

    import django  # noqa: PLC0415
    from django.conf import settings  # noqa: PLC0415
    from django.core.management import call_command  # noqa: PLC0415

    static_root = Path.cwd() / "collected-static"
    settings.configure(
        SECRET_KEY=secrets.token_urlsafe(32),
        INSTALLED_APPS=["django.contrib.staticfiles", "insight_ui"],
        ROOT_URLCONF=__name__,
        DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}},
        TEMPLATES=[{"BACKEND": "django.template.backends.django.DjangoTemplates", "APP_DIRS": True}],
        STATIC_URL="/static/",
        STATIC_ROOT=static_root,
        STATICFILES_FINDERS=["django.contrib.staticfiles.finders.AppDirectoriesFinder"],
        STORAGES={
            "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
            "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
        },
        INSIGHT_UI={"assets": {"cdn_enabled": False, "use_minified": False}, "use_tailwind_cli": False},
        DEFAULT_AUTO_FIELD="django.db.models.BigAutoField",
    )
    django.setup()
    call_command("check", verbosity=0, fail_level="WARNING")
    check_component()
    check_assets(package, static_root)
    check_imports(environment)
    sys.stdout.write(f"Imports, Django check, button render and collectstatic passed: {package}\n")


def smoke_archive(archive: Path, uv: str) -> None:
    """Install one exact archive, never an editable checkout or index substitute."""
    with tempfile.TemporaryDirectory(prefix="insight-ui-distribution-") as temporary:
        root = Path(temporary).resolve()
        if root.is_relative_to(SOURCE_ROOT):
            message = "Temporary directory is inside the checkout; set TMPDIR to an external directory."
            raise RuntimeError(message)
        environment = clean_environment(root)
        venv = root / "venv"
        python = venv / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
        uv_command = [uv, "--no-config", "--no-cache", "--no-python-downloads"]
        commands = [
            [*uv_command, "venv", "--python", sys.executable, str(venv)],
            [
                *uv_command,
                "pip",
                "install",
                "--python",
                str(python),
                "--default-index",
                "https://pypi.org/simple",
                "--keyring-provider",
                "disabled",
                str(archive.resolve()),
            ],
            [str(python), "-I", str(Path(__file__).resolve()), "--probe", str(venv)],
        ]
        for stage, command in zip(("venv", "install", "probe"), commands, strict=True):
            sys.stdout.write(f"{archive.name}: {stage}\n")
            sys.stdout.flush()
            try:
                # Arguments are separate, environment is cleared, and no shell is involved.
                subprocess.run(  # noqa: S603 # nosec B603
                    command, check=True, cwd=root, env=environment, timeout=STEP_TIMEOUT
                )
            except (OSError, subprocess.SubprocessError) as error:
                message = f"{archive.name}: {stage} failed: {error}"
                raise RuntimeError(message) from error


def main(argv: list[str] | None = None) -> int:
    """Smoke all artifacts in a build directory, stopping on the first failure."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", nargs="?", type=Path, default=Path("dist"))
    parser.add_argument("--probe", type=Path, help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    try:
        if args.probe is not None:
            probe(args.probe)
        else:
            archives = find_archives(args.directory)
            uv = shutil.which("uv")
            if uv is None:
                sys.stderr.write("Distribution smoke failed: uv is required on PATH.\n")
                return 1
            for archive in archives:
                smoke_archive(archive, str(Path(uv).resolve()))
    except (ValueError, RuntimeError, OSError) as error:
        sys.stderr.write(f"Distribution smoke failed: {error}\n")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
