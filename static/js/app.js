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

