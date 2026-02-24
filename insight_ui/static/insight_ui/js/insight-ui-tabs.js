export class Tabs {
    // Weak references used to prevent multiple initialization of the same instance
    static instances = new WeakMap();

    constructor(element) {
        // If an instance for this element already exists, return it
        if (Tabs.instances.has(element)) {
            return Tabs.instances.get(element);
        }

        this.element = element;
        this.tabs = Array.from(element.children[0].children);
        this.tabContent = element.children[1];

        // Store bound handlers for cleanup
        this.boundTabHandlers = [];
        this.boundHTMXAfterSwap = null;

        this.bindEvents();

        this.element.__insightInstance = this;
        Tabs.instances.set(element, this);

        debugLog("New tab bar created: ", this.element);
    }

    bindEvents() {
        // Keyboard control
        this.tabs.forEach((tab, index) => {
            const keydownHandler = (e) => this.handleKeyDown(e, index);
            const clickHandler = () => this.activateTab(tab);
            tab.addEventListener('keydown', keydownHandler);
            tab.addEventListener('click', clickHandler);
            this.boundTabHandlers.push({ element: tab, keydownHandler, clickHandler });
        });

        // HTMX-Focus
        this.boundHTMXAfterSwap = (event) => {
            if (event.detail.target.id === 'tab-content') {
                this.tabContent.focus();
            }
        };
        document.body.addEventListener('htmx:afterSwap', this.boundHTMXAfterSwap);
    }

    handleKeyDown(e, index) {
        let newIndex = null;
        const length = this.tabs.length;

        switch (e.key) {
            case 'ArrowRight':
                newIndex = (index + 1) % length;
                break;
            case 'ArrowLeft':
                newIndex = (index - 1 + length) % length;
                break;
            case 'Home':
                newIndex = 0;
                break;
            case 'End':
                newIndex = length - 1;
                break;
        }

        if (newIndex !== null) {
            e.preventDefault();
            this.tabs[newIndex].focus();
        }
    }

    activateTab(selectedTab) {
        this.tabs.forEach(tab => {
            const isSelected = tab === selectedTab;
            tab.setAttribute('aria-selected', isSelected ? 'true' : 'false');

            if (isSelected) {
                tab.classList.remove('border-gray-300', 'text-primary', 'border-b');
                tab.classList.add('border-insight-primary', 'text-insight-primary', 'border-b-3');
                this.tabContent.setAttribute('aria-label', tab.id);
            } else {
                tab.classList.remove('border-insight-primary', 'text-insight-primary', 'border-b-3');
                tab.classList.add('border-gray-300', 'text-primary', 'border-b');
            }
        });
    }

    /**
     * Destroys the tabs instance and removes all event listeners.
     * Call this before removing the element from DOM.
     */
    destroy() {
        debugLog("Destroy tab bar: ", this.element);

        // Remove tab keydown and click handlers
        this.boundTabHandlers.forEach(({ element, keydownHandler, clickHandler }) => {
            element.removeEventListener('keydown', keydownHandler);
            element.removeEventListener('click', clickHandler);
        });
        this.boundTabHandlers = [];

        // Remove global HTMX handler
        if (this.boundHTMXAfterSwap) {
            document.body.removeEventListener('htmx:afterSwap', this.boundHTMXAfterSwap);
        }

        Tabs.instances.delete(this.element);
        delete this.element.__insightInstance;

        this.element = null;
        this.tabContent = null;
    }

    // Static method for initializing all tabs
    static initAll() {
        document.querySelectorAll("[data-tabs]").forEach(el => new Tabs(el));
    }
}
