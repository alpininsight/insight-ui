# Test Coverage Requirements

This document outlines identified gaps and requirements for improving test coverage in Insight UI to meet enterprise standards.

## Current State Summary

| Metric | Current | Target |
|--------|---------|--------|
| Total Test Files | 5 | 15+ |
| Total Test Functions | 49 | 200+ |
| Template Tag Coverage | 39.5% (17/43) | 80%+ |
| JavaScript Coverage | 0% (0/19 files) | 80%+ |
| E2E Test Coverage | 0% | Core workflows |
| Accessibility Tests | 0% | WCAG 2.1 AA |

## Critical Issues

### 1. No JavaScript Testing Framework

**Severity**: CRITICAL

**Current State**: 19 JavaScript files with 0% test coverage. No testing framework installed.

| File | Lines | Complexity | Risk |
|------|-------|------------|------|
| `insight-ui-multiselect.js` | 286 | High | Critical |
| `insight-ui-accordion.js` | 162 | Medium | High |
| `insight-ui-carousel.js` | 135 | Medium | High |
| `insight-ui-3D-carousel.js` | 86 | Medium | Medium |
| `insight-ui-tabs.js` | 83 | Medium | Medium |
| `insight-ui-modal.js` | 70 | Medium | High |
| `insight-ui-dropdown.js` | 58 | Low | Medium |
| `insight-ui-checkbox.js` | 57 | Low | Medium |
| `insight-ui-floater.js` | ~100 | Medium | High |
| `insight-ui-sidebar.js` | ~100 | Medium | Medium |
| `insight-ui-init.js` | ~50 | Low | High |
| `insight-ui-websocket.js` | ~80 | Medium | High |
| Others (7 files) | ~200 | Low-Medium | Medium |

**Requirement**: Install and configure Vitest or Jest for JavaScript unit testing.

**Implementation**:
```bash
# Option 1: Vitest (recommended - faster, ESM-native)
npm install -D vitest jsdom @testing-library/dom

# Option 2: Jest
npm install -D jest jest-environment-jsdom @testing-library/dom
```

**Test file structure**:
```
insight_ui/static/insight_ui/js/
├── __tests__/
│   ├── insight-ui-accordion.test.js
│   ├── insight-ui-carousel.test.js
│   ├── insight-ui-modal.test.js
│   └── ...
```

### 2. No End-to-End Testing

**Severity**: CRITICAL

**Current State**: No browser automation testing. User workflows completely untested.

**Requirement**: Implement Playwright for E2E testing.

**Implementation**:
```bash
npm install -D @playwright/test
npx playwright install
```

**Test scenarios required**:
- Modal open/close with keyboard (Escape)
- Accordion expand/collapse with keyboard navigation
- Dropdown selection with arrow keys
- Carousel navigation (buttons, swipe, autoplay)
- Tab switching with keyboard
- Form submission with validation
- Multiselect search and selection
- Theme toggle persistence

**Test file structure**:
```
tests/
├── e2e/
│   ├── test_modal_interaction.py
│   ├── test_accordion_keyboard.py
│   ├── test_form_submission.py
│   └── ...
```

### 3. No Accessibility Testing

**Severity**: HIGH

**Current State**: Accessibility claims in component documentation are unverified.

**Requirement**: Implement automated accessibility testing with axe-core.

**Implementation**:
```bash
# For Playwright E2E tests
npm install -D @axe-core/playwright

# For Python tests
pip install axe-selenium-python
```

**WCAG 2.1 AA compliance tests required**:
- All interactive elements have accessible names
- Focus indicators visible on all focusable elements
- Color contrast ratios meet minimum requirements
- Keyboard navigation works for all components
- ARIA attributes correctly applied
- Screen reader announcements for dynamic content

**Test pattern**:
```python
# tests/accessibility/test_component_a11y.py
import pytest
from axe_playwright_python.sync_playwright import Axe

def test_modal_accessibility(page):
    page.goto("/components/modal/demo/")
    axe = Axe()
    results = axe.run(page)
    assert results.violations_count == 0, results.generate_report()
```

## High Priority Issues

### 4. Incomplete Template Tag Unit Tests

**Severity**: HIGH

**Current State**: Only 17 of 43 template tags have unit tests (39.5% coverage).

**Untested template tags** (26 tags):

| Tag | File | Priority |
|-----|------|----------|
| `input` | `insight_tags.py` | High |
| `textarea` | `insight_tags.py` | High |
| `dropdown` | `insight_tags.py` | High |
| `select` | `insight_tags.py` | High |
| `multiselect` | `insight_tags.py` | High |
| `radio_block` | `insight_tags.py` | Medium |
| `range_slider` | `insight_tags.py` | Medium |
| `chat` | `insight_tags.py` | Medium |
| `chat_response` | `insight_tags.py` | Medium |
| `geo_map` | `insight_tags.py` | Low |
| `bar_chart` | `insight_tags.py` | Medium |
| `line_chart` | `insight_tags.py` | Medium |
| `card_carousel` | `insight_tags.py` | Medium |
| `image_carousel` | `insight_tags.py` | Medium |
| `3D_carousel` | `insight_tags.py` | Low |
| `flip_card` | `insight_tags.py` | Low |
| `horizontale_card` | `insight_tags.py` | Low |
| `steps_bar` | `insight_tags.py` | Low |
| `bullet_point_list` | `insight_tags.py` | Low |
| `progress_bar` | `insight_tags.py` | Medium |
| `tooltip` | `insight_tags.py` | Medium |
| `popover` | `insight_tags.py` | Medium |
| `code_block` | `insight_tags.py` | Low |
| `generic_filter` | `insight_tags.py` | Medium |
| `search_bar` | `insight_tags.py` | Medium |
| `query_builder` | `insight_tags.py` | Medium |

**Requirement**: Add unit tests for all template tags, prioritizing input elements and interactive components.

**Test pattern**:
```python
# tests/unit/test_template_tags.py
class InputTemplateTagTest(TestCase):
    def test_input_renders_with_required_params(self):
        rendered = render_template_tag("input", {
            "tag_id": "email",
            "name": "email",
            "label": "Email Address"
        })
        soup = BeautifulSoup(rendered, "html.parser")
        input_el = soup.find("input")
        self.assertEqual(input_el["id"], "email")
        self.assertEqual(input_el["name"], "email")

    def test_input_renders_with_validation(self):
        # Test required, pattern, min/max attributes
        pass

    def test_input_renders_with_error_state(self):
        # Test error message display
        pass
```

### 5. Minimal Integration Tests

**Severity**: HIGH

**Current State**: Only 3 integration tests exist. Most view logic tested only via smoke tests (HTTP 200).

**Views requiring integration tests**:

| View | Current Tests | Required Tests |
|------|---------------|----------------|
| `live_data_view` | 2 | 5+ |
| `chat_response` | 0 | 3+ |
| `form_submit` | 0 | 5+ |
| `pagination` | 0 | 3+ |
| `more_items_view` | 0 | 3+ |
| `toggle_view` | 0 | 2+ |
| `tabs_view` | 0 | 2+ |

**Requirement**: Add comprehensive integration tests for all view functions.

**Test scenarios**:
```python
# tests/integration/test_form_submission.py
class FormSubmitIntegrationTest(TestCase):
    def test_form_submit_valid_data(self):
        pass

    def test_form_submit_invalid_data_returns_errors(self):
        pass

    def test_form_submit_htmx_returns_partial(self):
        pass

    def test_form_submit_csrf_protection(self):
        pass

    def test_form_submit_rate_limiting(self):
        pass
```

### 6. Untested Utility Modules

**Severity**: MEDIUM

**Current State**: Only pagination utility tested. Query builder utilities (107 lines) completely untested.

| Module | Lines | Tests | Coverage |
|--------|-------|-------|----------|
| `pagination.py` | 55 | 22 | 100% |
| `query_builder_utils.py` | 107 | 0 | 0% |
| `diff.py` | 23 | 0 | 0% |

**Requirement**: Add unit tests for all utility modules.

**Test scenarios for query_builder_utils.py**:
```python
# tests/unit/test_query_builder_utils.py
class FilterFieldConfigTest(TestCase):
    def test_filter_field_config_initialization(self):
        pass

    def test_get_allowed_operators_for_text_field(self):
        pass

    def test_get_allowed_operators_for_numeric_field(self):
        pass

    def test_get_allowed_operators_for_date_field(self):
        pass

    def test_invalid_field_type_raises_error(self):
        pass
```

## Medium Priority Issues

### 7. No HTMX Integration Tests

**Severity**: MEDIUM

**Current State**: HTMX is a core dependency but interaction patterns are untested.

**Requirement**: Add tests for HTMX-specific behaviors.

**Test scenarios**:
- `hx-get` / `hx-post` request handling
- `hx-target` content replacement
- `hx-swap` modes (innerHTML, outerHTML, beforeend, etc.)
- `hx-trigger` event handling
- Loading indicators (`htmx:beforeRequest`, `htmx:afterRequest`)
- Error handling (`htmx:responseError`)
- Component re-initialization after HTMX swaps

### 8. No Form Validation Tests

**Severity**: MEDIUM

**Current State**: ChatForm exists but has no tests. Form validation logic untested.

**Requirement**: Add tests for all forms and validation logic.

**Test scenarios**:
```python
# tests/unit/test_forms.py
class ChatFormTest(TestCase):
    def test_chat_form_valid_message(self):
        pass

    def test_chat_form_empty_message_invalid(self):
        pass

    def test_chat_form_max_length_validation(self):
        pass

    def test_chat_form_xss_sanitization(self):
        pass
```

### 9. Single Python Version in CI

**Severity**: MEDIUM

**Current State**: CI only tests Python 3.13. Package claims 3.12-3.14 support.

**Requirement**: Add test matrix for all supported Python versions.

**Implementation** (`.github/workflows/feature-ci.yml`):
```yaml
jobs:
  test:
    strategy:
      matrix:
        python-version: ["3.12", "3.13", "3.14"]
    steps:
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
```

### 10. No Coverage Reporting in CI

**Severity**: MEDIUM

**Current State**: pytest-cov installed but not used in CI. No coverage thresholds enforced.

**Requirement**: Enable coverage reporting with minimum threshold.

**Implementation**:
```yaml
# .github/workflows/feature-ci.yml
- name: Run tests with coverage
  run: |
    uv run pytest --cov=insight_ui --cov-report=xml --cov-fail-under=70

- name: Upload coverage to Codecov
  uses: codecov/codecov-action@v4
  with:
    file: ./coverage.xml
```

## Low Priority Issues

### 11. No Visual Regression Testing

**Severity**: LOW

**Current State**: No screenshot-based testing for visual consistency.

**Requirement**: Consider implementing visual regression tests for critical components.

**Tools**: Playwright screenshots, Percy, Chromatic

### 12. No Performance Benchmarks

**Severity**: LOW

**Current State**: No performance testing for large dataset rendering.

**Requirement**: Add performance tests for pagination, table rendering, and carousels with large datasets.

### 13. Skipped Test Not Addressed

**Severity**: LOW

**Current State**: `test_radio_block_block` is skipped with comment "Needs to be finished!"

**Location**: `tests/unit/test_template_tags.py`

**Requirement**: Complete or remove the skipped test.

## Implementation Guidelines

### Test File Naming Convention

```
tests/
├── unit/
│   ├── test_template_tags.py      # Template tag unit tests
│   ├── test_utils.py              # Utility function tests
│   ├── test_forms.py              # Form validation tests
│   └── test_views.py              # View unit tests (mocked)
├── integration/
│   ├── test_api.py                # API integration tests
│   ├── test_htmx.py               # HTMX integration tests
│   └── test_forms.py              # Form submission tests
├── smoke/
│   └── test_smoke.py              # HTTP 200 checks
├── e2e/
│   ├── test_modal.py              # Modal E2E tests
│   ├── test_accordion.py          # Accordion E2E tests
│   └── test_form_workflow.py      # Form workflow tests
├── accessibility/
│   └── test_wcag.py               # WCAG compliance tests
└── js/
    └── (managed via npm/vitest)   # JavaScript unit tests
```

### Pytest Markers Usage

```python
# Existing markers
@pytest.mark.smoke        # Fast HTTP checks
@pytest.mark.integration  # API/DB integration
@pytest.mark.django_db    # Database access required

# New markers to add
@pytest.mark.e2e          # End-to-end browser tests
@pytest.mark.a11y         # Accessibility tests
@pytest.mark.slow         # Tests taking >1s
@pytest.mark.js           # JavaScript-dependent tests
```

### CI Test Stages

```yaml
jobs:
  lint:
    # Ruff check
  unit-tests:
    # pytest tests/unit/
  integration-tests:
    # pytest tests/integration/
  smoke-tests:
    # pytest -m smoke
  e2e-tests:
    # pytest tests/e2e/ (with Playwright)
  a11y-tests:
    # pytest tests/accessibility/
  js-tests:
    # npm test (Vitest/Jest)
```

## Priority Matrix

| Issue | Severity | Effort | Priority |
|-------|----------|--------|----------|
| No JavaScript testing framework | Critical | High | P0 |
| No E2E testing | Critical | High | P0 |
| No accessibility testing | High | Medium | P1 |
| Incomplete template tag tests | High | Medium | P1 |
| Minimal integration tests | High | Medium | P1 |
| Untested utility modules | Medium | Low | P2 |
| No HTMX integration tests | Medium | Medium | P2 |
| No form validation tests | Medium | Low | P2 |
| Single Python version in CI | Medium | Low | P2 |
| No coverage reporting in CI | Medium | Low | P2 |
| No visual regression testing | Low | High | P3 |
| No performance benchmarks | Low | Medium | P3 |
| Skipped test not addressed | Low | Low | P3 |

## Target Test Coverage

| Area | Current | 3-Month Target | 6-Month Target |
|------|---------|----------------|----------------|
| Template Tags | 39.5% | 70% | 85% |
| JavaScript | 0% | 50% | 80% |
| Views | 92% (smoke) | 80% (unit+int) | 90% |
| Utilities | 33% | 80% | 95% |
| E2E Workflows | 0% | 5 core flows | 15 flows |
| Accessibility | 0% | WCAG AA critical | WCAG AA full |
