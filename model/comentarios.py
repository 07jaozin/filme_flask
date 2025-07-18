class Comentarios:

    def __init__(self, comentario, avaliacao, id_usuario, id_filme, id = None):

        self.__id = id
        self.__comentario = comentario
        self.__avaliacao = avaliacao
        self.__id_usuario = id_usuario
        self.__id_filme = id_filme


    @property
    def id(self):
        return self.__id
    @property
    def comentario(self):
        return self.__comentario
    @property
    def avaliacao(self):
        return self.__avaliacao
    @property
    def id_usuario(self):
        return self.__id_usuario
    @property
    def id_filme(self):
        return self.__id_filme
    
    @comentario.setter
    def comentario(self, comentario):
        self.__comentario = comentario
    @avaliacao.setter
    def avaliacao(self, avaliacao):
        self.__avaliacao = avaliacao
        