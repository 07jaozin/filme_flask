import mysql.connector
from model.canais import Canais

class CanaisDAO:

    def __init__(self):
        self.__conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="105192119",
            database="filmes", 
            port=3306
        )
        self.__cursor = self.__conexao.cursor()

    def inserir_canal(self, canal):
        sql = "INSERT INTO canais (nome, link, foto) VALUES (%s, %s, %s)"
        valores = (canal.nome, canal.link, canal.foto)
        self.__cursor.execute(sql, valores)
        self.__conexao.commit()
        return self.__cursor.lastrowid

    def listar_canais(self):
        sql = "SELECT id, nome, link, foto FROM canais"
        self.__cursor.execute(sql)
        resultados = self.__cursor.fetchall()
        lista = []

        for r in resultados:
            id, nome, link, foto = r
            canal = Canais(nome, link, foto, id)
            lista.append(canal)

        return lista

    def buscar_canal_por_id(self, id):
        sql = "SELECT id, nome, link, foto FROM canais WHERE id = %s"
        self.__cursor.execute(sql, (id,))
        resultado = self.__cursor.fetchone()

        if resultado:
            id, nome, link, foto = resultado
            return Canais(nome, link, foto, id)
        return None

    def editar_canal(self, id, nome, link, foto):
        sql = "UPDATE canais SET nome = %s, link = %s WHERE id = %s"
        self.__cursor.execute(sql, (nome, link, id))
        self.__conexao.commit()

        if foto:
            sql = "UPDATE canais SET foto = %s WHERE id = %s"
            self.__cursor.execute(sql, (foto, id))
            self.__conexao.commit()
        return True

    def deletar_canal(self, id):
        sql = "DELETE FROM canais WHERE id = %s"
        self.__cursor.execute(sql, (id,))
        self.__conexao.commit()
        return self.__cursor.rowcount > 0
    
    def deletar_canalFilme(self, id):
        sql = "DELETE FROM canais_filme WHERE canal_id = %s"
        self.__cursor.execute(sql, (id,))
        self.__conexao.commit()
        return self.__cursor.rowcount > 0

