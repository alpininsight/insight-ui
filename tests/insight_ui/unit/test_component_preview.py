# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Exercise the source-only contributor preview and its distribution boundary."""

import io
import json
import tarfile
import zipfile
from collections.abc import Iterator
from dataclasses import replace
from email.message import EmailMessage
from http import HTTPStatus
from pathlib import Path
from unittest.mock import Mock
from urllib.parse import urlsplit

import pytest
from bs4 import BeautifulSoup
from devtools import preview, settings as preview_settings
from devtools.__main__ import main
from django.test import Client, override_settings
from insight_ui.component_manifest import load_manifest
from scripts.check_distribution import REQUIRED, SOURCE_ONLY, check_archive


@pytest.fixture
def preview_client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Iterator[Client]:
    """Render real ButtonConfig examples from a temporary declarative contract."""
    contract = {
        "schema_version": 1,
        "slug": "button",
        "name": "Example Button",
        "category": "input",
        "level": "atom",
        "config_class": "insight_ui.configs.input.ButtonConfig",
        "template": "insight_ui/components/button.html",
        "uses": [],
        "examples": [
            {"name": "default", "config": {"label": "Local example", "tag_id": "preview-button"}},
            {"name": "escaped", "config": {"label": '<script>alert("example")</script>', "tag_id": "escaped-button"}},
        ],
        "js_module": None,
    }
    (tmp_path / "button.json").write_text(json.dumps(contract), encoding="utf-8")
    monkeypatch.setattr(preview, "manifest_path", lambda slug: tmp_path / f"{slug}.json")
    with override_settings(
        ROOT_URLCONF="devtools.urls",
        INSTALLED_APPS=preview_settings.INSTALLED_APPS,
        MIDDLEWARE=preview_settings.MIDDLEWARE,
        TEMPLATES=preview_settings.TEMPLATES,
        ALLOWED_HOSTS=preview_settings.ALLOWED_HOSTS,
        INSIGHT_UI=preview_settings.INSIGHT_UI,
        INSIGHT_UI_PREVIEW_COMPONENT="button",
        STATIC_URL="/static/",
        STORAGES=preview_settings.STORAGES,
    ):
        yield Client(headers={"host": "127.0.0.1"})


def test_preview_renders_only_selected_component(preview_client: Client) -> None:
    """The root is a single real component, never the full documentation host."""
    response = preview_client.get("/?component=navbar")
    assert response.status_code == HTTPStatus.OK
    soup = BeautifulSoup(response.content, "html.parser")
    stage = soup.select_one(".preview-stage")
    assert stage is not None
    assert stage.select_one("#preview-button").get_text(strip=True) == "Local example"
    assert len(stage.find_all("button")) == 1
    assert soup.title.get_text() == "Example Button | Local component preview"
    assert preview_client.get("/navbar/").status_code == HTTPStatus.NOT_FOUND
    assert preview_client.get("/docs/components/button/").status_code == HTTPStatus.NOT_FOUND


def test_preview_escapes_config_text(preview_client: Client) -> None:
    """JSON strings remain escaped when the real inclusion tag renders them."""
    response = preview_client.get("/?example=escaped")
    assert response.status_code == HTTPStatus.OK
    soup = BeautifulSoup(response.content, "html.parser")
    button = soup.select_one("#escaped-button")
    assert button is not None
    assert button.get_text(strip=True) == '<script>alert("example")</script>'
    assert button.find("script") is None


@pytest.mark.parametrize("example", ["missing", "../default", "{% debug %}"])
def test_unknown_example_is_not_rendered(preview_client: Client, example: str) -> None:
    """Unknown example input never becomes a file path or template expression."""
    assert preview_client.get("/", {"example": example}).status_code == HTTPStatus.NOT_FOUND


@pytest.mark.parametrize("slug", ["missing", "../button", "button %}{% debug", ""])
def test_unknown_component_is_not_rendered(preview_client: Client, slug: str) -> None:
    """Absent or invalid CLI selections produce a bounded 404 response."""
    with override_settings(INSIGHT_UI_PREVIEW_COMPONENT=slug):
        assert preview_client.get("/").status_code == HTTPStatus.NOT_FOUND


def test_manifest_must_match_selected_slug(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """A manifest cannot redirect an allowed slug to a different template tag."""
    manifest = Mock(slug="navbar")
    monkeypatch.setattr(preview, "manifest_path", lambda slug: tmp_path / f"{slug}.json")
    monkeypatch.setattr(preview, "load_manifest", lambda _path: manifest)
    with pytest.raises(ValueError, match="does not match"):
        preview.selected_manifest("button")


@pytest.mark.parametrize("host", ["example.com", "0.0.0.0", "192.168.1.10"])  # noqa: S104
def test_preview_rejects_non_local_hosts(preview_client: Client, host: str) -> None:
    """Loopback binding is backed by an explicit Host allowlist."""
    assert preview_client.get("/", HTTP_HOST=host).status_code == HTTPStatus.BAD_REQUEST


def test_preview_has_no_write_endpoint(preview_client: Client) -> None:
    """The browser cannot invoke the scaffold command or mutate examples."""
    assert preview_client.post("/", {"name": "Unexpected Component"}).status_code == HTTPStatus.METHOD_NOT_ALLOWED
    assert preview_client.post("/create_component/").status_code == HTTPStatus.NOT_FOUND


def test_preview_assets_stay_local_and_uncached(preview_client: Client) -> None:
    """No base-template CDN dependencies or mutable CDN paths leak into preview."""
    response = preview_client.get("/")
    soup = BeautifulSoup(response.content, "html.parser")
    asset_urls = [node["src"] for node in soup.select("script[src], img[src]")]
    asset_urls += [node["href"] for node in soup.select("link[href]")]
    assert "/static/insight_ui/css/tailwind.css" in asset_urls
    assert "/static/insight_ui/js/insight-ui-utils.js" in asset_urls
    assert "/static/devtools/preview.js" in asset_urls
    assert all(url.startswith("/") and not urlsplit(url).netloc for url in asset_urls)
    assert "script-src 'self'" in response.headers["Content-Security-Policy"]
    assert "connect-src 'self'" in response.headers["Content-Security-Policy"]
    assert "form-action 'none'" in response.headers["Content-Security-Policy"]
    assert "no-store" in response.headers["Cache-Control"]
    assert response.headers["Referrer-Policy"] == "no-referrer"
    assert response.headers["X-Content-Type-Options"] == "nosniff"


def test_preview_settings_have_no_documentation_or_cdn() -> None:
    """The contributor host always opts out of CDN and full self-documentation."""
    assert preview_settings.INSIGHT_UI["assets"] == {"cdn_enabled": False, "use_minified": False}
    assert preview_settings.INSIGHT_UI["use_tailwind_cli"] is False
    assert preview_settings.STATIC_URL == "/static/"
    assert "documentation" not in preview_settings.INSTALLED_APPS
    assert "core" not in preview_settings.INSTALLED_APPS
    assert "devtools" in preview_settings.INSTALLED_APPS
    assert preview_settings.DATABASES["default"]["NAME"] == ":memory:"


@pytest.mark.parametrize("module", ["https://example.com/evil.js", "//example.com/evil.js", "insight_ui/js/../evil.js"])
def test_preview_rejects_non_package_javascript(
    preview_client: Client,
    monkeypatch: pytest.MonkeyPatch,
    module: str,
) -> None:
    """The optional initializer cannot introduce arbitrary network dependencies."""
    manifest = load_manifest(preview.manifest_path("button"))
    manifest = replace(manifest, js_module=module)
    monkeypatch.setattr(preview, "selected_manifest", lambda _slug: manifest)
    with pytest.raises(ValueError, match="local insight_ui/js"):
        preview_client.get("/")


def test_preview_exposes_only_local_component_modules(
    preview_client: Client,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The optional selected initializer is serialized as data, not inline code."""
    manifest = load_manifest(preview.manifest_path("button"))
    manifest = replace(manifest, js_module="insight_ui/js/insight-ui-theme-toggle.js")
    monkeypatch.setattr(preview, "selected_manifest", lambda _slug: manifest)
    response = preview_client.get("/")
    assert response.status_code == HTTPStatus.OK
    soup = BeautifulSoup(response.content, "html.parser")
    modules = soup.select_one("#preview-component-modules")
    assert modules["type"] == "application/json"
    assert json.loads(modules.string) == ["/static/insight_ui/js/insight-ui-theme-toggle.js"]


def test_preview_local_static_files_exist(preview_client: Client) -> None:
    """Every initial HTML resource and each stock initializer is available locally."""
    from django.contrib.staticfiles import finders  # noqa: PLC0415

    response = preview_client.get("/")
    soup = BeautifulSoup(response.content, "html.parser")
    urls = [node["href"] for node in soup.select("link[href]")]
    urls += [node["src"] for node in soup.select("script[src]")]
    for url in urls:
        if url.startswith("/static/"):
            assert finders.find(url.removeprefix("/static/")), url
    assert preview_client.get("/jsi18n/").status_code == HTTPStatus.OK


def test_preview_module_dependencies_do_not_recurse_forever(
    preview_client: Client,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Mutually referencing local contracts are visited only once."""
    manifest = load_manifest(preview.manifest_path("button"))
    manifest = replace(manifest, uses=("button",), js_module="insight_ui/js/insight-ui-theme-toggle.js")
    monkeypatch.setattr(preview, "selected_manifest", lambda _slug: manifest)
    response = preview_client.get("/")
    assert response.status_code == HTTPStatus.OK
    soup = BeautifulSoup(response.content, "html.parser")
    assert json.loads(soup.select_one("#preview-component-modules").string) == [
        "/static/insight_ui/js/insight-ui-theme-toggle.js"
    ]


def test_create_command_passes_dry_run_to_django(monkeypatch: pytest.MonkeyPatch) -> None:
    """The CLI delegates to the existing management command, not a second writer."""
    dispatch = Mock()
    monkeypatch.setattr("devtools.__main__.execute_from_command_line", dispatch)
    monkeypatch.setenv("DJANGO_SETTINGS_MODULE", "unused.production.settings")
    arguments = [
        "create_component",
        "--name",
        "Example Panel",
        "--category",
        "form",
        "--level",
        "molecule",
        "--compose",
        "input_field,button",
        "--dry-run",
    ]
    main(arguments)
    dispatch.assert_called_once_with(["devtools", *arguments, "--settings=devtools.settings"])


@pytest.mark.parametrize("option", ["--settings=other.settings", "--pythonpath=/tmp/other"])
def test_create_command_cannot_replace_source_host(monkeypatch: pytest.MonkeyPatch, option: str) -> None:
    """Pass-through generator flags must not switch to unrelated Django hosts."""
    monkeypatch.setenv("DJANGO_SETTINGS_MODULE", "tests.settings")
    with pytest.raises(SystemExit, match="2"):
        main(["create_component", option])


def test_preview_command_binds_loopback(monkeypatch: pytest.MonkeyPatch) -> None:
    """The CLI has no address argument and always binds its validated TCP port locally."""
    dispatch = Mock()
    monkeypatch.setattr("devtools.__main__.execute_from_command_line", dispatch)
    monkeypatch.setattr(preview, "selected_manifest", Mock())
    monkeypatch.setenv("DJANGO_SETTINGS_MODULE", "tests.settings")
    monkeypatch.setenv("INSIGHT_UI_PREVIEW_COMPONENT", "")
    main(["preview", "example_panel", "--port", "8017", "--no-reload"])
    dispatch.assert_called_once_with(
        ["devtools", "runserver", "127.0.0.1:8017", "--settings=devtools.settings", "--noreload"]
    )


@pytest.mark.parametrize("port", ["0", "65536", "-1", "0.0.0.0:8010", "not-a-port"])
def test_preview_command_rejects_invalid_ports(monkeypatch: pytest.MonkeyPatch, port: str) -> None:
    """Runserver cannot receive an arbitrary address disguised as a port."""
    monkeypatch.setenv("DJANGO_SETTINGS_MODULE", "tests.settings")
    with pytest.raises(SystemExit, match="2"):
        main(["preview", "example_panel", "--port", port])


def _archive(path: Path, names: set[str], metadata: bytes = b"") -> None:
    """Make tiny deterministic archives to verify the public package boundary."""
    if path.suffix == ".whl":
        with zipfile.ZipFile(path, "w") as archive:
            for name in sorted(names):
                archive.writestr(name, "test fixture")
            if metadata:
                archive.writestr("insight_ui-0.0.0.dist-info/METADATA", metadata)
    else:
        with tarfile.open(path, "w:gz") as archive:
            for name in sorted(names):
                member = tarfile.TarInfo(f"insight_ui-0.0.0/{name}")
                data = b"test fixture"
                member.size = len(data)
                archive.addfile(member, io.BytesIO(data))
            if metadata:
                member = tarfile.TarInfo("insight_ui-0.0.0/PKG-INFO")
                member.size = len(metadata)
                archive.addfile(member, io.BytesIO(metadata))


def test_preview_is_source_only_in_distributions(tmp_path: Path, distribution_metadata: EmailMessage) -> None:
    """A valid source archive includes the helper; a wheel must exclude all of it."""
    wheel = tmp_path / "insight_ui-0.0.0-py3-none-any.whl"
    sdist = tmp_path / "insight_ui-0.0.0.tar.gz"
    _archive(wheel, REQUIRED, distribution_metadata.as_bytes())
    _archive(sdist, REQUIRED | SOURCE_ONLY, distribution_metadata.as_bytes())
    check_archive(wheel)
    check_archive(sdist)
    _archive(wheel, REQUIRED | {"devtools/__main__.py"})
    with pytest.raises(SystemExit, match=r"devtools/__main__\.py"):
        check_archive(wheel)


def test_source_archive_requires_preview_helpers(tmp_path: Path) -> None:
    """A source release must not advertise a command it forgot to include."""
    sdist = tmp_path / "insight_ui-0.0.0.tar.gz"
    _archive(sdist, REQUIRED)
    with pytest.raises(SystemExit, match=r"missing=.*devtools"):
        check_archive(sdist)


@pytest.mark.parametrize("name", ["documentation/views.py", "enterprise/audit.py", "docs/internal.md"])
def test_preview_does_not_relax_documentation_boundary(tmp_path: Path, name: str) -> None:
    """Allowing source preview files never permits the private docs app or reports."""
    sdist = tmp_path / "insight_ui-0.0.0.tar.gz"
    _archive(sdist, REQUIRED | SOURCE_ONLY | {name})
    with pytest.raises(SystemExit, match="unexpected="):
        check_archive(sdist)
