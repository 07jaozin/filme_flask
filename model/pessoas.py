class Pessoas: # definindo uma classe 
   

    def __init__(self, nome, senha, email, foto, tipo, id = None): # init seria o que iria contruiir meu objeto, chamado de construtor
        
        self.__id = id
        self.__nome = nome.title()
        self.__senha = senha
        self.__email = email
        self.__foto = foto
        self.__tipo = tipo
      
    def urlDoPessoas(self):
        if self.__id is not None: 
            return f'/perfil_usuario/{self.__id}'
        return f'/perfil_usuario/desconhecido'
    
    def to_dict(self):
        return{
            "id": self.__id,
            "nome": self.__nome,
            "senha": self.__senha,
            "email": self.__email,
            "foto": self.__foto,
            "tipo": self.__tipo
        }
    
    
    @property
    def id(self):
        return self.__id
    
    @property
    def tipo(self):
        return self.__tipo
    
    @property
    def nome(self):
        return self.__nome

    @property
    def senha(self):
        return self.__senha
    
    @property
    def email(self):
        return self.__email
    
    @property
    def foto(self):
        return self.__foto
    
    @nome.setter
    def nome(self, nome):
        self.__nome = nome.title()
    @senha.setter
    def senha(self, senha):
        self.__senha = senha

    @email.setter
    def email(self, email):
        self.__email = email

    @foto.setter
    def foto(self, foto):
        self.__foto = foto

    @tipo.setter
    def tipo(self, tipo):
        self.__tipo = tipo