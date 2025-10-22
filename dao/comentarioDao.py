import mysql.connector
from model.comentarios import Comentarios

class ComentarioDAO:

    def __init__(self):
        self.__conexao = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "105192119",
            database = "filmes",
            port = 3306
        )
        self.__cursor = self.__conexao.cursor()
        self.__id = 0

    def inserir_comentario(self, comentario):
        sql = "INSERT INTO comentarios (comentario, avaliacao, id_usuario, id_filme) VALUES(%s, %s, %s, %s)"
        valores = (comentario.comentario,comentario.avaliacao, comentario.id_usuario, comentario.id_filme)
        self.__cursor.execute(sql, valores)
        self.__conexao.commit()
        return self.__cursor.lastrowid
    



    def lista_comentarios(self):
        sql = "select id, comentario, avaliacao, id_usuario, id_filme from comentarios"
        self.__cursor.execute(sql)
        resultados = self.__cursor.fetchall()
        lista = []

        for r in resultados:
            id, comentarios, avaliacao, id_usuario, id_filme = r
            sql_usu = "select lo"
            novo_comentario = Comentarios(comentarios, avaliacao, id_usuario, id_filme, id)

            lista.append(novo_comentario)

        
        return lista
    
    def filme_comentario(self, id):

        sql = "select id, comentario, avaliacao, id_usuario, id_filme from comentarios where id_filme = %s"
        self.__cursor.execute(sql, (id,))
        resultados = self.__cursor.fetchall()
        lista = []

        for r in resultados:
            id_comentario, comentarios, avaliacao, id_usuario, id_filme = r
            sql_usuario = "Select id, nome, senha, foto, tipo from usuario where id = %s"
            self.__cursor.execute(sql_usuario, (id_usuario,))
            resultados_usuario = self.__cursor.fetchall()

            for ru in resultados_usuario:
                id_usuario, nome, senha, foto, tipo = ru

            comentario_add = {
                'id': id_comentario,
                'id_usuario': id_usuario,
                'nome_usuario': nome,
                'avaliacao': avaliacao,
                'foto': foto,
                'comentario':comentarios
            }
            lista.append(comentario_add)

        return lista
    
    def atualiza_avaliacao(self, id):
        total = 0
        quant = 0
        sql = "select avaliacao from comentarios where id_filme = %s"
        self.__cursor.execute(sql, (id,))
        resultados = self.__cursor.fetchall()
        print('print ',resultados)

        for r in resultados:
            avaliacao = r[0] 
            quant += 1
            total += avaliacao

        print(quant)
        if quant > 0:
            media = round(total / quant, 1)
        else:
            media = 0  

        print(media)

      
        sql_update = "UPDATE filme SET avaliacao = %s WHERE id = %s"
        self.__cursor.execute(sql_update, (media, id))
        self.__conexao.commit()

        return True
    
    def excluir_comentario(self, id):
        sql = "DELETE FROM comentarios where id = %s"
        self.__cursor.execute(sql, (id,))

        return True
    
    def comentario(self, id):
        sql = "select id, comentario, avaliacao from comentarios where id = %s"
        self.__cursor.execute(sql, (id,))
        resultados = self.__cursor.fetchall()
        
        for r in resultados:
            id_comen, comen, avaliacao = r
            comentario_especifico = {
                'id': id_comen,
                'comentario': comen,
                'avaliacao': avaliacao
            }

        return comentario_especifico
    
    def editar(self, comentario, avaliacao, id):
        sql = "UPDATE comentarios SET comentario = %s, avaliacao = %s where id = %s"
        valores = (comentario, avaliacao, id)
        self.__cursor.execute(sql, valores)
        self.__conexao.commit()

        return True 
    
    def delete_usuario(self, id):
        sql_comentario = "DELETE FROM comentarios WHERE id_usuario = %s"
        self.__cursor.execute(sql_comentario, (id,)) 
        self.__conexao.commit()
        return True

    
        


            

            
        

        






            
