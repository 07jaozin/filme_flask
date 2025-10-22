from model.pessoas import Pessoas
from dao.userdao import UserDAO
from flask import session, flash, current_app
from werkzeug.utils import secure_filename
import os


class PessoaController:
    
    def __init__(self):
        self.__lista_pessoas = []
        self.__dao = UserDAO()
       

        
    def adicionar_pessoa(self, nome, senha, email, foto, tipo):
        nome_ajustado_principal = nome.strip()
        email_ajustado_principal = email.strip()
        senha_ajustado = senha.replace("","")
        print('foto:',foto)
        if not foto:
            
            novo_pessoa = Pessoas( nome_ajustado_principal.lower(), senha, email_ajustado_principal, 'padrao.jpg', tipo.lower())
        else:
            extensao = os.path.splitext(foto.filename)[1]
            nome_ajustado = secure_filename(nome.lower().replace(" ", "_"))
            nome_arquivo = f"{nome_ajustado}{extensao}"
            caminho = os.path.join(current_app.config['UPLOAD_FOLDER'], nome_arquivo)
            foto.save(caminho)
            print('diminutivo', nome.lower())
            novo_pessoa = Pessoas( nome_ajustado_principal.lower(), senha_ajustado, email_ajustado_principal, nome_arquivo, tipo.lower())
        #self.__lista_pessoas.append(novo_pessoa)
        self.__dao.insirir_usuario(novo_pessoa)
        self.__dao.listar_usuarios()
        self.__lista_pessoas.append(novo_pessoa)
    
    @property
    def listar(self):
        self.__lista_pessoas = self.__dao.listar_usuarios()
        return self.__lista_pessoas
    
    
    def edita_pessoa(self, id, nome, senha, email, foto):
        #pessoa = self.buscar_pessoa(id)
        senha_ajustado = senha.replace(" ","")
        nome_ajustado_principal = nome.strip()
        email_ajustado_principal = email.strip()
        if not foto:
            self.__dao.editar( nome_ajustado_principal.lower(), senha_ajustado, email_ajustado_principal, '', id)

        else:
            extensao = os.path.splitext(foto.filename)[1]
            nome_ajustado = secure_filename(nome.lower().replace(" ", "_"))
            nome_arquivo = f"{nome_ajustado}{extensao}"
            caminho = os.path.join(current_app.config['UPLOAD_FOLDER'], nome_arquivo)
            foto.save(caminho)
            self.__dao.editar( nome_ajustado_principal.lower(), senha_ajustado, email_ajustado_principal, nome_arquivo, id)
        #    pessoa.nome = nome
        #    pessoa.email = email
        #    pessoa.foto = foto
        #    return True
        return True
    
    def perfil(self, id):
        return self.__dao.perfil(id)
    
    def verificação(self, email, senha):
        senha_ajustado = senha.replace(" ","")
        email_ajustado = email.strip()
        funcao = self.__dao.verificar_usuario(email_ajustado.lower(), senha_ajustado)
        if funcao:
            session['logado'] = True
            session['id'] = funcao['id']
            session['email_recuperar'] = email
            if funcao['tipo'] == 'adm':
                print("olaaaaaaaaa")
                session['adm'] = True
            
            return True
        else:
            flash("usuario não encontrado")
            return False
    
    def excluir_usuario_controler(self, id):
        self.__dao.deletar_usuario(id)
        return True
    
    def remover_foto(self, id):
        foto = 'padrao.jpg'
        if self.__dao.deletar_foto_perfil(id, foto):
            return True
        else:
            return False
        
    def verifica_email(self, email):
        return self.__dao.verificar_email(email)
    
    def atualiza_senha(self, email, senha):
        return self.__dao.atualiza_senha_por_email(email, senha)
        
        
        

        

    
    
