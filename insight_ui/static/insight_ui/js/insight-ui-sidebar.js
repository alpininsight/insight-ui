window.InsightUI = window.InsightUI || {};

InsightUI.Sidebar = {
  init: function () {
    const sidebar_wrappers = document.querySelectorAll('[data-insight-sidebar]');
    if (!sidebar_wrappers) return;

    for (let wrapper of sidebar_wrappers)
    {
      const side = wrapper.getAttribute("data-insight-sidebar");
      const sidebar = wrapper.getElementsByTagName("aside")[0];
      const openBtn = document.querySelector(`.open-btn[data-sidebar-target="${side}"]`);
      wrapper.querySelectorAll('[data-insight-dismiss="sidebar"]').forEach(closeButton => {
        closeButton.addEventListener('click', function () {
          closeSidebar();
        });
      });

      // Sidebar closes automatically when the mouse leaves the sidebar
      const autoClose = sidebar.getAttribute("data-auto-close") === "true";

      // Sidebar initial verstecken
      initSidebar();
      function initSidebar() {
        if (document.documentElement.dir === "rtl")
        {
          if (side == "right") sidebar.style.transform = 'translateX(-100%)';
          else if (side == "left") sidebar.style.transform = 'translateX(100%)';
        }
        else
        {
          if (side == "right") sidebar.style.transform = 'translateX(100%)';
          else if (side == "left") sidebar.style.transform = 'translateX(-100%)';
        }
      }

      // Funktion zum Öffnen der Sidebar
      function openSidebar() {
        wrapper.classList.remove("hidden");
        InsightUI.utils.trapFocus(wrapper);
        sidebar.style.transform = 'translateX(0)';
      }

      // Funktion zum Schließen der Sidebar
      function closeSidebar() {
        if (document.documentElement.dir === "rtl")
        {
          if (side == "right") sidebar.style.transform = 'translateX(-100%)';
          else if (side == "left") sidebar.style.transform = 'translateX(100%)';
        }
        else
        {
          if (side == "right") sidebar.style.transform = 'translateX(100%)';
          else if (side == "left") sidebar.style.transform = 'translateX(-100%)';
        }

        sidebar.addEventListener('transitionend', function(event) {
          // Todo: sometimes the transformation gets skipped, find fix
          // if (event.propertyName === 'transform' && sidebar.style.transform === 'translateX(-100%)') {
          //   // Wenn die Transformation abgeschlossen ist und der Wert stimmt, den Button sichtbar machen
          // }

          wrapper.classList.add("hidden");

          if (openBtn)
            openBtn.classList.toggle("hidden", false);
        }, { once: true });
      }

      if (autoClose)
      {
        // Öffnen, wenn Maus nahe an der Fenster Seite ist
        document.addEventListener('mousemove', (e) => {
          const xThreshold = 50; // Pixel Abstand vom Rand
          const yThreshold = 64 // Pixel Abstand vom oberen Rand (wird durch Navbar bestimmt)

          if (e.clientY > yThreshold)
          {
            if (document.documentElement.dir === "rtl")
            {
              if (side == "right" && e.clientX < xThreshold) { openSidebar(); }
              else if (side == "left" && window.innerWidth - e.clientX < xThreshold) { openSidebar(); }
            }
            else
            {
              if (side == "right" && window.innerWidth - e.clientX < xThreshold) { openSidebar(); }
              else if (side == "left" && e.clientX < xThreshold) { openSidebar(); }
            }
          }
        });

        // Schließen, wenn Maus die Sidebar verlässt
        sidebar.addEventListener('mouseleave', () => { closeSidebar(); });
      }

      if (openBtn)
      {
        openBtn.addEventListener('click', () => {
          openSidebar();
          openBtn.classList.toggle("hidden", true);
        });
      }
    }
  }
};

document.addEventListener('DOMContentLoaded', InsightUI.Sidebar.init);
