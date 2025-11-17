window.InsightUI = window.InsightUI || {};

InsightUI.Modal = {
  init: function () {
    document.querySelectorAll('[data-insight-toggle="modal"]').forEach(button => {
      button.addEventListener('click', function () {
        const targetId = this.getAttribute('data-insight-target');
        const modal = document.getElementById(targetId);
        if (modal) {
          modal.style.display = 'block';
          modal.querySelectorAll('[data-insight-dismiss="modal"]').forEach(closeButton => {
            closeButton.addEventListener('click', function () {
              modal.style.display = 'none';
            });
          });
          InsightUI.utils.trapFocus(modal);
        }
      });
    });

    console.log("Modals initialized!");
  }
};
