/**
 * Navigation state management for Insight UI.
 *
 * Automatically highlights active navigation links based on the current URL path.
 * Works with both standard navigation and side navigation components.
 * Updates state on DOMContentLoaded, HTMX content swaps, and browser history navigation.
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
     * Checks if a link href matches the current page URL.
     *
     * @param {string} href - The normalized href to check
     * @param {string} current - The normalized current path
     * @returns {boolean} True if the link is active
     */
    function isLinkActive(href, current) {
        if (href === "/") {
            return current === "/";
        }
        return current === href || current.startsWith(href + "/");
    }

    /**
     * Updates the active state of navigation links based on the current URL.
     * Sets aria-current="page" on active links and aria-current="true" on
     * dropdown buttons that contain an active link. CSS handles the visual styling.
     */
    function updateActiveNav() {
        const current = normalize(window.location.pathname);

        // Process navbar and sidebar navigation links
        document.querySelectorAll("[data-insight-nav] a[href], [data-insight-side-nav] a[href]").forEach(el => {
            const href = normalize(new URL(el.href, window.location.origin).pathname);
            const isActive = isLinkActive(href, current);

            if (isActive) {
                el.setAttribute("aria-current", "page");
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
                const href = normalize(new URL(link.href, window.location.origin).pathname);
                return isLinkActive(href, current);
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
})();
