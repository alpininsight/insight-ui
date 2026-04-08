/**
 * Insight UI Theme Toggle.
 * Setzt sowohl .dark (für Tailwind) als auch [data-theme] (für Insight UI CSS)
 */
export class ThemeToggle {
    // Weak references used to prevent multiple initialization of the same instance
    static instances = new WeakMap();

    constructor(trigger) {
        // If an instance for this element already exists, return it
        if (ThemeToggle.instances.has(trigger)) {
            return ThemeToggle.instances.get(trigger);
        }

        this.trigger = trigger;
        this.themeKey = 'insight-ui-theme';
        this.root = document.documentElement;

        // Bind handlers for proper cleanup
        this.clickHandler = () => {
            const currentTheme = this.root.classList.contains('dark') ? 'dark' : 'light';
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            this.setTheme(newTheme);
        };

        this.init();

        this.trigger.__insightInstance = this;
        ThemeToggle.instances.set(trigger, this);

        debugLog("New theme toggle created: ", this.trigger);
    }

    init() {
        this.trigger.addEventListener("click", this.clickHandler);

        // Set the initial theme based on saved preferences or system default
        this.loadSavedTheme();
    }

    setTheme(theme) {
        this.root.classList.toggle('dark', theme === 'dark');
        this.root.setAttribute('data-theme', theme);
        localStorage.setItem(this.themeKey, theme);
    }

    loadSavedTheme() {
        const savedTheme = localStorage.getItem(this.themeKey);
        if (savedTheme === 'dark' || savedTheme === 'light') {
            this.setTheme(savedTheme);
        } else {
            const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
            this.setTheme(prefersDark ? 'dark' : 'light');
        }
    }

    /**
     * Destroys the theme toggle instance and removes all event listeners.
     * Call this before removing the element from DOM.
     */
    destroy() {
        debugLog("Destroy demo container: ", this.trigger);

        this.trigger.removeEventListener("click", this.clickHandler);

        ThemeToggle.instances.delete(this.trigger);
        delete this.trigger.__insightInstance;

        this.trigger = null;
    }

    // Static method for initializing all toggle buttons
    static initAll() {
        document.querySelectorAll('[data-theme-toggle]').forEach(toggleButton => new ThemeToggle(toggleButton));
    }
};
