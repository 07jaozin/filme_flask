import mysql.connector
from model.pessoas import Pessoas

class UserDAO:

    def __init__(self):
        self.__conexao = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "105192119",
            database = "filmes",
            port = 3306
        )
        self.__cursor = self.__conexao.cursor()

    def insirir_usuario(self, usuario):
        sql = "INSERT INTO usuario (nome, senha, foto, tipo) VALUES (%s, %s, %s, %s)"
        
        valores = (usuario.nome.lower(), usuario.senha, usuario.foto, usuario.tipo)
        print(valores)
        self.__cursor.execute(sql,valores)
        self.__conexao.commit()
        return self.__cursor.lastrowid
    
    def listar_usuarios(self):
        sql = "Select id, nome, senha, foto, tipo from usuario"
        self.__cursor.execute(sql)
        resultados = self.__cursor.fetchall()
        lista = []

        for r in resultados:
            id, nome, senha, foto, tipo = r 
            novo_usuario = Pessoas(nome, senha, foto, tipo, id)
            lista.append(novo_usuario)
            
        print(lista)
        return lista
   
    def perfil(self, id):
        sql = "SELECT id, nome, senha, foto, tipo FROM usuario WHERE id = %s"
        self.__cursor.execute(sql, (id,)) 
        resultados = self.__cursor.fetchall()
        print(resultados)
        
        if resultados == []:
            return False
        for r in resultados:
            id, nome, senha, foto, tipo = r 
            novo_usuario = Pessoas(nome, senha, foto, tipo, id)
            
       
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
        
        sql = "SELECT id, nome, senha, foto, tipo FROM usuario WHERE nome = %s and senha = %s"
        print(nome, senha)
        self.__cursor.execute(sql, (nome, senha,))
        resultados = self.__cursor.fetchall()
        if resultados != []:
            for r in resultados:
                id, nome, senha, foto, tipo = r 
                novo_usuario = {
                'id': id,
                'nome': nome,
                'senha': senha,
                'foto': foto,
                'tipo': tipo
                }
                print(tipo)


            return novo_usuario
        else:
            return False
        
    def deletar_usuario(self, id):
        sql_comentario = "DELETE FROM comentarios WHERE id_usuario = %s"
        self.__cursor.execute(sql_comentario, (id,)) 
        sql = "DELETE FROM usuario WHERE id = %s"
        self.__cursor.execute(sql, (id,)) 
        self.__conexao.commit()
        
        return self.__cursor.rowcount > 0
    
    def deletar_foto_perfil(self, id, foto):
        sql = "UPDATE usuario SET foto = %s WHERE id = %s"
        valores = (foto, id)
        self.__cursor.execute(sql, valores)
        self.__conexao.commit()
        return True
   
       