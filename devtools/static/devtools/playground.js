// SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
// SPDX-License-Identifier: AGPL-3.0-only
(() => {
    const frame = document.getElementById("component-preview");
    const viewport = document.getElementById("viewport-select");
    const rtl = document.getElementById("rtl-toggle");
    const widths = { full: "100%", desktop: "1024px", tablet: "768px", mobile: "375px" };

    function applyViewport() {
        frame.style.width = widths[viewport.value] || widths.desktop;
    }

    function applyAppearance() {
        try {
            const root = frame.contentDocument?.documentElement;
            if (!root) return;
            const theme = document.documentElement.dataset.theme || "light";
            root.dir = rtl.checked ? "rtl" : "ltr";
            root.dataset.theme = theme;
            root.classList.toggle("dark", theme === "dark");
        } catch (error) {
            // A component may navigate its frame off-origin; do not access that page.
            if (error.name !== "SecurityError") throw error;
        }
    }

    viewport.addEventListener("change", applyViewport);
    rtl.addEventListener("change", applyAppearance);
    frame.addEventListener("load", applyAppearance);
    new MutationObserver(applyAppearance).observe(document.documentElement, {
        attributes: true, attributeFilter: ["data-theme"]
    });
    applyViewport();
    applyAppearance();
})();
