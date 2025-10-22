document.addEventListener("DOMContentLoaded", async () => {
  const perfil_filme = document.getElementById("filme-perfil");
  const body = document.getElementById("body");
  const urlPath = window.location.pathname;
  const partes = urlPath.split("/");
  const id = partes[partes.length - 1];


  try {
    

    // === 1. BUSCAR DADOS DO FILME ===
    const fetchFilme = await fetch(`/filme/getFilme/${id}`);
    if (!fetchFilme.ok) throw new Error("Erro ao buscar filme");
    const dataFilme = await fetchFilme.json();

    const estrelas_cheias = Math.floor(dataFilme.avaliacao);
    const tem_meia = (dataFilme.avaliacao - estrelas_cheias) >= 0.25 && (dataFilme.avaliacao - estrelas_cheias) < 0.75;
    const estrelas_vazias = 5 - estrelas_cheias - (tem_meia ? 1 : 0);
    let estrelasHTML = "";
    for (let i = 0; i < estrelas_cheias; i++) estrelasHTML += `<i class='bx bxs-star'></i>`;
    if (tem_meia) estrelasHTML += `<i class='bx bxs-star-half'></i>`;
    for (let i = 0; i < estrelas_vazias; i++) estrelasHTML += `<i class='bx bx-star'></i>`;
    console.log(estrelasHTML)
    

    // === MONTAR CABEÇALHO DO FILME ===
    perfil_filme.innerHTML = `
      <img src="/static/img/${dataFilme.foto}" alt="" class="play-img">
      <div class="play-text">
          <h2>${dataFilme.titulo}</h2>
          <div class="rating">${new Date(dataFilme.lancamento).toLocaleDateString("pt-BR")}</div>
          <div class="rating">${estrelasHTML}</div>
          
          <div class="tags">

              <span>${dataFilme.genero}</span>
              <span>4K</span>
          </div>
          <br>
      </div>
      <i class='bx bx-right-arrow play-movie'></i>
      <div class="video-container">
          <div class="video-box">
              <video id="myvideo" src="/static/video/${dataFilme.video}" controls></video>
              <i class='bx bx-x close-video'></i>
          </div>
      </div>`;
    body.innerHTML += ` <br><br>
      <center>
        <div class="sinopse container">
          <p>${dataFilme.descricao}</p>
        </div>
      </center>
      <div class="next-page">
        <a href="/static/video/${dataFilme.video}" download class="next-btn">Download do trailer</a>
      </div>`;
      
    // === AVALIAÇÃO (ESTRELAS DO FILME) ===
    const playText = perfil_filme.querySelector(".play-text");
    console.log(playText)
    

    // === 2. BUSCAR CANAIS ===
    const canaisRes = await fetch(`/canais/buscar_canal_id/${id}`);
    if (!canaisRes.ok) throw new Error("Erro ao buscar canais");
    const canais = await canaisRes.json();

    const ondeAssistirHeading = document.createElement("div");
    ondeAssistirHeading.classList.add("heading", "container");
    ondeAssistirHeading.innerHTML = `<h2 class="heading-title">Onde assistir</h2>`;
    body.appendChild(ondeAssistirHeading);

    const canaisContainer = document.createElement("div");
    canaisContainer.classList.add("movies-content", "container");
    body.appendChild(canaisContainer);
    console.log(canais)

    if (canais.length != "erro") {
      canais.forEach(c => {
        const canalBox = document.createElement("div");
        canalBox.classList.add("canais-box");
        canalBox.innerHTML = `
          <img src="/static/img/${c.foto}" data-link="${c.link}" alt="${c.nome}" class="movie-box-img">
        `;
        canaisContainer.appendChild(canalBox);
      });
    } else {
      canaisContainer.innerHTML = `<p>Nenhum canal disponível</p>`;
    }

    canaisContainer.addEventListener("click", (e) => {
      const img = e.target.closest("img[data-link]");
      if (img) window.open(img.dataset.link, "_blank");
    });

    // === 3. BUSCAR COMENTÁRIOS ===
    const comentariosRes = await fetch(`/comentario/${id}`);
    if (!comentariosRes.ok) throw new Error("Erro ao buscar comentários");
    const comentarios = await comentariosRes.json();

    const avaliacaoHeading = document.createElement("div");
    avaliacaoHeading.classList.add("heading", "container");
    avaliacaoHeading.innerHTML = `<h2 class="heading-title">Avaliações</h2>`;
    body.appendChild(avaliacaoHeading);

    if (comentarios == 'nenhum') {
      body.innerHTML += `
      </br>
      </br>
        <center>
          <p class="heading-title">
            Sem Avaliações ainda, seja o primeiro a 
            <span><a style="color: hsl(0, 78%, 43%);" href="/comentarios/${dataFilme.id}">avaliar</a></span>
          </p>
          </br>
          </br>
          </br>
          </br>
          </br>
        </center>`;
    } else {
      comentarios.forEach(async (c, index) => {
        const comentarioDiv = document.createElement("div");
        comentarioDiv.classList.add("comentarios", "container");
        if (index >= 5) comentarioDiv.classList.add("comentario-extra", "hidden");

        const estrelas_cheias = Math.floor(c.avaliacao);
        const tem_meia = (c.avaliacao - estrelas_cheias) >= 0.25 && (c.avaliacao - estrelas_cheias) < 0.75;
        const estrelas_vazias = 5 - estrelas_cheias - (tem_meia ? 1 : 0);
        let estrelasHTML = "";
        for (let i = 0; i < estrelas_cheias; i++) estrelasHTML += `<i class='bx bxs-star'></i>`;
        if (tem_meia) estrelasHTML += `<i class='bx bxs-star-half'></i>`;
        for (let i = 0; i < estrelas_vazias; i++) estrelasHTML += `<i class='bx bx-star'></i>`;

        const fetchIdUsuario = await fetch('/user/session');

        const jsonidUsuario = await fetchIdUsuario.json();

        let idUsuario;

        if(jsonidUsuario != "nao logado"){
          idUsuario = jsonidUsuario.id;
        }
        else{
          idUsuario = 0;
        }

        const editavel = c.id_usuario === idUsuario;
      

        console.log(c.id_usuario)
        console.log(id)

        comentarioDiv.innerHTML = `
          <div class="informacoes">
            <a href="#" class="user">
              <img src="/static/img/${c.foto}" alt="" class="user-img">
            </a>
            <div class="rating">${estrelasHTML}</div>
            ${editavel ? `
              <div class="options-container">
                <button class="options-btn" onclick="toggleMenu(this)">⋮</button>
                <div class="options-menu hidden">
                  <a style="cursor: pointer;" data-id="${c.id}" data-texto="${c.comentario}" data-avaliacao="${c.avaliacao}" data-filme="${id}" onclick="editar_comentario(this)">Editar</a>
                  <button data-filme="${dataFilme.id}" data-id="${c.id}" onclick="excluir_comentario(this)" class="option-item">Excluir</button>
                </div>
              </div>` : ""
            }
          </div>
          <p>${c.comentario}</p>
        `;
        body.appendChild(comentarioDiv);
        body.appendChild(document.createElement("br"));
      });

      if (comentarios.length > 5) {
        const verTodos = document.createElement("div");
        verTodos.classList.add("text-center", "mt-4");
        verTodos.innerHTML = `
          <center>
            <button class="ver-todos-btn" id="ver-todos">Ver todos</button>
          </center>
        `;
        body.appendChild(verTodos);

        document.addEventListener("click", (e) => {
          if (e.target.id === "ver-todos") {
            document.querySelectorAll(".comentario-extra").forEach(c => c.classList.remove("hidden"));
            e.target.style.display = "none";
          }
        });

        body.innerHTML += ""
      }
    }
  } catch (err) {
    console.error("Erro ao carregar página:", err);
    perfil_filme.innerHTML = `<p style="color:red; text-align:center;">Erro ao carregar informações do filme.</p>`;
  }
});
document.addEventListener("click", (e) => {
  // Abrir vídeo
  if (e.target.matches(".play-movie")) {
    const video = document.querySelector(".video-container");
    const myvideo = document.querySelector("#myvideo");
    video.classList.add("show-video");
    myvideo.play();
  }

  // Fechar vídeo
  if (e.target.matches(".close-video")) {
    const video = document.querySelector(".video-container");
    const myvideo = document.querySelector("#myvideo");
    video.classList.remove("show-video");
    myvideo.pause();
  }

  // Acessar link do canal
  const img = e.target.closest("img[data-link]");
  if (img) window.open(img.dataset.link, "_blank");
});

async function abrir_comentarios(){
 const overlay = document.getElementById("comentario-overlay");
  const fechar = document.getElementById("fechar-comentario");
  const enviar = document.getElementById("enviar-comentario");
  const input = document.getElementById("texto-comentario");
  const avaliacao = document.getElementById("avaliacao");
  const comentarios = document.querySelector('.comentarios');
  const fetchIdUsuario = await fetch('/user/session');

  const jsonidUsuario = await fetchIdUsuario.json();

  if(jsonidUsuario == "nao logado") return window.location.href ='/user/login';

  overlay.classList.remove("hidden");
  input.focus();

  // Fecha ao clicar no X ou fora da barra
  fechar.addEventListener("click", () => overlay.classList.add("hidden"));
  overlay.addEventListener("click", (e) => {
    if (e.target === overlay) overlay.classList.add("hidden");
  });

  // Envia comentário
  enviar.addEventListener("click", () => {
    const texto = input.value.trim();
    const estrelas = parseInt(avaliacao.value);

    const dataForm = new FormData();

    dataForm.append("comentario", texto);
    dataForm.append("avaliacao-comentarios", estrelas);

    if (texto.length > 0) {
       const urlPath = window.location.pathname;
       console.log(urlPath)

       const partes = urlPath.split("/");
       console.log(partes)

       const id = partes[partes.length - 1];

      fetch(`/comentario/${id}`, {
        method: "POST",
        body: dataForm
      })
      .then(res => res.json())
      .then(data => {
        console.log("Comentário enviado:", data);
        input.value = "";
        overlay.classList.add("hidden");
        window.location.reload();
      });
    }
  });
}
function editar_comentario(e){
  const comentario = {
    id: e.dataset.id,
    texto: e.dataset.texto,
    avaliacao: e.dataset.avaliacao,
    id_filme: e.dataset.filme
  }
  editarComentario(comentario)
}
function excluir_comentario(e){
  const comentario = {
    id: e.dataset.id,
    id_filme: e.dataset.filme
  }
  excluirComentario(comentario, e.closest('.comentarios'))
}

function excluirComentario(comentario, comentarioDiv){
    fetch(`/comentario/${comentario.id}/${comentario.id_filme}`,
      {
        method: "DELETE"
      }
    )
    .then( res => res.json() )
    .then( data => {
      if(data.sucesso){
        if(comentarioDiv) comentarioDiv.remove();
        else{
          console.log(comentarioDiv)
        }
      }
    })
    .catch( err => {
      console.error(err)
    })
}

// Função para abrir overlay com dados do comentário para edição
function editarComentario(comentario) {
  const overlay = document.getElementById("comentario-overlay");
  const input = document.getElementById("texto-comentario");
  const select = document.getElementById("avaliacao");
  const enviarBtn = document.getElementById("enviar-comentario");
  const fecharBtn = document.getElementById("fechar-comentario");  
  overlay.classList.remove("hidden");
  input.focus();
  input.value = comentario.texto;         
  select.value = comentario.avaliacao; 


  // Remove event listener anterior para evitar duplicidade
  enviarBtn.replaceWith(enviarBtn.cloneNode(true));
  const novoEnviarBtn = document.getElementById("enviar-comentario");

  fecharBtn.addEventListener("click", () => overlay.classList.add("hidden"));
  overlay.addEventListener("click", (e) => {
    if (e.target === overlay) overlay.classList.add("hidden");
  });

  novoEnviarBtn.addEventListener("click", async () => {
    const texto = input.value.trim();
    const estrelas = select.value;

    if (!texto) return alert("Digite um comentário");

    const dataForm = new FormData();
    dataForm.append("comentario-editar", texto);
    dataForm.append("avaliacao-editar", estrelas);

    // Aqui você passa o ID do comentário que está editando
    const res = await fetch(`/comentario/${comentario.id}/${comentario.id_filme}`, {
      method: "PUT",
      body: dataForm
    });

    const resultado = await res.json();

    if (resultado.sucesso) {
      window.location.reload();
      overlay.classList.add("hidden");
      // Atualiza o comentário na página (pode refazer fetch ou atualizar o DOM diretamente)
    } else {
      alert("Erro ao atualizar comentário!");
    }
  });
}


