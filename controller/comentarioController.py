from model.comentarios import Comentarios
from dao.comentarioDao import ComentarioDAO


class ComentarioController:


        def __init__(self):
            self.__lista = []
            self.__dao = ComentarioDAO()

        def inserir_comentario_controller(self, comentario,avaliacao, id_usuario, id_filme):
              novo_comentario = Comentarios(comentario,avaliacao, id_usuario, id_filme)
              self.__dao.inserir_comentario(novo_comentario)
              self.__dao.lista_comentarios()
              self.__lista.append(novo_comentario)
              self.__dao.atualiza_avaliacao(id_filme)

              return True

        @property
        def lista_comentario(self):
              return self.__lista
        
        def listar_comentarios_filme(self, id):
            return self.__dao.filme_comentario(id)
        
        def excluir_comen(self,id, id_filme):
            self.__dao.excluir_comentario(id)
            self.__dao.atualiza_avaliacao(id_filme)

            return True
        
        def comentario_espe(self, id):
            return self.__dao.comentario(id)
        
        def editar_comen(self, comentario, avaliacao, id, id_filme):
            self.__dao.editar(comentario, avaliacao, id)
            self.__dao.atualiza_avaliacao(id_filme)
            return True

        def delete_comentario_controller(self, id):
            return self.__dao.delete_usuario(id)
           
        
       
           

            
        
            
