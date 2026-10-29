// SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
// SPDX-License-Identifier: AGPL-3.0-only
import { afterEach, beforeEach, expect, it, vi } from 'vitest';
import { Search } from '../../insight_ui/static/insight_ui/js/insight-ui-search.js';

const searches = [];

beforeEach(() => {
    // Supply deterministic results without fetching the index or Fuse.js.
    vi.spyOn(Search.prototype, 'init').mockResolvedValue();
});

afterEach(() => {
    searches.splice(0).forEach(search => search.destroy());
    vi.restoreAllMocks();
});

function createSearch(id) {
    const element = document.createElement('div');
    element.innerHTML = '<input type="search" aria-expanded="false">' +
        '<div data-search-results role="listbox" class="hidden"></div>' +
        '<template data-search-template="result"><div role="option">' +
        '<a><span data-slot="icon"></span><span data-slot="name"></span>' +
        '<span data-slot="category"></span><span data-slot="description"></span></a>' +
        '</div></template>';
    element.querySelector('input').id = id;
    document.body.appendChild(element);
    const search = new Search(element);
    search.bindEvents();
    searches.push(search);
    return search;
}

it('keeps option IDs and keyboard active descendants local to each search bar', () => {
    const first = createSearch('docs-search');
    const second = createSearch('catalog-search');
    const results = ['Button', 'Card'].map(name => ({
        item: { name, url: '/components/', category: 'component', group: 'UI', description: '' },
    }));
    first.renderResults(results);
    second.renderResults(results);
    const options = [...document.querySelectorAll('[role="option"]')];
    options.forEach(option => { option.scrollIntoView = vi.fn(); });
    expect(new Set(options.map(option => option.id)).size).toBe(4);

    second.input.dispatchEvent(new KeyboardEvent('keydown', { key: 'ArrowDown', bubbles: true }));
    const active = document.getElementById(second.input.getAttribute('aria-activedescendant'));
    expect(active).toBe(second.resultsContainer.querySelector('[role="option"]'));
    expect(active.getAttribute('aria-selected')).toBe('true');
    expect(first.input.hasAttribute('aria-activedescendant')).toBe(false);
});
