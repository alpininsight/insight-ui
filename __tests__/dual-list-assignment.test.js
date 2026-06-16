/**
 * Tests for DualListAssignment component functionality
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const jsDir = path.join(__dirname, '../insight_ui/static/insight_ui/js');

function loadComponent(filename) {
  const filepath = path.join(jsDir, filename);
  const code = fs.readFileSync(filepath, 'utf-8');
  const transformed = code.replace(/export class\s+(\w+)/g, 'window.InsightUI.$1 = class $1');
  eval(transformed);
}

function createDualListDOM() {
  return TestUtils.createDOM(`
    <div data-insight-dual-list-assignment data-name="role_slugs">
      <input data-insight-dual-list-filter="available" type="search">
      <select data-insight-dual-list-available multiple>
        <option value="organization-member" data-index="0">Organization Member</option>
        <option value="organization-admin" data-index="2">Organization Admin</option>
      </select>
      <button type="button" data-insight-dual-list-add></button>
      <button type="button" data-insight-dual-list-remove></button>
      <input data-insight-dual-list-filter="assigned" type="search">
      <select data-insight-dual-list-assigned multiple>
        <option value="organization-developer" data-index="1">Organization Developer</option>
      </select>
      <span data-insight-dual-list-available-count></span>
      <span data-insight-dual-list-assigned-count></span>
      <div data-insight-dual-list-hidden></div>
      <p data-insight-dual-list-status></p>
    </div>
  `);
}

describe('DualListAssignment Component', () => {
  beforeEach(() => {
    globalThis.InsightUI = {};
    globalThis.window.InsightUI = globalThis.InsightUI;
    loadComponent('insight-ui-dual-list-assignment.js');
  });

  it('creates hidden inputs for initially assigned options', () => {
    const container = createDualListDOM();
    const element = container.querySelector('[data-insight-dual-list-assignment]');

    new InsightUI.DualListAssignment(element);

    const hiddenInput = element.querySelector('input[type="hidden"]');
    expect(hiddenInput).not.toBeNull();
    expect(hiddenInput.name).toBe('role_slugs');
    expect(hiddenInput.value).toBe('organization-developer');
  });

  it('moves selected options into assigned and dispatches the assigned values', () => {
    const container = createDualListDOM();
    const element = container.querySelector('[data-insight-dual-list-assignment]');
    const available = element.querySelector('[data-insight-dual-list-available]');
    const assigned = element.querySelector('[data-insight-dual-list-assigned]');
    const changeHandler = vi.fn();

    new InsightUI.DualListAssignment(element);
    element.addEventListener('change', changeHandler);

    available.options[0].selected = true;
    available.dispatchEvent(new Event('change', { bubbles: true }));
    changeHandler.mockClear();
    element.querySelector('[data-insight-dual-list-add]').click();

    expect(Array.from(assigned.options).map(option => option.value)).toEqual([
      'organization-member',
      'organization-developer',
    ]);
    expect(changeHandler).toHaveBeenCalledOnce();
    expect(changeHandler.mock.calls[0][0].detail.value).toEqual([
      'organization-member',
      'organization-developer',
    ]);
  });

  it('filters options without changing submitted assigned values', () => {
    const container = createDualListDOM();
    const element = container.querySelector('[data-insight-dual-list-assignment]');
    const assigned = element.querySelector('[data-insight-dual-list-assigned]');
    const assignedFilter = element.querySelector('[data-insight-dual-list-filter="assigned"]');

    new InsightUI.DualListAssignment(element);

    assignedFilter.value = 'missing';
    assignedFilter.dispatchEvent(new Event('input', { bubbles: true }));

    expect(assigned.options[0].hidden).toBe(true);
    expect(element.querySelector('input[type="hidden"]').value).toBe('organization-developer');
  });
});
