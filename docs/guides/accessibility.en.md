# Accessibility (Version 0.1.0)

> Note: Insight UI is still evolving. Some components need additional polishing to meet every WCAG success criterion. Treat this guide as a living checklist while you extend the library.

Insight UI is built with accessibility in mind. Components aim for WCAG 2.1 AA compliance so that users—regardless of ability or input method—can navigate and understand the interface.

## Built-in Accessibility Features

### Keyboard Navigation
- Logical tab order that follows the document flow
- Visible focus outlines on interactive elements
- Keyboard shortcuts for common actions where appropriate
- Skip links to bypass navigation blocks and jump to the main content

### Screen Reader Support
- Semantic HTML structure with appropriate ARIA roles
- Meaningful `alt` text for imagery (decorative icons hidden from assistive tech)
- ARIA live regions for dynamic updates such as alerts or live content
- Descriptive labels and instructions for all form controls

### Colour & Contrast
- Colour palette targets WCAG 2.1 AA contrast ratios in light and dark themes
- High-contrast token set available for custom themes
- Never rely on colour alone to convey information
- Responsive typography to support user zoom preferences

### Responsiveness
- Layouts adapt to a wide range of breakpoints
- Usable at 400 % zoom without functional loss
- Supports multiple input types (keyboard, mouse, touch)

## Accessibility Checklist
Use this list when reviewing new components or changes:

1. **Keyboard** – All interactive elements reachable and operable via keyboard, with logical focus order.
2. **Focus styling** – Focus indicators clearly visible and with sufficient contrast.
3. **Semantics** – Appropriate HTML elements and ARIA roles; avoid generic wrappers when native elements exist.
4. **Labels & instructions** – Form controls labeled, error messages announced, instructions visible.
5. **Colour contrast** – Text/UI contrast meets WCAG 2.1 AA in both light and dark themes.
6. **Motion/animation** – Respect `prefers-reduced-motion`; avoid distracting effects.
7. **Dynamic updates** – Use polite/assertive ARIA live regions for auto-updated content.
8. **Testing** – Verify with keyboard only, screen readers (NVDA/VoiceOver), and automated tooling (axe, Lighthouse).

## Resources
- [WCAG 2.1 AA Overview](https://www.w3.org/TR/WCAG21/)
- [WAI-ARIA Authoring Practices](https://www.w3.org/TR/wai-aria-practices/)
- [Deque Axe DevTools](https://www.deque.com/axe/)

Keep this guide updated whenever you introduce new components or refine existing ones.
