window.InsightUI = window.InsightUI || {};

InsightUI.Accordion = {
    init: function () {
        // Collect all elements with 'data-accordion=<target_ID>'
        const accordions = document.querySelectorAll("[data-accordion]");

        accordions.forEach((accordion) => {
            if (accordion.dataset.initialized === "true") {
                return;
            }

            accordion.dataset.initialized = "true";

            const buttons = Array.from(accordion.querySelectorAll("button[aria-controls]"));
            const exclusive = accordion.getAttribute("data-accordion-exclusive");

            function closePanel(button, panel) {
                button.setAttribute('aria-expanded', 'false');
                button.querySelector('svg')?.classList.remove('rotate-180');

                panel.style.height = panel.scrollHeight + 'px';
                panel.offsetHeight;

                panel.style.transition = 'height 0.3s ease, opacity 0.3s ease';
                panel.style.height = '0px';
                panel.style.opacity = '0';

                panel.addEventListener('transitionend', function handler(event) {
                    if (event.propertyName === 'height') {
                        panel.removeEventListener('transitionend', handler);
                        panel.style.transition = '';
                        panel.style.height = '0px';
                    }
                });
            }

            function openPanel(button, panel, scroll = true) {
                button.setAttribute('aria-expanded', 'true');
                button.querySelector('svg')?.classList.add('rotate-180');

                panel.style.transition = 'none';
                panel.style.height = 'auto';
                const height = panel.scrollHeight + 'px';
                panel.style.height = '0px';
                panel.offsetHeight;

                panel.style.transition = 'height 0.3s ease, opacity 0.3s ease';
                panel.style.height = height;
                panel.style.opacity = '1';

                panel.addEventListener('transitionend', function handler(event) {
                    if (event.propertyName === 'height') {
                        panel.removeEventListener('transitionend', handler);
                        panel.style.transition = '';
                        panel.style.height = 'auto';
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

        console.log("Accordions: ", accordions);
        console.log("Accordions initialized!");
    }
};
