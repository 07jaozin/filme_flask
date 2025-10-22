document.addEventListener("DOMContentLoaded", async () => {

    const container = document.querySelector('.container');
    const registerBtn = document.querySelector('.register-btn');
    const loginBtn = document.querySelector('.login-btn');
    const mensagem_erro = document.querySelector(".erro");
    const modalCodigo = document.getElementById("modal-codigo-cadastro");
    const modalerro = document.getElementById("modal-erro");
    const codigoInput = document.getElementById("codigo-digitado-cadastro");
    const btnVerificar = document.getElementById("verificar-codigo-cadastro");
    const erro_verificacao = document.querySelector("#erro-verificacao-cadastro");
    const btnClose= document.getElementById("close-cadastro");
    const btnCloseErro= document.getElementById("fechar-modal-erro");

    btnClose.addEventListener("click", () => {
        modalCodigo.style.display = "none";
    });
    btnCloseErro.addEventListener("click", () =>{
        modalerro.classList.add('hidden');
    });

    mensagem_erro.style.display = "none";
    erro_verificacao.style.display = "none";

    
    registerBtn.addEventListener('click', () => container.classList.add('active'));
    loginBtn.addEventListener('click', () => container.classList.remove('active'));

    // Mostrar/ocultar senha
    const eye = document.querySelectorAll('.ri-eye-line');
    const senha = document.querySelectorAll('.senha');
    eye.forEach((botao, index) => {
        botao.addEventListener("click", () => {
            senha[index].type = senha[index].type === 'password' ? 'text' : 'password';
        });
    });

    // Impedir espaços na senha
    senha.forEach(input => {
        input.addEventListener("keydown", (event) => {
            if (event.key === ' ') event.preventDefault();
        });
    });

    // Campos de login e cadastro
    const nomeCadastrar = document.getElementById('nome-cadastrar');
    const emailCadastrar = document.getElementById('email-cadastrar');
    const senhaCadastrar = document.getElementById('senha-cadastrar');
    const emailLogin = document.getElementById('email');
    const senhaLogin = document.getElementById('senha');

    const botoes = document.querySelectorAll('.btns');
    botoes.forEach(btn => {
        btn.disabled = true;
        btn.classList.add("desabilitado");
    });

    function verificarCampos() {
        // Verifica campos de cadastro
        if (nomeCadastrar.value.trim() && emailCadastrar.value.trim() && senhaCadastrar.value.trim()) {
            botoes[1].disabled = false;
            botoes[1].classList.remove("desabilitado");
        } else {
            botoes[1].disabled = true;
            botoes[1].classList.add("desabilitado");
        }

        // Verifica campos de login
        if (emailLogin.value.trim() && senhaLogin.value.trim()) {
            botoes[0].disabled = false;
            botoes[0].classList.remove("desabilitado");
        } else {
            botoes[0].disabled = true;
            botoes[0].classList.add("desabilitado");
        }
    }

    // Detecta digitação nos campos
    [nomeCadastrar, emailCadastrar, senhaCadastrar, emailLogin, senhaLogin].forEach(campo => {
        campo.addEventListener('input', verificarCampos);
    });

    // SUBMIT LOGIN
    const login = document.getElementById("login-form");
    login.addEventListener("submit", (e) => {
        e.preventDefault();

        const dadosLogin = new FormData();
        dadosLogin.append("email", emailLogin.value.trim());
        dadosLogin.append("senha", senhaLogin.value.trim());

        fetch('/user/login', {
            method: "POST",
            body: dadosLogin
        })
        .then(res => res.json())
        .then(data => {
            if (data) {
                window.location.href = '/';
            } else {
                mensagem_erro.style.display = "flex";
                mensagem_erro.textContent = data.erro || "Email ou senha incorretos!";
            }
        })
        .catch(err => console.error("Erro no login:", err));
    });

    // SUBMIT CADASTRO
    const cadastro = document.getElementById("cadastro-form");
    cadastro.addEventListener("submit", async (e) => {
        e.preventDefault();
        const emailCadastrarvalue = document.getElementById('email-cadastrar').value;

        const respValida = await fetch("/user/verifica_email_existe", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({"email": emailCadastrarvalue })
            });

        const dataValida = await respValida.json();

        if(dataValida){
            modalerro.classList.remove('hidden');
        }
        else{

        console.log(emailCadastrarvalue)

        

        const res = await fetch("/user/verificar_email_cadastro", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ "email":emailCadastrarvalue })
            });



        const data = await res.json();

        if(!data) throw new Error("erro email enviar");

        modalCodigo.style.display = "flex";

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
                const dadosCadastrar = new FormData();
                dadosCadastrar.append("nome-cadastrar", nomeCadastrar.value.trim());
                dadosCadastrar.append("email-cadastrar", emailCadastrar.value.trim());
                dadosCadastrar.append("senha-cadastrar", senhaCadastrar.value.trim());

                fetch('/user/cadastro', {
                    method: "POST",
                    body: dadosCadastrar
                })
                .then(res => res.json())
                .then(data => {
                    if (data) {
                         modalCodigo.style.display = "none";
                        const modal = document.getElementById("modal-sucesso");
                        modal.classList.remove("hidden");
                    
                        document.getElementById("fechar-modal").addEventListener("click", () => {
                            modal.classList.add("hidden");
                            container.classList.remove("active");
                        });
                    
                        setTimeout(() => {
                            modal.classList.add("hidden");
                            container.classList.remove("active");
                        }, 4000);
                    } else {
                        mensagem_erro.style.display = "flex";
                        mensagem_erro.textContent = data.erro || "Erro ao cadastrar.";
                    }
                })
                .catch(err => console.error("Erro no cadastro:", err));
                }
            });}


    });

    

});
