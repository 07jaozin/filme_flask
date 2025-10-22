document.addEventListener("DOMContentLoaded", async () => {

  const checkbox_canais = document.getElementById("checkbox-canais");

  const canaisGet = await fetch('/canais/getCanais');

  const dataCanaisGet = await canaisGet.json();

  if(dataCanaisGet){
    const checkbox_canais = document.getElementById("checkbox-canais");
    dataCanaisGet.forEach((e) => {
        console.log(e.nome)
        checkbox_canais.innerHTML += `
        <label class="custom-checkbox" style="color: #000000;">
            <input type="checkbox" name="canais" value="${e.id}">
            <span class="checkmark"></span>${e.nome}
        </label>`
    })
  }

  const tbody = document.getElementById("filmes-tbody");
  const formCadastro = document.getElementById("form-cadastro-filme");
  const modalEditar = document.getElementById("modal-editar");
  const formEditar = document.getElementById("form-editar-filme");
  const modalSucesso = document.getElementById("modal-sucesso");
  const btnAtualizar = document.getElementById("btn-atualizar");

  // Buscar filmes
  async function listarFilmes() {
    const res = await fetch("/filme/listaFilmes");
    const filmes = await res.json();
    tbody.innerHTML = "";
    filmes.forEach(f => {
  
      tbody.innerHTML += `
        <tr>
          <td>${f.id}</td>
          <td>${f.titulo}</td>
          <td>${f.categoria}</td>
          <td>${new Date(f.lancamento).toLocaleDateString("pt-BR")}</td>
          <td>${f.genero}</td>
          <td>
            <button class="edit-btn" onclick="editarFilme(${f.id})">Editar</button>
            <button class="delete-btn" onclick="excluirFilme(${f.id})">Excluir</button>
          </td>
        </tr>
      `;
    });
  }

  await listarFilmes();

  // Cadastrar filme via fetch
  formCadastro.addEventListener("submit", async (e) => {
    e.preventDefault();
    const formData = new FormData(formCadastro);
    const res = await fetch("/filme/", {
      method: "POST",
      body: formData
    });
    const data = await res.json();
    if (data.sucesso) {
      alert("Filme cadastrado!");
      formCadastro.reset();
      listarFilmes();
    } else {
      alert(data.erro || "Erro ao cadastrar filme");
    }
  });

  // Função para mostrar preview de arquivo
  function mostrarPreview(arquivoAtual, elementoPreview, placeholder, isImage = true) {
    if (arquivoAtual && arquivoAtual !== '') {
      if (isImage) {
        elementoPreview.querySelector('img').src = arquivoAtual;
        elementoPreview.querySelector('img').style.display = 'block';
      } else {
        elementoPreview.querySelector('video').src = arquivoAtual;
        elementoPreview.querySelector('video').style.display = 'block';
      }
      placeholder.style.display = 'none';
    } else {
      if (isImage) {
        elementoPreview.querySelector('img').style.display = 'none';
      } else {
        elementoPreview.querySelector('video').style.display = 'none';
      }
      placeholder.style.display = 'block';
    }
  }

  // Editar filme (Melhorado com previews e validações)
  window.editarFilme = async (id) => {
    modalEditar.classList.remove("hidden");
    btnAtualizar.disabled = true;
    btnAtualizar.textContent = "Carregando...";

    try {
      const res = await fetch(`/filme/getFilme/${id}`);
      const f = await res.json();

      // Preencher campos básicos
      document.getElementById("editar-id").value = f.id;
      document.getElementById("editar-titulo").value = f.titulo || '';
      document.getElementById("editar-genero").value = f.genero || '';
      document.getElementById("editar-categoria").value = f.categoria || 'home';
      document.getElementById("editar-data").value = f.lancamento ? new Date(f.lancamento).toISOString().split('T')[0] : ''; // Formato YYYY-MM-DD
      document.getElementById("editar-descricao").value = f.descricao || '';

      // Mostrar previews de arquivos atuais (assumindo que o backend retorna URLs em f.foto_url e f.video_url)
      mostrarPreview(`../static/img/${f.foto}`, document.getElementById("editar-foto-preview"), document.getElementById("editar-foto-placeholder"), true);
      mostrarPreview(`../static/video/${f.video}`, document.getElementById("editar-video-preview"), document.getElementById("editar-video-placeholder"), false);
          
            // Buscar canais do filme
            // 1. Buscar todos os canais
      const canaisRes = await fetch(`/canais/getCanais`);
      const canais = await canaisRes.json();
          
      // 2. Buscar canais que este filme já possui
      const canaisDoFilmeRes = await fetch(`/canais/buscar_canal_id/${f.id}`);
      const canaisDoFilme = await canaisDoFilmeRes.json(); // retorna algo como [{id:1, nome:"Netflix"}, {id:2, nome:"Prime"}]
          
      // 3. Extrair os ids dos canais do filme
      const idsCanaisDoFilme = canaisDoFilme.map(c => c.id);
          
      // 4. Montar checkboxes com o "checked" correto
      const container = document.getElementById("editar-checkbox-canais");
      container.innerHTML = "";
      canais.forEach(c => {
        const estaSelecionado = idsCanaisDoFilme.includes(c.id) ? "checked" : "";
        container.innerHTML += `
          <label class="custom-checkbox">
            <input type="checkbox" name="canais-editar" value="${c.id}" ${estaSelecionado}>
            <span class="checkmark"></span>${c.nome}
          </label>
        `;
      });
      

      // Listeners para novos arquivos (preview dinâmico)
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

      document.getElementById("editar-video").addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
          const reader = new FileReader();
          reader.onload = function(e) {
            document.getElementById("editar-video-player").src = e.target.result;
            document.getElementById("editar-video-player").style.display = 'block';
            document.getElementById("editar-video-placeholder").style.display = 'none';
          };
          reader.readAsDataURL(file);
          document.getElementById("manter-video").checked = false;
        }
      });

    } catch (error) {
      alert("Erro ao carregar dados do filme: " + error.message);
      modalEditar.classList.add("hidden");
    } finally {
      btnAtualizar.disabled = false;
      btnAtualizar.textContent = "Atualizar";
    }
  };

  // Fechar modal
  document.getElementById("fechar-editar").addEventListener("click", () => {
    modalEditar.classList.add("hidden");
    formEditar.reset(); // Limpar form ao fechar
  });

  document.getElementById("btn-cancelar").addEventListener("click", () => {
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

  // Validação simples antes de submit
  formEditar.addEventListener("submit", async (e) => {
    e.preventDefault();

    // Verificar campos obrigatórios
    const titulo = document.getElementById("editar-titulo").value.trim();
    const genero = document.getElementById("editar-genero").value.trim();
    const categoria = document.getElementById("editar-categoria").value;
    const data = document.getElementById("editar-data").value;
    const descricao = document.getElementById("editar-descricao").value.trim();

    if (!titulo || !genero || !categoria || !data || !descricao) {
      alert("Por favor, preencha todos os campos obrigatórios.");
      return;
    }

    btnAtualizar.disabled = true;
    btnAtualizar.textContent = "Atualizando...";

    const formData = new FormData(formEditar);
    const id = document.getElementById("editar-id").value;
    try {
      const res = await fetch(`/filme/${id}`, {
        method: "PUT",
        body: formData
      });
      const data = await res.json();
      if (data.sucesso) {
        modalEditar.classList.add("hidden");
        formEditar.reset();
        modalSucesso.classList.remove("hidden");
        setTimeout(() => modalSucesso.classList.add("hidden"), 2000);
        listarFilmes();
      } else {
        alert(data.erro || "Erro ao atualizar filme");
      }
    } catch (error) {
      alert("Erro de conexão: " + error.message);
    } finally {
      btnAtualizar.disabled = false;
      btnAtualizar.textContent = "Atualizar";
    }
  });

  // Fechar modal de sucesso
  document.getElementById("fechar-modal-sucesso").addEventListener("click", () => {
    modalSucesso.classList.add("hidden");
  });

  // Excluir filme
  window.excluirFilme = async (id) => {
    if (!confirm("Deseja realmente excluir este filme?")) return;
    const res = await fetch(`/filme/${id}`, { method: "DELETE" });
    const data = await res.json();
    if (data.sucesso) {
      listarFilmes();
      modalSucesso.innerHTML = '<div class="modal-content"><span class="close" id="fechar-modal-sucesso">&times;</span><h3>Excluído com sucesso!</h3></div>'; // Atualizar texto para exclusão
      modalSucesso.classList.remove("hidden");
      setTimeout(() => modalSucesso.classList.add("hidden"), 2000);
    } else {
      alert(data.erro || "Erro ao excluir filme");
    }
  };

  // Re-adicionar listener para fechar sucesso após exclusão
  document.addEventListener('click', (e) => {
    if (e.target.id === 'fechar-modal-sucesso') {
      modalSucesso.classList.add("hidden");
    }
  });
});