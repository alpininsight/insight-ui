export class ThemeSwitcher {
    static instances = new WeakMap();

    constructor(selector) {
        if (ThemeSwitcher.instances.has(selector)) {
            return ThemeSwitcher.instances.get(selector);
        }

        this.selector = selector;
        this.root = document.documentElement;
        this.storageKey = selector.dataset.storageKey || "insight-ui-design-theme";
        this.themeStylesheet = document.getElementById("insight-ui-theme-stylesheet");
        this.changeHandler = () => this.setTheme(this.selector.value);
        this.iframeLoadHandler = (event) => this.applyThemeToIframe(event.currentTarget);
        this.currentTheme = this.selector.value;
        this.currentHref = "";

        this.init();

        this.selector.__insightInstance = this;
        ThemeSwitcher.instances.set(selector, this);

        debugLog("New design theme switcher created: ", this.selector);
    }

    init() {
        this.selector.addEventListener("change", this.changeHandler);
        this.bindDemoIframes();

        const savedTheme = localStorage.getItem(this.storageKey);
        const initialTheme = this.hasTheme(savedTheme) ? savedTheme : this.selector.value;
        this.setTheme(initialTheme, { persist: false });
    }

    hasTheme(theme) {
        return Boolean(theme && this.selector.querySelector(`option[value="${CSS.escape(theme)}"]`));
    }

    setTheme(theme, options = {}) {
        const selectedOption = this.selector.querySelector(`option[value="${CSS.escape(theme)}"]`);
        if (!selectedOption) {
            return;
        }

        this.selector.value = theme;
        this.currentTheme = theme;
        this.currentHref = selectedOption.dataset.themeHref || "";
        this.root.setAttribute("data-insight-design-theme", theme);

        if (this.themeStylesheet && this.currentHref) {
            this.themeStylesheet.href = this.currentHref;
        }

        if (options.persist !== false) {
            localStorage.setItem(this.storageKey, theme);
        }

        this.syncDemoIframes();
    }

    bindDemoIframes() {
        document.querySelectorAll("[data-insight-demo-iframe]").forEach((iframe) => {
            iframe.removeEventListener("load", this.iframeLoadHandler);
            iframe.addEventListener("load", this.iframeLoadHandler);
            this.applyThemeToIframe(iframe);
        });
    }

    syncDemoIframes() {
        document.querySelectorAll("[data-insight-demo-iframe]").forEach((iframe) => this.applyThemeToIframe(iframe));
    }

    applyThemeToIframe(iframe) {
        if (!iframe?.contentDocument?.documentElement) {
            return;
        }

        const frameDocument = iframe.contentDocument;
        frameDocument.documentElement.setAttribute("data-insight-design-theme", this.currentTheme);

        const frameThemeStylesheet = frameDocument.getElementById("insight-ui-theme-stylesheet");
        if (frameThemeStylesheet && this.currentHref) {
            frameThemeStylesheet.href = this.currentHref;
        }
    }

    destroy() {
        debugLog("Destroy design theme switcher: ", this.selector);

        this.selector.removeEventListener("change", this.changeHandler);
        document.querySelectorAll("[data-insight-demo-iframe]").forEach((iframe) => {
            iframe.removeEventListener("load", this.iframeLoadHandler);
        });

        ThemeSwitcher.instances.delete(this.selector);
        delete this.selector.__insightInstance;

        this.selector = null;
    }

    static initAll() {
        document.querySelectorAll("[data-insight-theme-switcher]").forEach((selector) => {
            const instance = new ThemeSwitcher(selector);
            instance.bindDemoIframes();
        });
    }
};
