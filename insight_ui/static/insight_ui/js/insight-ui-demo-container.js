/**
 * Demo iframe controller for Insight UI documentation.
 *
 * Manages demo iframes with controls for viewport width, RTL direction,
 * and theme toggling. Automatically syncs with the parent document's theme
 * and handles iframe resizing.
 *
 * @example
 * // HTML structure
 * <div data-insight-demo-container="demo1">
 *   <iframe data-insight-demo-iframe="demo1" src="..."></iframe>
 *   <input type="radio" name="width-toggle-demo1" value="mobile">
 *   <input id="dir-toggle-demo1" type="checkbox">
 *   <input id="theme-toggle-demo1" type="checkbox">
 * </div>
 */
export class DemoIframeController {
    /** @type {WeakMap<HTMLElement, DemoIframeController>} Weak references to prevent multiple initialization */
    static instances = new WeakMap();

    /**
     * Creates a new DemoIframeController instance.
     *
     * @param {HTMLElement} element - The container element with data-insight-demo-container attribute
     */
    constructor(element) {
        // If an instance for this element already exists, return it
        if (DemoIframeController.instances.has(element)) {
            return DemoIframeController.instances.get(element);
        }

        this.element = element;
        this.demoId = this.element.getAttribute("data-insight-demo-container");
        this.iframe = this.element.querySelector(`[data-insight-demo-iframe="${this.demoId}"]`);
        if (!this.iframe) return;

        this.iframe.classList.add("opacity-0", "transition-opacity", "duration-200");  // Hide <iframe> until rendering has finished, to hide flickering

        this.widthRadios = this.element.querySelectorAll(
            `input[type="radio"][name="width-toggle-${this.demoId}"]`
        );
        this.dirToggle = document.getElementById(`dir-toggle-${this.demoId}`);
        this.themeToggle = document.getElementById(`theme-toggle-${this.demoId}`);

        // Store bound handlers for cleanup
        this.onIframeLoadInit = this.onIframeLoadInit.bind(this);
        this.onIframeLoadObserver = this.onIframeLoadObserver.bind(this);
        this.onWidthChange = this.onWidthChange.bind(this);
        this.onDirToggleClick = this.onDirToggleClick.bind(this);
        this.onThemeToggleClick = this.onThemeToggleClick.bind(this);
        this.onThemeMutation = this.onThemeMutation.bind(this);

        this.initEvents();
        this.initIframeObservers();

        this.element.__insightInstance = this;

        DemoIframeController.instances.set(element, this);

        debugLog("New DemoIframeController created: ", this.element);
    }

    /**
     * Handler for iframe initial load - initializes the iframe state.
     */
    onIframeLoadInit() {
        this.initIFrame();
    }

    /**
     * Handler for iframe load - sets up resize observers and removes loading state.
     */
    onIframeLoadObserver() {
        this.iframe.classList.remove("opacity-0");
        this.resizeIframe();

        this.mutationObserver = new MutationObserver(this.resizeIframe);
        this.mutationObserver.observe(this.iframe.contentDocument.body, {
            childList: true,
            subtree: true,
            characterData: true
        });

        this.resizeObserver = new ResizeObserver(this.resizeIframe);
        this.resizeObserver.observe(this.iframe.contentDocument.body);
    }

    /**
     * Handler for width radio button changes.
     *
     * @param {Event} e - The change event
     */
    onWidthChange(e) {
        if (e.target.checked) {
            this.setWidth(e.target.value);
        }
    }

    /**
     * Handler for RTL toggle clicks.
     */
    onDirToggleClick() {
        this.toggleRTL();
    }

    /**
     * Handler for theme toggle clicks.
     */
    onThemeToggleClick() {
        this.toggleTheme();
    }

    /**
     * Handler for theme mutations on the parent document.
     */
    onThemeMutation() {
        this.themeToggle.checked =
            document.documentElement.classList.contains("dark");
        this.setTheme(this.themeToggle.checked);
    }

    /**
     * Initializes event listeners for controls and iframe.
     */
    initEvents() {
        this.iframe.addEventListener("load", this.onIframeLoadInit);

        this.widthRadios.forEach(radio => {
            radio.addEventListener("change", this.onWidthChange);
        });

        if (this.dirToggle) {
            this.dirToggle.addEventListener("click", this.onDirToggleClick);
        }

        if (this.themeToggle) {
            this.themeToggle.addEventListener("click", this.onThemeToggleClick);
        }
    }

    /**
     * Initializes the iframe state including width, direction, and theme.
     */
    initIFrame() {
        this.widthRadios.forEach(radio => {
            radio.checked = radio.value === "desktop";
        });

        if (this.dirToggle) this.dirToggle.checked = false;
        if (this.themeToggle) this.themeToggle.checked = false;

        if (document.documentElement.classList.contains("dark")) {
            this.toggleTheme();
            if (this.themeToggle) this.themeToggle.checked = true;
        }

        const config = { attributes: true };

        this.themeObserver = new MutationObserver(this.onThemeMutation);
        this.themeObserver.observe(document.documentElement, config);
    }

    /**
     * Sets up iframe observers for content changes and resizing.
     */
    initIframeObservers() {
        this.iframe.addEventListener("load", this.onIframeLoadObserver);
    }

    /**
     * Sets the iframe width based on the selected viewport variant.
     *
     * @param {string} variant - The viewport variant: "mobile", "tablet", or "desktop"
     */
    setWidth(variant) {
        this.iframe.classList.remove("max-w-sm", "max-w-lg");

        if (variant === "mobile") {
            this.iframe.classList.add("max-w-sm");
        } else if (variant === "tablet") {
            this.iframe.classList.add("max-w-lg");
        }
    }

    /**
     * Gets the HTML element of the iframe document.
     *
     * @returns {HTMLElement} The documentElement of the iframe
     */
    getHtmlTag() {
        return this.iframe.contentWindow.document.documentElement;
    }

    /**
     * Toggles the text direction between LTR and RTL in the iframe.
     */
    toggleRTL() {
        const htmlTag = this.getHtmlTag();
        htmlTag.dir = (htmlTag.dir === "ltr" || htmlTag.dir === "") ? "rtl" : "ltr";
    }

    /**
     * Toggles the theme between light and dark in the iframe.
     */
    toggleTheme() {
        const htmlTag = this.getHtmlTag();

        htmlTag.classList.toggle("dark");
        htmlTag.setAttribute(
            "data-theme",
            htmlTag.classList.contains("dark") ? "dark" : "light"
        );
    }

    /**
     * Sets a specific theme in the iframe.
     *
     * @param {boolean} dark - True for dark theme, false for light theme
     */
    setTheme(dark) {
        const htmlTag = this.getHtmlTag();

        if (dark === true) {
            htmlTag.classList.add("dark");
            htmlTag.setAttribute("data-theme", "dark");
        }
        else {
            htmlTag.classList.remove("dark");
            htmlTag.setAttribute("data-theme", "light");
        }
    }

    /**
     * Resizes the iframe height to fit its content, up to a maximum of 756px.
     */
    resizeIframe = () => {
        requestAnimationFrame(() => {
            if (this.iframe?.contentDocument) {
                const doc = this.iframe.contentDocument;
                this.iframe.style.height = Math.min(doc.body.scrollHeight, 756) + "px";
            }
        });
    };

    /**
     * Destroys the demo container instance and removes all event listeners.
     * Call this before removing the element from DOM.
     */
    destroy() {
        debugLog("Destroy demo container: ", this.element);

        // Remove event listeners
        this.iframe?.removeEventListener("load", this.onIframeLoadInit);
        this.iframe?.removeEventListener("load", this.onIframeLoadObserver);

        this.widthRadios?.forEach(radio => {
            radio.removeEventListener("change", this.onWidthChange);
        });

        this.dirToggle?.removeEventListener("click", this.onDirToggleClick);
        this.themeToggle?.removeEventListener("click", this.onThemeToggleClick);

        // Disconnect observers
        this.mutationObserver?.disconnect();
        this.resizeObserver?.disconnect();
        this.themeObserver?.disconnect();

        DemoIframeController.instances.delete(this.element);
        delete this.element.__insightInstance;

        this.element = null;
    }

    /**
     * Initializes all demo container instances on the page.
     *
     * @static
     */
    static initAll() {
        document.querySelectorAll("[data-insight-demo-container]").forEach(el => new DemoIframeController(el));
    }
}
