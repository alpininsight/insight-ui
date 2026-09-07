// SPDX-FileCopyrightText: 2025-2026 Alpin Insight Solutions GmbH & Co. KG
// SPDX-License-Identifier: AGPL-3.0-only
/**
 * Navigation state management for Insight UI.
 *
 * Automatically highlights active navigation links based on the current URL.
 * Works with both standard navigation and side navigation components.
 * Updates state on DOMContentLoaded, HTMX content swaps, browser history navigation,
 * and fragment changes.
 *
 * @module insight-ui-state
 */
(function () {
    /**
     * Normalizes a URL path by removing trailing slashes.
     *
     * @param {string} path - The URL path to normalize
     * @returns {string} The normalized path
     */
    function normalize(path) {
        return path.replace(/\/+$/, "") || "/";
    }

    /**
     * Returns the ARIA current value for a link, or null when it is inactive.
     *
     * @param {URL} url - The resolved link URL
     * @param {URL} current - The current browser URL
     * @returns {"page"|"location"|null} The matching ARIA current value
     */
    function getCurrentValue(url, current) {
        if (url.origin !== current.origin) {
            return null;
        }

        const hrefPath = normalize(url.pathname);
        const currentPath = normalize(current.pathname);

        if (url.hash) {
            return hrefPath === currentPath && url.hash === current.hash ? "location" : null;
        }

        if (hrefPath === "/") {
            return currentPath === "/" ? "page" : null;
        }
        return currentPath === hrefPath || currentPath.startsWith(hrefPath + "/") ? "page" : null;
    }

    /**
     * Updates the active state of navigation links based on the current URL.
     * Sets aria-current="page" on active links and aria-current="true" on
     * dropdown buttons that contain an active link. CSS handles the visual styling.
     */
    function updateActiveNav() {
        const current = new URL(window.location.href);

        // Process navbar and sidebar navigation links
        document.querySelectorAll("[data-insight-nav] a[href], [data-insight-side-nav] a[href]").forEach(el => {
            const currentValue = getCurrentValue(new URL(el.href, window.location.origin), current);

            if (currentValue) {
                el.setAttribute("aria-current", currentValue);
            } else {
                el.removeAttribute("aria-current");
            }
        });

        // Process dropdown buttons: highlight if any child link is active
        document.querySelectorAll("[data-insight-nav] button[data-insight-dropdown]").forEach(button => {
            const dropdownId = button.getAttribute("data-insight-dropdown");
            const dropdown = document.getElementById(dropdownId);
            if (!dropdown) return;

            // Check if any link in this dropdown is active
            const hasActiveChild = Array.from(dropdown.querySelectorAll("a[href]")).some(link => {
                return Boolean(getCurrentValue(new URL(link.href, window.location.origin), current));
            });

            if (hasActiveChild) {
                button.setAttribute("aria-current", "true");
            } else {
                button.removeAttribute("aria-current");
            }
        });
    }

    document.addEventListener("DOMContentLoaded", updateActiveNav);
    document.body.addEventListener("htmx:afterOnLoad", updateActiveNav);
    window.addEventListener("popstate", updateActiveNav);
    window.addEventListener("hashchange", updateActiveNav);
})();
