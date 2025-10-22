from model.canais import Canais
from dao.canaisDao import CanaisDAO
from flask import current_app
from werkzeug.utils import secure_filename
import os

class CanaisController:

    def __init__(self):
        self.__dao = CanaisDAO()
        self.__lista_canais = []

    def adicionar_canal(self, nome, link, foto):
        extensao = os.path.splitext(foto.filename)[1]
        nome_ajustado = secure_filename(nome.lower().replace(" ", "_"))
        nome_arquivo = f"{nome_ajustado}{extensao}"

        caminho = os.path.join(current_app.config['UPLOAD_FOLDER'], nome_arquivo)
        foto.save(caminho)

        novo_canal = Canais(nome.title(), link, nome_arquivo)
        self.__dao.inserir_canal(novo_canal)
        self.__lista_canais.append(novo_canal)
        return True

    def listar_canais(self):
        return self.__dao.listar_canais()

    def buscar_por_id(self, id):
        return self.__dao.buscar_canal_por_idfilme(id)
    
    def buscar_por_idCanal(self, id):
        return self.__dao.buscar_canal_por_id(id)

    def editar_canal(self, id, nome, link, foto):
        nome_arquivo = ''
        if foto and foto.filename != '':
            extensao = os.path.splitext(foto.filename)[1]
            nome_ajustado = secure_filename(nome.lower().replace(" ", "_"))
            nome_arquivo = f"{nome_ajustado}{extensao}"
            caminho = os.path.join(current_app.config['UPLOAD_FOLDER'], nome_arquivo)
            foto.save(caminho)

        self.__dao.editar_canal(id, nome.title(), link, nome_arquivo)
        return True

    def deletar_canal(self, id):
        self.__dao.deletar_canalFilme(id)
        return self.__dao.deletar_canal(id)
