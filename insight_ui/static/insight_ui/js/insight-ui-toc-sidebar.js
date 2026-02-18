/**
 * Collapsible TOC sidebar with circle toggle button.
 *
 * In-flow within the flex layout — expanding the sidebar changes the
 * wrapper width, which causes the content area to shrink and reflow.
 *
 * Collapsed: circle button fixed top-right, wrapper has w-0.
 * Expanded: wrapper widens to 16rem, panel becomes visible, content adjusts.
 */
export class TocSidebar {
    static instances = new WeakMap();

    constructor(wrapper) {
        if (TocSidebar.instances.has(wrapper)) {
            return TocSidebar.instances.get(wrapper);
        }

        this.wrapper = wrapper;
        this.rail = wrapper.querySelector("#toc-rail");
        this.panel = wrapper.querySelector("#toc-panel");
        this.closeBtn = wrapper.querySelector("#toc-close");
        this.expanded = false;

        if (!this.rail || !this.panel) return;

        this.rail.addEventListener("click", () => this.toggle());
        if (this.closeBtn) {
            this.closeBtn.addEventListener("click", () => this.collapse());
        }

        TocSidebar.instances.set(wrapper, this);
        debugLog("New TocSidebar created: ", wrapper);
    }

    toggle() {
        if (this.expanded) {
            this.collapse();
        } else {
            this.expand();
        }
    }

    expand() {
        this.expanded = true;
        this.rail.setAttribute("aria-expanded", "true");
        // Widen the wrapper so flex layout gives it space
        this.wrapper.classList.remove("w-0");
        this.wrapper.classList.add("w-[16rem]");
        // Show the panel
        this.panel.classList.remove("opacity-0", "overflow-hidden");
        this.panel.classList.add("opacity-100");
        // Hide the circle button
        this.rail.classList.add("hidden");
    }

    collapse() {
        this.expanded = false;
        this.rail.setAttribute("aria-expanded", "false");
        // Shrink the wrapper so content reclaims the space
        this.wrapper.classList.add("w-0");
        this.wrapper.classList.remove("w-[16rem]");
        // Hide the panel
        this.panel.classList.add("opacity-0", "overflow-hidden");
        this.panel.classList.remove("opacity-100");
        // Show the circle button
        this.rail.classList.remove("hidden");
    }

    destroy() {
        TocSidebar.instances.delete(this.wrapper);
    }

    static initAll() {
        document.querySelectorAll("[data-insight-toc-sidebar]").forEach(el => {
            new TocSidebar(el);
        });
    }
}
