document.addEventListener("DOMContentLoaded", () => {
  const forgotLink = document.getElementById("forgot-link");
  const modalForgot = document.getElementById("modal-forgot");
  const modalCodigo = document.getElementById("modal-codigo");
  const btnEnviar = document.getElementById("enviar-codigo");
  const btnVerificar = document.getElementById("verificar-codigo");

  const emailInput = document.getElementById("email-verificar");
  const codigoInput = document.getElementById("codigo-digitado");
  const closes = document.querySelectorAll(".close");
  const erro_recuperacao = document.querySelector("#erro-recuperacao");
  const erro_verificacao = document.querySelector("#erro-verificacao");
  erro_recuperacao.style.display = 'none';
  erro_verificacao.style.display = 'none';

  // Abre o modal
  forgotLink.addEventListener("click", () => {
    modalForgot.style.display = "flex";
  });

  // Fecha modais
  closes.forEach(c => c.addEventListener("click", () => {
    modalForgot.style.display = "none";
    modalCodigo.style.display = "none";
  }));

  // Enviar email para verificação
  btnEnviar.addEventListener("click", async () => {
    const email = emailInput.value.trim();
    if (!email) return alert("Digite um e-mail!");

    const res = await fetch("/user/verifica_email_existe", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email })
    });

    const data = await res.json();

    if (!data) {
      erro_recuperacao.style.display = 'block'
      erro_recuperacao.textContent = 'Esse Email não esta registrado';
    } else {
      alert("Código enviado para seu e-mail!");
      modalForgot.style.display = "none";
      modalCodigo.style.display = "flex";
    }
  });

  // Verificar código digitado
  btnVerificar.addEventListener("click", async () => {
    const codigo = codigoInput.value.trim();

    const res = await fetch("/user/verificar_codigo", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ codigo })
    });

    const data = await res.json();

    if (!data.sucesso) {
      erro_verificacao.style.display = 'block';
      erro_verificacao.textContent = 'Codigo incorreto';
    } else {
     
      modalCodigo.style.display = "none";
      window.location.href = '/user/atualiza_senha';
    }
  });
});
