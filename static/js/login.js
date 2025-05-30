const container = document.querySelector('.container');
const registerBtn = document.querySelector('.register-btn');
const loginBtn = document.querySelector('.login-btn');

registerBtn.addEventListener('click', () => {
    container.classList.add('active');
})

loginBtn.addEventListener('click', () => {
    container.classList.remove('active');
})
const eye = document.querySelectorAll('.ri-eye-line');
const senha = document.querySelectorAll('.senha');
        
eye.forEach( (botao, index) => {
    botao.addEventListener("click", () => {
        if (senha[index].type === 'password') {
                senha[index].type = 'text';
        } 
        else {
               senha[index].type = 'password';}
            })
} )


const inputName = document.querySelectorAll('.nome');
console.log(inputName)
const btn = document.querySelectorAll('.btn');

senha.forEach(button => {
    button.addEventListener("keydown", function(event){
            if(event.key === ' '){
                event.preventDefault();
            }
    })
})



const nomeCadastrar = document.getElementById('nome-cadastrar');
const senhaCadastrar = document.getElementById('senha-cadastrar');
const nomeLogin = document.getElementById('nome');
const senhaLogin = document.getElementById('senha');
const botaoCadastrar = document.querySelectorAll('.btn'); // segundo botão
botaoCadastrar[1].disabled = true;
botaoCadastrar[1].classList.add("desabilitado");
botaoCadastrar[0].disabled = true;
botaoCadastrar[0].classList.add("desabilitado");

function verificarCampos() {
    if(nomeCadastrar.value.trim() === '' || senhaCadastrar.value.trim() === ''){
        botaoCadastrar[1].disabled = true;
        botaoCadastrar[1].classList.add("desabilitado");
    } else {
        botaoCadastrar[1].disabled = false;
        botaoCadastrar[1].classList.remove("desabilitado");
    };
    if(nomeLogin.value.trim() === '' || senhaLogin.value.trim() === ''){
        botaoCadastrar[0].disabled = true;
        botaoCadastrar[0].classList.add("desabilitado");
    } else {
        botaoCadastrar[0].disabled = false;
        botaoCadastrar[0].classList.remove("desabilitado");
    };
}

// Executar verificação sempre que o usuário digitar
nomeCadastrar.addEventListener('input', verificarCampos);
senhaCadastrar.addEventListener('input', verificarCampos);
nomeLogin.addEventListener('input', verificarCampos);
senhaLogin.addEventListener('input', verificarCampos);

// Impede espaço na senha




