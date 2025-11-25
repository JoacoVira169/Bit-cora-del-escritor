window.addEventListener("load", () => {
  const welcome = document.getElementById("welcome");
  if (!welcome) return;

  // Arranca oculto
  welcome.classList.remove("show");

  // Espera y boom
  setTimeout(() => {
    welcome.classList.add("show");

    // Confeti sincronizado
    setTimeout(() => {
      if (typeof confetti === "function") {
        const rect = welcome.getBoundingClientRect();
        const x = (rect.left + rect.width / 2) / window.innerWidth;
        const y = (rect.top + rect.height / 2) / window.innerHeight;

        confetti({
          particleCount: 140,
          spread: 70,
          startVelocity: 45,
          scalar: 0.9,
          origin: { x, y } // centrado en el título
        });
      }
    }, 220);
  }, 200);
});



document.addEventListener('DOMContentLoaded', () => {
  const menuButtons = document.querySelectorAll('.menu-button');

  menuButtons.forEach(button => {
    button.addEventListener('click', (e) => {
      const targetPanelId = button.getAttribute('aria-controls');
      const targetPanel = document.getElementById(targetPanelId);

      if (!targetPanel) return;

      // Cerrar otros paneles abiertos
      document.querySelectorAll('.mega-panel.open').forEach(openPanel => {
        if (openPanel.id !== targetPanelId) {
          openPanel.classList.remove('open');
          // Actualizar el aria-expanded del botón correspondiente
          const correspondingButton = document.querySelector(`[aria-controls="${openPanel.id}"]`);
          if (correspondingButton) {
            correspondingButton.setAttribute('aria-expanded', 'false');
          }
        }
      });

      // Alternar el panel actual
      targetPanel.classList.toggle('open');
      const isExpanded = targetPanel.classList.contains('open');
      button.setAttribute('aria-expanded', isExpanded.toString());

      e.stopPropagation();
    });
  });

  // Cerrar paneles si se hace clic fuera
  document.addEventListener('click', (e) => {
    if (!e.target.closest('.navbar-menu') && !e.target.closest('.mega-panel')) {
      document.querySelectorAll('.mega-panel.open').forEach(openPanel => {
        openPanel.classList.remove('open');
        const correspondingButton = document.querySelector(`[aria-controls="${openPanel.id}"]`);
        if (correspondingButton) {
          correspondingButton.setAttribute('aria-expanded', 'false');
        }
      });
    }
  });

  // Cerrar con la tecla Escape
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      document.querySelectorAll('.mega-panel.open').forEach(openPanel => {
        openPanel.classList.remove('open');
        const correspondingButton = document.querySelector(`[aria-controls="${openPanel.id}"]`);
        if (correspondingButton) {
          correspondingButton.setAttribute('aria-expanded', 'false');
        }
      });
    }
  });
});

(function(){
  document.addEventListener('DOMContentLoaded', function(){
    const bar = document.querySelector('.accessibility-bar');
    const handle = document.querySelector('.acc-handle');

    if (!bar || !handle) return;

    handle.addEventListener('click', (e) => {
      e.preventDefault();
      bar.classList.toggle('open');
    });

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') bar.classList.remove('open');
    });

    document.addEventListener('click', (e) => {
      if (!bar.classList.contains('open')) return;
      if (!bar.contains(e.target) && e.target !== handle) {
        bar.classList.remove('open');
      }
    });
  });
})();