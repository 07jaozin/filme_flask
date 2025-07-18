class Canais:

    def __init__(self, nome, link, foto, id = None):
        self.__nome = nome
        self.__link = link
        self.__foto = foto
        self.__id = id
        self.__checked = ""


    
    @property
    def id(self):
        return self.__id
    @property
    def nome(self):
        return self.__nome
    @property
    def link(self):
        return self.__link

    @property
    def foto(self):
        return self.__foto
    @property
    def checked(self):
        return self.__checked


    @nome.setter
    def nome(self, nome):
        self.__nome = nome
    @link.setter
    def link(self, link):
        self.__link = link

    @foto.setter
    def foto(self, foto):
        self.__foto = foto 

    @checked.setter
    def checked(self,c):
        self.__checked = c