export class DemoIframeController {
    // Manages all <iframe> controller instances of the DOM
    static instances = new WeakMap();

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

        this.initEvents();
        this.initIframeObservers();

        DemoIframeController.instances.set(element, this);

        debugLog("New DemoIframeController created: ", this.element);
    }

    initIFrame() {
        this.widthRadios.forEach(radio => {
            if (radio.value == "desktop")
                radio.checked = true;
            else
                radio.checked = false;
        });

        this.dirToggle.checked = false;
        this.themeToggle.checked = false;

        // Apply main theme to demo container
        if (document.documentElement.classList.contains('dark')) {
            this.toggleTheme();
            this.themeToggle.checked = true;
        }

        // Add MutationObserver to notify theme changes
        const config = { attributes: true, childList: false, subtree: false };
        const callback = (mutationList, observer) => {
            for (const mutation of mutationList) {
                this.themeToggle.checked = document.documentElement.classList.contains('dark');
                this.setTheme(this.themeToggle.checked);
            }
        };

        const observer = new MutationObserver(callback);
        observer.observe(document.documentElement, config);
    }

    initEvents() {
        this.iframe.addEventListener("load", (e) => {
            this.initIFrame();
        });

        this.widthRadios.forEach(radio => {
            radio.addEventListener("change", (e) => {
                if (e.target.checked) {
                    this.setWidth(e.target.value);
                }
            });
        });

        if (this.dirToggle) {
            this.dirToggle.addEventListener("click", () => this.toggleRTL());
        }

        if (this.themeToggle) {
            this.themeToggle.addEventListener("click", () => this.toggleTheme());
        }
    }

    setWidth(variant) {
        this.iframe.classList.remove("max-w-sm", "max-w-lg");

        if (variant === "mobile") {
            this.iframe.classList.add("max-w-sm");
        } else if (variant === "tablet") {
            this.iframe.classList.add("max-w-lg");
        }
    }

    getHtmlTag() {
        return this.iframe.contentWindow.document.documentElement;
    }

    toggleRTL() {
        const htmlTag = this.getHtmlTag();
        htmlTag.dir = (htmlTag.dir === "ltr" || htmlTag.dir === "") ? "rtl" : "ltr";
    }

    toggleTheme() {
        const htmlTag = this.getHtmlTag();

        htmlTag.classList.toggle("dark");
        htmlTag.setAttribute(
            "data-theme",
            htmlTag.classList.contains("dark") ? "dark" : "light"
        );
    }

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

    resizeIframe = () => {
        requestAnimationFrame(() => {
            if (this.iframe.contentDocument)
            {
                const doc = this.iframe.contentDocument;
                this.iframe.style.height = Math.min(doc.body.scrollHeight, 756) + "px";
            }
        });
    };

    initIframeObservers() {
        this.iframe.addEventListener("load", () => {
            this.iframe.classList.remove("opacity-0");  // Show <iframe> after rendering has finished
            this.resizeIframe();

            const mutationObserver = new MutationObserver(this.resizeIframe);
            mutationObserver.observe(this.iframe.contentDocument.body, {
                childList: true,
                subtree: true,
                characterData: true
            });

            const resizeObserver = new ResizeObserver(this.resizeIframe);
            resizeObserver.observe(this.iframe.contentDocument.body);
        });
    }

    // Static method for initializing all iframe container
    static initAll() {
        document.querySelectorAll("[data-insight-demo-container]").forEach(el => new DemoIframeController(el));
    }
}
