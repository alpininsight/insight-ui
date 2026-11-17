// SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
// SPDX-License-Identifier: AGPL-3.0-only
/**
 * Tests for the QueryBuilder component: adding, removing and filling filter rows.
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

const FIELDS = [
  { field: 'title', label: 'Title', operations: { icontains: 'contains', iexact: 'is' }, choices: {}, input_type: 'text' },
  { field: 'pages', label: 'Pages', operations: { gte: 'at least' }, choices: {}, input_type: 'number' },
  { field: 'available', label: 'Available', operations: { exact: 'is' }, choices: { true: 'Yes', false: 'No' }, input_type: 'text' },
];

function rowHTML(index) {
  return `
    <fieldset data-insight-query-builder-row>
      <legend data-insight-query-builder-legend>Filter ${index + 1}</legend>
      <div aria-hidden="true" hidden data-insight-query-builder-divider>OR</div>
      <fieldset data-insight-query-builder-logic ${index === 0 ? 'class="invisible" disabled' : ''}>
        <label><input type="radio" name="filters-${index}-logic" value="AND" checked data-insight-query-builder-part="logic"> AND</label>
        <label><input type="radio" name="filters-${index}-logic" value="OR" data-insight-query-builder-part="logic"> OR</label>
      </fieldset>
      <label for="books-${index}-field" data-insight-query-builder-label="field">Field</label>
      <select id="books-${index}-field" name="filters-${index}-field" data-insight-query-builder-part="field">
        <option value="">Choose a field</option>
        ${FIELDS.map(field => `<option value="${field.field}">${field.label}</option>`).join('')}
      </select>
      <label for="books-${index}-operator" data-insight-query-builder-label="operator">Condition</label>
      <select id="books-${index}-operator" name="filters-${index}-operator" data-insight-query-builder-part="operator" disabled></select>
      <label for="books-${index}-value" data-insight-query-builder-label="value">Value</label>
      <input id="books-${index}-value" name="filters-${index}-value" class="input w-full" data-insight-query-builder-part="value" disabled>
      <button type="button" data-insight-query-builder-remove>Remove filter</button>
    </fieldset>
  `;
}

function builderHTML(rowCount = 1, maxFilters = 20) {
  return `
    <form id="books" data-insight-query-builder data-param-name="filters" data-max-filters="${maxFilters}">
      <script id="books-fields" type="application/json">${JSON.stringify(FIELDS)}</script>
      <p data-insight-query-builder-help hidden>AND binds tighter than OR</p>
      <div data-insight-query-builder-rows>${Array.from({ length: rowCount }, (_, index) => rowHTML(index)).join('')}</div>
      <template data-insight-query-builder-template>${rowHTML(0)}</template>
      <button type="button" data-insight-query-builder-add>Add filter</button>
      <p hidden data-insight-query-builder-limit>You can combine up to ${maxFilters} filters.</p>
      <p role="status" data-insight-query-builder-status></p>
    </form>
  `;
}

function rows() {
  return [...document.querySelectorAll('[data-insight-query-builder-rows] > [data-insight-query-builder-row]')];
}

function part(row, name) {
  return row.querySelector(`[data-insight-query-builder-part="${name}"]`);
}

function chooseField(row, value) {
  const select = part(row, 'field');
  select.value = value;
  select.dispatchEvent(new Event('change', { bubbles: true }));
}

describe('QueryBuilder', () => {
  beforeEach(() => {
    globalThis.interpolate = (text, values) => text.replace(/%\((\w+)\)s/g, (_, key) => values[key]);
    loadComponent('insight-ui-query-builder.js');
  });

  it('adds a numbered row and focuses its field select', () => {
    document.body.innerHTML = builderHTML(1);
    InsightUI.QueryBuilder.initAll();

    document.querySelector('[data-insight-query-builder-add]').click();

    const [, added] = rows();
    expect(part(added, 'field').name).toBe('filters-1-field');
    expect(part(added, 'field').id).toBe('books-1-field');
    expect(added.querySelector('[data-insight-query-builder-label="field"]').htmlFor).toBe('books-1-field');
    expect(added.querySelector('legend').textContent).toBe('Filter 2');
    expect(added.querySelector('[data-insight-query-builder-logic]').classList.contains('invisible')).toBe(false);
    expect(added.querySelector('[data-insight-query-builder-logic]').disabled).toBe(false);
    expect(document.activeElement).toBe(part(added, 'field'));
    expect(document.querySelector('[role="status"]').textContent).toBe('Filter added');
  });

  it('renumbers the rows after a removal and moves the focus to the next row', () => {
    document.body.innerHTML = builderHTML(3);
    InsightUI.QueryBuilder.initAll();

    rows()[0].querySelector('[data-insight-query-builder-remove]').click();

    const remaining = rows();
    expect(remaining).toHaveLength(2);
    expect(part(remaining[0], 'field').name).toBe('filters-0-field');
    expect(part(remaining[1], 'field').name).toBe('filters-1-field');
    expect(remaining[0].querySelector('[data-insight-query-builder-logic]').disabled).toBe(true);
    expect(remaining[0].querySelector('[data-insight-query-builder-logic]').classList.contains('invisible')).toBe(true);
    expect(document.activeElement).toBe(part(remaining[0], 'field'));
    expect(remaining[0].querySelector('[data-insight-query-builder-label="field"]').classList.contains('md:sr-only')).toBe(false);
    expect(remaining[1].querySelector('[data-insight-query-builder-label="field"]').classList.contains('md:sr-only')).toBe(true);
    expect(document.querySelector('[role="status"]').textContent).toBe('Filter removed');
  });

  it('focuses the add button when the last row is removed', () => {
    document.body.innerHTML = builderHTML(1);
    InsightUI.QueryBuilder.initAll();

    rows()[0].querySelector('[data-insight-query-builder-remove]').click();

    expect(rows()).toHaveLength(0);
    expect(document.activeElement).toBe(document.querySelector('[data-insight-query-builder-add]'));
  });

  it('fills the conditions of the chosen field', () => {
    document.body.innerHTML = builderHTML(1);
    InsightUI.QueryBuilder.initAll();
    const [row] = rows();

    chooseField(row, 'title');

    const operator = part(row, 'operator');
    expect(operator.disabled).toBe(false);
    expect([...operator.options].map(option => [option.value, option.text])).toEqual([
      ['icontains', 'contains'],
      ['iexact', 'is'],
    ]);
    expect(part(row, 'value').disabled).toBe(false);
  });

  it('replaces the value control to match the field type', () => {
    document.body.innerHTML = builderHTML(1);
    InsightUI.QueryBuilder.initAll();
    const [row] = rows();

    chooseField(row, 'pages');
    expect(part(row, 'value').type).toBe('number');
    expect(part(row, 'value').name).toBe('filters-0-value');
    expect(part(row, 'value').id).toBe('books-0-value');
    expect(part(row, 'value').className).toBe('input w-full');
    expect(part(row, 'value').required).toBe(true);

    chooseField(row, 'available');
    const value = part(row, 'value');
    expect(value.tagName).toBe('SELECT');
    expect([...value.options].map(option => option.text)).toEqual(['Yes', 'No']);
  });

  it('disables condition and value again when no field is chosen', () => {
    document.body.innerHTML = builderHTML(1);
    InsightUI.QueryBuilder.initAll();
    const [row] = rows();

    chooseField(row, 'title');
    chooseField(row, '');

    expect(part(row, 'operator').disabled).toBe(true);
    expect(part(row, 'operator').value).toBe('');
    expect(part(row, 'value').disabled).toBe(true);
  });

  it('initializes once and removes its listeners on destroy', () => {
    document.body.innerHTML = builderHTML(1);
    const form = document.getElementById('books');
    const builder = new InsightUI.QueryBuilder(form);

    expect(new InsightUI.QueryBuilder(form)).toBe(builder);

    builder.destroy();
    document.querySelector('[data-insight-query-builder-add]').click();

    expect(rows()).toHaveLength(1);
    expect(form.__insightInstance).toBeUndefined();
  });
  it('shows the precedence hint from two filters on', () => {
    document.body.innerHTML = builderHTML(1);
    InsightUI.QueryBuilder.initAll();
    const help = document.querySelector('[data-insight-query-builder-help]');

    expect(help.hidden).toBe(true);
    document.querySelector('[data-insight-query-builder-add]').click();
    expect(help.hidden).toBe(false);
  });

  it('stops adding rows at max filters and allows it again after a removal', () => {
    document.body.innerHTML = builderHTML(1, 2);
    InsightUI.QueryBuilder.initAll();
    const add = document.querySelector('[data-insight-query-builder-add]');
    const hint = document.querySelector('[data-insight-query-builder-limit]');

    add.click();
    expect(rows()).toHaveLength(2);
    expect(add.disabled).toBe(true);
    expect(hint.hidden).toBe(false);

    rows()[1].querySelector('[data-insight-query-builder-remove]').click();
    expect(add.disabled).toBe(false);
    expect(hint.hidden).toBe(true);
  });

  it('shows the OR divider when a row is combined with OR', () => {
    document.body.innerHTML = builderHTML(2);
    InsightUI.QueryBuilder.initAll();
    const [first, second] = rows();
    const or = second.querySelector('input[value="OR"]');

    or.checked = true;
    or.dispatchEvent(new Event('change', { bubbles: true }));
    expect(second.querySelector('[data-insight-query-builder-divider]').hidden).toBe(false);

    first.querySelector('[data-insight-query-builder-remove]').click();
    expect(rows()[0].querySelector('[data-insight-query-builder-divider]').hidden).toBe(true);
  });

  it('asks for a field first when the field is cleared', () => {
    document.body.innerHTML = builderHTML(1);
    InsightUI.QueryBuilder.initAll();
    const [row] = rows();

    chooseField(row, 'title');
    expect(part(row, 'value').placeholder).toBe('');
    chooseField(row, '');

    expect([...part(row, 'operator').options].map(option => option.text)).toEqual(['Choose a field first']);
    expect(part(row, 'value').placeholder).toBe('Choose a field first');
  });
});
