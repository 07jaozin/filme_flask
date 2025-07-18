 //show
 let playButton = document.querySelector('.play-movie');
 let video = document.querySelector('.video-container');
 let myvideo = document.querySelector('#myvideo');
 let closebtn = document.querySelector('.close-video');


 playButton.onclick = () =>{
  video.classList.add('show-video');

  myvideo.play();
 };
 closebtn.onclick = () =>{
  video.classList.remove('show-video');
  myvideo.pause();

 };

  function mostrarTodos(event) {
    document.querySelectorAll(".comentario-extra").forEach(el => {
      el.classList.remove("hidden");
    });
    // Esconde o botão após clicar
    event.target.style.display = "none";
  }
