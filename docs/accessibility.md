# Accessibility (a11y)

Insight UI should be developed with accessibility in mind. All components must comply with WCAG 2.1 AA guidelines and should provide an optimal user experience for all users, regardless of their abilities or the technology they use.

## Accessibility features

### Keyboard navigation

All interactive elements are fully accessible via the keyboard:

- Focus order follows the natural document flow
- Visible focus indicator for all interactive elements
- Keyboard shortcuts for frequently used actions
- Skip links for skipping navigation blocks

### Screen reader support

All components are optimized for screen readers:

- Semantic HTML with correct ARIA attributes
- Meaningful alt text for images
- ARIA live regions for dynamic content
- Descriptive labels for form elements

### Color contrast and visibility

- All text and UI elements meet WCAG 2.1 AA contrast requirements
- High contrast mode for users with visual impairments
- No information conveyed solely by color
- Responsive designs with customizable text size

### Responsive Design

- Fully responsive layouts for all screen sizes
- Support for zoom up to 400% without loss of functionality
- Adaptation to different input methods (mouse, keyboard, touch)

Accessibility Checklist

Here is a checklist you can use to ensure your application remains accessible:

- [ ] All images have meaningful alt text
- [ ] Color contrast meets WCAG 2.1 AA requirements (4.5:1 for normal text, 3:1 for large text)
- [ ] All functions are accessible via the keyboard
- [ ] Focus order is logical and intuitive
- [ ] Form elements have descriptive labels
- [ ] Dynamic content uses ARIA live regions
- [ ] No information is conveyed solely through color
- [ ] Page is still usable at 200% zoom
- [ ] Semantic HTML is used
- [ ] Skip links are available

## Testing for accessibility

### Automated tests

- _May be available at some point._

### Manual testing

- Test with a screen reader (e.g., NVDA, JAWS, VoiceOver)
- Navigate through your application using only the keyboard
- Test with different zoom levels
- Check color contrast with tools such as the WAVE Browser Extension
- Test in high contrast mode

## Resources

- [WCAG 2.1 Guidelines](https://www.w3.org/TR/WCAG21/)
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- [The A11Y Project](https://www.a11yproject.com/)
- [MDN Web Docs: Accessibility](https://developer.mozilla.org/en-US/docs/Web/Accessibility)
