// SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
// SPDX-License-Identifier: AGPL-3.0-only
/**
 * Tests for shared navigation state management.
 */

import { beforeAll, describe, expect, it } from 'vitest';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const stateScript = path.join(
  __dirname,
  '../../insight_ui/static/insight_ui/js/insight-ui-state.js'
);

beforeAll(() => {
  eval(fs.readFileSync(stateScript, 'utf-8'));
});

function renderNavigation() {
  return TestUtils.createDOM(`
    <nav data-insight-nav>
      <a href="/docs/">Documentation</a>
      <a href="/#capabilities">Capabilities</a>
      <a href="/#architecture">Architecture</a>
      <a href="https://example.com/">External</a>
    </nav>
  `);
}

function updateNavigation() {
  document.dispatchEvent(new Event('DOMContentLoaded'));
}

describe('Navigation state', () => {
  it('marks only the matching fragment as the current location', () => {
    window.history.replaceState({}, '', '/#architecture');
    const navigation = renderNavigation();

    updateNavigation();

    expect(
      navigation.querySelector('a[href="/#architecture"]').getAttribute('aria-current')
    ).toBe('location');
    expect(
      navigation.querySelector('a[href="/#capabilities"]').getAttribute('aria-current')
    ).toBeNull();
  });

  it('keeps path matches as the current page', () => {
    window.history.replaceState({}, '', '/docs/integration/');
    const navigation = renderNavigation();

    updateNavigation();

    expect(navigation.querySelector('a[href="/docs/"]').getAttribute('aria-current')).toBe(
      'page'
    );
  });

  it('does not mark an external link with the same path as active', () => {
    window.history.replaceState({}, '', '/');
    const navigation = renderNavigation();

    updateNavigation();

    expect(
      navigation
        .querySelector('a[href="https://example.com/"]')
        .getAttribute('aria-current')
    ).toBeNull();
  });

  it('updates fragment navigation without a page reload', () => {
    window.history.replaceState({}, '', '/#capabilities');
    const navigation = renderNavigation();
    updateNavigation();

    window.history.replaceState({}, '', '/#architecture');
    window.dispatchEvent(new HashChangeEvent('hashchange'));

    expect(
      navigation.querySelector('a[href="/#capabilities"]').getAttribute('aria-current')
    ).toBeNull();
    expect(
      navigation.querySelector('a[href="/#architecture"]').getAttribute('aria-current')
    ).toBe('location');
  });
});
