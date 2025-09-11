window.InsightUI = window.InsightUI || {};

InsightUI.Tooltip = {
    init: function () {
        // Collect all elements with 'data-tooltip-trigger=<target_ID>'
        const triggers = document.querySelectorAll("[data-tooltip-trigger]");

        triggers.forEach((trigger) => {
            const tooltipId = trigger.getAttribute("data-tooltip-trigger");
            const tooltip = document.getElementById(tooltipId);
            const tooltipArrow = tooltip.querySelector('.tooltip-arrow');

            if (!tooltip) return;

            tooltip.classList.add("absolute", "hidden", "z-50");

            // Dynamic positioning
            function updateTooltipPosition() {
                const position = trigger.getAttribute('data-position') || "top";
                const rect = trigger.getBoundingClientRect();
                const scrollY = window.scrollY || document.documentElement.scrollTop;

                switch (position) {
                    case 'top':
                        tooltip.style.top = `${rect.top + scrollY - tooltip.offsetHeight - 8}px`;
                        tooltip.style.left = `${rect.left + rect.width / 2 - tooltip.offsetWidth / 2}px`;
                        if (tooltipArrow)
                        {
                            tooltipArrow.classList.add('rotate-180');
                            tooltipArrow.style.top = `${tooltip.offsetHeight - 2}px`;
                        }
                        break;
                    case 'bottom':
                        tooltip.style.top = `${rect.bottom + scrollY + 8}px`;
                        tooltip.style.left = `${rect.left + rect.width / 2 - tooltip.offsetWidth / 2}px`;
                        if (tooltipArrow)
                        {
                            tooltipArrow.classList.remove('rotate-180');
                            tooltipArrow.style.top = '';
                        }
                        break;
                    case 'left':
                        tooltip.style.top = `${rect.top + rect.height / 2 - tooltip.offsetHeight / 2 + scrollY}px`;
                        tooltip.style.left = `${rect.left - tooltip.offsetWidth - 8}px`;
                        if (tooltipArrow)
                        {
                            tooltipArrow.classList.add('rotate-90');
                            tooltipArrow.style.top = `${tooltip.offsetHeight / 2 - 5}px`;
                            tooltipArrow.style.left = `${tooltip.offsetWidth + 3}px`;
                        }
                        break;
                    case 'right':
                        tooltip.style.top = `${rect.top + rect.height / 2 - tooltip.offsetHeight / 2 + scrollY}px`;
                        tooltip.style.left = `${rect.right + 8}px`;
                        if (tooltipArrow)
                        {
                            tooltipArrow.classList.add('-rotate-90');
                            tooltipArrow.style.top = `${tooltip.offsetHeight / 2 - 5}px`;
                            tooltipArrow.style.left = `${-3}px`;
                        }
                        break;
                }
            }

            trigger.addEventListener("mouseover", (event) => {
                event.stopPropagation();
                tooltip.classList.remove("hidden");
                updateTooltipPosition();
            });

            trigger.addEventListener("mouseout", (event) => {
                event.stopPropagation();
                tooltip.classList.add("hidden");
            });

            // Update position on scroll
            window.addEventListener('scroll', updateTooltipPosition);
        });

        /* Close all menus on click everywhere */
        document.addEventListener("click", () => {
            hideAllTooltips();
        });

        /* Close all menus */
        function hideAllTooltips() {
            const triggers = document.querySelectorAll("[data-tooltip-trigger]");
            triggers.forEach((trigger) => {
                const tooltipId = trigger.getAttribute("data-tooltip-trigger");
                const tooltip = document.getElementById(tooltipId);

                if (!tooltip) return;

                if (tooltip.classList.contains("hidden")) return;
                tooltip.classList.add("hidden");
            });
        }
    }
};

document.addEventListener('DOMContentLoaded', InsightUI.Tooltip.init);
