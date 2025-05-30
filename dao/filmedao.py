import mysql.connector
from model.filmes import Filmes

class FilmeDAO:

    def __init__(self):
        self.__conexao = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "105192119",
            database = "filmes",
            port = 3306
        )
        self.__cursor = self.__conexao.cursor()

    def insirir_filmes(self, filme):
        sql = "INSERT INTO filme (titulo, genero, categoria, lancamento, descricao, avaliacao, foto, video) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        valores =(filme.titulo, filme.genero, filme.categoria, filme.lancamento, filme.descricao, filme.avaliacao , filme.foto, filme.video)
        self.__cursor.execute(sql,valores)
        self.__conexao.commit()
        return self.__cursor.lastrowid
    
    
   
    def perfil_filme(self, id):
        sql = "SELECT id, titulo, genero, categoria, lancamento, descricao, avaliacao, foto, video FROM filme WHERE id = %s"
        self.__cursor.execute(sql, (id,)) 
        resultados = self.__cursor.fetchall()
        print(resultados)
        
        for r in resultados:
            id, titulo, genero, categoria, lancamento, descricao, avaliacao, foto, video = r 
            filme = {
            'id': id,
            'titulo': titulo, 
            'genero': genero, 
            'categoria': categoria,
            'lancamento': lancamento,
            'descricao': descricao,
            'avaliacao': avaliacao, 
            'foto': foto, 
            'video': video
            }
            
       
        return filme
    
    def editar_filme_dao(self, titulo, genero, categoria, lancamento, descricao, avaliacao, foto, video, id):
        sql = "UPDATE filme SET titulo = %s, genero = %s, categoria = %s, lancamento = %s, descricao = %s, avaliacao = %s WHERE id = %s"
        valores = (titulo, genero, categoria, lancamento, descricao, avaliacao, id)
        self.__cursor.execute(sql,valores)
        self.__conexao.commit()
        if foto != '':
            sql = "UPDATE filme SET foto = %s  WHERE id = %s"
            valores = (foto,id)
            print(valores)
            self.__cursor.execute(sql,valores)
            self.__conexao.commit()
        if video != '':

            sql = "UPDATE filme SET video = %s WHERE id = %s"
            valores = (video ,id)
            print(valores)
            self.__cursor.execute(sql,valores)
            self.__conexao.commit()

        return True
    
    def deletar_filme(self, id):
        sql = "DELETE FROM filme WHERE id = %s"
        
        self.__cursor.execute(sql, (id,)) 
        self.__conexao.commit()

    def listar_filme(self):
        sql = "Select id, titulo, genero, categoria, lancamento, descricao, avaliacao, foto, video from filme"
        self.__cursor.execute(sql)
        resultados = self.__cursor.fetchall()
        lista = []

        for r in resultados:
            id, titulo, genero, categoria, lancamento, descricao, avaliacao, foto, video = r 
            novo_filme = Filmes(titulo, genero, categoria, lancamento,descricao, avaliacao, foto, video ,id)
            lista.append(novo_filme)
            
        print(lista)
        return lista
    
    def pesquisa(self, campo):
        sql = "SELECT id, titulo, genero, categoria, lancamento, descricao, avaliacao, foto, video FROM filme WHERE titulo LIKE %s"
        parametro = f"{campo}%"
        self.__cursor.execute(sql, (parametro,))
        resultados = self.__cursor.fetchall()
        print(resultados)
        lista = []
        for r in resultados:
            id, titulo, genero, categoria, lancamento,descricao, avaliacao, foto, video = r 
            filme = Filmes(titulo, genero, categoria, lancamento,descricao, avaliacao, foto, video ,id)
            lista.append(filme)
            
       
        return lista
    
    def excluir_filme(self, id):
        sql = "DELETE FROM filme WHERE id = %s"
        
        self.__cursor.execute(sql, (id,)) 
        self.__conexao.commit()
        
        return self.__cursor.rowcount > 0

    
       