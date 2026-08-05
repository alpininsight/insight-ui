/**
 * Theme toggle component for Insight UI.
 *
 * Manages light/dark theme switching with persistence via localStorage and cookies.
 * Sets both the `.dark` class (for Tailwind) and `data-theme` attribute (for Insight UI CSS).
 * Respects system color scheme preferences on initial load.
 *
 * @example
 * // HTML structure
 * <button data-insight-theme-toggle>Toggle Theme</button>
 */
export class ThemeToggle {
    /** @type {WeakMap<HTMLElement, ThemeToggle>} Weak references to prevent multiple initialization */
    static instances = new WeakMap();

    /**
     * Creates a new ThemeToggle instance.
     *
     * @param {HTMLElement} trigger - The toggle button element with data-insight-theme-toggle attribute
     */
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

    /**
     * Initializes the theme toggle by binding the click handler and loading saved theme.
     */
    init() {
        this.trigger.addEventListener("click", this.clickHandler);

        // Set the initial theme based on saved preferences or system default
        this.loadSavedTheme();
    }

    /**
     * Sets the theme and persists it to localStorage and cookies.
     *
     * @param {string} theme - The theme to set: "light" or "dark"
     */
    setTheme(theme) {
        this.root.classList.toggle('dark', theme === 'dark');
        this.root.setAttribute('data-theme', theme);
        localStorage.setItem(this.themeKey, theme);
        document.cookie = "theme=" + theme + "; path=/; max-age=31536000";
    }

    /**
     * Loads and applies the saved theme from localStorage, or falls back to system preference.
     */
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

    /**
     * Initializes all theme toggle instances on the page.
     *
     * @static
     */
    static initAll() {
        document.querySelectorAll('[data-insight-theme-toggle]').forEach(toggleButton => new ThemeToggle(toggleButton));
    }
}
