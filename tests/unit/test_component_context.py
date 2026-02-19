from insight_ui.component_details.component_context import get_component_context
from insight_ui.component_details.related_components_context import get_related_components_context


def test_get_component_context_dispatches_by_component() -> None:
    """Ensure component context is resolved for the requested component, not hardcoded."""
    context = get_component_context("accordion")
    assert context["description"]
    assert "accordion" in context["description"][0].lower()


def test_get_component_context_resolves_alias_based_functions() -> None:
    """Ensure alias-mapped components resolve the correct context providers."""
    context = get_component_context("toggle_button")
    assert "main_params" in context
    related_names = {topic["component_name"] for topic in context["related_topics"]}
    assert "toggle" not in related_names


def test_get_component_context_handles_unknown_component_gracefully() -> None:
    """Ensure unknown components do not crash and return a minimal context."""
    context = get_component_context("unknown_component")
    assert context["component_name"] == "Unknown Component"
    assert context["related_topics"] == []


def test_related_components_normalizes_aliases_and_filters_invalid() -> None:
    """Ensure related component aliases are normalized and invalid entries are filtered."""
    related_topics = get_related_components_context(
        "card", valid_component_names={"toggle_view", "card", "card_carousel", "image_carousel"}
    )
    related_names = {topic["component_name"] for topic in related_topics}
    assert related_names == {"toggle_view"}
