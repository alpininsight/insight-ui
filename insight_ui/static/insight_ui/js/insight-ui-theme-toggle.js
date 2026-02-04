/**
 * Insight UI Theme Toggle.
 * Setzt sowohl .dark (für Tailwind) als auch [data-theme] (für Insight UI CSS)
 */
export class ThemeToggle {
    // Manages all ThemeToggle instances of the DOM
    static instances = new WeakMap();

    constructor(button) {
        // If an instance for this element already exists, return it
        if (ThemeToggle.instances.has(button)) {
            return ThemeToggle.instances.get(button);
        }

        this.button = button;
        this.themeKey = 'insight-ui-theme';
        this.root = document.documentElement;

        this.init();

        ThemeToggle.instances.set(button, this);

        debugLog("New theme toggle created: ", this.button);
    }

    init() {
        this.button.addEventListener('click', () => {
            const currentTheme = this.root.classList.contains('dark') ? 'dark' : 'light';
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            this.setTheme(newTheme);
        });

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

    // Static method for initializing all toggle buttons
    static initAll() {
        document.querySelectorAll('[data-theme-toggle]').forEach(toggleButton => new ThemeToggle(toggleButton));
    }
};
