window.InsightUI = window.InsightUI || {};

InsightUI.Dropdown = {
    init: function () {
        const toggleButtons = document.querySelectorAll("[data-dropdown-toggle]");

        toggleButtons.forEach((button) => {
            const targetId = button.getAttribute("data-dropdown-toggle");
            const menu = document.getElementById(targetId);

            if (!menu) return;

            menu.classList.add("absolute", "hidden", "z-50", "mt-2");

            button.addEventListener("click", (event) => {
                event.stopPropagation();
                closeAllDropdowns(); // Close all (other) menus
                menu.classList.toggle("hidden"); // Open current menu
            });
        });

        /* Close all menus on click everywhere */
        document.addEventListener("click", () => {
            closeAllDropdowns();
        });

        /* Close all menus */
        function closeAllDropdowns() {
            const toggleButtons = document.querySelectorAll("[data-dropdown-toggle]");
            toggleButtons.forEach((button) => {
                const targetId = button.getAttribute("data-dropdown-toggle");
                const menu = document.getElementById(targetId);

                if (!menu) return;

                if (menu.classList.contains("hidden")) return;
                menu.classList.add("hidden");
            });
        }

        console.log("Dropdowns: ", toggleButtons);
        console.log("Dropdowns initialized!");
    }
};
