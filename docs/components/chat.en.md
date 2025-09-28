# Chat Component (Version 0.1.0)

The chat component demonstrates a conversational UI layout with message bubbles, timestamps, and avatars.

## Usage

```django
{% include "insight_ui/components/chat.html" with messages=chat_messages %}
```

`chat_messages` should be an ordered list of dictionaries:

```python
chat_messages = [
    {
        "author": "User",
        "avatar": "insight_ui/img/avatar-user.png",
        "timestamp": "10:24",
        "text": "Hi there!",
        "alignment": "right",
    },
    {
        "author": "Support",
        "avatar": "insight_ui/img/avatar-support.png",
        "timestamp": "10:25",
        "text": "How can I help you today?",
        "alignment": "left",
    },
]
```

## Customisation

- Swap avatars or add status indicators by editing `components/chat.html`.
- Tailor the bubble colours via Tailwind tokens in `input.css`.
- Combine with HTMX or WebSockets to stream live updates.

## Accessibility

Ensure each message conveys speaker context (name + timestamp). Use ARIA live regions if messages update automatically.

## Related Guides
- WebSocket demo (`utils/main.py`)
- [Styling](../guides/styling.md)
