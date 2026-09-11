# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Test the distribution smoke gate without network resolution or package builds."""

import subprocess
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

import django
import pytest
from django.contrib.staticfiles import finders
from django.core import management
from django.test import override_settings
from scripts import smoke_distribution as smoke


@pytest.fixture
def artifacts(tmp_path: Path) -> list[Path]:
    """Create small archive placeholders; installation is always mocked."""
    paths = [tmp_path / "insight_ui-1.0-py3-none-any.whl", tmp_path / "insight_ui-1.0.tar.gz"]
    for path in paths:
        path.touch()
    return paths


def test_find_archives_uses_every_exact_file(artifacts: list[Path]) -> None:
    """Multiple builds are all checked, while unrelated files are ignored."""
    directory = artifacts[0].parent
    extra = directory / "insight_ui-2.0-py3-none-any.whl"
    extra.touch()
    (directory / "README.txt").touch()
    (directory / "not-an-archive.whl").mkdir()
    assert smoke.find_archives(directory) == [artifacts[0], extra, artifacts[1]]


@pytest.mark.parametrize("names", [[], ["example.whl"], ["example.tar.gz"]])
def test_find_archives_requires_both_formats(tmp_path: Path, names: list[str]) -> None:
    """A missing build format fails before any environment or network work."""
    for name in names:
        (tmp_path / name).touch()
    with pytest.raises(ValueError, match="build both wheel and sdist"):
        smoke.find_archives(tmp_path)


def test_clean_environment_drops_host_configuration(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Neither Python injection nor private indexes, proxies or credentials survive."""
    inherited = {
        "PATH": "/usr/bin",
        "SystemRoot": "C:/Windows",
        "PYTHONPATH": "/checkout",
        "PYTHONHOME": "/other-python",
        "VIRTUAL_ENV": "/host-venv",
        "DJANGO_SETTINGS_MODULE": "documentation.settings",
        "UV_INDEX_URL": "https://private.invalid/simple",
        "UV_EXTRA_INDEX_URL": "https://private.invalid/simple",
        "UV_CONFIG_FILE": "/private-config.toml",
        "UV_KEYRING_PROVIDER": "subprocess",
        "PIP_INDEX_URL": "https://private.invalid/simple",
        "HTTPS_PROXY": "https://private.invalid",
        "GITHUB_TOKEN": "test-only",
        "HOME": "/host-home",
        "NETRC": "/host-netrc",
    }
    monkeypatch.setattr(smoke.os, "environ", inherited)
    environment = smoke.clean_environment(tmp_path)
    assert environment["PATH"] == inherited["PATH"]
    assert environment["SystemRoot"] == inherited["SystemRoot"]
    assert environment["HOME"] == str(tmp_path)
    assert environment["NETRC"] == str(tmp_path / ".netrc")
    assert environment["UV_CREDENTIALS_DIR"] == str(tmp_path / "credentials")
    assert not (inherited.keys() - {"PATH", "SystemRoot", "HOME", "NETRC"}) & environment.keys()


def test_each_archive_gets_a_disposable_environment(artifacts: list[Path], monkeypatch: pytest.MonkeyPatch) -> None:
    """Both formats get a direct install and isolated probe outside the checkout."""
    run = Mock()
    monkeypatch.setattr(smoke.subprocess, "run", run)
    for artifact in artifacts:
        smoke.smoke_archive(artifact, "/tools/uv")
    calls = run.call_args_list
    assert len(calls) == 6  # noqa: PLR2004
    roots = [calls[index].kwargs["cwd"] for index in (0, 3)]
    assert roots[0] != roots[1]
    for offset, artifact, root in zip((0, 3), artifacts, roots, strict=True):
        assert not root.exists()
        assert not root.is_relative_to(smoke.SOURCE_ROOT)
        create, install, probe = calls[offset : offset + 3]
        assert create.args[0][-4:] == ["venv", "--python", smoke.sys.executable, str(root / "venv")]
        assert install.args[0][-1] == str(artifact.resolve())
        assert install.args[0][:4] == ["/tools/uv", "--no-config", "--no-cache", "--no-python-downloads"]
        assert install.args[0][4:6] == ["pip", "install"]
        assert "--editable" not in install.args[0]
        assert install.args[0][-5:-1] == [
            "--default-index",
            "https://pypi.org/simple",
            "--keyring-provider",
            "disabled",
        ]
        assert probe.args[0][1:] == ["-I", str(Path(smoke.__file__).resolve()), "--probe", str(root / "venv")]
        assert install.args[0][7] == probe.args[0][0]
        for call in (create, install, probe):
            assert call.kwargs["cwd"] == root
            assert call.kwargs["check"] is True
            assert call.kwargs["timeout"] == smoke.STEP_TIMEOUT
            assert "PYTHONPATH" not in call.kwargs["env"]
            assert call.kwargs["env"]["HOME"] == str(root)


@pytest.mark.parametrize("stage", ["venv", "install", "probe"])
@pytest.mark.parametrize("error", [subprocess.CalledProcessError(2, "test"), subprocess.TimeoutExpired("test", 1)])
def test_failure_reports_artifact_stage_and_cleans_up(
    artifacts: list[Path], monkeypatch: pytest.MonkeyPatch, stage: str, error: Exception
) -> None:
    """Failures propagate, stop later steps and still remove temporary environments."""
    index = ("venv", "install", "probe").index(stage)
    run = Mock(side_effect=[*[None] * index, error])
    monkeypatch.setattr(smoke.subprocess, "run", run)
    with pytest.raises(RuntimeError, match=rf"{artifacts[0].name}: {stage} failed"):
        smoke.smoke_archive(artifacts[0], "/tools/uv")
    assert run.call_count == index + 1
    assert not run.call_args.kwargs["cwd"].exists()


def test_checkout_temporary_directory_is_rejected(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """An inherited TMPDIR cannot silently move the smoke back into the checkout."""
    monkeypatch.setattr(smoke, "SOURCE_ROOT", tmp_path)
    monkeypatch.setattr(smoke.tempfile, "tempdir", str(tmp_path))
    run = Mock()
    monkeypatch.setattr(smoke.subprocess, "run", run)
    with pytest.raises(RuntimeError, match="Temporary directory is inside the checkout"):
        smoke.smoke_archive(tmp_path / "example.whl", "/tools/uv")
    run.assert_not_called()
    assert list(tmp_path.iterdir()) == []


def test_import_origins_include_submodules(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """A package root in the environment cannot hide a source-loaded submodule."""
    venv = tmp_path / "venv"
    modules = {name: SimpleNamespace(__file__=str(venv / name / "__init__.py")) for name in smoke.PUBLIC_MODULES}
    monkeypatch.setattr(smoke, "sys", SimpleNamespace(modules=modules))
    monkeypatch.setattr(smoke.importlib, "import_module", Mock())
    assert smoke.check_imports(venv) == venv / "insight_ui"
    modules["insight_ui.config"] = SimpleNamespace(__file__=str(tmp_path / "checkout" / "config.py"))
    with pytest.raises(RuntimeError, match="Unexpected origin"):
        smoke.check_imports(venv)


def test_origins_resolve_symlinks(tmp_path: Path) -> None:
    """Symlinks to source files cannot masquerade as installed assets or modules."""
    outside = tmp_path / "checkout.py"
    outside.touch()
    venv = tmp_path / "venv"
    venv.mkdir()
    linked = venv / "package.py"
    linked.symlink_to(outside)
    with pytest.raises(RuntimeError, match="Unexpected origin"):
        smoke.require_origin(linked, venv)


def test_component_uses_real_public_tag() -> None:
    """The existing test host renders a real component without docs or Enterprise."""
    with override_settings(INSTALLED_APPS=["django.contrib.staticfiles", "insight_ui"]):
        smoke.check_component()


def test_component_rejects_incomplete_markup(monkeypatch: pytest.MonkeyPatch) -> None:
    """Successful template evaluation alone is not successful component rendering."""
    template = Mock(return_value=Mock(render=Mock(return_value="Distribution smoke")))
    monkeypatch.setattr("django.template.Template", template)
    with pytest.raises(RuntimeError, match="expected markup"):
        smoke.check_component()


def test_base_page_rejects_an_empty_title(monkeypatch: pytest.MonkeyPatch) -> None:
    """A successful component smoke must not hide an invalid page shell."""
    monkeypatch.setattr("django.template.loader.render_to_string", Mock(return_value="<!DOCTYPE html><title></title>"))
    with pytest.raises(RuntimeError, match="Default base page"):
        smoke.check_base_page()


@pytest.fixture
def static_fixture(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> tuple[Path, Path]:
    """Use tiny local assets and mock only Django discovery and collection."""
    package, destination = tmp_path / "insight_ui", tmp_path / "collected"
    for name in smoke.REQUIRED_ASSETS | {"insight_ui/fonts/example.woff2"}:
        for directory in (package / "static", destination):
            path = directory / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"local asset fixture")
    monkeypatch.setattr(finders, "find", lambda name: str(package / "static" / name))
    monkeypatch.setattr(management, "call_command", Mock())
    return package, destination


def test_assets_discovers_and_collects_all_files(static_fixture: tuple[Path, Path]) -> None:
    """The smoke checks actual files and invokes noninteractive collectstatic."""
    smoke.check_assets(*static_fixture)
    management.call_command.assert_called_once_with("collectstatic", interactive=False, verbosity=0)


@pytest.mark.parametrize("failure", ["missing", "discovery", "uncollected", "corrupt"])
def test_assets_rejects_missing_or_wrong_content(
    static_fixture: tuple[Path, Path], monkeypatch: pytest.MonkeyPatch, failure: str
) -> None:
    """Missing source, wrong discovery and incomplete collection all fail closed."""
    package, destination = static_fixture
    asset = "insight_ui/css/tailwind.css"
    if failure == "missing":
        (package / "static" / asset).unlink()
    elif failure == "discovery":
        monkeypatch.setattr(finders, "find", lambda _name: None)
    elif failure == "uncollected":
        (destination / asset).unlink()
    else:
        (destination / asset).write_bytes(b"wrong content")
    with pytest.raises(RuntimeError, match=r"static assets|Static discovery|collectstatic"):
        smoke.check_assets(package, destination)


@pytest.mark.parametrize("failure", ["not-isolated", "wrong-venv", "base-python", "inside-checkout"])
def test_probe_rejects_non_isolated_runtime(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, failure: str) -> None:
    """The internal probe cannot report success from the contributor's interpreter."""
    runtime = SimpleNamespace(flags=SimpleNamespace(isolated=1), prefix=str(tmp_path), base_prefix="/base-python")
    if failure == "not-isolated":
        runtime.flags.isolated = 0
    elif failure == "wrong-venv":
        runtime.prefix = "/different-venv"
    elif failure == "base-python":
        runtime.base_prefix = runtime.prefix
    monkeypatch.setattr(smoke, "sys", runtime)
    if failure == "inside-checkout":
        monkeypatch.setattr(smoke, "SOURCE_ROOT", Path.cwd())
    with pytest.raises(RuntimeError, match=r"own virtual environment|outside the source checkout"):
        smoke.probe(tmp_path)


def test_probe_configures_only_public_local_host(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Settings and every smoke stage are verified without touching global Django state."""
    runtime = SimpleNamespace(
        flags=SimpleNamespace(isolated=1), prefix=str(tmp_path), base_prefix="/base-python", stdout=Mock()
    )
    settings, setup, command, component, assets, page = Mock(), Mock(), Mock(), Mock(), Mock(), Mock()
    imports = Mock(return_value=tmp_path / "insight_ui")
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(smoke, "sys", runtime)
    monkeypatch.setattr("django.conf.settings", settings)
    monkeypatch.setattr(django, "setup", setup)
    monkeypatch.setattr(management, "call_command", command)
    monkeypatch.setattr(smoke, "check_imports", imports)
    monkeypatch.setattr(smoke, "check_component", component)
    monkeypatch.setattr(smoke, "check_assets", assets)
    monkeypatch.setattr(smoke, "check_base_page", page)
    smoke.probe(tmp_path)
    config = settings.configure.call_args.kwargs
    assert config["INSTALLED_APPS"] == ["django.contrib.staticfiles", "insight_ui"]
    assert config["DATABASES"]["default"]["NAME"] == ":memory:"
    assert config["INSIGHT_UI"]["assets"] == {"cdn_enabled": False, "use_minified": False}
    assert config["TEMPLATES"][0]["APP_DIRS"] is True
    assert config["DEBUG"] is False
    assert config["STORAGES"]["staticfiles"]["BACKEND"] == (
        "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"
    )
    assert config["STATIC_ROOT"] == tmp_path / "collected-static"
    assert smoke.urlpatterns == []
    setup.assert_called_once_with()
    command.assert_called_once_with("check", verbosity=0, fail_level="WARNING")
    component.assert_called_once_with()
    assets.assert_called_once_with(tmp_path / "insight_ui", tmp_path / "collected-static")
    page.assert_called_once_with()
    assert imports.call_count == 2  # noqa: PLR2004
    imports.assert_called_with(tmp_path)


def test_main_runs_all_artifacts(artifacts: list[Path], monkeypatch: pytest.MonkeyPatch) -> None:
    """The public CLI dispatches each exact artifact once."""
    run = Mock()
    monkeypatch.setattr(smoke.shutil, "which", lambda _name: "/tools/uv")
    monkeypatch.setattr(smoke, "smoke_archive", run)
    assert smoke.main([str(artifacts[0].parent)]) == 0
    assert [call.args[0] for call in run.call_args_list] == artifacts


def test_main_fails_without_uv(
    artifacts: list[Path], monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Missing prerequisites produce a concise, nonzero CLI failure."""
    monkeypatch.setattr(smoke.shutil, "which", lambda _name: None)
    assert smoke.main([str(artifacts[0].parent)]) == 1
    assert "uv is required on PATH" in capsys.readouterr().err


def test_main_stops_on_failed_archive(artifacts: list[Path], monkeypatch: pytest.MonkeyPatch) -> None:
    """No success status is returned after any artifact failed its smoke."""
    run = Mock(side_effect=RuntimeError("installation failed"))
    monkeypatch.setattr(smoke.shutil, "which", lambda _name: "/tools/uv")
    monkeypatch.setattr(smoke, "smoke_archive", run)
    assert smoke.main([str(artifacts[0].parent)]) == 1
    run.assert_called_once()
