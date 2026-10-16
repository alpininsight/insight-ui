// SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
// SPDX-License-Identifier: AGPL-3.0-only
/**
 * Tests for the BadgeList component: keyboard focus after removing badges.
 */

import { describe, it, expect, beforeEach } from 'vitest';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const jsDir = path.join(__dirname, '../../insight_ui/static/insight_ui/js');

function loadComponent(filename) {
  const filepath = path.join(jsDir, filename);
  const code = fs.readFileSync(filepath, 'utf-8');
  const transformed = code.replace(/export class\s+(\w+)/g, 'window.InsightUI.$1 = class $1');
  eval(transformed);
}

function badgeListHTML(labels, { clearAll = true } = {}) {
  const items = labels.map(label => `
    <li><div class="badge">${label}<button type="button" data-insight-badge-remove aria-label="Remove: ${label}">x</button></div></li>
  `).join('');
  const clearAllButton = clearAll && labels.length
    ? '<button type="button" data-insight-badge-clear-all>Remove all</button>'
    : '';
  return `
    <div id="active-filters" data-insight-badge-list>
      <ul role="list" aria-label="Active filters" tabindex="-1">${items}</ul>
      ${clearAllButton}
    </div>
  `;
}

/** Simulates HTMX replacing the list with the server response and settling. */
function swapList(container, labels, trigger) {
  container.innerHTML = badgeListHTML(labels);
  InsightUI.BadgeList.initAll();
  document.dispatchEvent(new CustomEvent('htmx:afterSettle', { detail: { requestConfig: { elt: trigger } } }));
}

function removeButtons() {
  return [...document.querySelectorAll('#active-filters [data-insight-badge-remove]')];
}

describe('BadgeList Component', () => {
  let container;

  beforeEach(() => {
    globalThis.InsightUI = {};
    globalThis.window.InsightUI = globalThis.InsightUI;
    loadComponent('insight-ui-badge-list.js');
    container = TestUtils.createDOM(badgeListHTML(['Country: Germany', 'Status: Open', 'Year: 2026']));
    InsightUI.BadgeList.initAll();
  });

  it('should move the focus to the next badge after a badge in the middle was removed', () => {
    const trigger = removeButtons()[1];
    trigger.click();

    swapList(container, ['Country: Germany', 'Year: 2026'], trigger);

    expect(document.activeElement).toBe(removeButtons()[1]);
    expect(document.activeElement.getAttribute('aria-label')).toBe('Remove: Year: 2026');
  });

  it('should move the focus to the previous badge after the last badge was removed', () => {
    const trigger = removeButtons()[2];
    trigger.click();

    swapList(container, ['Country: Germany', 'Status: Open'], trigger);

    expect(document.activeElement.getAttribute('aria-label')).toBe('Remove: Status: Open');
  });

  it('should move the focus to the empty list after the only badge was removed', () => {
    container.innerHTML = badgeListHTML(['Country: Germany']);
    InsightUI.BadgeList.initAll();
    const trigger = removeButtons()[0];
    trigger.click();

    swapList(container, [], trigger);

    expect(document.activeElement).toBe(document.querySelector('#active-filters ul'));
  });

  it('should move the focus to the list after all badges were removed at once', () => {
    const trigger = document.querySelector('[data-insight-badge-clear-all]');
    trigger.click();

    swapList(container, [], trigger);

    expect(document.activeElement).toBe(document.querySelector('#active-filters ul'));
  });

  it('should ignore swaps of other requests that settle before the remove request', () => {
    const trigger = removeButtons()[1];
    trigger.click();
    const unrelated = document.createElement('div');

    document.dispatchEvent(new CustomEvent('htmx:afterSettle', { detail: { requestConfig: { elt: unrelated } } }));
    expect(document.activeElement).toBe(document.body);

    swapList(container, ['Country: Germany', 'Year: 2026'], trigger);
    expect(document.activeElement.getAttribute('aria-label')).toBe('Remove: Year: 2026');
  });

  it('should not move the focus if the remove request failed', () => {
    const trigger = removeButtons()[1];
    trigger.click();

    document.dispatchEvent(new CustomEvent('htmx:afterRequest', { detail: { successful: false, requestConfig: { elt: trigger } } }));
    document.dispatchEvent(new CustomEvent('htmx:afterSettle', { detail: { requestConfig: { elt: trigger } } }));

    expect(document.activeElement).toBe(document.body);
  });
});
