export class Tabs {
    // Manages all Tab instances of the DOM
    static instances = new WeakMap();

    constructor(tabBar) {
        // If an instance for this element already exists, return it
        if (Tabs.instances.has(tabBar)) {
            return Tabs.instances.get(tabBar);
        }

        this.tabBar = tabBar;
        this.tabs = Array.from(tabBar.children[0].children);
        this.tabContent = tabBar.children[1];

        this.bindEvents();
        Tabs.instances.set(tabBar, this);

        debugLog("New tab bar created: ", this.tabBar);
    }

    bindEvents() {
        // Keyboard control
        this.tabs.forEach((tab, index) => {
            tab.addEventListener('keydown', e => this.handleKeyDown(e, index));
            tab.addEventListener('click', () => this.activateTab(tab));
        });

        // HTMX-Focus
        document.body.addEventListener('htmx:afterSwap', event => {
            if (event.detail.target.id === 'tab-content') {
                this.tabContent.focus();
            }
        });
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

    // Static method for initializing all tabs
    static initAll() {
        document.querySelectorAll("[data-tabs]").forEach(tabBar => new Tabs(tabBar));
    }
}
