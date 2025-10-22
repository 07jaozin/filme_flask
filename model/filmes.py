class Filmes:

    def __init__(self, titulo, genero, categoria, lancamento,descricao, avaliacao, foto, video, id = None, canais = []):

        self.__id = id
        self.__titulo = titulo
        self.__genero = genero
        self.__categoria = categoria
        self.__lancamento = lancamento
        self.__descricao = descricao
        self.__avaliacao = avaliacao
        self.__foto = foto
        self.__video = video
        self.__canais = canais

    def perfil_video(self):
        if self.__id is not None:
            return f'filme/{self.__id}'
        
        return f'filme/desconhecido'
    
    def to_dict(self):
        return{
            "id": self.__id,
            "titulo": self.__titulo,
            "genero": self.__genero,
            "categoria": self.__categoria,
            "lancamento": self.__lancamento,
            "descricao": self.__descricao,
            "avaliacao": self.__avaliacao,
            "foto": self.__foto,
            "video": self.__video
        }
    @property
    def id(self):
        return self.__id
    @property
    def titulo(self):
        return self.__titulo
    @property
    def genero(self):
        return self.__genero
    @property
    def categoria(self):
        return self.__categoria
    @property
    def lancamento(self):
        return self.__lancamento
    @property
    def descricao(self):
        return self.__descricao
    @property
    def avaliacao(self):
        return self.__avaliacao
    @property
    def foto(self):
        return self.__foto
    @property
    def video(self):
        return self.__video
    @property
    def canais(self):
        return self.__canais
    
    @titulo.setter
    def titulo(self, titulo):
        self.__titulo = titulo
    @genero.setter
    def genero(self, genero):
        self.__genero = genero
    @categoria.setter
    def categoria(self, categoria):
        self.__categoria = categoria
    @lancamento.setter
    def lancamento(self, lancamento):
        self.__lancamento = lancamento
    @descricao.setter
    def descricao(self, descricao):
        self.__descricao = descricao
    @avaliacao.setter
    def avaliacao(self, avaliacao):
        self.__avaliacao = avaliacao
    @foto.setter
    def foto(self, foto):
        self.__foto = foto
    @video.setter
    def video(self, video):
        self.__video = video
    
        
        