


function togglePassword(inputId) {
            const input = document.getElementById(inputId);
            const toggleBtn = input.nextElementSibling; // O botão toggle
            const icon = toggleBtn.querySelector('i');

            if (input.type === 'password') {
                input.type = 'text';
                icon.classList.remove('fa-eye-slash');
                icon.classList.add('fa-eye');
            } else {
                input.type = 'password';
                icon.classList.remove('fa-eye');
                icon.classList.add('fa-eye-slash');
            }
        }

        // Validação básica no submit
        document.getElementById('passwordForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const newPassword = document.getElementById('newPassword').value;
            const confirmPassword = document.getElementById('confirmPassword').value;
            const newPasswordError = document.getElementById('newPasswordError');
            const confirmPasswordError = document.getElementById('confirmPasswordError');

            // Reset erros
            newPasswordError.style.display = 'none';
            confirmPasswordError.style.display = 'none';

            let isValid = true;

            if (newPassword.length < 6) {
                newPasswordError.style.display = 'block';
                isValid = false;
            }

            if (newPassword !== confirmPassword) {
                confirmPasswordError.style.display = 'block';
                isValid = false;
            }

            if (isValid) {
                const dadosSenha = new FormData();
                dadosSenha.append("nova-senha", newPassword);
                fetch('/user/atualiza_senha', {
                    method: 'PUT',
                    body: dadosSenha
                })
                .then( res => res.json())
                .then( data => {
                    if(data){
                        const modal = document.getElementById("modal-sucesso");
                        modal.classList.remove("hidden");

                        document.getElementById("fechar-modal").addEventListener("click", () => {
                            window.location.href = '/user/login';
                        });
                    
                        setTimeout(() => {
                            window.location.href = '/user/login';
                        }, 6000);
                    }
                })
            }
        });

        // Validação em tempo real para confirmação
        document.getElementById('confirmPassword').addEventListener('input', function() {
            const newPassword = document.getElementById('newPassword').value;
            const confirmPassword = this.value;
            const confirmPasswordError = document.getElementById('confirmPasswordError');

            if (confirmPassword && newPassword !== confirmPassword) {
                confirmPasswordError.style.display = 'block';
            } else {
                confirmPasswordError.style.display = 'none';
            }
        });