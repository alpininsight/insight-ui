# SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
# SPDX-License-Identifier: AGPL-3.0-only
"""Every variable a component template reads must come from its inclusion tag.

An inclusion tag renders its template with only the dict it returns, so a variable the tag does not
provide is always empty. Such typos fail silently (e.g. ``as_row`` instead of
``radio_group_config.as_row`` made the option a no-op), so this test checks all components at once.
"""

import ast
from collections.abc import Iterable, Iterator
from pathlib import Path

import pytest
from django.template import Node, NodeList, engines
from django.template.base import FilterExpression, TokenType, Variable
from django.template.defaulttags import ForNode, IfNode, TemplateLiteral, WithNode
from django.template.loader_tags import BlockNode, ExtendsNode, IncludeNode
from django.template.smartif import TokenBase
from django.templatetags.i18n import BlockTranslateNode

import insight_ui

TAGS = Path(insight_ui.__file__).parent / "templatetags" / "insight_tags.py"

# Names Django itself provides to every template.
BUILTINS = {"True", "False", "None", "forloop", "block", "csrf_token"}

# Known gaps, each removed with the rebuild that fixes it. Do not add new entries for new components.
KNOWN_GAPS = {
    # The threshold is passed nowhere and htmx's revealed trigger has no threshold; dropped in the rebuild.
    "insight_ui/components/infinite_scroll.html": {"threshold"},
    # Restoring filters, the operator list and the filter partial's values are unfinished; the component is
    # up for review.
    "insight_ui/components/search_query_builder/sq_builder.html": {
        "custom_filters",
        "ov_list",
        "index",
        "selected_field",
        "selected_logic",
        "selected_value",
        "filter_operator",
        "filter_value",
    },
}

# Parameters a shared partial documents as optional; callers that need them pass them, the others leave them out.
OPTIONAL_INCLUDE_PARAMETERS = {
    # invalid=False only for roles without aria-invalid support, e.g. a plain fieldset.
    "insight_ui/components/_form_field_aria.html": {"invalid"},
}


def inclusion_tags() -> dict[str, tuple[str, set[str]]]:
    """Map each component template to its tag and the context keys the tag returns."""
    result: dict[str, tuple[str, set[str]]] = {}
    for function in ast.parse(TAGS.read_text(encoding="utf-8")).body:
        if not isinstance(function, ast.FunctionDef):
            continue
        for decorator in function.decorator_list:
            if isinstance(decorator, ast.Call) and getattr(decorator.func, "attr", "") == "inclusion_tag":
                keys: set[str] = set()
                for node in own_returns(function):
                    assert isinstance(node.value, ast.Dict), f"{function.name} must return a dict literal"
                    keys |= {key.value for key in node.value.keys if isinstance(key, ast.Constant)}
                result[decorator.args[0].value] = (function.name, keys)
    return result


def own_returns(function: ast.FunctionDef) -> Iterator[ast.Return]:
    """Yield the return statements of a function, without those of nested functions, e.g. a URL helper."""
    pending: list[ast.AST] = list(function.body)
    while pending:
        node = pending.pop()
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.Lambda | ast.ClassDef):
            continue
        if isinstance(node, ast.Return) and node.value is not None:
            yield node
        pending.extend(ast.iter_child_nodes(node))


def expression_names(expression: object) -> Iterator[str]:
    """Yield the root names an expression, filter argument or if-condition reads."""
    if isinstance(expression, FilterExpression):
        yield from expression_names(expression.var)
        for _func, arguments in expression.filters:
            for is_lookup, argument in arguments:
                if is_lookup:
                    yield from expression_names(argument)
    elif isinstance(expression, Variable) and expression.lookups:
        yield expression.lookups[0]
    elif isinstance(expression, TemplateLiteral):
        yield from expression_names(expression.value)
    elif isinstance(expression, TokenBase):
        for side in ("first", "second"):
            if getattr(expression, side, None) is not None:
                yield from expression_names(getattr(expression, side))


def node_expressions(node: Node) -> Iterator[object]:
    """Yield the expressions stored on a node, also those of custom tags (args, kwargs, ...)."""
    for value in vars(node).values():
        if isinstance(value, FilterExpression | Variable):
            yield value
        elif isinstance(value, list | tuple):
            yield from (item for item in value if isinstance(item, FilterExpression | Variable))
        elif isinstance(value, dict):
            yield from (item for item in value.values() if isinstance(item, FilterExpression | Variable))


def read(expressions: Iterable[object], defined: set[str]) -> Iterator[str]:
    """Yield the names the expressions read that are not defined."""
    for expression in expressions:
        yield from (name for name in expression_names(expression) if name not in defined)


def template_nodes(name: str) -> NodeList:
    """Return the parsed nodes of a template."""
    return engines["django"].engine.get_template(name).nodelist


# One function per node that creates names or pulls in other templates; every other node is handled
# generically (its expressions are read, its child nodelists walked).
type Blocks = dict[str, NodeList]


def extends_names(node: ExtendsNode, defined: set[str], blocks: Blocks) -> Iterator[str]:
    """Walk the parent template with the child's blocks in place."""
    child_blocks = {block.name: block.nodelist for block in node.nodelist.get_nodes_by_type(BlockNode)}
    yield from undefined_names(template_nodes(node.parent_name.var), defined, {**child_blocks, **blocks})


def block_names(node: BlockNode, defined: set[str], blocks: Blocks) -> Iterator[str]:
    """Walk the block's content, or the child template's version of it."""
    yield from undefined_names(blocks.get(node.name, node.nodelist), defined, blocks)


def for_names(node: ForNode, defined: set[str], blocks: Blocks) -> Iterator[str]:
    """The loop variables exist inside the loop only."""
    yield from read([node.sequence], defined)
    yield from undefined_names(node.nodelist_loop, defined | set(node.loopvars), blocks)
    yield from undefined_names(node.nodelist_empty, defined, blocks)


def with_names(node: WithNode, defined: set[str], blocks: Blocks) -> Iterator[str]:
    """The assigned names exist inside the with block only."""
    yield from read(node.extra_context.values(), defined)
    yield from undefined_names(node.nodelist, defined | set(node.extra_context), blocks)


def blocktranslate_names(node: BlockTranslateNode, defined: set[str], _blocks: Blocks) -> Iterator[str]:
    """Placeholders in the message read the with-names, the counter or the context."""
    yield from read(node.extra_context.values(), defined)
    local = defined | set(node.extra_context) | {node.countervar}
    for token in [*node.singular, *(node.plural or [])]:
        if token.token_type == TokenType.VAR and token.contents not in local:
            yield token.contents


def include_names(node: IncludeNode, defined: set[str], _blocks: Blocks) -> Iterator[str]:
    """An included template sees the context plus its with-names, so it is checked as part of this one."""
    name = node.template.var
    optional = OPTIONAL_INCLUDE_PARAMETERS.get(name, set())
    yield from read(node.extra_context.values(), defined)
    yield from undefined_names(template_nodes(name), defined | set(node.extra_context) | optional, {})


def if_names(node: IfNode, defined: set[str], blocks: Blocks) -> Iterator[str]:
    """Conditions are not stored as plain expressions, so they are read explicitly."""
    for condition, branch in node.conditions_nodelists:
        yield from read([condition], defined)
        yield from undefined_names(branch, defined, blocks)


def generic_names(node: Node, defined: set[str], blocks: Blocks) -> Iterator[str]:
    """Read every expression stored on the node (custom tags included) and walk its children."""
    yield from read(node_expressions(node), defined)
    for attribute in node.child_nodelists:
        yield from undefined_names(getattr(node, attribute, None) or NodeList(), defined, blocks)


HANDLERS = {
    ExtendsNode: extends_names,
    BlockNode: block_names,
    ForNode: for_names,
    WithNode: with_names,
    BlockTranslateNode: blocktranslate_names,
    IncludeNode: include_names,
    IfNode: if_names,
}


def undefined_names(nodelist: NodeList, defined: set[str], blocks: Blocks) -> Iterator[str]:
    """Yield the names read in a nodelist that are neither in ``defined`` nor created by the template."""
    for node in nodelist:
        yield from HANDLERS.get(type(node), generic_names)(node, defined, blocks)
        # "{% tag ... as name %}" defines name for the rest of the template.
        targets = (getattr(node, attribute, None) for attribute in ("asvar", "target_var", "varname", "variable"))
        defined = defined | {target for target in targets if isinstance(target, str)}


def missing_names(template_name: str) -> set[str]:
    """Return the names a component template reads that its tag does not provide."""
    _, provided = inclusion_tags()[template_name]
    return set(undefined_names(template_nodes(template_name), provided | BUILTINS, {}))


@pytest.mark.parametrize(("template_name", "tag"), [(name, tag) for name, (tag, _) in inclusion_tags().items()])
def test_component_templates_read_only_what_their_tag_provides(template_name: str, tag: str) -> None:
    """A variable the tag does not return is always empty: read it through the tag's context instead."""
    missing = missing_names(template_name) - KNOWN_GAPS.get(template_name, set())

    assert not missing, f"{template_name} reads {sorted(missing)}, which {{% {tag} %}} does not provide"


@pytest.mark.parametrize("template_name", sorted(KNOWN_GAPS))
def test_known_gaps_are_still_gaps(template_name: str) -> None:
    """Remove an entry from KNOWN_GAPS as soon as the template no longer reads the name."""
    assert KNOWN_GAPS[template_name] <= missing_names(template_name), (
        f"{template_name} is fixed; remove it from KNOWN_GAPS"
    )
