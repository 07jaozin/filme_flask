   
    document.getElementById('data').addEventListener('input', function (e) {
  let valor = e.target.value;

  
  valor = valor.replace(/\D/g, '');

 
  if (valor.length > 2 && valor.length <= 4) {
    valor = valor.slice(0, 2) + '/' + valor.slice(2);
  } else if (valor.length > 4) {
    valor = valor.slice(0, 2) + '/' + valor.slice(2, 4) + '/' + valor.slice(4, 8);
  }

 
  valor = valor.slice(0, 10);

  e.target.value = valor;
});

const avaliacao = document.querySelector('#avaliacao');

avaliacao.addEventListener("keydown", function(event) {
  const key = event.key;

 
  if (
    (key >= '0' && key <= '9') || 
    key === '.' ||
    key === 'Backspace' || 
    key === 'Delete' || 
    key === 'ArrowLeft' || 
    key === 'ArrowRight' || 
    key === 'Tab'
  ) {
    const valorAtual = avaliacao.value;
    const novoValor = valorAtual + key;

    // Permitir digitação se resultado for menor ou igual a 5
    const numero = parseFloat(novoValor);
    if (numero > 5) {
      event.preventDefault();
    }
  } else {
    // Bloquear qualquer tecla que não seja número, ponto ou controle
    event.preventDefault();
  }
});

