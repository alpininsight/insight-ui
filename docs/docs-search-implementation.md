# Documentation Search

The documentation includes a client-side fuzzy search powered by [Fuse.js](https://www.fusejs.io/). It allows users to quickly find components, types, and categories without server requests.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Search Flow                               │
│                                                                   │
│  ┌──────────────┐    ┌──────────────────┐    ┌───────────────┐  │
│  │ User types   │───▶│ Fuse.js fuzzy    │───▶│ Results       │  │
│  │ in search    │    │ matching         │    │ dropdown      │  │
│  └──────────────┘    └──────────────────┘    └───────────────┘  │
│         │                    │                                   │
│         │                    ▼                                   │
│         │           ┌──────────────────┐                        │
│         │           │ search-index-    │                        │
│         └──────────▶│ {locale}.json    │                        │
│                     └──────────────────┘                        │
└─────────────────────────────────────────────────────────────────┘
```

### Key Files

| File | Purpose |
|------|---------|
| `insight_ui/static/insight_ui/js/insight-ui-search.js` | Search JavaScript class |
| `documentation/static/documentation/data/search-index-{locale}.json` | Pre-built search index per language |
| `documentation/management/commands/build_search_index.py` | Management command to generate indexes |
| `insight_ui/templates/insight_ui/components/search_bar.html` | Search bar template in navbar |

## Generating the Search Index

The search index must be regenerated when components, types, or categories change.

```bash
# Generate indexes for all configured languages
uv run python manage.py build_search_index

# Generate for a specific language only
uv run python manage.py build_search_index --locale de
uv run python manage.py build_search_index --locale en

# Preview without writing files
uv run python manage.py build_search_index --dry-run
```

The command reads component descriptions from `component_details/description_context.py` and uses Django's translation system to generate localized indexes.

## Multilingual Support

The generic search component supports a host-provided index URL. The documentation app supplies the localized URL through `NavbarConfig.search_index_url`:

```javascript
const indexUrl = this.element.dataset.searchIndex;
```

This keeps `insight-ui` reusable: another host can provide a different static or absolute index URL without changing package JavaScript. The documentation app maps `<html lang="de">` to `/static/documentation/data/search-index-de.json` and `<html lang="en">` to `/static/documentation/data/search-index-en.json`.

Descriptions and category names are translated via Django's `gettext`. To add a new language:

1. Add the language to `settings.LANGUAGES`
2. Create translations in `locale/{lang}/LC_MESSAGES/django.po`
3. Run `uv run python manage.py build_search_index`

## Fuse.js Configuration

The search behavior is configured in `insight-ui-search.js`:

```javascript
this.fuse = new Fuse(this.searchIndex, {
    keys: [
        { name: 'name', weight: 2 },        // Component name (highest priority)
        { name: 'description', weight: 1 }, // Description text
        { name: 'keywords', weight: 0.5 },  // Keywords array
        { name: 'group', weight: 0.3 }      // Category group name
    ],
    threshold: 0.3,          // 0.0 = exact match, 1.0 = match anything
    includeScore: true,
    minMatchCharLength: 2    // Minimum characters before searching
});
```

### Tuning the Threshold

| Threshold | Behavior |
|-----------|----------|
| `0.0` | Exact matches only |
| `0.2` | Very strict fuzzy matching |
| `0.3` | Strict fuzzy matching (current) |
| `0.4` | Moderate fuzzy matching |
| `0.6` | Loose fuzzy matching |

If users report false positives (e.g., "small" matching "email"), lower the threshold. If users can't find items with typos, raise it.

### Key Weights

Higher weights mean matches in that field rank higher:
- `name: 2` - Matching the component name is most important
- `description: 1` - Description matches are secondary
- `keywords: 0.5` - Keywords help but aren't primary
- `group: 0.3` - Category matches are lowest priority

## Index Structure

Each entry in the search index has this structure:

```json
{
  "id": "component:button",
  "name": "Button",
  "category": "component",
  "group": "Input",
  "description": "For a standard button, our UI framework provides...",
  "keywords": ["button", "input", "button"],
  "url": "/docs/components/button/"
}
```

### Entry Types

| Category | ID Pattern | Example |
|----------|------------|---------|
| Components | `component:{name}` | `component:button` |
| Types | `type:{TypeName}` | `type:ButtonType` |
| Categories | `category:{name}` | `category:input` |
| Configs | `config:{ClassName}` | `config:ButtonConfig` |

## Adding Custom Keywords

Keywords are auto-generated from component names and groups. To add custom keywords, modify `_build_component_entries()` in `build_search_index.py`:

```python
# Current auto-generation
keywords = [
    component.value,
    component.group.value,
    *component.formatted_name.lower().split(),
]

# Example: Add custom keywords for specific components
if component == Component.BUTTON:
    keywords.extend(["click", "submit", "action"])
```

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+K` / `Cmd+K` | Focus search input |
| `↓` / `↑` | Navigate results |
| `Enter` | Open selected result |
| `Escape` | Close results dropdown |

## Troubleshooting

### Search returns unexpected results

1. Check the threshold value - lower it for stricter matching
2. Verify the index contains expected keywords: `cat search-index-en.json | jq '.[] | select(.name == "Button")'`
3. Rebuild the index: `uv run python manage.py build_search_index`

### Index not updating

1. Ensure you run `build_search_index` after changing `description_context.py`
2. Clear browser cache or hard refresh
3. Check that the correct locale file is being loaded (inspect Network tab)

### Translations not appearing

1. Verify translations exist in `.po` files
2. Compile messages: `django-admin compilemessages`
3. Rebuild index with correct locale: `uv run python manage.py build_search_index --locale de`
