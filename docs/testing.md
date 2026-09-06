# Testing Guide

This document describes the test structure, tools, and conventions for Insight UI.

## Directory Structure

All tests are located in the [`tests/`](../tests/) directory:

```text
tests/
├── insight_ui/              # Package tests (pytest + Django)
│   ├── unit/                # Unit tests (components, configs, utils, tokens)
│   │   ├── components/      # Per-component template/tag tests
│   │   ├── configs/
│   │   └── utils/
│   └── integration/         # Integration / runtime contract tests
├── core/                    # Core app unit tests
│   └── unit/
├── documentation/           # Documentation app tests
│   ├── unit/
│   └── integration/
├── smoke/                   # Smoke tests for critical paths
├── js/                      # JavaScript tests (Vitest + jsdom)
│   ├── setup.js             # Global test setup and utilities
│   └── *.test.js            # Component tests
└── conftest.py              # Shared pytest fixtures
```

## Running Tests

### Python Tests

```bash
# Run all Python tests
uv run pytest

# Run specific test file
uv run pytest tests/insight_ui/unit/components/test_button.py

# Run with coverage
uv run pytest --cov

# Run specific test by name
uv run pytest -k "test_button"

# Verbose output with print statements
uv run pytest -vvs
```

### JavaScript Tests

```bash
# Run all JS tests with local Node.js dependencies
npm install
npm test

# Run all JS tests in Docker
docker run --rm -v "$(pwd):/app" -w /app node:25-alpine sh -c "npm install && npx vitest run"

# Run with coverage
docker run --rm -v "$(pwd):/app" -w /app node:25-alpine sh -c "npm install && npx vitest run --coverage"

# Run specific test file
docker run --rm -v "$(pwd):/app" -w /app node:25-alpine sh -c "npm install && npx vitest run carousel"

# Watch mode
npx vitest
```

### Static Asset Checks

The tracked Tailwind stylesheet and generated CDN browser assets must build
successfully:

```bash
npm run verify:static-build
```

When this command fails after changing `input.css` or browser assets, rebuild
the generated CDN artifacts:

```bash
npm run build:static-all
```

Generated `*.min.css` and `*.min.js` files are ignored and published by CI;
they must not be committed.

### All Tests

```bash
# Run both Python and JS tests
make test
```

## Test Categories

### Python Tests

| Category | Location | Purpose |
|----------|----------|---------|
| Unit (package) | [`tests/insight_ui/unit/`](../tests/insight_ui/unit/) | Individual components, template tags, configs, utils |
| Integration (package) | [`tests/insight_ui/integration/`](../tests/insight_ui/integration/) | Runtime contract and component interactions |
| Core | [`tests/core/unit/`](../tests/core/unit/) | Core settings, setup, packaging contracts |
| Documentation | [`tests/documentation/`](../tests/documentation/) | Documentation accuracy, demos, commands |
| Smoke | [`tests/smoke/`](../tests/smoke/) | Critical package paths |

### JavaScript Tests

Files live under [`tests/js/`](../tests/js/).

| Component | File | Coverage |
|-----------|------|----------|
| 3D Carousel | [`3d-carousel.test.js`](../tests/js/3d-carousel.test.js) | Navigation, layout |
| Accordion | [`accordion.test.js`](../tests/js/accordion.test.js) | Navigation, animation, URL state |
| Carousel | [`carousel.test.js`](../tests/js/carousel.test.js) | Navigation, autoplay, touch, RTL |
| Checkbox | [`checkbox.test.js`](../tests/js/checkbox.test.js) | Min/max constraints, validation |
| Code Block | [`code-block.test.js`](../tests/js/code-block.test.js) | Copy / highlight behavior |
| Dropdown | [`dropdown.test.js`](../tests/js/dropdown.test.js) | Toggle, outside click |
| Floater | [`floater.test.js`](../tests/js/floater.test.js) | Tooltip/popover, positioning |
| HTMX | [`htmx.test.js`](../tests/js/htmx.test.js) | HTMX hooks |
| Lifecycle | [`lifecycle.test.js`](../tests/js/lifecycle.test.js) | Mount / destroy lifecycle |
| Modal | [`modal.test.js`](../tests/js/modal.test.js) | Focus trap, scroll blocking |
| Multiselect | [`multiselect.test.js`](../tests/js/multiselect.test.js) | Selection, search, keyboard nav |
| Progress Bar | [`progress-bar.test.js`](../tests/js/progress-bar.test.js) | Polling, SSE, error handling |
| Range Slider | [`range-slider.test.js`](../tests/js/range-slider.test.js) | Value updates, constraints |
| Sidebar | [`sidebar.test.js`](../tests/js/sidebar.test.js) | Mobile drawer, auto-close |
| Singleton | [`singleton.test.js`](../tests/js/singleton.test.js) | Instance registry |
| Tabs | [`tabs.test.js`](../tests/js/tabs.test.js) | Tab switching, ARIA |
| Theme Toggle | [`theme-toggle.test.js`](../tests/js/theme-toggle.test.js) | Dark mode, persistence |
| Utils | [`utils.test.js`](../tests/js/utils.test.js) | Focus trap, scroll blocking |
| WebSocket | [`websocket.test.js`](../tests/js/websocket.test.js) | Connection helpers |

## Writing Tests

### Python Test Conventions

```python
from django.template import Context, Template


class TestButtonComponent:
    """Tests for the button component."""

    def test_renders_with_default_props(self):
        """Button renders with default styling."""
        template = Template("{% load insight_tags %}{% button label='Click' %}")
        result = template.render(Context())

        assert "Click" in result
        assert "btn-" in result

    def test_accepts_config_object(self, button_config):
        """Button accepts a config dataclass."""
        template = Template("{% load insight_tags %}{% button config=cfg %}")
        result = template.render(Context({"cfg": button_config}))

        assert button_config.label in result
```

### JavaScript Test Conventions

```javascript
import { describe, it, expect, beforeEach, vi } from 'vitest';

describe('ComponentName', () => {
  beforeEach(() => {
    globalThis.InsightUI = {};
    globalThis.window.InsightUI = globalThis.InsightUI;
    loadComponent('insight-ui-component.js');
  });

  describe('Feature Group', () => {
    it('should do something specific', () => {
      const container = createComponentDOM();
      const element = container.querySelector('[data-insight-component]');

      const instance = new InsightUI.Component(element);

      expect(instance.someProperty).toBe(expectedValue);
    });
  });

  describe('destroy() method', () => {
    it('should remove event listeners', () => {
      // Test cleanup
    });

    it('should remove instance from WeakMap', () => {
      // Test singleton cleanup
    });
  });
});
```

## Test Utilities

### Python ([`tests/conftest.py`](../tests/conftest.py))

- `@pytest.fixture` for common test data
- Django test client setup
- template rendering helpers

### JavaScript ([`tests/js/setup.js`](../tests/js/setup.js))

- `TestUtils.createDOM(html)` - create DOM elements
- `TestUtils.click(element)` - simulate click events
- `TestUtils.createCarousel()` - component-specific helpers
- `TestUtils.createAlert(type)` - alert component helper
- mock for `debugLog()` function

## What To Test

| Change type | Expected test coverage |
|-------------|------------------------|
| Template tag or Python config | Unit tests under [`tests/insight_ui/unit/`](../tests/insight_ui/unit/) |
| Component rendering | Template output tests and self-documentation demo update |
| JavaScript behavior | Vitest test under [`tests/js/`](../tests/js/) |
| Static asset build behavior | Static asset check or script-level test |
| Accessibility-sensitive markup | Semantic HTML, ARIA, and keyboard behavior checks where applicable |

Keep tests focused on the public package contract. Private deployment behavior
belongs in the operating organization's private platform tests and runbooks.

## Coverage

### Python Coverage

```bash
# Generate coverage report
uv run pytest --cov --cov-report=html

# View report
open htmlcov/index.html
```

### JavaScript Coverage

```bash
# Generate coverage report
npx vitest run --coverage

# Coverage is output to coverage/ directory
```

Coverage targets:

- Python: 80% minimum
- JavaScript: 70% minimum for browser-facing components

## CI Integration

Tests run automatically on every pull request:

1. Python tests with pytest.
2. JavaScript tests with Vitest.
3. Linting and quality checks.
4. Static asset freshness checks when relevant.
