(function () {
    function normalize(path) {
        return path.replace(/\/+$/, "") || "/";
    }

    function updateActiveNav() {
        const current = normalize(window.location.pathname);
        document.querySelectorAll("[data-insight-nav]").forEach(container => {
            container.querySelectorAll("a[href]").forEach(el => {
                const href = normalize(new URL(el.href, window.location.origin).pathname);

                let isActive = false;

                if (href === "/") {
                    isActive = current === "/";
                } else {
                    isActive = current === href || current.startsWith(href + "/");
                }

                el.classList.remove("transition-colors", "duration-200");
                el.classList.toggle("text-insight-text-link", isActive);
            });
        });

        document.querySelectorAll("[data-insight-side-nav]").forEach(container => {
            container.querySelectorAll("a[href]").forEach(el => {
                const href = normalize(new URL(el.href, window.location.origin).pathname);

                let isActive = false;

                if (href === "/") {
                    isActive = current === "/";
                } else {
                    isActive = current === href || current.startsWith(href + "/");
                }

                if (isActive)
                    el.setAttribute("class", "flex gap-2 px-2 py-1 text-sm text-primary font-semibold insight-surface-soft border-s-2 border-insight-primary hover:border-insight-primary-hover");
                else
                    el.setAttribute("class", "flex gap-2 px-2 py-1 text-sm text-primary border-s insight-border-surface hover:border-insight-border-muted hover:text-insight-text-secondary")
            });
        });
    }

    document.addEventListener("DOMContentLoaded", updateActiveNav);
    document.body.addEventListener("htmx:afterOnLoad", updateActiveNav);
    window.addEventListener("popstate", updateActiveNav);
})();
