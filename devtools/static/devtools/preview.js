// SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
// SPDX-License-Identifier: AGPL-3.0-only
// Import real component classes, not the application initializer that requires HTMX.
const componentModules = [
    "accordion", "carousel", "checkbox", "code-block", "collapsible", "dropdown",
    "flip-card", "floater", "modal", "multiselect", "progress-bar", "range-slider",
    "search", "sidebar", "tabs", "theme-toggle", "3D-carousel",
].map(name => new URL(`../insight_ui/js/insight-ui-${name}.js`, import.meta.url).href);

const selectedModules = JSON.parse(document.getElementById("preview-component-modules").textContent);
componentModules.push(...selectedModules.map(url => new URL(url, window.location.href).href));

window.InsightUI.handlers.init();
let initializationFailed = false;
for (const url of new Set(componentModules)) {
    try {
        const exports = await import(url);
        for (const [name, component] of Object.entries(exports)) {
            if (typeof component?.initAll === "function") {
                window.InsightUI[name] = component;
                component.initAll();
            }
        }
    } catch (error) {
        initializationFailed = true;
        console.error("Local component preview initialization failed:", url, error);
        const notice = document.getElementById("preview-error");
        notice.textContent = "A local JavaScript component could not initialize. Check the browser console.";
        notice.hidden = false;
    }
}

if (!initializationFailed) {
    document.dispatchEvent(new CustomEvent("insightui:ready", { bubbles: true }));
}
