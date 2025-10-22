document.addEventListener("DOMContentLoaded", async () =>{
    try{
        const loader = document.querySelector(".carr");
       
        
        const home = document.getElementById("home");
        const popular = document.getElementById("slide-populares");
        const show = document.getElementById("slides-show");
        console.log("aqui")

        const fetchFilme = await fetch("/filme/listaFilmes");
        

       
        if(!fetchFilme.ok) throw new Error("Usuário não encontrado");

        const lista = await fetchFilme.json();
        loader.style.display = 'none';

        lista.forEach((filme) => {
            if (filme.categoria == 'home'){
                const dataBr = new Date(filme.lancamento).toLocaleDateString("pt-BR");
                const filmeHome = `
               <img src="/static/img/${filme.foto}" alt="" class="home-img">
                <div class="home-text">
                    <h1 class="home-title">${ filme.titulo }</h1>
                    <p>${ dataBr }</p>
                    <a href="/filme/${ filme.id }" class="watch-btn">
                        <i class='bx bx-right-arrow'></i>
                        <span>Ver mais</span>
                    </a>

                </div>`;
                home.innerHTML += filmeHome;            
            }
            else if (filme.categoria == 'popular'){
                
                const filmePopular = `
                <div class="swiper-slide">
                    <div class="movie-box">
                        <img src="/static/img/${filme.foto}" alt="" class="movie-box-img">
                        <div class="box-text">
                            <h2 class="movie-title">${ filme.titulo }</h2>
                            <span class="movie-type">${ filme.genero }</span>
                            <a href="/filme/${ filme.id }" class="watch-btn play-btn">
                                <i class='bx bx-right-arrow'></i>
                            </a>
                            
                        </div>
                    </div>
                </div>`;
                popular.innerHTML += filmePopular;
            }

            else{
                const filmeShow = `
                <div class="movie-box">
                <img src="/static/img/${filme.foto}" alt="" class="movie-box-img">
                <div class="box-text">
                    <h2 class="movie-title">${ filme.titulo }</h2>
                    <span class="movie-type">${ filme.genero }</span>
                    <a href="/filme/${ filme.id }" class="watch-btn play-btn">
                        <i class='bx bx-right-arrow'></i>
                    </a>
                    
                </div>
            </div>`;
                show.innerHTML += filmeShow;
            }
        })

    }
    catch(err){
        console.error(err);
    }
})