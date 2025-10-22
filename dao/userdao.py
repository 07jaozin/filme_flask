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
        sql = "INSERT INTO usuario (nome, senha, email, foto, tipo) VALUES (%s, %s, %s, %s, %s)"
        
        valores = (usuario.nome.lower(), usuario.senha, usuario.email, usuario.foto, usuario.tipo)
        print(valores)
        self.__cursor.execute(sql,valores)
        self.__conexao.commit()
        return self.__cursor.lastrowid
    
    def listar_usuarios(self):
        sql = "Select id, nome, senha, email, foto, tipo from usuario"
        self.__cursor.execute(sql)
        resultados = self.__cursor.fetchall()
        lista = []

        for r in resultados:
            id, nome, senha, email, foto, tipo = r 
            novo_usuario = Pessoas(nome, senha, email, foto, tipo, id)
            lista.append(novo_usuario)
            
        print(lista)
        return lista
   
    def perfil(self, id):
        sql = "SELECT id, nome, senha, email, foto, tipo FROM usuario WHERE id = %s"
        self.__cursor.execute(sql, (id,)) 
        resultados = self.__cursor.fetchall()
        print(resultados)
        
        if resultados == []:
            return []
        for r in resultados:
            id, nome, senha, email, foto, tipo = r 
            novo_usuario = Pessoas(nome, senha,email, foto, tipo, id)
            
       
        return novo_usuario
    
    def editar(self, nome, senha, email, foto, id):
        if foto == '':
            sql = "UPDATE usuario SET nome = %s, senha = %s, email = %s WHERE id = %s"
            valores = (nome.lower() ,senha, email, id)
        else:
             sql = "UPDATE usuario SET nome = %s, senha = %s, email = %s, foto = %s WHERE id = %s"
             valores = (nome.lower() ,senha, email, foto ,id)
        
        self.__cursor.execute(sql,valores)
        self.__conexao.commit()
        return True
    
    def verificar_usuario(self, email, senha):
        
        sql = "SELECT id, nome, senha, email, foto, tipo FROM usuario WHERE email = %s and senha = %s"
        print(email, senha)
        self.__cursor.execute(sql, (email, senha,))
        resultados = self.__cursor.fetchall()
        if resultados != []:
            for r in resultados:
                id, nome, senha, email, foto, tipo = r 
                novo_usuario = {
                'id': id,
                'nome': nome,
                'senha': senha,
                'email': email,
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
    
    def atualiza_senha_por_email(self, email, senha):
        sql = "UPDATE usuario SET senha = %s WHERE email = %s"
        valores = (senha, email)
        self.__cursor.execute(sql, valores)
        self.__conexao.commit()
        return True
    
    def verificar_email(self, email):
        sql = "select id from usuario where email = %s"
        self.__cursor.execute(sql, (email,))
        resultado = self.__cursor.fetchone()

        return resultado is not None

        
   
       