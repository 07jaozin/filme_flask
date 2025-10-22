document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("filtrar");
    const pesquisa = document.getElementById("pesquisa");
    const search_input = document.getElementById("search-input");
    const movies = document.getElementById("movies");
    let video = document.querySelector('.video-container');

    pesquisa.addEventListener("submit", async (e) => {
        e.preventDefault();
        await filtrarFilmes();
    })


    // Opcional: busca instantânea ao digitar
    search_input.addEventListener("input", async (e) => {
        movies.innerHTML += '<center><p>Carregando...</p></center>';
        await filtrarFilmes();
        video.classList.remove('show-video');
        
        
    });

   
    form.addEventListener("submit", async (e) => {
        movies.innerHTML += '<center><p>Carregando...</p></center>';
        e.preventDefault(); 
        await filtrarFilmes();
        
    });

    async function filtrarFilmes() {
        
        
        const query = search_input.value;

        const data_inicio = document.getElementById("data_inicio").value;
        const data_fim = document.getElementById("data_fim").value;
        const avaliacao = document.getElementById("avaliacao").value;
        const categoria = document.getElementById("categoria").value;

        
        const parametros = new URLSearchParams({
            campo: query,
            data_inicio: data_inicio,
            data_fim: data_fim,
            avaliacao_filtro: avaliacao,
            categoria_filtro: categoria
        });

        try {
            const response = await fetch(`/filme/lista_filmes_filtrados?${parametros.toString()}`);
            if (!response.ok) throw new Error("Erro ao buscar filmes");

            const data = await response.json();
            movies.innerHTML = ""; 

            if (data.length === 0) {
                movies.innerHTML = `<center><p>Nenhum resultado encontrado!</p></center>`;
                return;
            }

            const div = document.createElement("div");
            div.classList.add("movies-content");
            movies.appendChild(div);

            data.forEach((filme) => {
                const resultadoFilme = `
                <div class="movie-box">
                    <img src="/static/img/${filme.foto}" alt="" class="movie-box-img">
                    <div class="box-text">
                        <h2 class="movie-title">${filme.titulo}</h2>
                        <span class="movie-type">${filme.genero}</span>
                        <a href="/filme/${filme.id}" class="watch-btn">
                            <i class='bx bx-right-arrow'></i>
                        </a>
                    </div>
                </div>`;
                div.innerHTML += resultadoFilme;
            });

        } catch (err) {
            console.error(err);
        }
    }
});
