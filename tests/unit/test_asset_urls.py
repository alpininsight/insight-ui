from http import HTTPStatus

import pytest
from django.conf import settings
from django.template import Context, Template
from django.test import override_settings
from insight_ui.asset_urls import design_theme_asset_url, insight_asset_url, to_minified_asset_path
from insight_ui.config import get_config


def test_to_minified_asset_path_handles_css_and_js() -> None:
    """CSS and JavaScript assets should resolve to generated minified siblings."""
    assert to_minified_asset_path("insight_ui/js/insight-ui-utils.js") == "insight_ui/js/insight-ui-utils.min.js"
    assert to_minified_asset_path("insight_ui/css/tailwind.css") == "insight_ui/css/tailwind.min.css"
    assert to_minified_asset_path("insight_ui/js/already.min.js") == "insight_ui/js/already.min.js"
    assert to_minified_asset_path("insight_ui/favicon/favicon.ico") == "insight_ui/favicon/favicon.ico"


@override_settings(INSIGHT_UI={"assets": {"use_minified": False, "cdn_enabled": False}})
def test_insight_asset_url_uses_local_staticfiles_by_default() -> None:
    """Local development should keep readable staticfiles by default."""
    assert insight_asset_url("insight_ui/js/insight-ui-utils.js") == "/static/insight_ui/js/insight-ui-utils.js"


def test_project_settings_do_not_enable_cdn_implicitly() -> None:
    """Production must opt in explicitly before templates emit CDN URLs."""
    assert settings.INSIGHT_UI["assets"]["cdn_enabled"] is False


@override_settings(INSIGHT_UI={"assets": {"use_minified": True, "cdn_enabled": False}})
def test_insight_asset_url_can_use_local_minified_staticfiles() -> None:
    """Minified assets should also work through Django staticfiles."""
    assert insight_asset_url("insight_ui/css/tailwind.css") == "/static/insight_ui/css/tailwind.min.css"


@override_settings(
    INSIGHT_UI={
        "assets": {
            "use_minified": True,
            "cdn_enabled": True,
            "cdn_base_url": "https://cdn.alpininsight.ai/",
            "cdn_prefix": "/insight-ui/",
            "cdn_version": "1.2.3",
        }
    }
)
def test_insight_asset_url_uses_versioned_cdn_minified_asset() -> None:
    """CDN delivery should use versioned minified files for production."""
    assert (
        insight_asset_url("insight_ui/js/insight-ui-utils.js")
        == "https://cdn.alpininsight.ai/insight-ui/v1.2.3/js/insight-ui-utils.min.js"
    )


@override_settings(INSIGHT_UI={"assets": {"cdn_enabled": True, "cdn_version": "latest"}})
def test_insight_asset_template_tag_uses_latest_cdn_alias() -> None:
    """The template tag should expose the same CDN URL resolution."""
    template = Template("{% load insight_assets %}{% insight_asset 'insight_ui/css/prism.css' %}")

    assert template.render(Context()) == "https://cdn.alpininsight.ai/insight-ui/latest/css/prism.min.css"


@pytest.mark.parametrize("cdn_version", ["develop", "main"])
def test_insight_asset_url_keeps_branch_cdn_aliases(cdn_version: str) -> None:
    """Branch aliases should not be normalized as immutable SemVer paths."""
    with override_settings(INSIGHT_UI={"assets": {"cdn_enabled": True, "cdn_version": cdn_version}}):
        assert (
            insight_asset_url("insight_ui/css/tailwind.css")
            == f"https://cdn.alpininsight.ai/insight-ui/{cdn_version}/css/tailwind.min.css"
        )


@override_settings(INSIGHT_UI={"assets": {"use_minified": True, "cdn_enabled": True, "cdn_version": "develop"}})
def test_design_theme_asset_url_preserves_host_owned_stylesheets() -> None:
    """Host-owned design themes must not be minified or moved to the Insight UI CDN."""
    assert design_theme_asset_url("custom/theme.css") == "/static/custom/theme.css"
    assert design_theme_asset_url("/assets/theme.css") == "/assets/theme.css"
    assert design_theme_asset_url("https://example.test/theme.css") == "https://example.test/theme.css"


@override_settings(INSIGHT_UI={"assets": {"use_minified": True, "cdn_enabled": True, "cdn_version": "develop"}})
def test_design_theme_asset_url_rewrites_insight_ui_owned_stylesheets() -> None:
    """Built-in design themes still use Insight UI asset delivery rules."""
    assert (
        design_theme_asset_url("insight_ui/css/themes/cerulean.css")
        == "https://cdn.alpininsight.ai/insight-ui/develop/css/themes/cerulean.min.css"
    )


@pytest.mark.parametrize("theme_name", ["skeuomorphic", "flat", "material", "neumorphic", "glass", "bento", "drawn"])
@override_settings(INSIGHT_UI={"assets": {"use_minified": True, "cdn_enabled": True, "cdn_version": "develop"}})
def test_style_family_theme_assets_use_versioned_cdn_minified_files(theme_name: str) -> None:
    """Packaged style-family themes should publish through the same CDN contract."""
    assert (
        design_theme_asset_url(f"insight_ui/css/themes/{theme_name}.css")
        == f"https://cdn.alpininsight.ai/insight-ui/develop/css/themes/{theme_name}.min.css"
    )


@override_settings(INSIGHT_UI={"assets": {"cdn_enabled": True}})
def test_config_merges_nested_asset_defaults() -> None:
    """Partial asset settings should keep default CDN metadata."""
    assets = get_config("assets")

    assert assets["cdn_enabled"] is True
    assert assets["cdn_base_url"] == "https://cdn.alpininsight.ai"
    assert assets["cdn_prefix"] == "insight-ui"


@pytest.mark.django_db
@override_settings(
    INSIGHT_UI={
        "assets": {
            "use_minified": True,
            "cdn_enabled": True,
            "cdn_base_url": "https://cdn.alpininsight.ai",
            "cdn_prefix": "insight-ui",
            "cdn_version": "1.2.3",
        }
    }
)
def test_base_template_uses_cdn_minified_assets(client) -> None:  # noqa: ANN001
    """Rendered pages should use CDN-backed minified Insight UI assets."""
    response = client.get("/")

    assert response.status_code == HTTPStatus.OK
    html = response.content.decode()
    assert "https://cdn.alpininsight.ai/insight-ui/v1.2.3/js/insight-ui-utils.min.js" in html
    assert "https://cdn.alpininsight.ai/insight-ui/v1.2.3/css/tailwind.min.css" in html
