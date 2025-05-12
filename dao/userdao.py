import mysql.connector
from model.pessoas import Pessoas

class UserDAO:

    def __init__(self):
        self.__conexao = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "105192119",
            database = "usuarios",
            port = 3306
        )
        self.__cursor = self.__conexao.cursor()

    def insirir_usuario(self, usuario):
        sql = "INSERT INTO usuario (nome, senha, foto) VALUES (%s, %s, %s)"
        
        valores = (usuario.nome.lower(), usuario.senha, usuario.foto)
        print(valores)
        self.__cursor.execute(sql,valores)
        self.__conexao.commit()
        return self.__cursor.lastrowid
    
    def listar_usuarios(self):
        sql = "Select id, nome, senha, foto from usuario"
        self.__cursor.execute(sql)
        resultados = self.__cursor.fetchall()
        lista = []

        for r in resultados:
            id, nome, senha, foto = r 
            novo_usuario = Pessoas(nome, senha, foto, id)
            lista.append(novo_usuario)
            
        print(lista)
        return lista
   
    def perfil(self, id):
        sql = "SELECT id, nome, senha, foto FROM usuario WHERE id = %s"
        self.__cursor.execute(sql, (id,)) 
        resultados = self.__cursor.fetchall()
        print(resultados)
        
        for r in resultados:
            id, nome, senha, foto = r 
            novo_usuario = Pessoas(nome, senha, foto, id)
            
       
        return novo_usuario
    
    def editar(self, nome, senha, foto, id):
        if foto == '':
            sql = "UPDATE usuario SET nome = %s, senha = %sWHERE id = %s"
            valores = (nome.lower() ,senha ,id)
        else:
             sql = "UPDATE usuario SET nome = %s, senha = %s, foto = %s WHERE id = %s"
             valores = (nome.lower() ,senha, foto ,id)
        
        self.__cursor.execute(sql,valores)
        self.__conexao.commit()
        return True
    
    def verificar_usuario(self, nome, senha):
    
        sql = "SELECT id, nome, senha, foto FROM usuario WHERE nome = %s and senha = %s"
        print(nome, senha)
        self.__cursor.execute(sql, (nome, senha,))
        resultados = self.__cursor.fetchall()
        if resultados != []:
            print(resultados)

            for r in resultados:
                id, nome, senha, foto = r 
                novo_usuario = {
                'id': id,
                'nome': nome,
                'senha': senha,
                'foto': foto
                }


            return novo_usuario
        else:
            return False
        
    def deletar_usuario(self, id):
        sql = "DELETE FROM usuario WHERE id = %s"
        
        self.__cursor.execute(sql, (id,)) 
        self.__conexao.commit()
        
        return self.__cursor.rowcount > 0
   
       