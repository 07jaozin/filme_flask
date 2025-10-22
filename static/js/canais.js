document.addEventListener("DOMContentLoaded", async () => {
        const tbody = document.getElementById("canais-tbody");
        const formCadastro = document.getElementById("form-cadastro-canal");
        const modalEditar = document.getElementById("modal-editar-canal");
        const formEditar = document.getElementById("form-editar-canal");
        const modalSucesso = document.getElementById("modal-sucesso-canal");
        const btnAtualizar = document.getElementById("btn-atualizar-canal");

        // Buscar canais
        async function listarCanais() {
            const res = await fetch("/canais/getCanais"); // Assumindo endpoint para listar canais
            const canais = await res.json();
            tbody.innerHTML = "";
            canais.forEach(c => {
                tbody.innerHTML += `
                    <tr>
                        <td>${c.id}</td>
                        <td>${c.nome}</td>
                        <td><a href="${c.link}" target="_blank">${c.link}</a></td>
                        <td><img src="${c.foto_url || ''}" alt="${c.nome}" style="width: 50px; height: 30px; object-fit: cover; border-radius: 4px;" onerror="this.style.display='none'"></td>
                        <td>
                            <button class="edit-btn" onclick="editarCanal(${c.id})">Editar</button>
                            <button class="delete-btn" onclick="excluirCanal(${c.id})">Excluir</button>
                        </td>
                    </tr>
                `;
            });
        }

        await listarCanais();

        // Cadastrar canal via fetch
        formCadastro.addEventListener("submit", async (e) => {
            e.preventDefault();
            const formData = new FormData(formCadastro);
            const res = await fetch("/canais", {
                method: "POST",
                body: formData
            });
            const data = await res.json();
            if (data.sucesso) {
                alert("Canal cadastrado!");
                formCadastro.reset();
                listarCanais();
            } else {
                alert(data.erro || "Erro ao cadastrar canal");
            }
        });

        // Função para mostrar preview de foto
        function mostrarPreviewFoto(fotoAtual, previewElement, placeholderElement) {
            if (fotoAtual && fotoAtual !== '') {
                previewElement.querySelector('img').src = fotoAtual;
                previewElement.querySelector('img').style.display = 'block';
                placeholderElement.style.display = 'none';
            } else {
                previewElement.querySelector('img').style.display = 'none';
                placeholderElement.style.display = 'block';
            }
        }

        // Editar canal (Melhorado com preview)
        window.editarCanal = async (id) => {
            modalEditar.classList.remove("hidden");
            btnAtualizar.disabled = true;
            btnAtualizar.textContent = "Carregando...";

            try {
                const res = await fetch(`/canais/getCanal/${id}`); // Assumindo endpoint para buscar canal
                const c = await res.json();

                // Preencher campos
                document.getElementById("editar-id-canal").value = c.id;
                document.getElementById("editar-nome").value = c.nome || '';
                document.getElementById("editar-link").value = c.link || '';

                // Mostrar preview da foto atual (assumindo que o backend retorna URL em c.foto_url)
                mostrarPreviewFoto(`../static/img/${c.foto}`, document.getElementById("editar-foto-preview"), document.getElementById("editar-foto-placeholder"));

                // Listener para nova foto (preview dinâmico)
                document.getElementById("editar-foto").addEventListener('change', function(e) {
                    const file = e.target.files[0];
                    if (file) {
                        const reader = new FileReader();
                        reader.onload = function(e) {
                            document.getElementById("editar-foto-img").src = e.target.result;
                            document.getElementById("editar-foto-img").style.display = 'block';
                            document.getElementById("editar-foto-placeholder").style.display = 'none';
                        };
                        reader.readAsDataURL(file);
                        document.getElementById("manter-foto").checked = false;
                    }
                });

            } catch (error) {
                alert("Erro ao carregar dados do canal: " + error.message);
                modalEditar.classList.add("hidden");
            } finally {
                btnAtualizar.disabled = false;
                btnAtualizar.textContent = "Atualizar";
            }
        };

        // Fechar modal editar
        document.getElementById("fechar-editar-canal").addEventListener("click", () => {
            modalEditar.classList.add("hidden");
            formEditar.reset();
        });

        document.getElementById("btn-cancelar-canal").addEventListener("click", () => {
            modalEditar.classList.add("hidden");
            formEditar.reset();
        });

        // Fechar modal clicando fora
        window.addEventListener('click', (e) => {
            if (e.target === modalEditar) {
                modalEditar.classList.add("hidden");
                formEditar.reset();
            }
        });

        // Atualizar canal
        formEditar.addEventListener("submit", async (e) => {
            e.preventDefault();

            // Verificar campos obrigatórios
            const nome = document.getElementById("editar-nome").value.trim();
            const link = document.getElementById("editar-link").value.trim();

            if (!nome || !link) {
                alert("Por favor, preencha todos os campos obrigatórios.");
                return;
            }

            btnAtualizar.disabled = true;
            btnAtualizar.textContent = "Atualizando...";

            const formData = new FormData(formEditar);
            const id = document.getElementById("editar-id-canal").value;
            try {
                const res = await fetch(`/canais/${id}`, {
                    method: "PUT",
                    body: formData
                });
                const data = await res.json();
                if (data.sucesso) {
                    modalEditar.classList.add("hidden");
                    formEditar.reset();
                    modalSucesso.classList.remove("hidden");
                    setTimeout(() => modalSucesso.classList.add("hidden"), 2000);
                    listarCanais();
                } else {
                    alert(data.erro || "Erro ao atualizar canal");
                }
            } catch (error) {
                alert("Erro de conexão: " + error.message);
            } finally {
                btnAtualizar.disabled = false;
                btnAtualizar.textContent = "Atualizar";
            }
        });

        // Fechar modal de sucesso
        document.getElementById("fechar-modal-sucesso-canal").addEventListener("click", () => {
            modalSucesso.classList.add("hidden");
        });

        // Excluir canal
        window.excluirCanal = async (id) => {
            if (!confirm("Deseja realmente excluir este canal?")) return;
            const res = await fetch(`/canais/${id}`, { method: "DELETE" });
            const data = await res.json();
            if (data.sucesso) {
                listarCanais();
                modalSucesso.innerHTML = '<div class="modal-content"><span class="close" id="fechar-modal-sucesso-canal">&times;</span><h3>Excluído com sucesso!</h3></div>';
                modalSucesso.classList.remove("hidden");
                setTimeout(() => modalSucesso.classList.add("hidden"), 2000);
            } else {
                alert(data.erro || "Erro ao excluir canal");
            }
        };

        
        document.addEventListener('click', (e) => {
            if (e.target.id === 'fechar-modal-sucesso-canal') {
                modalSucesso.classList.add("hidden");
            }
        });
    });