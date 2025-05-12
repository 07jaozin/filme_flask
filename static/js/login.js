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
