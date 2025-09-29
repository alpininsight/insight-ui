window.InsightUI = window.InsightUI || {};

InsightUI.Collapsible = {
  init: function () {
    document.querySelectorAll('[data-insight-toggle="collapsible"]').forEach(button => {
      button.addEventListener('click', function () {
        const targetId = this.getAttribute('data-insight-target');
        const targetEl = document.getElementById(targetId);
        if (targetEl) {
          targetEl.classList.toggle("hidden");
        }
      });
    });

    console.log("Collapsible initialized!");
  }
};
