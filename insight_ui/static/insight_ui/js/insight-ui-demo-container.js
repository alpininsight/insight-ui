class DemoIframeController {
    // Manages all iframe controller instances of the DOM
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

    initEvents() {
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
        htmlTag.dir = (htmlTag.dir === "rtl") ? "ltr" : "rtl";
    }

    toggleTheme() {
        const htmlTag = this.getHtmlTag();

        htmlTag.classList.toggle("dark");
        htmlTag.setAttribute(
            "data-theme",
            htmlTag.classList.contains("dark") ? "dark" : "light"
        );
    }

    resizeIframe = () => {
        requestAnimationFrame(() => {
            const doc = this.iframe.contentDocument || this.iframe.contentWindow.document;
            this.iframe.style.height =
                Math.min(doc.body.scrollHeight, 756) + "px";
        });
    };

    initIframeObservers() {
        this.iframe.addEventListener("load", () => {
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
        const controller = document.querySelectorAll("[data-insight-demo-container]");
        controller.forEach((el) => {
            if (!DemoIframeController.instances.has(el)) {
                new DemoIframeController(el);
            }
        });
    }
}

window.InsightUI = window.InsightUI || {};
window.InsightUI.DemoIframeController = DemoIframeController;
