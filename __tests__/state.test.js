/**
 * Tests for shared navigation state handling.
 */

import { beforeEach, describe, expect, it } from 'vitest';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const jsDir = path.join(__dirname, '../insight_ui/static/insight_ui/js');

function loadStateScript() {
  const filepath = path.join(jsDir, 'insight-ui-state.js');
  const code = fs.readFileSync(filepath, 'utf-8');
  eval(code);
}

describe('Insight UI state script', () => {
  beforeEach(() => {
    TestUtils.cleanup();
    window.history.pushState({}, '', '/docs/components/tabs/');
  });

  it('keeps side navigation active classes theme-aware', () => {
    const container = TestUtils.createDOM(`
      <li data-insight-side-nav>
        <a href="/docs/components/tabs/">Tabs</a>
      </li>
      <li data-insight-side-nav>
        <a href="/docs/components/button/">Button</a>
      </li>
    `);

    loadStateScript();
    document.dispatchEvent(new Event('DOMContentLoaded'));

    const activeLink = container.querySelector('a[href="/docs/components/tabs/"]');
    const inactiveLink = container.querySelector('a[href="/docs/components/button/"]');

    expect(activeLink.classList.contains('insight-surface-soft')).toBe(true);
    expect(activeLink.classList.contains('bg-gray-100')).toBe(false);
    expect(activeLink.classList.contains('dark:bg-gray-700')).toBe(false);

    expect(inactiveLink.classList.contains('insight-border-surface')).toBe(true);
    expect(inactiveLink.classList.contains('border-gray-200')).toBe(false);
    expect(inactiveLink.classList.contains('dark:border-gray-700')).toBe(false);
  });
});
