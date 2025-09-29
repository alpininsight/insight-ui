# Code Block Component (Version 0.1.0)

The code block component renders syntax-highlighted snippets with Tailwind styling. It is mainly used in documentation pages and demo partials.

## Usage

```django
{% include "insight_ui/components/code_block.html" with code=snippet language="python" %}
```

- `code`: the raw code string to display.
- `language`: optional hint for the highlighter (e.g. `python`, `django`, `bash`).

## Features

- Preserves indentation and wraps long lines gracefully.
- Supports copy-to-clipboard via the bundled JavaScript.
- Uses the theme tokens so colours adapt to light/dark mode.

## Customisation

Override `components/code_block.html` to change the wrapper (e.g. add line numbers) or to plug in a different highlight library.

## Related Resources

- Tailwind configuration in `insight_ui/utils/input.css`
- Demo partial: `insight_ui/templates/insight_ui/docs/partial/code_block_detailpage.html`
