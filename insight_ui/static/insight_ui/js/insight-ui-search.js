// SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
// SPDX-License-Identifier: AGPL-3.0-only
/**
 * Insight UI - Documentation Search
 *
 * Client-side fuzzy search using Fuse.js for searching components,
 * types, and categories in the documentation.
 */

export class Search {
    /** @type {WeakMap<HTMLElement, Search>} Weak references to prevent multiple initialization */
    static instances = new WeakMap();

    /** @type {Search|null} Currently open search dropdown instance */
    static currentOpen = null;

    /**
     * Creates a new Search instance.
     *
     * @param {HTMLElement} element - The search container element with data-insight-search attribute
     */
    constructor(element) {
        // If an instance for this element already exists, return it
        if (Search.instances.has(element)) {
            debugLog("Search element already instantiated: ", element);
            return Search.instances.get(element);
        }

        this.element = element;
        this.input = element.querySelector('input[type="search"]');
        this.resultsContainer = element.querySelector('[data-search-results]');
        this.resultTemplate = element.querySelector('[data-search-template="result"]');
        this.noResultsTemplate = element.querySelector('[data-search-template="no-results"]');
        this.iconContainer = element.querySelector('[data-search-icons]');
        this.fuse = null;
        this.focusedIndex = -1;
        this.isOpen = false;
        this.searchIndex = [];
        this.categoryLabels = this.loadCategoryLabels();

        if (!this.input || !this.resultsContainer) {
            debugLog("Search: Missing required elements (input or results container)");
            return;
        }

        // Bind handlers for proper cleanup
        this.boundHandleInput = this.debounce(this.handleInput.bind(this), 150);
        this.boundHandleKeydown = this.handleKeydown.bind(this);
        this.boundHandleGlobalKeydown = this.handleGlobalKeydown.bind(this);
        this.boundHandleDocumentClick = this.handleDocumentClick.bind(this);
        this.boundHandleFocus = this.handleFocus.bind(this);

        this.init();

        this.element.__insightInstance = this;
        Search.instances.set(element, this);

        debugLog("New search created: ", this.element);
    }

    /**
     * Initializes the search by loading the index and setting up Fuse.js.
     *
     * @async
     */
    async init() {
        try {
            // Load search index for current locale
            const locale = document.documentElement.lang || 'en';
            const indexUrl = this.element.dataset.searchIndex ||
                `/static/insight_ui/data/search-index-${locale}.json`;
            const response = await fetch(indexUrl);
            if (!response.ok) {
                debugLog("Search: Failed to load search index");
                return;
            }
            this.searchIndex = await response.json();

            // Dynamically import Fuse.js
            const Fuse = (await import('https://cdn.jsdelivr.net/npm/fuse.js@7.1.0/dist/fuse.mjs')).default;

            this.fuse = new Fuse(this.searchIndex, {
                keys: [
                    { name: 'name', weight: 2 },
                    { name: 'description', weight: 1 },
                    { name: 'keywords', weight: 0.5 },
                    { name: 'group', weight: 0.3 }
                ],
                threshold: 0.3,
                includeScore: true,
                minMatchCharLength: 2
            });

            this.bindEvents();
            debugLog("Search initialized with", this.searchIndex.length, "entries");
        } catch (error) {
            debugLog("Search initialization error:", error);
        }
    }

    /**
     * Binds event listeners for input, keyboard navigation, and outside clicks.
     */
    bindEvents() {
        this.input.addEventListener('input', this.boundHandleInput);
        this.input.addEventListener('keydown', this.boundHandleKeydown);
        this.input.addEventListener('focus', this.boundHandleFocus);
        document.addEventListener('keydown', this.boundHandleGlobalKeydown);
        document.addEventListener('click', this.boundHandleDocumentClick);
    }

    /**
     * Handles input changes and triggers search.
     */
    handleInput() {
        const query = this.input.value.trim();
        this.search(query);
    }

    /**
     * Handles focus on the search input.
     */
    handleFocus() {
        const query = this.input.value.trim();
        if (query.length >= 2 && this.fuse) {
            this.search(query);
        }
    }

    /**
     * Handles keyboard navigation within search results.
     *
     * @param {KeyboardEvent} e - The keydown event
     */
    handleKeydown(e) {
        if (!this.isOpen) return;

        const items = this.resultsContainer.querySelectorAll('[role="option"]');

        switch (e.key) {
            case 'ArrowDown':
                e.preventDefault();
                this.focusedIndex = Math.min(this.focusedIndex + 1, items.length - 1);
                this.highlightItem(items);
                break;

            case 'ArrowUp':
                e.preventDefault();
                this.focusedIndex = Math.max(this.focusedIndex - 1, -1);
                this.highlightItem(items);
                break;

            case 'Enter':
                e.preventDefault();
                if (this.focusedIndex >= 0 && items[this.focusedIndex]) {
                    const link = items[this.focusedIndex].querySelector('a');
                    if (link) {
                        link.click();
                    }
                }
                break;

            case 'Escape':
                e.preventDefault();
                this.close();
                break;
        }
    }

    /**
     * Handles global keyboard shortcuts (Ctrl+K or Cmd+K to focus search).
     *
     * @param {KeyboardEvent} e - The keydown event
     */
    handleGlobalKeydown(e) {
        // Ctrl+K or Cmd+K to focus search
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            this.input.focus();
            this.input.select();
        }
    }

    /**
     * Handles clicks outside the search to close results.
     *
     * @param {MouseEvent} e - The click event
     */
    handleDocumentClick(e) {
        if (!this.element.contains(e.target)) {
            this.close();
        }
    }

    /**
     * Performs a fuzzy search with the given query.
     *
     * @param {string} query - The search query
     */
    search(query) {
        if (!this.fuse) return;

        if (query.length < 2) {
            this.close();
            return;
        }

        const results = this.fuse.search(query, { limit: 8 });
        this.renderResults(results);
    }

    /**
     * Renders search results to the results container.
     *
     * @param {Array} results - Fuse.js search results
     */
    renderResults(results) {
        this.resultsContainer.innerHTML = '';

        if (results.length === 0) {
            this.resultsContainer.appendChild(this.renderNoResults());
            this.open();
            return;
        }

        const fragment = document.createDocumentFragment();
        results.forEach((result, index) => {
            fragment.appendChild(this.renderResultItem(result.item, index));
        });
        this.resultsContainer.appendChild(fragment);
        this.focusedIndex = -1;
        this.open();
    }

    /**
     * Renders a single search result item.
     *
     * @param {Object} item - The search result item
     * @param {number} index - The item index
     * @returns {HTMLElement} The rendered result element
     */
    renderResultItem(item, index) {
        if (!this.resultTemplate) {
            debugLog("Search: Missing result template");
            return document.createElement('div');
        }

        const clone = this.resultTemplate.content.cloneNode(true);
        const el = clone.querySelector('[role="option"]');

        el.id = `search-result-${index}`;
        el.dataset.index = index;

        const link = el.querySelector('a');
        link.href = item.url;

        el.querySelector('[data-slot="name"]').textContent = item.name;
        el.querySelector('[data-slot="category"]').textContent = this.getCategoryLabel(item.category);
        el.querySelector('[data-slot="description"]').textContent =
            item.group + (item.description ? ' · ' + item.description : '');

        // Clone and insert category icon
        const iconSlot = el.querySelector('[data-slot="icon"]');
        const icon = this.getCategoryIcon(item.category);
        if (icon) {
            iconSlot.appendChild(icon);
        }

        return el;
    }

    /**
     * Renders the "no results" message.
     *
     * @returns {DocumentFragment|HTMLElement} The no results element
     */
    renderNoResults() {
        if (!this.noResultsTemplate) {
            debugLog("Search: Missing no-results template");
            const div = document.createElement('div');
            div.textContent = 'No results found';
            return div;
        }
        return this.noResultsTemplate.content.cloneNode(true);
    }

    /**
     * Gets the icon element for a category.
     *
     * @param {string} category - The category name
     * @returns {HTMLElement|null} The cloned icon element or null
     */
    getCategoryIcon(category) {
        if (!this.iconContainer) return null;
        const iconEl = this.iconContainer.querySelector(`[data-icon="${category}"]`);
        if (!iconEl) {
            // Fallback to component icon
            const fallback = this.iconContainer.querySelector('[data-icon="component"]');
            return fallback ? fallback.cloneNode(true).firstElementChild : null;
        }
        return iconEl.cloneNode(true).firstElementChild;
    }

    /**
     * Gets the localized label for a category.
     *
     * @param {string} category - The category name
     * @returns {string} The localized label
     */
    getCategoryLabel(category) {
        return this.categoryLabels[category] || category;
    }

    /**
     * Loads category labels from the embedded JSON script element.
     *
     * @returns {Object} Map of category names to localized labels
     */
    loadCategoryLabels() {
        const script = this.element.querySelector('[data-search-labels]');
        if (!script) {
            return { component: 'Component', type: 'Type', category: 'Category' };
        }
        try {
            return JSON.parse(script.textContent);
        } catch (e) {
            debugLog("Search: Failed to parse category labels", e);
            return { component: 'Component', type: 'Type', category: 'Category' };
        }
    }

    /**
     * Highlights the focused search result item.
     *
     * @param {NodeList} items - List of result item elements
     */
    highlightItem(items) {
        items.forEach((item, index) => {
            const isHighlighted = index === this.focusedIndex;
            item.setAttribute('aria-selected', isHighlighted.toString());

            if (isHighlighted) {
                item.classList.add('bg-gray-100', 'dark:bg-gray-700');
                item.scrollIntoView({ block: 'nearest' });
            } else {
                item.classList.remove('bg-gray-100', 'dark:bg-gray-700');
            }
        });

        // Update aria-activedescendant on input
        if (this.focusedIndex >= 0 && items[this.focusedIndex]) {
            this.input.setAttribute('aria-activedescendant', `search-result-${this.focusedIndex}`);
        } else {
            this.input.removeAttribute('aria-activedescendant');
        }
    }

    /**
     * Opens the search results dropdown.
     */
    open() {
        if (Search.currentOpen && Search.currentOpen !== this) {
            Search.currentOpen.close();
        }

        this.resultsContainer.classList.remove('hidden');
        this.input.setAttribute('aria-expanded', 'true');
        this.isOpen = true;
        Search.currentOpen = this;
    }

    /**
     * Closes the search results dropdown.
     */
    close() {
        this.resultsContainer.classList.add('hidden');
        this.input.setAttribute('aria-expanded', 'false');
        this.input.removeAttribute('aria-activedescendant');
        this.isOpen = false;
        this.focusedIndex = -1;

        if (Search.currentOpen === this) {
            Search.currentOpen = null;
        }
    }

    /**
     * Creates a debounced version of a function.
     *
     * @param {Function} func - The function to debounce
     * @param {number} wait - The debounce delay in milliseconds
     * @returns {Function} The debounced function
     */
    debounce(func, wait) {
        let timeout;
        return (...args) => {
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(this, args), wait);
        };
    }

    /**
     * Destroys the search instance and removes all event listeners.
     * Call this before removing the element from DOM.
     */
    destroy() {
        debugLog("Destroy search: ", this.element);

        this.input.removeEventListener('input', this.boundHandleInput);
        this.input.removeEventListener('keydown', this.boundHandleKeydown);
        this.input.removeEventListener('focus', this.boundHandleFocus);
        document.removeEventListener('keydown', this.boundHandleGlobalKeydown);
        document.removeEventListener('click', this.boundHandleDocumentClick);

        if (Search.currentOpen === this) {
            Search.currentOpen = null;
        }

        Search.instances.delete(this.element);
        delete this.element.__insightInstance;

        this.element = null;
        this.input = null;
        this.resultsContainer = null;
        this.resultTemplate = null;
        this.noResultsTemplate = null;
        this.iconContainer = null;
        this.fuse = null;
        this.categoryLabels = null;
    }

    /**
     * Initializes all search instances on the page.
     *
     * @static
     */
    static initAll() {
        document.querySelectorAll("[data-insight-search]").forEach(el => new Search(el));
    }
}
