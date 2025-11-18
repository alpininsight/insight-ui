window.InsightUI = window.InsightUI || {};

InsightUI.SelectLanguage = {
  init: function () {
    const languageSelect = document.getElementById('language-select');
    if (!languageSelect) return;

    languageSelect.addEventListener('change', function () {
      const selectedLanguage = this.value;
      InsightUI.SelectLanguage.changeLanguage(selectedLanguage);
    });

    debugLog("Language Select initialized!");
  },

  changeLanguage: function (languageCode) {
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = '/i18n/setlang/';
    form.style.display = 'none';

    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    const csrfHiddenInput = document.createElement('input');
    csrfHiddenInput.type = 'hidden';
    csrfHiddenInput.name = 'csrfmiddlewaretoken';
    csrfHiddenInput.value = csrfToken;
    form.appendChild(csrfHiddenInput);

    const languageInput = document.createElement('input');
    languageInput.type = 'hidden';
    languageInput.name = 'language';
    languageInput.value = languageCode;
    form.appendChild(languageInput);

    const nextInput = document.createElement('input');
    nextInput.type = 'hidden';
    nextInput.name = 'next';
    nextInput.value = window.location.pathname + window.location.search;
    form.appendChild(nextInput);

    document.body.appendChild(form);
    form.submit();
  }
};
