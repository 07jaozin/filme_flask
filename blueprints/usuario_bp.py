from flask import Flask, request, redirect, flash, render_template, session, jsonify, Blueprint, url_for
from controller.usercontroller import PessoaController
import random
from app import mail
from flask_mail import Message


userControler = PessoaController()


user_bp = Blueprint("user", __name__, template_folder="../templates")

@user_bp.route('/login')
def pagLogin():
    return render_template("login.html")

@user_bp.route('/atualiza_senha')
def atualiza_senha():
    return render_template("atualiza_senha.html")

@user_bp.route('/login', methods = ['POST'])
def login():
    email = request.form.get('email')
    senha = request.form.get('senha')
    if userControler.verificação(email, senha):
        return jsonify(True), 200
    else:
        return jsonify(False), 404
        
    
    
@user_bp.route('/<int:id>', methods = ['PUT'])
def editar(id):
     nome = request.form.get('nome-editar')
     senha = request.form.get('senha-editar')
     email = request.form.get('email-editar')
     foto = request.files['foto-editar']

     if userControler.edita_pessoa(id, nome, senha, email, foto):
        return jsonify(True), 200
     
     return jsonify(False), 404
@user_bp.route('/cadastro', methods = ['POST'])
def cadastrar():
     nome = request.form.get('nome-cadastrar')
     senha = request.form.get('senha-cadastrar')
     email = request.form.get('email-cadastrar')
     print(nome, senha, email)
     foto = ''
     tipo = 'normal'

     userControler.adicionar_pessoa(nome, senha, email, foto, tipo)

     return jsonify(True), 200

@user_bp.route('/perfil_usuario/<int:id>')
def perfil_usuario(id):
    if 'logado' not in session:
       return jsonify({"logado": False}), 404
    else:
        usuario = userControler.perfil(id)
        if usuario != []:
            return jsonify(usuario.to_dict()), 202
        return jsonify("nenhum usuario com este email"), 404
    
@user_bp.route('/session')
def getSession():
    if 'id' in session:
        return jsonify({"id": session['id']}), 200
    else:
        return jsonify("nao logado"), 200
    
@user_bp.route('/<int:id>', methods = ['DELETE'])
def excluir(id):
    if 'logado' not in session:
        return jsonify({"logado": False}), 404
    
    if userControler.excluir_usuario_controler(id):
        return jsonify({"sucesso": True})
    
    return jsonify({"sucesso": False})

@user_bp.route('/foto/<int:id>', methods = ['DELETE'])
def excluirFoto(id):
    if 'logado' not in session:
        return jsonify({"logado": False}), 404
    
    if userControler.remover_foto(id):
        return jsonify({"sucesso": True})
    
    return jsonify({"sucesso": False})
    
@user_bp.route('/pagina_perfil/<int:id>')
def pagina_perfil(id):
    return render_template("perfil.html")

@user_bp.route("/verificar_email", methods=["POST"])
def verificar_email():
    data = request.get_json()
    email = data.get("email")
    print(email)
    print(userControler.verifica_email(email))
    #if not userControler.verifica_email(email):
    #    return jsonify({"sucesso": False})

    codigo = random.randint(1000, 9999)
    session["codigo_verificacao"] = str(codigo)
    session["email_recuperar"] = email

    msg = Message(
        subject="Recuperação de senha",
        recipients=[email],  # destinatário
        body=f"Aqui está seu código de verificação \n {codigo}"
    )
    mail.send(msg)

    return jsonify({"sucesso": True})
@user_bp.route("/verificar_email_cadastro", methods=["POST"])
def verificar_email_cadastro():
    data = request.get_json()
    email = data.get("email")
    print(email)
    if email == None:
        return jsonify("erro"),404

    codigo = random.randint(1000, 9999)
    session["codigo_verificacao"] = str(codigo)
    session["email_recuperar"] = email

    msg = Message(
        subject="Recuperação de senha",
        recipients=[email],  # destinatário
        body=f"Aqui está seu código de verificação \n {codigo}"
    )
    mail.send(msg)

    return jsonify({"sucesso": True})


@user_bp.route("/verificar_codigo", methods=["POST"])
def verificar_codigo():
    data = request.get_json()
    codigo = data.get("codigo")

    if codigo == session.get("codigo_verificacao"):
        return jsonify({"sucesso": True}), 200
    else:
        return jsonify({"sucesso": False}), 404
    
@user_bp.route("/atualiza_senha", methods = ['PUT'])
def atualizar_senha():
    
    senha = request.form.get("nova-senha")

    print(senha)
    email = session['email_recuperar']
    print(email)

    if userControler.atualiza_senha(email, senha):
        return jsonify(True), 200
    
    return jsonify(False), 404

@user_bp.route('/verifica_email_existe', methods = ['POST'])
def verifica_email_existe():
    data = request.get_json()
    email = data.get("email")

    if userControler.verifica_email(email):
        return jsonify(True), 200
    
    return jsonify(False), 200