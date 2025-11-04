window.InsightUI = window.InsightUI || {};

InsightUI.Collapsible = {
  init: function () {
    const toggleButtons = document.querySelectorAll('[data-insight-toggle="collapsible"]')
    toggleButtons.forEach(button => {
      if (!button.dataset.initialized) {
        button.addEventListener('click', function () {
          const targetId = this.getAttribute('data-insight-target');
          const targetEl = document.getElementById(targetId);
          if (targetEl) {
            targetEl.classList.toggle("hidden");
          }
        });

        button.dataset.initialized = "true";
      }
    });

    console.log("Collapsible: ", toggleButtons);
    console.log("Collapsible initialized!");
  }
};
