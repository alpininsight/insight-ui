# Modal Component (Version 0.1.0)

The modal component renders an accessible dialog with focus trapping, optional action buttons, and Tailwind theming.

## Usage

```django
{% load insight_tags %}
{% modal html_tag_id="demo-modal" title="Demo" description="Additional context" actions=modal_actions %}
```

### Parameters
- **html_tag_id**: unique ID for the modal container.
- **title**: heading displayed in the dialog.
- **description** (optional): supporting text.
- **content** (optional): HTML body.
- **actions** (optional): list of button dictionaries (text, url, type).

## Accessibility
- Uses semantic dialog markup and focus trapping.
- Close button and overlay are keyboard operable.
- Provide meaningful `title`/`description` to give screen readers context.

## Customisation
- Override `components/modal.html` to add form layouts or extra sections.
- Use theme tokens in `input.css` to adjust colours.

## Related Components
- [Alert banner](alert.en.md)
- [Form](form.en.md)
