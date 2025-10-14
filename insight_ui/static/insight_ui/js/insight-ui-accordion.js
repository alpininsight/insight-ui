window.InsightUI = window.InsightUI || {};

InsightUI.Accordion = {
    init: function () {
        // Collect all elements with 'data-accordion=<target_ID>'
        const accordions = []; // document.querySelectorAll("[data-accordion]");

        accordions.forEach((accordion) => {
            const buttons = Array.from(accordion.querySelectorAll("button[aria-controls]"));
            const exclusive = accordion.getAttribute("data-accordion-exclusive");

            function closePanel(button, panel) {
                button.setAttribute('aria-expanded', 'false');
                panel.style.height = panel.scrollHeight + 'px';
                requestAnimationFrame(() => {
                    panel.style.height = '0';
                    panel.style.opacity = '0';
                });
                button.querySelector('svg')?.classList.remove('rotate-180');
            }

            function openPanel(button, panel, scroll = true) {
                button.setAttribute('aria-expanded', 'true');
                panel.style.height = panel.scrollHeight + 'px';
                panel.style.opacity = '1';
                button.querySelector('svg')?.classList.add('rotate-180');

                panel.addEventListener('transitionend', function handler(event) {
                    if (event.propertyName === 'height') {
                        panel.style.height = 'auto';
                        panel.removeEventListener('transitionend', handler);

                        if (scroll) {
                            const rect = panel.getBoundingClientRect();
                            const isOutOfView =
                                rect.top < 0 || rect.bottom > (window.innerHeight || document.documentElement.clientHeight);
                            if (isOutOfView) {
                                button.scrollIntoView({ behavior: 'smooth', block: 'start' });
                            }
                        }
                    }
                });
            }

            function updateURL(id) {
                const url = new URL(window.location);
                url.searchParams.set('open', id);
                window.history.replaceState({}, '', url);
            }

            buttons.forEach((button, index) => {
                const panelId = button.getAttribute('aria-controls');
                const panel = document.getElementById(panelId);

                button.addEventListener('click', () => {
                    const isExpanded = button.getAttribute('aria-expanded') === 'true';

                    if (exclusive === "true") {
                        buttons.forEach((btn) => {
                            const pid = btn.getAttribute('aria-controls');
                            const p = document.getElementById(pid);
                            if (btn !== button) {
                                closePanel(btn, p);
                            }
                        });
                    }

                    if (isExpanded) {
                        closePanel(button, panel);
                    } else {
                        openPanel(button, panel);
                        updateURL(panelId);
                    }
                });

                button.addEventListener('keydown', (event) => {
                    let targetIndex = null;
                    if (event.key === 'ArrowDown') {
                        targetIndex = (index + 1) % buttons.length;
                    } else if (event.key === 'ArrowUp') {
                        targetIndex = (index - 1 + buttons.length) % buttons.length;
                    } else if (event.key === 'Home') {
                        targetIndex = 0;
                    } else if (event.key === 'End') {
                        targetIndex = buttons.length - 1;
                    }

                    if (targetIndex !== null) {
                        event.preventDefault();
                        buttons[targetIndex].focus();
                    }
                });
            });

            const params = new URLSearchParams(window.location.search);
            const openId = params.get('open');
            if (openId) {
                const buttonToOpen = buttons.find(btn => btn.getAttribute('aria-controls') === openId);
                const panelToOpen = document.getElementById(openId);

                if (buttonToOpen && panelToOpen) {
                    if (exclusive === "true") {
                        buttons.forEach((btn) => {
                            const pid = btn.getAttribute('aria-controls');
                            const p = document.getElementById(pid);
                            closePanel(btn, p);
                        });
                    }
                    openPanel(buttonToOpen, panelToOpen, true);
                }
            }
        });
    }
};
