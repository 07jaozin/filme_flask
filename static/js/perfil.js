document.addEventListener("DOMContentLoaded", async () => {
    const perfilCard = document.getElementById("perfil-card");
    const perfilFoto = document.getElementById("perfil-foto");
    const perfilNome = document.getElementById("perfil-nome");
    const perfilEmail = document.getElementById("perfil-email");
    const remover_foto = document.getElementById("remover-foto");

    const editarBtn = document.getElementById("editar-perfil-btn");
    const modalEditar = document.getElementById("modal-editar");
    const fecharEditar = document.getElementById("fechar-editar");

    const editarForm = document.getElementById("editar-perfil-form");
    const inputNome = document.getElementById("editar-nome");
    const inputEmail = document.getElementById("editar-email");
    const inputSenha = document.getElementById("editar-senha");

    const modalCodigo = document.getElementById("modal-codigo");
    const codigoInput = document.getElementById("codigo-verificacao");
    const btnVerificar = document.getElementById("verificar-codigo");
    const erroVerificacao = document.getElementById("erro-verificacao");

    const modalSucesso = document.getElementById("modal-sucesso");
    const fecharSucesso = document.getElementById("fechar-sucesso");

    // Pega o ID do usuário da URL
    const urlParts = window.location.pathname.split("/");
    const userId = urlParts[urlParts.length - 1];

    // Carregar dados do usuário
    const perfilRes = await fetch(`/user/perfil_usuario/${userId}`);
    const usuario = await perfilRes.json();

    perfilFoto.src = `/static/img/${usuario.foto}`;
    perfilNome.textContent = usuario.nome;
    perfilEmail.textContent = usuario.email;

    remover_foto.addEventListener("click", async () => {
        fetch(`/user/foto/${userId}`,
            {
                method: 'DELETE'
            }
        )
        .then( res => res.json())
        .then(data => {
            if(data.sucesso){
                perfilFoto.src = '/static/img/padrao.jpg';
            }
            else{
                console.log("erro para remover a foto");
            }
        })
        .catch(err => {
            console.error(err)
        })
    })

    // Abrir modal de edição
    editarBtn.addEventListener("click", () => {
        inputNome.value = usuario.nome;
        inputEmail.value = usuario.email;
        inputSenha.value = usuario.senha;

        modalEditar.classList.remove("hidden");
    });

    fecharEditar.addEventListener("click", () => {
        modalEditar.classList.add("hidden");
    });

    // Submit edição → envia código de verificação
    editarForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const email = inputEmail.value.trim();

        // Envia email com código de verificação
        const res = await fetch("/user/verificar_email", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({email})
        });

        const data = await res.json();
        if(!data.sucesso){
            alert(data.erro || "Erro ao enviar código de verificação");
            return;
        }

        modalEditar.classList.add("hidden");
        modalCodigo.classList.remove("hidden");
    });

    // Verificar código
    btnVerificar.addEventListener("click", async () => {
        const codigo = codigoInput.value.trim();

        const res = await fetch("/user/verificar_codigo", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({codigo})
        });

        const data = await res.json();
        if(!data.sucesso){
            erroVerificacao.style.display = "block";
            erroVerificacao.textContent = "Código incorreto!";
            return;
        }

        // Código correto → atualiza o perfil
        const formData = new FormData(editarForm);
        

        const atualizarRes = await fetch(`/user/${userId}`, {
            method: "PUT",
            body: formData
        });

        const resultado = await atualizarRes.json();
        if(resultado){
            modalCodigo.classList.add("hidden");
            modalSucesso.classList.remove("hidden");
        }
    });

    fecharSucesso.addEventListener("click", () => {
        modalSucesso.classList.add("hidden");
        window.location.reload();
    });
});
