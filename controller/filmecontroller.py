from model.filmes import Filmes
from dao.filmedao import FilmeDAO
from flask import session, flash
from flask import current_app
from werkzeug.utils import secure_filename
import os

class FilmeController:
    
    def __init__(self):
        self.__lista_filme = []
        self.__lista_filme_pesquisa = []
        self.__lista_campo_pesquisa = ''
        self.__dao = FilmeDAO()
       

        
    def adicionar_filme(self, titulo, genero, categoria, data, descricao, avaliacao, foto, video):
        
        extensao = os.path.splitext(foto.filename)[1]
        extensao_video = os.path.splitext(video.filename)[1]
        nome_ajustado = secure_filename(titulo.lower().replace(" ", "_"))
        nome_arquivo = f"{nome_ajustado}{extensao}"
        nome_arquivo_video = f"{nome_ajustado}{extensao_video}"
        caminho = os.path.join(current_app.config['UPLOAD_FOLDER'], nome_arquivo)
        caminho_video = os.path.join(current_app.config['UPLOAD_VIDEO'], nome_arquivo_video)
        foto.save(caminho)
        video.save(caminho_video)
        novo_filme = Filmes( titulo.title(), genero, categoria, data,descricao, avaliacao, nome_arquivo, nome_arquivo_video)
        #self.__lista_pessoas.append(novo_filme)
        self.__dao.insirir_filmes(novo_filme)
        self.__dao.listar_filme()
        self.__lista_filme.append(novo_filme)
    
    @property
    def listar_pesquisa(self):
        print(self.__lista_filme_pesquisa)
        return self.__lista_filme_pesquisa
    @property
    def campo_pesquisa(self):
        print(self.__lista_campo_pesquisa)
        return self.__lista_campo_pesquisa
    
    
    
    def edita_filme(self, titulo, genero, categoria, data,descricao, avaliacao, foto, video, id):
        
        nome_arquivo = ''
        nome_arquivo_video = ''
        if foto.filename != '':
            extensao = os.path.splitext(foto.filename)[1]
            nome_ajustado = secure_filename(titulo.lower().replace(" ", "_"))
            nome_arquivo = f"{nome_ajustado}{extensao}"
            caminho = os.path.join(current_app.config['UPLOAD_FOLDER'], nome_arquivo)
            foto.save(caminho)
        if video.filename != '':
            
            extensao_video = os.path.splitext(video.filename)[1]
            nome_ajustado = secure_filename(titulo.lower().replace(" ", "_"))
            nome_arquivo_video = f"{nome_ajustado}{extensao_video}"
            caminho_video = os.path.join(current_app.config['UPLOAD_VIDEO'], nome_arquivo_video)
            video.save(caminho_video)

        self.__dao.editar_filme_dao(titulo.title(), genero, categoria, data, descricao, avaliacao, nome_arquivo, nome_arquivo_video, id)
        return True
            
                
    
    def listar_filmes(self):
        return self.__dao.listar_filme()
    
    def pesquisar_filme(self, campo):
        session['primeira_vez'] = True
        self.__lista_filme_pesquisa = self.__dao.pesquisa(campo)
        self.__lista_campo_pesquisa = campo
        return True
        
    def perfil_filme(self, id):
        return self.__dao.perfil_filme(id)
    
    def excluir_filme_controller(self, id):
        self.__dao.excluir_filme(id)
        return True
    

        

    
    
