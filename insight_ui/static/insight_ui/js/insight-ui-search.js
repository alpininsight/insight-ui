/**
 * Insight UI - Documentation Search
 *
 * Client-side fuzzy search using Fuse.js for searching components,
 * types, and categories in the documentation.
 */

export class Search {
    // Weak references used to prevent multiple initialization of the same instance
    static instances = new WeakMap();

    // Currently open search dropdown (only one can be open)
    static currentOpen = null;

    constructor(element) {
        // If an instance for this element already exists, return it
        if (Search.instances.has(element)) {
            debugLog("Search element already instantiated: ", element);
            return Search.instances.get(element);
        }

        this.element = element;
        this.input = element.querySelector('input[type="search"]');
        this.resultsContainer = element.querySelector('[data-search-results]');
        this.fuse = null;
        this.focusedIndex = -1;
        this.isOpen = false;
        this.searchIndex = [];

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

    bindEvents() {
        this.input.addEventListener('input', this.boundHandleInput);
        this.input.addEventListener('keydown', this.boundHandleKeydown);
        this.input.addEventListener('focus', this.boundHandleFocus);
        document.addEventListener('keydown', this.boundHandleGlobalKeydown);
        document.addEventListener('click', this.boundHandleDocumentClick);
    }

    handleInput() {
        const query = this.input.value.trim();
        this.search(query);
    }

    handleFocus() {
        const query = this.input.value.trim();
        if (query.length >= 2 && this.fuse) {
            this.search(query);
        }
    }

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

    handleGlobalKeydown(e) {
        // Ctrl+K or Cmd+K to focus search
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            this.input.focus();
            this.input.select();
        }
    }

    handleDocumentClick(e) {
        if (!this.element.contains(e.target)) {
            this.close();
        }
    }

    search(query) {
        if (!this.fuse) return;

        if (query.length < 2) {
            this.close();
            return;
        }

        const results = this.fuse.search(query, { limit: 8 });
        this.renderResults(results);
    }

    renderResults(results) {
        if (results.length === 0) {
            this.resultsContainer.innerHTML = this.renderNoResults();
            this.open();
            return;
        }

        const html = results.map((result, index) => this.renderResultItem(result.item, index)).join('');
        this.resultsContainer.innerHTML = html;
        this.focusedIndex = -1;
        this.open();
    }

    renderResultItem(item, index) {
        const categoryIcon = this.getCategoryIcon(item.category);
        const categoryLabel = this.getCategoryLabel(item.category);

        return `
            <div role="option" id="search-result-${index}" class="search-result-item"
                 aria-selected="false" data-index="${index}">
                <a href="${item.url}"
                   class="flex items-start gap-3 px-4 py-3 hover:bg-gray-100 dark:hover:bg-gray-700
                          focus:bg-gray-100 dark:focus:bg-gray-700 focus:outline-none transition-colors">
                    <span class="flex-shrink-0 w-5 h-5 mt-0.5 text-gray-400 dark:text-gray-500">
                        ${categoryIcon}
                    </span>
                    <div class="flex-1 min-w-0">
                        <div class="flex items-center gap-2">
                            <span class="font-medium text-gray-900 dark:text-white truncate">
                                ${this.escapeHtml(item.name)}
                            </span>
                            <span class="flex-shrink-0 text-xs px-1.5 py-0.5 rounded
                                         bg-gray-100 dark:bg-gray-700
                                         text-gray-500 dark:text-gray-400">
                                ${categoryLabel}
                            </span>
                        </div>
                        <div class="text-sm text-gray-500 dark:text-gray-400 truncate">
                            ${item.group}${item.description ? ' · ' + this.escapeHtml(item.description) : ''}
                        </div>
                    </div>
                </a>
            </div>
        `;
    }

    renderNoResults() {
        return `
            <div class="px-4 py-6 text-center text-gray-500 dark:text-gray-400">
                <p class="text-sm">No results found</p>
                <p class="text-xs mt-1">Try a different search term</p>
            </div>
        `;
    }

    getCategoryIcon(category) {
        const icons = {
            component: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="size-5">
                <path d="M14.5 10a4.5 4.5 0 0 0-4.284-4.493v-1.49A6.001 6.001 0 0 1 16 10h-1.5Zm-4.284 4.493a4.5 4.5 0 0 0 4.284-4.493H16a6.001 6.001 0 0 1-5.784 5.983v-1.49ZM5.5 10a4.5 4.5 0 0 0 4.284 4.493v1.49A6.001 6.001 0 0 1 4 10h1.5Zm4.284-4.493A4.5 4.5 0 0 0 5.5 10H4a6.001 6.001 0 0 1 5.784-5.983v1.49Z"/>
            </svg>`,
            type: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="size-5">
                <path fill-rule="evenodd" d="M6.28 5.22a.75.75 0 0 1 0 1.06L2.56 10l3.72 3.72a.75.75 0 0 1-1.06 1.06L.97 10.53a.75.75 0 0 1 0-1.06l4.25-4.25a.75.75 0 0 1 1.06 0Zm7.44 0a.75.75 0 0 1 1.06 0l4.25 4.25a.75.75 0 0 1 0 1.06l-4.25 4.25a.75.75 0 0 1-1.06-1.06L17.44 10l-3.72-3.72a.75.75 0 0 1 0-1.06ZM11.377 2.011a.75.75 0 0 1 .612.867l-2.5 14.5a.75.75 0 0 1-1.478-.255l2.5-14.5a.75.75 0 0 1 .866-.612Z" clip-rule="evenodd"/>
            </svg>`,
            category: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="size-5">
                <path fill-rule="evenodd" d="M2 4.75A.75.75 0 0 1 2.75 4h14.5a.75.75 0 0 1 0 1.5H2.75A.75.75 0 0 1 2 4.75Zm7 10.5a.75.75 0 0 1 .75-.75h7.5a.75.75 0 0 1 0 1.5h-7.5a.75.75 0 0 1-.75-.75ZM2 10a.75.75 0 0 1 .75-.75h14.5a.75.75 0 0 1 0 1.5H2.75A.75.75 0 0 1 2 10Z" clip-rule="evenodd"/>
            </svg>`
        };
        return icons[category] || icons.component;
    }

    getCategoryLabel(category) {
        const labels = {
            component: 'Component',
            type: 'Type',
            category: 'Category'
        };
        return labels[category] || category;
    }

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

    open() {
        if (Search.currentOpen && Search.currentOpen !== this) {
            Search.currentOpen.close();
        }

        this.resultsContainer.classList.remove('hidden');
        this.input.setAttribute('aria-expanded', 'true');
        this.isOpen = true;
        Search.currentOpen = this;
    }

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

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

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
        this.fuse = null;
    }

    // Static method for initializing all search instances
    static initAll() {
        document.querySelectorAll("[data-insight-search]").forEach(el => new Search(el));
    }
}
