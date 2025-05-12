const excluir = document.querySelector('.excluir');
const card = document.querySelector('.confirmacao-modal');
const cancelar = document.querySelector('.btn-cancelar');


excluir.addEventListener("click", () => {
    card.classList.add("aparecer");
})

cancelar.addEventListener("click", () =>{
    card.classList.remove("aparecer")
})