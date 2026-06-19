from django.utils.translation import gettext as _

from insight_ui.component_details.component_context import ParameterDetails, ParameterDoc, register_component
from insight_ui.component_details.components import Component


@register_component(Component.POPOVER)
def get_popover_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the popover component."""
    return {
        "params": [
            ParameterDoc(
                "",
                [
                    ParameterDetails(
                        "data-insight-popover='<target-id>'",
                        "str",
                        _("Determines the popover object to be displayed on hover."),
                        "''",
                    ),
                    ParameterDetails(
                        "data-position='<position>'",
                        "str",
                        _(
                            "Determines where the popover should be displayed relative to the element. Possible values are: 'top', 'bottom', 'right', and 'left'."
                        ),
                        "''",
                    ),
                    ParameterDetails(
                        "data-show-arrow",
                        "bool",
                        _("Shows an arrow at the edge of the popover pointing to the triggering object."),
                        "False",
                    ),
                    ParameterDetails("data-follow-mouse", "bool", _("Popup follows mouse position."), "False"),
                ],
                """""",
            )
        ]
    }


@register_component(Component.TOOLTIP)
def get_tooltip_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the tooltip component."""
    return {
        "params": [
            ParameterDoc(
                None,
                [
                    ParameterDetails(
                        "data-insight-tooltip='<text>'",
                        "str",
                        _("Shows a tooltip with the specified text when hovering over the element."),
                        "''",
                    ),
                    ParameterDetails(
                        "data-position='<position>'",
                        "str",
                        _(
                            "Determines where the tooltip should be displayed relative to the element. Possible values are: 'top', 'bottom', 'right', and 'left'."
                        ),
                        "''",
                    ),
                    ParameterDetails(
                        "data-show-arrow",
                        "bool",
                        _("Shows an arrow at the edge of the tooltip pointing to the triggering object."),
                        "False",
                    ),
                    ParameterDetails("data-follow-mouse", "bool", _("Tooltip follows mouse position."), "False"),
                ],
                """""",
            )
        ]
    }


@register_component(Component.CODE_BLOCK)
def get_code_block_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the code block component."""
    return {
        "params": [
            ParameterDoc(
                None,
                [
                    ParameterDetails(
                        "id", "str", _("Optional, unique tag ID for identifying the element in JavaScript."), "''"
                    ),
                    ParameterDetails(
                        "data-insight-code-block",
                        "str",
                        _("Identifies this object as a code block and specifies the used language."),
                        "''",
                    ),
                    ParameterDetails(
                        "data-filename",
                        "str",
                        _("Displays the text as a hint for the user in the header of the code block."),
                        "''",
                    ),
                ],
                """""",
            )
        ]
    }


@register_component(Component.DIFFERENTIATOR)
def get_differentiator_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the differentiator component."""
    return {
        "params": [
            ParameterDoc(
                None,
                [
                    ParameterDetails("textA", "str", _("First or older version of the text."), "''"),
                    ParameterDetails("textB", "str", _("Second or newer version of the text."), "''"),
                ],
                """""",
            )
        ]
    }


@register_component(Component.PROGRESS_BAR)
def get_progress_bar_parameter_context() -> dict[str, list[str]]:
    """Serve parameter documentation for the progress bar component."""
    return {"params": [ParameterDoc(None, [ParameterDetails("TODO!", "-", "-", "-")], """""")]}
