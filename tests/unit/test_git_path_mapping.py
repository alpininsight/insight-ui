from insight_ui.component_details.git_path_mapping import SCRIPT_PATHS, TEMPLATE_PATHS


def test_template_path_aliases_match_view_component_names() -> None:
    """Ensure canonical component keys resolve to the same template URLs as legacy aliases."""
    assert TEMPLATE_PATHS["card"] == TEMPLATE_PATHS["cards"]
    assert TEMPLATE_PATHS["breadcrumb"] == TEMPLATE_PATHS["breadcrumbs"]
    assert TEMPLATE_PATHS["web_socket"] == TEMPLATE_PATHS["websocket"]
    assert TEMPLATE_PATHS["input_field"] == TEMPLATE_PATHS["input"]
    assert TEMPLATE_PATHS["query_builder"] == TEMPLATE_PATHS["sq_builder"]


def test_template_paths_cover_common_doc_components() -> None:
    """Ensure frequently used documented components have explicit source mappings."""
    assert "chart" in TEMPLATE_PATHS
    assert "code_block" in TEMPLATE_PATHS
    assert "hero" in TEMPLATE_PATHS


def test_script_path_aliases_match_view_component_names() -> None:
    """Ensure websocket script mapping supports the component name used in views."""
    assert SCRIPT_PATHS["web_socket"] == SCRIPT_PATHS["websocket"]
