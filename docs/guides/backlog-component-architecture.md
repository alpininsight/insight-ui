# Epic: Component Architecture Improvements

**Epic ID:** ARCH-001
**Status:** In Progress
**Priority:** High
**Created:** 2025-12-18
**Updated:** 2025-12-18
**Requirements:** [component-architecture-requirements.md](component-architecture-requirements.md)

## Epic Description

Improve the JavaScript component architecture to eliminate memory leaks, enhance security, and establish consistent patterns across all UI components.

## Acceptance Criteria

- [x] All components implement `destroy()` method for proper cleanup *(Sprint 1)*
- [x] No memory leaks from global event listeners *(Sprint 1)*
- [x] HTMX content swaps properly clean up old component instances *(Sprint 1)*
- [ ] All `|safe` filter usage is reviewed and documented or removed
- [ ] No inline `onclick` handlers with interpolated values
- [x] Consistent singleton pattern across all components *(Sprint 1 - Carousel converted)*
- [ ] Consistent data attribute naming convention
- [ ] JavaScript test coverage for component lifecycle

---

## Sprint 1: Critical Foundation (P0) ✅ COMPLETED

**Goal:** Establish proper component lifecycle management to prevent memory leaks

**Completed:** 2025-12-18
**Commit:** `6ec8b8f` feat(js): add destroy() lifecycle methods to all components

### User Stories

#### ARCH-001-01: Component Cleanup Infrastructure ✅
**As a** developer
**I want** a standardized destroy() pattern
**So that** components can be properly cleaned up when removed from DOM

**Tasks:**
| ID | Task | File | Story Points | Status |
|----|------|------|--------------|--------|
| 1.1 | Create base `destroy()` helper in utils | `insight-ui-utils.js` | 2 | ✅ Done |
| 1.2 | Add `destroy()` to Dropdown | `insight-ui-dropdown.js` | 2 | ✅ Done |
| 1.3 | Add `destroy()` to Floater | `insight-ui-floater.js` | 2 | ✅ Done |
| 1.4 | Add `destroy()` to Multiselect | `insight-ui-multiselect.js` | 3 | ✅ Done |
| 1.5 | Add `destroy()` to Sidebar | `insight-ui-sidebar.js` | 2 | ✅ Done |
| 1.6 | Add `destroy()` to Carousel + clear interval | `insight-ui-carousel.js` | 3 | ✅ Done |
| 1.7 | Add `destroy()` to Accordion | `insight-ui-accordion.js` | 2 | ✅ Done |
| 1.8 | Add `destroy()` to Modal | `insight-ui-modal.js` | 2 | ✅ Done |
| 1.9 | Add `destroy()` to Tabs | `insight-ui-tabs.js` | 2 | ✅ Done |
| 1.10 | Add `destroy()` to Checkbox | `insight-ui-checkbox.js` | 2 | ✅ Done |

**Sprint Points:** 22 ✅

#### ARCH-001-02: HTMX Lifecycle Integration ✅
**As a** developer
**I want** HTMX swaps to automatically clean up old components
**So that** dynamic content updates don't cause memory leaks

**Tasks:**
| ID | Task | File | Story Points | Status |
|----|------|------|--------------|--------|
| 1.11 | Add `htmx:beforeSwap` cleanup handler | `insight-ui-init.js` | 3 | ✅ Done |
| 1.12 | Add `destroyAllIn(container)` utility function | `insight-ui-utils.js` | 2 | ✅ Done |
| 1.13 | Test HTMX swap cleanup behavior | Manual testing | 2 | ✅ Done |

**Sprint Points:** 7 ✅

**Sprint 1 Total:** 29 points ✅

### Sprint 1 Notes

- Carousel was converted from data-attribute flag to WeakMap singleton pattern (originally Sprint 3 Task 3.1)
- All components now store bound handlers for proper `removeEventListener` cleanup
- `lifecycle.destroyAllIn()` added to utils (not init.js) for better organization
- `htmx:beforeSwap` hook automatically cleans up components before DOM replacement

---

## Sprint 2: Security Hardening (P1) ✅ COMPLETED

**Goal:** Eliminate XSS vulnerabilities and code injection risks

**Completed:** 2025-12-18
**Note:** Tasks 2.1 and 2.8 (modal.html) deferred - kept as-is per project decision

### User Stories

#### ARCH-001-03: Safe Filter Audit ✅
**As a** security-conscious developer
**I want** all `|safe` filter usage reviewed
**So that** XSS vulnerabilities are eliminated or documented

**Tasks:**
| ID | Task | File | Story Points | Status |
|----|------|------|--------------|--------|
| 2.1 | Audit `modal.html` - document or remove `\|safe` | `modal.html` | 1 | ⏸️ Deferred |
| 2.2 | Audit `live_content.html` - document or remove `\|safe` | `live_content.html` | 1 | ✅ Reviewed |
| 2.3 | Audit `bar_chart.html` - document or remove `\|safe` | `bar_chart.html` | 1 | ✅ Reviewed |
| 2.4 | Audit `websocket.html` - document or remove `\|safe` | `websocket.html` | 1 | ✅ Reviewed |

**Sprint Points:** 4 (3 completed, 1 deferred)

#### ARCH-001-04: Inline Handler Removal ✅
**As a** security-conscious developer
**I want** inline onclick handlers replaced with event delegation
**So that** code injection risks are eliminated

**Tasks:**
| ID | Task | File | Story Points | Status |
|----|------|------|--------------|--------|
| 2.5 | Refactor `radio_block.html` - use data attributes | `radio_block.html` | 3 | ✅ Done |
| 2.6 | Refactor `form_errors.html` - use JS event binding | `form_errors.html` | 2 | ✅ Done |
| 2.7 | Refactor `alert.html` - use JS event binding | `alert.html` | 2 | ✅ Done |
| 2.8 | Refactor `modal.html` - use data attributes | `modal.html` | 3 | ⏸️ Deferred |

**Sprint Points:** 10 (7 completed, 3 deferred)

**Sprint 2 Total:** 14 points (10 completed, 4 deferred)

### Sprint 2 Notes

**Safe Filter Audit Findings:**
- `live_content.html`: Uses `{{ initial_content|safe }}` - **Intentional** for rendering HTML content loaded via HTMX. Risk: Low if content is server-generated.
- `bar_chart.html`: Uses `{{ chart.series|safe }}` and `{{ chart.x_axis_legend|safe }}` - **Necessary** for passing JSON arrays to JavaScript. Risk: Medium if data contains user input.
- `websocket.html`: Uses `{{ options.initial_content|safe }}` - **Intentional** for HTML content. Risk: Low if content is server-generated.

**Recommendation:** Document in developer guide that `|safe` filter inputs must be sanitized server-side.

**Inline Handler Refactoring:**
- Added `InsightUI.handlers` module with event delegation for radio callbacks, alert dismissal, and form error dismissal
- Replaced `onclick` with `data-insight-dismiss` and `data-radio-callback` attributes
- Event delegation means handlers work for dynamically added content (HTMX compatible)

---

## Sprint 3: Standardization (P2) 🔜 READY

**Goal:** Establish consistent patterns across all components
**Status:** Ready to start

### User Stories

#### ARCH-001-05: Singleton Pattern Standardization
**As a** developer
**I want** all stateful components to use WeakMap singleton
**So that** component instance management is consistent

**Tasks:**
| ID | Task | File | Story Points | Status |
|----|------|------|--------------|--------|
| 3.1 | Convert Carousel to WeakMap singleton | `insight-ui-carousel.js` | 2 | ✅ Done (Sprint 1) |
| 3.2 | Add instance tracking to 3D-Carousel | `insight-ui-3D-carousel.js` | 2 | Backlog |

**Sprint Points:** 4 (2 remaining)

#### ARCH-001-06: Data Attribute Convention
**As a** developer
**I want** consistent data attribute naming
**So that** component APIs are predictable

**Tasks:**
| ID | Task | File | Story Points | Status |
|----|------|------|--------------|--------|
| 3.3 | Standardize dropdown data attributes | `dropdown.html` + JS | 2 | Backlog |
| 3.4 | Standardize accordion data attributes | `accordion.html` + JS | 2 | Backlog |
| 3.5 | Standardize multiselect data attributes | `multiselect.html` + JS | 2 | Backlog |
| 3.6 | Fix radio button `checked` attribute | `radio_button.html` | 1 | Backlog |
| 3.7 | Document convention in naming guide | `naming_conventions.md` | 2 | Backlog |

**Sprint Points:** 9

**Sprint 3 Total:** 13 points

---

## Sprint 4: Testing Infrastructure (P2)

**Goal:** Establish JavaScript testing to prevent regressions

### User Stories

#### ARCH-001-07: JavaScript Test Setup
**As a** developer
**I want** automated JavaScript tests
**So that** component behavior is verified and regressions are caught

**Tasks:**
| ID | Task | File | Story Points | Status |
|----|------|------|--------------|--------|
| 4.1 | Install and configure Vitest | `package.json`, `vitest.config.js` | 3 | Backlog |
| 4.2 | Create test utilities for DOM setup | `__tests__/setup.js` | 2 | Backlog |
| 4.3 | Add destroy() method tests | `__tests__/lifecycle.test.js` | 3 | Backlog |
| 4.4 | Add singleton pattern tests | `__tests__/singleton.test.js` | 2 | Backlog |
| 4.5 | Add HTMX integration tests | `__tests__/htmx.test.js` | 3 | Backlog |

**Sprint Points:** 13

**Sprint 4 Total:** 13 points

---

## Backlog Summary

| Sprint | Focus | Story Points | Status |
|--------|-------|--------------|--------|
| Sprint 1 | Critical Foundation (P0) | 29 | ✅ Completed |
| Sprint 2 | Security Hardening (P1) | 10/14 | ✅ Completed (4 deferred) |
| Sprint 3 | Standardization (P2) | 11 | 🔜 Ready |
| Sprint 4 | Testing Infrastructure (P2) | 13 | Backlog |
| **Total** | | **67** | **39 completed** |

*Notes:*
- *Sprint 3 reduced by 2 points (Task 3.1 completed early in Sprint 1)*
- *Sprint 2: 4 points deferred (modal.html tasks 2.1 and 2.8)*

## Definition of Done

- [ ] Code changes pass linting (`ruff check .`)
- [ ] Existing tests pass (`uv run pytest`)
- [ ] New JavaScript functionality has unit tests (Sprint 4+)
- [ ] Changes documented if affecting public API
- [ ] PR reviewed and approved
- [ ] No regressions in component behavior

## Dependencies

- Sprint 1 must complete before Sprint 2-4 (destroy methods needed for cleanup)
- Sprint 4 can run in parallel with Sprint 2-3 (test infrastructure is independent)

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Breaking existing component behavior | Medium | High | Thorough manual testing + add JS tests |
| HTMX integration complexity | Low | Medium | Test with real HTMX scenarios |
| Template changes affect dependent projects | Low | High | Document breaking changes in CHANGELOG |
