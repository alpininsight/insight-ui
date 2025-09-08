window.InsightUI = window.InsightUI || {};

InsightUI.Popover = {
    init: function () {
        // Collect all elements with 'data-popover-trigger=<target_ID>'
        const triggers = document.querySelectorAll("[data-popover-trigger]");

        triggers.forEach((trigger) => {
            const popoverId = trigger.getAttribute("data-popover-trigger");
            const popover = document.getElementById(popoverId);

            if (!popover) return;

            popover.classList.add("absolute", "hidden", "z-50");

            // Dynamic positioning
            function updateTooltipPosition() {
                const position = trigger.getAttribute('data-position') || "top";
                const rect = trigger.getBoundingClientRect();
                const scrollY = window.scrollY || document.documentElement.scrollTop;

                switch (position) {
                    case 'top':
                    popover.style.top = `${rect.top + scrollY - popover.offsetHeight - 8}px`;
                    popover.style.left = `${rect.left + rect.width / 2 - popover.offsetWidth / 2}px`;
                    popover.querySelector('.popover-arrow').classList.add('rotate-180');
                    popover.querySelector('.popover-arrow').style.top = `${popover.offsetHeight - 2}px`;
                    break;

                    case 'bottom':
                    popover.style.top = `${rect.bottom + scrollY + 8}px`;
                    popover.style.left = `${rect.left + rect.width / 2 - popover.offsetWidth / 2}px`;
                    popover.querySelector('.popover-arrow').classList.remove('rotate-180');
                    popover.querySelector('.popover-arrow').style.top = '';
                    break;

                    case 'left':
                    popover.style.top = `${rect.top + rect.height / 2 - popover.offsetHeight / 2 + scrollY}px`;
                    popover.style.left = `${rect.left - popover.offsetWidth - 8}px`;
                    popover.querySelector('.popover-arrow').classList.add('rotate-90');
                    popover.querySelector('.popover-arrow').style.top = `${popover.offsetHeight / 2 - 5}px`;
                    popover.querySelector('.popover-arrow').style.left = `${popover.offsetWidth + 3}px`;
                    break;

                    case 'right':
                    popover.style.top = `${rect.top + rect.height / 2 - popover.offsetHeight / 2 + scrollY}px`;
                    popover.style.left = `${rect.right + 8}px`;
                    popover.querySelector('.popover-arrow').classList.add('-rotate-90');
                    popover.querySelector('.popover-arrow').style.top = `${popover.offsetHeight / 2 - 5}px`;
                    popover.querySelector('.popover-arrow').style.left = `${-3}px`;
                    break;
                }
            }

            let hideTimeout;

            function showPopover() {
                clearTimeout(hideTimeout);
                popover.classList.remove("hidden");
                updateTooltipPosition();
            }

            function hidePopoverWithDelay() {
                // The element should not disappears immediately,
                // so the user has enough time to move the cursor over the popover, without disappearing.
                hideTimeout = setTimeout(() => {
                    popover.classList.add("hidden");
                }, 100);
            }

            trigger.addEventListener("mouseover", (event) => {
                event.stopPropagation();
                showPopover();
            });

            trigger.addEventListener("mouseout", (event) => {
                event.stopPropagation();
                hidePopoverWithDelay();
            });

            popover.addEventListener("mouseover", (event) => {
                event.stopPropagation();
                showPopover();
            });

            popover.addEventListener("mouseout", (event) => {
                event.stopPropagation();
                hidePopoverWithDelay();
            });

            // Update position on scroll
            window.addEventListener('scroll', updateTooltipPosition);
        });

        /* Close all menus on click everywhere */
        document.addEventListener("click", () => {
            hideAllPopovers();
        });

        /* Close all menus */
        function hideAllPopovers() {
            const triggers = document.querySelectorAll("[data-popover-trigger]");
            triggers.forEach((trigger) => {
                const popoverId = trigger.getAttribute("data-popover-trigger");
                const popover = document.getElementById(popoverId);

                if (!popover) return;

                if (popover.classList.contains("hidden")) return;
                popover.classList.add("hidden");
            });
        }
    }
};

document.addEventListener('DOMContentLoaded', InsightUI.Popover.init);
