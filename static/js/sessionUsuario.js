document.addEventListener("DOMContentLoaded", async () => {
    try{
    const res = await fetch('/user/session');
    console.log("aq")
    const data = await res.json();
    if (data == "nao logado") return;
    const userId = data.id;
    console.log(userId)
    console.log("aq")
    const response = await fetch(`/user/perfil_usuario/${userId}`);
    if (!response.ok) throw new Error("Usuário não encontrado");

    const usuario = await response.json();

    if(document.getElementById("user-link") &&  document.getElementById("user-img")) { 
        const userLink = document.getElementById("user-link");
        const userImg = document.getElementById("user-img");
        userImg.src = '../static/img/padrao.jpg';  
        userLink.href = `/user/pagina_perfil/${usuario.id}`;
        userLink.style.display = "block";
    }
   
    const loginLink = document.querySelector(".sair");
    const loginTitle = document.getElementById("login-title");
    const logar = document.getElementById("logar");

   
    loginLink.style.display = "flex";
    logar.style.display = "none";


    }
    catch (err) {
        console.error("Erro ao carregar perfil do usuário:", err);
    }
})