CREATE DATABASE if not exists filmes;

use filmes;





create table if not exists filme(
	id INT auto_increment primary key,
    titulo VARCHAR(255) NOT NULL,
    genero varchar(255) NOT NULL, 
    categoria varchar(255) NOT NULL,
    lancamento varchar(255) NOT NULL, 
    descricao varchar(10000) NOT NULL,
    avaliacao float not null,
    foto varchar(255) NOT NULL, 
    video varchar(255) NOT NULL
    
);
INSERT INTO filme (titulo, genero, categoria, lancamento, descricao, avaliacao, foto, video) VALUES
('Venom', 'Ação', 'home', '2018-02-07', 'O jornalista investigativo Eddie Brock tenta derrubar a Fundação Vida e seu enigmático fundador, Carlton Drake. Durante uma de suas investigações, ele entra em contato com um simbionte alienígena — uma criatura que precisa de um hospedeiro para sobreviver. Esse encontro transforma Eddie em Venom, um ser com força sobre-humana, poderes únicos e uma moral ambígua. Dividido entre sua humanidade e o instinto selvagem da criatura que agora vive dentro dele, Eddie precisa enfrentar inimigos perigosos enquanto tenta controlar a força devastadora do simbionte.', 4.5 ,  'venom.jpeg', 'venom.mp4'),

('Jumanji', 'Comédia', 'show', '2018-02-07', 'Quatro adolescentes são sugados para o mundo de Jumanji, onde assumem avatares adultos em uma aventura repleta de perigos e desafios. Para sair, precisam cooperar e sobreviver aos perigos da selva.',  4 , 'jumanji.jpg', 'jumanji.mp4'),

('Spider-Man: Volta Pra Casa', 'Ficção cientifica', 'popular', '2017-07-06', 'Peter Parker tenta equilibrar sua vida como um estudante comum e seu papel como o super-herói Homem-Aranha. Após os eventos de "Guerra Civil", ele enfrenta o vilão Abutre enquanto tenta provar seu valor para Tony Stark.',  5 ,  'spider-man_volta_pra_casa.jpg', 'spider-man_volta_pra_casa.mp4'),

('Jungle Cruise', 'Ação', 'popular', '2021-05-27', 'Uma intrépida exploradora contrata um capitão de barco para levá-la em uma jornada pela selva amazônica em busca de uma árvore lendária com poderes de cura. A dupla enfrenta perigos sobrenaturais e inimigos determinados a impedir sua missão.',  4.5 ,  'jungle_cruise.jpg', 'jungle_cruise.mp4'),

('Loki', 'Ação', 'popular', '2021-04-05', 'Após roubar o Tesseract, Loki é capturado pela Autoridade de Variância Temporal. Forçado a colaborar para impedir ameaças ao multiverso, ele enfrenta novas versões de si mesmo e descobre segredos que mudam tudo.',  5 ,  'loki.jpg', 'loki.mp4'),

('Round 6', 'Suspense', 'popular', '2021-05-02', 'Pessoas desesperadas por dinheiro são convidadas a participar de jogos infantis com consequências letais. Apenas um sobreviverá e levará o grande prêmio. Uma crítica social intensa sobre desigualdade e desespero.',  4 ,  'round_6.jpg', 'round_6.mp4'),

('The Falcon And The Winter Soldier', 'Ficção cientifica', 'popular', '2021-02-07', 'Após a aposentadoria do Capitão América, Sam Wilson e Bucky Barnes se unem para enfrentar uma nova ameaça global enquanto lidam com seu legado e conflitos pessoais.',  5 ,  'the_falcon_and_the_winter_soldier.jpg', 'the_falcon_and_the_winter_soldier.mp4'),

('Hawkeye', 'Ficção cientifica', 'popular', '2021-10-08', 'Clint Barton, o Gavião Arqueiro, tenta passar um Natal tranquilo com sua família, mas seu passado o alcança. Ele se une à jovem arqueira Kate Bishop para enfrentar inimigos e salvar o futuro.',  5 ,  'hawkeye.jpg', 'hawkeye.mp4'),

('Shang-Chi', 'Ação', 'show', '2021-06-24', 'Shang-Chi, mestre de artes marciais, precisa confrontar o passado que tentou deixar para trás ao ser atraído para a rede da misteriosa organização Dez Anéis liderada por seu pai.',  5 ,  'shang-chi.jpg',  'shang-chi.mp4'),

('Eternals', 'Ficção cientifica', 'show', '2021-10-21', 'Um grupo de seres imortais que viveu secretamente na Terra por milênios deve se reunir para proteger o planeta de uma ameaça ancestral chamada Deviantes.',  5 ,  'eternals.jpg', 'eternals.mp4'),

('The Wolverine', 'Ficção cientifica', 'show', '2013-03-28', 'Logan viaja ao Japão, onde enfrenta samurais, ninjas e dilemas sobre sua imortalidade. Em meio à perda e redenção, ele confronta seu passado e luta por um novo propósito.',  5 ,  'the_wolverine.jpg', 'the_wolverine.mp4');


--user
CREATE DATABASE if not exists usuarios;

use usuarios;

create table if not exists usuario(
	id INT auto_increment primary key,
    nome VARCHAR(255) NOT NULL,
	senha VARCHAR(255) NOT NULL,
	foto VARCHAR(255) NOT NULL
    

);

select * from usuario;


