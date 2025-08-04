window.InsightUI = window.InsightUI || {};

InsightUI.Sidebar = {
  init: function () {
    const sidebars = document.querySelectorAll('[data-insight-sidebar]');
    if (!sidebars) return;

    for (let sidebar of sidebars)
    {
      const side = sidebar.getAttribute("data-insight-sidebar");
      const openBtn = document.querySelector(`.open-btn[data-sidebar-target="${side}"]`);
      const closeBtn = sidebar.querySelector(".close-btn");

      // Sidebar closes automatically when the mouse leaves the sidebar
      const autoClose = sidebar.getAttribute("data-auto-close") === "true";

      // These classes were added so that the sidebar initially appears closed, but they prevent the sidebar from opening.
      sidebar.classList.remove("ltr:translate-x-full", "rtl:-translate-x-full", "ltr:-translate-x-full", "rtl:translate-x-full");

      // Funktion zum Öffnen der Sidebar
      function openSidebar() {
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
      }

      // Sidebar initial verstecken
      closeSidebar();

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

        // Optional: Schließen, wenn Maus die Sidebar verlässt
        sidebar.addEventListener('mouseleave', () => { closeSidebar(); });
      }

      if (openBtn)
      {
        openBtn.addEventListener('click', () => {
          openSidebar();
          openBtn.classList.toggle("hidden", true);
        });

        if (closeBtn)
        {
          closeBtn.addEventListener('click', () => {
            closeSidebar();
            openBtn.classList.toggle("hidden", false);
          });
        }
      }
    }
  }
};

document.addEventListener('DOMContentLoaded', InsightUI.Sidebar.init);
