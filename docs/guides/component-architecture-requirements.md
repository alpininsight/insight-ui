# Component Architecture Requirements

This document outlines identified issues and requirements for improving the component architecture in Insight UI.

## Critical Issues

### 1. Memory Leaks - Global Event Listeners Not Cleaned Up

Multiple components add `document.addEventListener` or `window.addEventListener` but never remove them, causing memory leaks and performance degradation.

| File | Line | Issue |
|------|------|-------|
| `insight-ui-dropdown.js` | 36 | `document.addEventListener("click")` accumulates per instance |
| `insight-ui-floater.js` | 46 | `document.addEventListener("click")` for click-outside |
| `insight-ui-floater.js` | 54 | `window.addEventListener("scroll")` for position updates |
| `insight-ui-multiselect.js` | 85 | `document.addEventListener("click")` per instance |
| `insight-ui-sidebar.js` | 81 | `document.addEventListener("mousemove")` never cleaned |
| `insight-ui-carousel.js` | 70 | `window.addEventListener("resize")` accumulates |

**Requirement:** All event listeners added to `document` or `window` must be removable and cleaned up when the component is destroyed.

### 2. Missing Cleanup/Destroy Methods

None of the component classes have a `destroy()` method. When HTMX swaps content, old instances remain with active listeners pointing to removed DOM elements.

**Affected components:** All JavaScript component classes (Accordion, Tabs, Modal, Checkbox, Dropdown, Floater, Multiselect, Sidebar, Carousel, etc.)

**Requirement:** All component classes must implement a `destroy()` method that:
- Removes all event listeners
- Clears all timers/intervals
- Removes the instance from the WeakMap
- Cleans up any DOM references

### 3. Uncleaned Intervals

`insight-ui-carousel.js:98` - `setInterval` for autoplay is never cleared when carousel is removed from DOM.

**Requirement:** All `setInterval` and `setTimeout` calls must be tracked and cleared in the `destroy()` method.

## High Priority Issues

### 4. XSS Vulnerabilities - Unsafe `|safe` Filter Usage

The following templates use the `|safe` filter which bypasses Django's auto-escaping:

| File | Line | Variable |
|------|------|----------|
| `modal.html` | 43 | `{{ content\|safe }}` |
| `live_content.html` | 20 | `{{ initial_content\|safe }}` |
| `bar_chart.html` | 20 | `{{ chart.series\|safe }}` |
| `bar_chart.html` | 48 | `{{ chart.x_axis_legend\|safe }}` |
| `websocket.html` | 9 | `{{ options.initial_content\|safe }}` |

**Requirement:** Review all `|safe` filter usage. Either:
- Ensure the data source is trusted and document why `|safe` is necessary
- Add server-side sanitization before marking as safe
- Remove `|safe` and use proper escaping

### 5. Inline `onclick` Handlers (Code Injection Risk)

Templates use inline `onclick` handlers with interpolated values:

| File | Line | Issue |
|------|------|-------|
| `radio_block.html` | 20, 54 | `onclick="{{ method }}('{{ item.value }}')"` |
| `form_errors.html` | 23 | `onclick="this.closest('#form-result').innerHTML = ''"` |
| `alert.html` | 27 | `onclick="this.parentElement.remove();"` |
| `modal.html` | 62, 70 | `onclick="{{ action.onclick }}"` |

**Requirement:** Replace inline `onclick` handlers with:
- Data attributes (`data-action`, `data-value`)
- Event delegation in JavaScript
- Proper event binding in component classes

### 6. HTMX Re-initialization Without Cleanup

`insight-ui-init.js:39-41` calls `initAll()` on every `htmx:afterRequest`, but old component instances with their listeners are never destroyed first.

**Requirement:** Before re-initializing components after HTMX swaps:
1. Find existing component instances in the swap target
2. Call `destroy()` on each instance
3. Then initialize new components

Example implementation:
```javascript
htmx.on("htmx:beforeSwap", (evt) => {
    const target = evt.detail.target;
    // Destroy existing components before swap
    target.querySelectorAll('[data-accordion]').forEach(el => {
        InsightUI.Accordion.instances.get(el)?.destroy();
    });
    // ... repeat for all component types
});
```

## Medium Priority Issues

### 7. Inconsistent Singleton Pattern

Not all components use the WeakMap singleton pattern consistently:

| Component | Pattern Used |
|-----------|-------------|
| Accordion, Modal, Tabs, Checkbox, Dropdown, Multiselect, Sidebar | WeakMap singleton |
| Carousel | `data-carouselInitialized` DOM attribute flag |
| 3D-Carousel | No instance tracking |

**Requirement:** Standardize on WeakMap singleton pattern for all components that maintain state.

### 8. Inconsistent Data Attribute Naming

Different naming conventions are used across components:

| Pattern | Components Using It |
|---------|---------------------|
| `data-insight-toggle="type"` | Modal, Collapsible |
| `data-dropdown-toggle` | Dropdown (no `insight` prefix) |
| `data-accordion` | Accordion (different pattern entirely) |
| `data-multiselect` | Multiselect |

**Requirement:** Establish and document a consistent naming convention:
- All component data attributes should use `data-insight-` prefix
- Toggle attributes should follow `data-insight-toggle="component-type"` pattern
- Document the convention in `docs/guides/naming_conventions.md`

### 9. HTML Attribute Error

`radio_button.html:14` uses `checked="true"` instead of the boolean `checked` attribute.

**Requirement:** Boolean HTML attributes should not have values. Use `checked` not `checked="true"`.

### 10. Missing JavaScript Tests

Python tests exist but there are no JavaScript unit tests.

**Requirement:** Add JavaScript tests covering:
- Component initialization
- Event listener attachment and removal
- WeakMap singleton enforcement
- HTMX re-initialization behavior
- Memory leak prevention (destroy method effectiveness)

## Implementation Guidelines

### Recommended `destroy()` Method Pattern

```javascript
class Component {
    static instances = new WeakMap();

    constructor(element) {
        if (Component.instances.has(element)) {
            return Component.instances.get(element);
        }

        this.element = element;
        this.boundClickOutside = this.handleClickOutside.bind(this);
        document.addEventListener('click', this.boundClickOutside);

        Component.instances.set(element, this);
    }

    destroy() {
        document.removeEventListener('click', this.boundClickOutside);
        if (this.autoplayInterval) {
            clearInterval(this.autoplayInterval);
        }
        Component.instances.delete(this.element);
        this.element = null;
    }

    static destroyAll(container = document) {
        container.querySelectorAll('[data-component]').forEach(el => {
            Component.instances.get(el)?.destroy();
        });
    }
}
```

### HTMX Integration Pattern

```javascript
// Clean up before swap
htmx.on("htmx:beforeSwap", (evt) => {
    InsightUI.destroyAllIn(evt.detail.target);
});

// Initialize after swap
htmx.on("htmx:afterSwap", (evt) => {
    initAll();
});
```

## Priority Matrix

| Issue | Severity | Effort | Priority |
|-------|----------|--------|----------|
| Global event listeners not cleaned | Critical | Medium | P0 |
| No destroy methods | Critical | Medium | P0 |
| Intervals not cleared | High | Low | P1 |
| XSS vulnerabilities | High | Low | P1 |
| Inline onclick handlers | High | Medium | P1 |
| HTMX cleanup integration | High | Medium | P1 |
| Inconsistent singleton pattern | Medium | Low | P2 |
| Inconsistent data attributes | Medium | Medium | P2 |
| Radio button attribute | Medium | Low | P2 |
| Missing JS tests | Medium | High | P2 |
