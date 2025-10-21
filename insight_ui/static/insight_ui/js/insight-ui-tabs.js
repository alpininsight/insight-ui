window.InsightUI = window.InsightUI || {};

InsightUI.Tabs = {
    init: function () {
        // Collect all elements with 'data-tabs=<target_ID>'
        const tabs = document.querySelectorAll("[data-tabs]");

        tabs.forEach((tabBar) => {
            const tabs = Array.from(tabBar.children[0].children);
            const tabContent = tabBar.children[1];

            document.body.addEventListener('htmx:afterSwap', (event) => {
                if (event.detail.target.id === 'tab-content') {
                    tabContent.focus();
                }
            });

            tabs.forEach((tab, index) => {
                tab.addEventListener('keydown', (e) => {
                    let newIndex = null;
                    if (e.key === 'ArrowRight') {
                        newIndex = (index + 1) % tabs.length;
                    } else if (e.key === 'ArrowLeft') {
                        newIndex = (index - 1 + tabs.length) % tabs.length;
                    } else if (e.key === 'Home') {
                        newIndex = 0;
                    } else if (e.key === 'End') {
                        newIndex = tabs.length - 1;
                    }

                    if (newIndex !== null) {
                        e.preventDefault();
                        tabs[newIndex].focus();
                    }
                });

                tab.addEventListener('click', () => {
                    activateTab(tab);
                });
            });

            function activateTab(selectedTab) {
                tabs.forEach(tab => {
                    if (tab === selectedTab) {
                        tab.setAttribute('aria-selected', 'true');
                        tab.classList.remove('border-gray-300', 'text-primary', 'border-b');
                        tab.classList.add('border-insight-primary', 'text-insight-primary', 'border-b-3');
                        tabContent.setAttribute('aria-label', tab.id);
                    } else {
                        tab.setAttribute('aria-selected', 'false');
                        tab.classList.remove('border-insight-primary', 'text-insight-primary', 'border-b-3');
                        tab.classList.add('border-gray-300', 'text-primary', 'border-b');
                    }
                });
            }
        });
    }
};
