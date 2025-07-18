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
        valores = (filme.titulo, filme.genero, filme.categoria, filme.lancamento, filme.descricao, filme.avaliacao , filme.foto, filme.video)
        self.__cursor.execute(sql,valores)
        filme_id = self.__cursor.lastrowid

        for c in filme.canais:
            sql_canais = "INSERT INTO canais_filme(filme_id, canal_id) VALUES(%s, %s)"
            valores_canais = (filme_id, c)
            self.__cursor.execute(sql_canais,valores_canais)
            self.__conexao.commit()

        self.__conexao.commit()
        return self.__cursor.lastrowid
    
    
   
    def perfil_filme(self, id):
        sql = "SELECT id, titulo, genero, categoria, lancamento, descricao, avaliacao, foto, video FROM filme WHERE id = %s"
        self.__cursor.execute(sql, (id,)) 
        resultados = self.__cursor.fetchall()
        print(resultados)
        sql_canais = " SELECT canais.id, canais.nome, canais.link, canais.foto FROM filme INNER JOIN canais_filme ON filme.id = canais_filme.filme_id  INNER JOIN canais ON canais_filme.canal_id = canais.id WHERE filme.id = %s;"
        self.__cursor.execute(sql_canais, (id,))
        resultados_canais = self.__cursor.fetchall()
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
            'video': video,
            'canais': resultados_canais
            }
            
       
        return filme
    
    def editar_filme_dao(self, titulo, genero, categoria, lancamento, descricao, foto, video, canais, id):
        sql = "UPDATE filme SET titulo = %s, genero = %s, categoria = %s, lancamento = %s, descricao = %s WHERE id = %s"
        valores = (titulo, genero, categoria, lancamento, descricao, id)
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

        sql_delete = "DELETE FROM canais_filme where filme_id = %s"
        self.__cursor.execute(sql_delete,(id,))

        for c in canais:
            sql_canais = "INSERT INTO canais_filme(filme_id, canal_id) VALUES(%s, %s)"
            valores_canais = (id, c)
            self.__cursor.execute(sql_canais,valores_canais)
            self.__conexao.commit()

        return True
    
    
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
    
    def excluir_comentario_filme(self, id):
        sql_comentario = "DELETE FROM comentarios where id_filme = %s"
        self.__cursor.execute(sql_comentario, (id,))
        self.__conexao.commit()
        return True
    
    def excluir_canais_filme(self, id):
        sql_comentario = "DELETE FROM canais_filme where filme_id = %s"
        self.__cursor.execute(sql_comentario, (id,))
        self.__conexao.commit()
        return True

    def filtrar(self, data_inicio, data_fim, avaliacao, categoria, titulo):

        categoria = f"{categoria}%"
        titulo = f"{titulo}%"

        sql_base = "SELECT id, titulo, genero, categoria, lancamento, descricao, avaliacao, foto, video FROM filme WHERE titulo LIKE %s AND genero LIKE %s"
        valores = [titulo, categoria]

        if avaliacao != '':
            sql_base += " AND floor(avaliacao) = %s"
            valores.append(float(avaliacao))

        if data_inicio and data_fim:
            sql_base += " AND lancamento BETWEEN %s AND %s"
            valores.extend([data_inicio, data_fim])
        elif data_inicio:
            sql_base += " AND lancamento >= %s"
            valores.append(data_inicio)
        elif data_fim:
            sql_base += " AND lancamento <= %s"
            valores.append(data_fim)

        self.__cursor.execute(sql_base, tuple(valores))
        resultados = self.__cursor.fetchall()

        lista = []
        for r in resultados:
            id, titulo, genero, categoria, lancamento, descricao, avaliacao, foto, video = r
            filme = Filmes(titulo, genero, categoria, lancamento, descricao, avaliacao, foto, video, id)
            lista.append(filme)

        return lista
    
    def atualiza_avaliacao_filmeDao(self, id):
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

        
       