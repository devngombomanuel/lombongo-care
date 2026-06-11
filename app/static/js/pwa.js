if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => {
    navigator.serviceWorker
      .register("/static/sw.js")
      .then((reg) => console.log("Service Worker registado com sucesso."))
      .catch((err) => console.log("Erro ao registar Service Worker:", err));
  });
}

window.addEventListener("online", () => {
  Swal.fire({
    title: "Ligação Restaurada",
    text: "A sincronizar dados pendentes com o servidor...",
    icon: "success",
    toast: true,
    position: "top-end",
    showConfirmButton: false,
    timer: 3000,
  });
});

window.addEventListener("offline", () => {
  Swal.fire({
    title: "Modo Offline Ativo",
    text: "Pode continuar a consultar o painel. Novos registos serão guardados localmente.",
    icon: "info",
    toast: true,
    position: "top-end",
    showConfirmButton: false,
    timer: 4000,
  });
});
