# New Component Checklist

This checklist is mandatory for contributors adding or changing reusable UI
components in the Insight UI ecosystem.

It applies to any Insight UI ecosystem package that exposes reusable UI
surfaces, including the core package and sibling packages.

The goal is simple: every reusable component must ship with the implementation,
the public Django-facing API, the live demo, and the self-documentation needed
for another project to use it without reading the source code.

## Mandatory rule

If a pull request adds or changes a reusable component, it must update the
component's self-documentation in the same pull request.

The reviewer should block the PR when a public template tag, component
template, design token, semantic class, `data-insight-*` hook, or accessibility
contract changes without the matching documentation and demo update.

For `insight-ui`, reusable component implementation lives in `insight_ui/*`.
The optional self-documentation app keeps its canonical documentation data in
`documentation/component_details/*`. For sibling packages that do not yet have
the same registry layout, use an equivalent package-local `component_details/`
structure and document the package-specific source-of-truth boundary.

## Required files for `insight-ui`

Use this table as the PR file checklist for a new component.

| Concern | Required file |
|---|---|
| Component enum and category | `documentation/component_details/components.py` |
| Django template tag API | `insight_ui/templatetags/insight_tags.py` |
| Component HTML | `insight_ui/templates/insight_ui/components/<component>.html` |
| JavaScript behavior, if interactive | `insight_ui/static/insight_ui/js/insight-ui-<component>.js` |
| Init registration, if interactive | `insight_ui/static/insight_ui/js/insight-ui-init.js` |
| Public description | `documentation/component_details/description_context.py` |
| Usage example | `documentation/component_details/usage_context.py` |
| Parameter table | `documentation/component_details/parameter_context.py` |
| Accessibility notes | `documentation/component_details/a11y_context.py` |
| Related components | `documentation/component_details/related_components_context.py` |
| GitHub source links | `documentation/component_details/git_path_mapping.py` |
| Demo context | `documentation/component_details/demo_context.py` |
| Demo presentation | `documentation/templates/documentation/docs/component_demo.html`, only when the generic demo renderer cannot display the component |
| Template tag tests | `insight_ui/tests/test_template_tags.py` or a focused test module |
| JavaScript tests, if behavior changes | Existing JS test suite or a new focused test |
| Design contract, if a token/class changes | `docs/design-system.md` and `insight_ui/utils/input.css` |
| Naming contract, if a hook changes | `docs/conventions.md` |

## Minimal example: `status_pill`

The following example is intentionally small. It shows the expected file touch
points without prescribing a real component for the product.

### 1. Add the component enum

File: `documentation/component_details/components.py`

```python
class Component(Enum):
    # ...
    STATUS_PILL = ("status_pill", ComponentCategory.UTIL)
```

Choose the category that controls where the component appears in Storybook.

### 2. Add the template tag

File: `insight_ui/templatetags/insight_tags.py`

```python
@register.inclusion_tag("insight_ui/components/status_pill.html")
def status_pill(label: str, status: str = "info") -> dict[str, str]:
    return {
        "label": label,
        "status": status,
    }
```

Keep template tag defaults simple and immutable. Use `None` plus local defaults
for lists or dictionaries.

### 3. Add the component template

File: `insight_ui/templates/insight_ui/components/status_pill.html`

```html
{% load i18n %}
<span
    data-insight-status-pill
    class="inline-tag insight-state-{{ status|default:'info' }}"
    role="status"
>
    {{ label }}
</span>
```

Use semantic HTML and ARIA where the component communicates state. Add
`data-insight-*` hooks only when JavaScript owns behavior for the component.

### 4. Add JavaScript only when the component is interactive

File: `insight_ui/static/insight_ui/js/insight-ui-status-pill.js`

```javascript
/**
 * Insight UI - StatusPill
 */
export class StatusPill {
	static instances = new WeakMap();

	constructor(element) {
		if (StatusPill.instances.has(element)) {
			return StatusPill.instances.get(element);
		}

		this.element = element;
		StatusPill.instances.set(element, this);
	}

	destroy() {
		StatusPill.instances.delete(this.element);
	}

	static initAll() {
		document.querySelectorAll("[data-insight-status-pill]").forEach(
			(el) => new StatusPill(el)
		);
	}
}
```

Static components do not need a JavaScript module. If a module exists, it must
use the existing singleton/lifecycle pattern and clean up event listeners in
`destroy()`.

### 5. Register JavaScript initialization

File: `insight_ui/static/insight_ui/js/insight-ui-init.js`

```javascript
import { StatusPill } from "./insight-ui-status-pill.js";

Object.assign(window.InsightUI, {
	StatusPill,
});

function initAll() {
	StatusPill.initAll();
}
```

Add the import, expose the class when lifecycle cleanup needs it, and call
`initAll()` from the central initializer. Ensure repeated HTMX swaps do not
double-bind behavior.

### 6. Add description context

File: `documentation/component_details/description_context.py`

```python
@register_component(Component.STATUS_PILL)
def get_status_pill_description() -> dict:
    return {
        "description": _(
            "Use a status pill to show a compact semantic state such as info, "
            "success, warning, or danger."
        )
    }
```

Explain what the component is for, not just what it looks like.

### 7. Add usage context

File: `documentation/component_details/usage_context.py`

```python
@register_component(Component.STATUS_PILL)
def get_status_pill_usage() -> dict:
    return {
        "usage": """{% load insight_tags %}
{% status_pill label="Published" status="success" %}"""
    }
```

The usage example should be copyable by a consumer application.

### 8. Add parameter context

File: `documentation/component_details/parameter_context.py`

```python
@register_component(Component.STATUS_PILL)
def get_status_pill_parameters() -> dict:
    return {
        "parameters": [
            {
                "name": "label",
                "type": "str",
                "required": True,
                "description": _("Visible status text."),
            },
            {
                "name": "status",
                "type": "str",
                "required": False,
                "default": "info",
                "description": _("Semantic state: info, success, warning, or danger."),
            },
        ]
    }
```

Keep this table aligned with the template tag signature. If the signature
changes, update this file in the same PR.

### 9. Add accessibility context

File: `documentation/component_details/a11y_context.py`

```python
@register_component(Component.STATUS_PILL)
def get_status_pill_a11y() -> dict:
    return {
        "a11y": [
            _("Uses role='status' when the pill communicates application state."),
            _("Does not rely on color alone; the visible label carries meaning."),
        ]
    }
```

Document keyboard, screen-reader, focus, contrast, and reduced-motion behavior
where relevant.

### 10. Add related components

File: `documentation/component_details/related_components_context.py`

```python
RELATED_COMPONENTS[Component.STATUS_PILL] = [
    Component.ALERT,
    Component.INFOBOX,
]
```

Use related components to help users choose the right pattern.

### 11. Add GitHub source links

File: `documentation/component_details/git_path_mapping.py`

```python
TEMPLATE_PATHS["status_pill"] = GIT_BASE_FILE + "status_pill.html"
SCRIPT_PATHS["status_pill"] = GIT_BASE_SCRIPT_FILE + "insight-ui-status-pill.js"
```

Only add `SCRIPT_PATHS` when a JavaScript file exists.

### 12. Add demo context

File: `documentation/component_details/demo_context.py`

```python
@register_demo_context(Component.STATUS_PILL)
def get_status_pill_demo_context() -> dict:
    return {
        "status_pill_examples": [
            {"label": _("Draft"), "status": "info"},
            {"label": _("Published"), "status": "success"},
            {"label": _("Blocked"), "status": "danger"},
        ]
    }
```

Demo context should be deterministic, safe to render in public docs, and free of
customer data.

### 13. Add demo presentation only when needed

File: `documentation/templates/documentation/docs/component_demo.html`

```html
{% if component_name == "status_pill" %}
    <div class="flex flex-wrap gap-2">
        {% for item in status_pill_examples %}
            {% status_pill label=item.label status=item.status %}
        {% endfor %}
    </div>
{% endif %}
```

Prefer the generic demo renderer when possible. Add component-specific demo
markup only when the component needs a custom layout, multiple states, iframe
behavior, or special setup.

### 14. Add tests

File: `insight_ui/tests/test_template_tags.py`

```python
def test_status_pill_renders_label():
    rendered = Template(
        "{% load insight_tags %}{% status_pill label='Published' status='success' %}"
    ).render(Context({}))

    assert "Published" in rendered
    assert "data-insight-status-pill" in rendered
```

Add behavior tests when JavaScript owns state, keyboard interaction, or lifecycle
cleanup.

## Required PR checklist

Add this checklist to PR descriptions when the PR adds or changes a reusable
component:

```markdown
- [ ] Template tag API added or updated.
- [ ] Component template added or updated.
- [ ] JavaScript module and init registration updated, or not needed.
- [ ] Description, usage, parameter, accessibility, related-component, and Git path docs updated.
- [ ] Demo context and demo presentation updated.
- [ ] Tests cover template tag output and interactive behavior where relevant.
- [ ] Design-system contract updated if tokens or semantic classes changed.
- [ ] Naming conventions updated if `data-insight-*` hooks changed.
- [ ] Ecosystem package docs updated if this component belongs outside the core package.
```

## Guidance for ecosystem packages

Ecosystem packages do not have to copy the exact `documentation/component_details/*`
implementation before they can comply with this checklist. They must still keep
the same source-of-truth split:

| Concern | Required package-local equivalent |
|---|---|
| Public API | Template tag, view, form, or Python API that consumers call |
| Component HTML | Package-local template that owns semantic structure and hooks |
| Behavior | Package-local JavaScript module and initializer |
| Self-documentation data | Package-local `component_details/` or equivalent registry/context module |
| Live docs/demo | Package-local docs or showcase page |
| Tests | Package-local unit/integration tests |

Package-specific mechanics remain package-owned. Reusable account, provider,
or extension UI surfaces should still document templates, forms, redirects,
security assumptions, and demo states with the same discipline as core
`insight-ui` components.

## Reviewer standard

A reviewer should be able to open the component detail page and answer these
questions without reading implementation files:

1. What is the component for?
2. How do I render it?
3. Which parameters are public and what are their defaults?
4. What accessibility behavior does it guarantee?
5. Which files own the template, JavaScript, and source links?
6. Which related component should I use instead when this one is not a fit?

If the component detail page cannot answer those questions, the PR is not done.
