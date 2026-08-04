# Accessibility

Insight UI components are designed to comply with WCAG 2.1 AA guidelines. This document explains accessibility features and how to maintain them when contributing.

## Built-in Accessibility Features

### Semantic HTML

Components use appropriate HTML elements:

- Buttons use `<button>`, not `<div>` with click handlers
- Navigation uses `<nav>` with proper list structure
- Headings use `<h1>`-`<h6>` in logical order
- Articles use `<article>`, sections use `<section>`

### ARIA Attributes

Components include ARIA attributes where needed:

```html
<!-- Modal with proper ARIA -->
<div role="dialog" aria-modal="true" aria-labelledby="modal-title">
    <h2 id="modal-title">Modal Title</h2>
</div>

<!-- Status notifications -->
<div role="status">Operation successful</div>
<div role="alert">Error: Something went wrong</div>

<!-- Decorative elements hidden -->
<svg aria-hidden="true">...</svg>
```

### Keyboard Navigation

All interactive components support keyboard navigation:

| Component | Keyboard Support |
|-----------|-----------------|
| Modal | `Escape` to close, focus trap |
| Dropdown | `Escape` to close, arrow keys to navigate |
| Tabs | Arrow keys to switch tabs |
| Accordion | `Enter`/`Space` to expand/collapse |
| Carousel | Arrow keys for navigation |

### Focus Management

- Visible focus indicators on all interactive elements
- Focus trap in modals and overlays
- Focus restoration when modals close
- Skip links for navigation blocks

### Color and Contrast

- Text meets WCAG AA contrast ratios (4.5:1 normal, 3:1 large)
- Information is not conveyed by color alone
- Support for high contrast mode
- Dark mode with appropriate contrast

## Component Accessibility Documentation

Each component has specific accessibility notes in `insight_ui/component_details/a11y_context.py`. These are displayed on component detail pages.

Examples from actual components:

**Modal:**
- Uses `role="dialog"` and `aria-modal="true"`
- Focus is trapped within the modal
- `Escape` key closes the modal
- Focus returns to trigger element on close

**Status Screen:**
- Title rendered as semantic `<h1>`
- Decorative icons use `aria-hidden`
- Error notices use `role="alert"`
- Other notices use `role="status"`

**Tabs:**
- Tab list uses `role="tablist"`
- Tabs use `role="tab"` with `aria-selected`
- Panels use `role="tabpanel"` with `aria-labelledby`
- Arrow keys navigate between tabs

## Accessibility Checklist for Contributors

When adding or modifying components:

- [ ] Use semantic HTML elements (`<button>`, `<nav>`, `<main>`, etc.)
- [ ] Add ARIA attributes where HTML semantics are insufficient
- [ ] Ensure keyboard navigation works (Tab, Enter, Escape, arrows)
- [ ] Maintain visible focus indicators
- [ ] Hide decorative elements with `aria-hidden="true"`
- [ ] Test color contrast (4.5:1 for normal text, 3:1 for large text)
- [ ] Ensure information is not conveyed by color alone
- [ ] Update `a11y_context.py` with accessibility notes
- [ ] Test with keyboard-only navigation

## Testing Accessibility

### Manual Testing

1. **Keyboard navigation**: Tab through the page, interact without a mouse
2. **Screen reader**: Test with NVDA (Windows), VoiceOver (macOS), or Orca (Linux)
3. **Zoom**: Verify functionality at 200% and 400% zoom
4. **Color contrast**: Use browser DevTools or [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
5. **High contrast mode**: Test in Windows High Contrast mode

### Browser Tools

- Chrome DevTools Accessibility panel
- Firefox Accessibility Inspector
- [WAVE Browser Extension](https://wave.webaim.org/extension/)
- [axe DevTools](https://www.deque.com/axe/devtools/)

### Quick Checks

```bash
# Check for missing alt text
grep -r "<img" insight_ui/templates | grep -v "alt="

# Check for clickable divs (should be buttons)
grep -r "onclick" insight_ui/templates | grep "<div"
```

## Common Patterns

### Interactive Elements

```html
<!-- Correct: Button for actions -->
<button type="button" onclick="doSomething()">Click me</button>

<!-- Incorrect: Div with click handler -->
<div onclick="doSomething()">Click me</div>
```

### Images

```html
<!-- Informative image -->
<img src="chart.png" alt="Sales increased 25% in Q4">

<!-- Decorative image -->
<img src="decoration.png" alt="" role="presentation">

<!-- Icon with visible label -->
<button>
    <svg aria-hidden="true">...</svg>
    Save
</button>

<!-- Icon-only button -->
<button aria-label="Close">
    <svg aria-hidden="true">...</svg>
</button>
```

### Dynamic Content

```html
<!-- Status message -->
<div role="status" aria-live="polite">
    File uploaded successfully
</div>

<!-- Error message (more urgent) -->
<div role="alert" aria-live="assertive">
    Upload failed: File too large
</div>
```

## Resources

- [WCAG 2.1 Guidelines](https://www.w3.org/TR/WCAG21/)
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- [The A11Y Project](https://www.a11yproject.com/)
- [MDN Accessibility Guide](https://developer.mozilla.org/en-US/docs/Web/Accessibility)
- [ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/)
